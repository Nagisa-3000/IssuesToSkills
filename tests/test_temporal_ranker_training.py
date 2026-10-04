from dataclasses import asdict, replace

import pytest
from adaptive_fixture import CUTOFF, make_fixture

from arex_skill_graph.action_contracts import digest
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.plan_validation import ResourcePolicy
from arex_skill_graph.temporal_ranker_data import (
    HistoricalQuery,
    SupervisionLabel,
    build_examples,
    pair_preferences,
    validate_training_snapshot,
)
from arex_skill_graph.workflow_ranker import WorkflowRanker, workflow_capsule


def make_dataset(tmp_path):
    package, task, _ = make_fixture(tmp_path)
    queries = []
    labels = []
    for i, date in enumerate(
        ("2021-01-01T00:00:00Z", "2022-01-01T00:00:00Z", "2023-06-01T00:00:00Z")
    ):
        query_task = replace(task, task_id="historical:" + str(i), input_available_at=date)
        query = HistoricalQuery(query_task, "query-cluster:" + str(i), "query-fix:" + str(i))
        queries.append(query)
        for letter in ("a", "b"):
            labels.append(
                SupervisionLabel(
                    query_task.task_id,
                    "workflow:" + letter,
                    "workflow",
                    "adaptively_usable" if letter == "a" else "unrelated",
                    "evidence_review",
                    ("current:issue",),
                    "synthetic-review",
                    date,
                    sampling_probability=0.5,
                )
            )

    def provider(task, refs, policy):
        resources = ResourcePolicy(policy, refs)
        return [workflow_capsule(w, task, resources) for p in resources.load() for w in p.workflows]

    examples, audits = build_examples(
        queries,
        [package.reference],
        labels,
        provider,
        training_cutoff="2023-01-01T00:00:00Z",
        main_cutoff=CUTOFF,
    )
    payload = {
        "schema": "temporal-workflow-ranker-data-v1",
        "training_cutoff": "2023-01-01T00:00:00Z",
        "main_cutoff": CUTOFF,
        "examples": [asdict(e) for e in examples],
        "pairs": list(pair_preferences(examples)),
        "audits": audits,
    }
    payload["dataset_sha256"] = digest(payload)
    return payload, package, task, queries, labels, provider


def test_temporal_self_future_alias_and_exposure_gates(tmp_path):
    data, p, _task, queries, labels, provider = make_dataset(tmp_path)
    validate_training_snapshot(data)
    assert data["audits"][0]["catalog_cutoff"] == queries[0].task.input_available_at
    assert data["audits"][-1]["catalog_cutoff"] == data["training_cutoff"]
    for mutation in ("self", "future", "alias", "exposed", "cluster", "fix"):
        changed = list(queries)
        if mutation == "self":
            changed[0] = replace(changed[0], aliases=("source:a",))
        elif mutation == "future":
            changed[0] = replace(
                changed[0], task=replace(changed[0].task, input_available_at="2019-01-01T00:00:00Z")
            )
        elif mutation == "alias":
            changed[1] = replace(changed[1], aliases=(changed[0].task.task_id,))
        elif mutation == "exposed":
            changed[0] = replace(changed[0], exposed=True)
        elif mutation == "cluster":
            changed[-1] = replace(changed[-1], bug_cluster_id=changed[0].bug_cluster_id)
        else:
            changed[-1] = replace(changed[-1], fix_id=changed[0].fix_id)
        with pytest.raises(ValueError):
            build_examples(
                changed,
                [p.reference],
                labels,
                provider,
                training_cutoff=data["training_cutoff"],
                main_cutoff=CUTOFF,
            )
    corrupted = {**data, "dataset_sha256": "0" * 64}
    with pytest.raises(ValueError, match="hash"):
        validate_training_snapshot(corrupted)


def test_pairwise_ties_and_unexecuted_are_not_failure(tmp_path):
    data, *_ = make_dataset(tmp_path)
    from arex_skill_graph.temporal_ranker_data import TrainingExample

    examples = [TrainingExample(**e) for e in data["examples"]]
    tied = [replace(e, label={**e.label, "applicability": "probe_only"}) for e in examples]
    pairs = pair_preferences(tied)
    assert all(p["target"] == 0.5 and p["tie"] for p in pairs)
    assert all(p["sampling_probabilities"] == [0.5, 0.5] for p in pairs)
    assert all(p["supervision"] == "reviewed_applicability" for p in pairs)
    assert all(e.label["outcome"] is None for e in tied)


def test_utility_calibration_separates_probe_permission_and_execution_outcome():
    from arex_skill_graph.ranker_training import calibration_utility

    passed = {
        "label_source": "execution",
        "applicability": "probe_only",
        "outcome": True,
        "regression_pass": True,
    }
    failed = {**passed, "outcome": False}
    regression = {**passed, "regression_pass": False}
    assert calibration_utility([passed]) == 1.0
    assert calibration_utility([passed, failed]) == 0.5
    assert calibration_utility([regression]) == 0.0
    assert (
        calibration_utility([{"label_source": "evidence_review", "applicability": "probe_only"}])
        == 0.0
    )


def tiny_model(path):
    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")
    path.mkdir()
    vocab = [
        "[PAD]",
        "[UNK]",
        "[CLS]",
        "[SEP]",
        "[MASK]",
        "type",
        "context",
        "diagnostic",
        "runtime",
        "repair",
        "guard",
        "verify",
        "known",
        "current",
        "static",
        "module",
        "true",
        "false",
    ]
    (path / "vocab.txt").write_text("\n".join(vocab) + "\n")
    tokenizer = transformers.BertTokenizerFast(
        vocab_file=str(path / "vocab.txt"), do_lower_case=True
    )
    tokenizer.save_pretrained(path)
    torch.manual_seed(9)
    model = transformers.BertModel(
        transformers.BertConfig(
            vocab_size=len(vocab),
            hidden_size=24,
            intermediate_size=48,
            num_hidden_layers=1,
            num_attention_heads=4,
            max_position_embeddings=512,
        )
    )
    model.save_pretrained(path)


def test_real_local_training_checkpoint_and_embeddings(tmp_path):
    from arex_skill_graph.action_contracts import TemporalPolicy
    from arex_skill_graph.adaptive_guidance import index_native_package
    from arex_skill_graph.embeddings import TransformerEncoder
    from arex_skill_graph.ranker_training import TrainedRankerScorer, train_ranker
    from arex_skill_graph.store import CatalogStore

    data, p, task, *_ = make_dataset(tmp_path)
    model_path = tmp_path / "tiny-model"
    tiny_model(model_path)
    encoder = TransformerEncoder(str(model_path))
    vectors = encoder.encode(["type context guard", "runtime diagnostic"])
    assert len(vectors) == 2 and len(vectors[0]) == 24
    with CatalogStore(tmp_path / "transformer.sqlite", encoder=encoder) as store:
        store.initialize()
        index_native_package(store, p.reference, TemporalPolicy(CUTOFF))
        assert store.search_vector("type context")
        with pytest.raises(ValueError, match="version"):
            store.search_vector("type", model_version="hash-v1")
    metadata = train_ranker(data, model_path, tmp_path / "checkpoint", epochs=3, learning_rate=0.01)
    assert metadata["training_pairs"] == 2 and metadata["development_queries"] == 1
    assert metadata["tokens_processed"] > 0
    assert metadata["input_encoding"] == "paired-query-candidate-longest-first-v1"
    assert metadata["repair_effectiveness_proven"] is False
    scorer = TrainedRankerScorer(tmp_path / "checkpoint")
    capsules = [
        workflow_capsule(w, task, ResourcePolicy(TemporalPolicy(CUTOFF), (p.reference,)))
        for w in p.workflows
    ]
    ledger = BudgetLedger(BudgetCaps(history_tokens=200000))
    result = WorkflowRanker(scorer=scorer, model=scorer.model_version).rank_workflows(
        task, capsules, ResourcePolicy(TemporalPolicy(CUTOFF), (p.reference,)), ledger
    )
    assert len(result.evaluations) == 2 and ledger.model_calls == 1
    (tmp_path / "checkpoint/head.pt").write_bytes(b"changed")
    with pytest.raises(ValueError, match="weights"):
        TrainedRankerScorer(tmp_path / "checkpoint")


def test_paired_ranker_keeps_both_long_query_and_candidate(tmp_path):
    from arex_skill_graph.embeddings import TransformerEncoder

    model_path = tmp_path / "model"
    tiny_model(model_path)
    encoder = TransformerEncoder(str(model_path))
    batch = encoder.tokenizer(
        ["type " * 2000],
        text_pair=["repair " * 2000],
        truncation="longest_first",
        max_length=encoder.max_length,
        return_tensors="pt",
    )
    ids = batch["input_ids"][0].tolist()
    assert encoder.tokenizer.convert_tokens_to_ids("type") in ids
    assert encoder.tokenizer.convert_tokens_to_ids("repair") in ids
    _, tokens = encoder.tensors(["type " * 2000], text_pairs=["repair " * 2000])
    assert tokens == encoder.max_length
    with pytest.raises(ValueError, match="cardinality"):
        encoder.tensors(["type"], text_pairs=[])


def test_execution_supervision_needs_actual_controlled_guidance(tmp_path):
    from arex_skill_graph.temporal_ranker_data import execution_label_from_run

    _data, _p, _task, queries, *_ = make_dataset(tmp_path)
    query = queries[0]
    run = {
        "task_id": query.task.task_id,
        "base_commit": query.task.base_commit,
        "solver_ended": True,
        "benchmark_resolved": True,
        "validated_resolved": True,
        "budget": {"model_tokens": 100},
        "requests": [{"operation": "finish", "arguments": {}, "rationale": "Controlled run ended"}],
        "evaluation": {
            "evaluation_completed": True,
            "evaluator_version": "synthetic-independent",
            "causal_controls_passed": True,
            "evaluation_spec_sha256": "a" * 64,
            "regression_exit_codes": [0],
        },
        "guidance_usage": [{"plan_id": "plan:one", "parent_workflow_ids": ["workflow:a"]}],
    }
    label = execution_label_from_run(query, "workflow:a", "workflow", run, sampling_probability=0.5)
    assert label.outcome and label.regression_pass and label.label_source == "execution"
    switched = {
        **run,
        "guidance_usage": [
            *run["guidance_usage"],
            {"plan_id": "plan:other", "parent_workflow_ids": ["workflow:b"]},
        ],
    }
    with pytest.raises(ValueError, match="switched away"):
        execution_label_from_run(
            query, "workflow:a", "workflow", switched, sampling_probability=0.5
        )
    with pytest.raises(ValueError, match="switched away"):
        execution_label_from_run(query, "plan:one", "plan", switched, sampling_probability=0.5)
    rebound = {
        **run,
        "guidance_usage": [
            *run["guidance_usage"],
            {
                "plan_id": "plan:rebound",
                "nominated_plan_id": "plan:one",
                "parent_workflow_ids": ["workflow:a"],
            },
        ],
    }
    assert execution_label_from_run(
        query, "plan:one", "plan", rebound, sampling_probability=0.5
    ).outcome

    for controls in (False, None):
        with pytest.raises(ValueError, match="causally reconciled"):
            execution_label_from_run(
                query,
                "workflow:a",
                "workflow",
                {**run, "evaluation": {**run["evaluation"], "causal_controls_passed": controls}},
                sampling_probability=0.5,
            )
    with pytest.raises(ValueError, match="did not use"):
        execution_label_from_run(query, "workflow:b", "workflow", run, sampling_probability=0.5)
    with pytest.raises(ValueError, match="independent"):
        execution_label_from_run(
            query,
            "workflow:a",
            "workflow",
            {**run, "solver_ended": False},
            sampling_probability=0.5,
        )
    stopped = {
        **run,
        "solver_ended": False,
        "solver_terminated": True,
        "failure": "shared model-token budget exhausted",
    }
    failed = execution_label_from_run(
        query, "workflow:a", "workflow", stopped, sampling_probability=0.5
    )
    assert failed.outcome is False
    assert failed.regression_pass is True
    with pytest.raises(ValueError, match="real solver request"):
        execution_label_from_run(
            query,
            "workflow:a",
            "workflow",
            {**stopped, "requests": []},
            sampling_probability=0.5,
        )
    with pytest.raises(ValueError, match="independent"):
        execution_label_from_run(
            query,
            "workflow:a",
            "workflow",
            {**stopped, "evaluation": {**run["evaluation"], "evaluation_completed": False}},
            sampling_probability=0.5,
        )


def test_online_neural_query_encoding_uses_shared_budget(tmp_path):
    from arex_skill_graph.adaptive_budget import BudgetedEncoder
    from arex_skill_graph.embeddings import TransformerEncoder

    model_path = tmp_path / "model"
    tiny_model(model_path)
    base = TransformerEncoder(str(model_path))
    ledger = BudgetLedger()
    encoder = BudgetedEncoder(base, ledger)
    vectors = encoder.encode(["type context"])
    assert len(vectors[0]) == base.dimensions
    assert ledger.model_calls == 1 and ledger.model_tokens > 0
    assert encoder.descriptor() == base.descriptor()


@pytest.mark.parametrize("learning_rate", [float("nan"), float("inf")])
def test_ranker_rejects_nonfinite_training_configuration(tmp_path, learning_rate):
    from arex_skill_graph.ranker_training import train_ranker

    data, *_ = make_dataset(tmp_path)
    with pytest.raises(ValueError, match="hyperparameters"):
        train_ranker(
            data, tmp_path / "unused-model", tmp_path / "checkpoint", learning_rate=learning_rate
        )


@pytest.mark.parametrize(
    "mutation", ["nan_head", "inf_head", "zero_temperature", "nan_temperature", "inf_threshold"]
)
def test_integrity_checked_ranker_rejects_invalid_numeric_state(tmp_path, mutation):
    import hashlib
    import json

    from arex_skill_graph.ranker_training import TrainedRankerScorer, train_ranker

    torch = pytest.importorskip("torch")
    data, *_ = make_dataset(tmp_path)
    model = tmp_path / "tiny-model"
    tiny_model(model)
    root = tmp_path / "checkpoint"
    metadata = train_ranker(data, model, root, epochs=1)
    if mutation.endswith("_head"):
        state = torch.load(root / "head.pt", map_location="cpu", weights_only=True)
        state["weight"][0, 0] = float("nan") if mutation == "nan_head" else float("inf")
        torch.save(state, root / "head.pt")
        metadata["head_sha256"] = hashlib.sha256((root / "head.pt").read_bytes()).hexdigest()
        metadata["checkpoint_sha256"] = digest(
            {k: v for k, v in metadata.items() if k != "checkpoint_sha256"}
        )
    elif mutation == "zero_temperature":
        metadata["temperature"] = 0.0
        metadata["checkpoint_sha256"] = digest(
            {k: v for k, v in metadata.items() if k != "checkpoint_sha256"}
        )
    elif mutation == "nan_temperature":
        metadata["temperature"] = float("nan")
    else:
        metadata["use_threshold"] = float("inf")
    (root / "ranker.json").write_text(json.dumps(metadata))
    with pytest.raises(ValueError, match="nonfinite|positive"):
        TrainedRankerScorer(root)


def test_nonfinite_ranker_features_fail_and_keep_call_accounting(tmp_path, monkeypatch):
    from arex_skill_graph.action_contracts import TemporalPolicy
    from arex_skill_graph.ranker_training import TrainedRankerScorer, train_ranker

    torch = pytest.importorskip("torch")
    data, package, task, *_ = make_dataset(tmp_path)
    model = tmp_path / "tiny-model"
    tiny_model(model)
    checkpoint = tmp_path / "checkpoint"
    train_ranker(data, model, checkpoint, epochs=1)
    scorer = TrainedRankerScorer(checkpoint)
    policy = ResourcePolicy(TemporalPolicy(CUTOFF), (package.reference,))
    capsules = [workflow_capsule(w, task, policy) for w in package.workflows]
    monkeypatch.setattr(
        scorer.encoder,
        "tensors",
        lambda texts, **_: (torch.full((len(texts), scorer.encoder.dimensions), float("nan")), 8),
    )
    ledger = BudgetLedger()
    with pytest.raises(ValueError, match="ranker features.*nonfinite"):
        scorer.evaluate(task, capsules, ledger)
    assert ledger.model_calls == 1 and ledger.model_tokens > 0
