"""Original supervision retains gaps and never uses private or native-parent inputs."""

import importlib.util
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest
from test_original_query_evaluator import (
    authority as authority,  # noqa: PLC0414 -- Re-export pytest fixture.
)

from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.original_supervision_registry import (
    OriginalSupervisionRegistry,
    build_original_supervision_registry,
)
from arex_skill_graph.temporal_ranker_data import HistoricalQuery

MODULE = "arex_skill_graph.original_supervision_registry"
TRAIN = "2021-01-01T00:00:00Z"
MAIN = "2024-01-01T00:00:00Z"


@pytest.fixture
def registered(authority, tmp_path, monkeypatch):
    # Extend and reseal the synthetic evaluator fixture. No actual model calls.
    import hashlib

    from arex_skill_graph.task_context import TaskContext

    monkeypatch.setattr(TaskContext, "verify", lambda self, **kwargs: None)
    task, verification, controls, runtime_hash = authority
    native = json.loads(verification.read_text())
    native["identity"]["fix_id"] = "example/project:pr:2"
    write_json(verification, native)
    cohort = json.loads((controls / "cohort.json").read_text())
    cohort["native_identity"] = native["identity"]
    cohort["native_report_content_sha256"] = fingerprint(native)
    cohort["cohort_sha256"] = fingerprint({k: v for k, v in cohort.items() if k != "cohort_sha256"})
    write_json(controls / "cohort.json", cohort)
    completion = json.loads((controls / "completion.json").read_text())
    from arex_skill_graph.historical_replay_controls import verify_replay_controls

    phases = {
        n: json.loads((controls / (n + ".json")).read_text())
        for n in ("original_base", "base_with_regression", "known_repair")
    }
    completion.update(
        verify_replay_controls(
            cohort, phases, source_files_unchanged=True, task_input_unchanged=True
        )
    )
    completion["native_verification_file_sha256"] = hashlib.sha256(
        verification.read_bytes()
    ).hexdigest()
    write_json(controls / "completion.json", completion)
    review_input = json.loads((controls / "input.json").read_text())
    review_input.update(frozen_current_cohort=cohort, mechanical_controls=completion)
    write_json(controls / "input.json", review_input)
    review = json.loads((controls / "review.json").read_text())
    review.update(
        review_input_sha256=fingerprint(review_input),
        control_completion_sha256=fingerprint(completion),
    )
    review["cohort_sha256"] = cohort["cohort_sha256"]
    write_json(controls / "review.json", review)
    query = HistoricalQuery(task, task.task_id, native["identity"]["fix_id"], (task.task_id,))
    raw = {
        "task": task.to_dict(),
        "bug_cluster_id": query.bug_cluster_id,
        "fix_id": query.fix_id,
        "aliases": list(query.aliases),
        "copied_from": [],
        "exposed": False,
    }
    queries, register_path = tmp_path / "queries.json", tmp_path / "query-register.json"
    write_json(queries, [raw])
    register = {
        "queries_sha256": fingerprint([raw]),
        "selected_registered_targets": 3,
        "audits": [
            {
                "query_id": task.task_id,
                "status": "registered_original_public_branch_query",
                "base_commit": task.base_commit,
                "input_available_at": task.input_available_at,
            },
            {"query_id": "example/project:3", "status": "original_input_unrecovered"},
            {"query_id": "example/project:4", "status": "public_branch_source_or_input_gap"},
        ],
    }
    write_json(register_path, register)
    runtime = tmp_path / "query-runtime"
    runtime.mkdir()
    bindings = {
        task.task_id: {
            "verification_path": str(verification),
            "controls_dir": str(controls),
            "independent_review_path": str(controls / "review.json"),
            "dependency_root": str(runtime),
        }
    }
    return {
        "query": query,
        "queries": queries,
        "register": register_path,
        "bindings": bindings,
        "controls": controls,
        "runtime": runtime,
        "runtime_hash": runtime_hash,
        "registry": tmp_path / "registry.json",
    }


def build(state, bindings=None):
    return build_original_supervision_registry(
        state["queries"],
        state["register"],
        state["bindings"] if bindings is None else bindings,
        training_cutoff=TRAIN,
        main_cutoff=MAIN,
    )


def load(state, bindings=None):
    write_json(state["registry"], build(state, bindings))
    return OriginalSupervisionRegistry(state["registry"], state["queries"], state["register"])


def test_ready_query_and_unrecovered_targets_share_full_denominator(registered):
    registry = load(registered)
    assert len(registry.coverage()) == 3
    assert [row["readiness"] for row in registry.coverage()] == [
        "ready",
        "original_input_unavailable",
        "original_input_unavailable",
    ]
    route = registry.route(registered["query"])
    assert route.dependency_root == registered["runtime"]
    assert route.required_runtime_sha256 == registered["runtime_hash"]
    assert all(row["failure_label_created"] is False for row in registry.coverage())
    assert registry.payload["training_cutoff"] == TRAIN
    assert registry.payload["formal_SWE_runs"] == 0


@pytest.mark.parametrize(
    "variant",
    ["duplicate_audit", "lost_audit", "lost_available_input", "extra_binding", "policy_drift"],
)
def test_registry_rejects_omissions_duplicates_and_retiming(registered, variant):
    register = json.loads(registered["register"].read_text())
    bindings = deepcopy(registered["bindings"])
    if variant == "duplicate_audit":
        register["audits"][-1] = register["audits"][0]
    elif variant == "lost_audit":
        register["audits"].pop()
    elif variant == "lost_available_input":
        write_json(registered["queries"], [])
        register["queries_sha256"] = fingerprint([])
    elif variant == "extra_binding":
        bindings["unregistered:5"] = {}
    else:
        register["training_cutoff"] = "2022-01-01T00:00:00Z"
    write_json(registered["register"], register)
    with pytest.raises(ValueError):
        build(registered, bindings)


@pytest.mark.parametrize(
    "artifact", ["queries", "register", "registry", "completion", "review", "calls", "diff"]
)
def test_sources_and_authority_are_rechecked_before_reuse(registered, artifact):
    registry = load(registered)
    paths = {
        **{key: registered[key] for key in ("queries", "register", "registry")},
        "completion": registered["controls"] / "completion.json",
        "review": registered["controls"] / "review.json",
        "calls": registered["controls"] / "calls.json",
        "diff": Path(
            registered["bindings"][registered["query"].task.task_id]["verification_path"]
        ).with_name("historical-diff.json"),
    }
    path = paths[artifact]
    path.write_text(path.read_text() + " ")
    with pytest.raises(ValueError):
        registry.route(registered["query"])


def test_alias_cluster_fix_and_task_drift_cannot_reuse_a_route(registered):
    registry = load(registered)
    for query in (
        replace(registered["query"], aliases=("another:issue",)),
        replace(registered["query"], bug_cluster_id="another:cluster"),
        replace(registered["query"], fix_id="another:fix"),
        replace(
            registered["query"],
            task=replace(registered["query"].task, public_problem="changed input"),
        ),
    ):
        with pytest.raises(ValueError, match="query record"):
            registry.route(query)


@pytest.mark.parametrize("mount", ["public", "runtime"])
def test_private_authority_cannot_enter_any_actor_mount(registered, mount):
    bindings = deepcopy(registered["bindings"])
    actor_root = Path(registered["query"].task.root) if mount == "public" else registered["runtime"]
    bindings[registered["query"].task.task_id]["independent_review_path"] = str(
        actor_root / "private-review.json"
    )
    with pytest.raises(ValueError, match="actor-visible"):
        build(registered, bindings)


@pytest.mark.parametrize(
    "variant,expected",
    [
        ("no_review", "independent_review_pending"),
        ("review_rejected", "independent_review_rejected"),
        ("no_runtime", "runtime_missing"),
        ("no_controls", "controls_missing"),
        ("unqualified_controls", "controls_unqualified"),
        ("old_controls", "controls_authority_incomplete"),
    ],
)
def test_unqualified_conditions_are_not_negative_labels(registered, variant, expected):
    bindings = deepcopy(registered["bindings"])
    binding = bindings[registered["query"].task.task_id]
    if variant == "no_review":
        binding["independent_review_path"] = None
    elif variant == "review_rejected":
        path = registered["controls"] / "review.json"
        review = json.loads(path.read_text())
        review.update(accepted_limited_replay=False, mechanism_alignment="UNKNOWN")
        write_json(path, review)
    elif variant == "no_runtime":
        binding["dependency_root"] = str(registered["runtime"] / "missing")
    elif variant == "no_controls":
        binding["controls_dir"] = str(registered["runtime"].parent / "missing-controls")
    else:
        path = registered["controls"] / "completion.json"
        value = json.loads(path.read_text())
        if variant == "old_controls":
            del value["production_projection"]
        else:
            value["mechanical_controls_passed"] = False
        write_json(path, value)
    registry = load(registered, bindings)
    row = registry.coverage()[0]
    assert row["readiness"] == expected
    assert not row["supervision_allowed"] and not row["failure_label_created"]
    assert registry.route(registered["query"]) is None


def test_fix_mismatch_is_not_a_pending_review(registered):
    verification = Path(
        registered["bindings"][registered["query"].task.task_id]["verification_path"]
    )
    value = json.loads(verification.read_text())
    value["identity"]["fix_id"] = "wrong:fix"
    write_json(verification, value)
    with pytest.raises(ValueError, match="fix identity"):
        build(registered)


def test_route_rechecks_private_authority_after_solver_termination(registered, monkeypatch):
    registry = load(registered)
    calls = []

    def factory(verification, runtime, controls, **kwargs):
        assert runtime == str(registered["runtime"])
        assert kwargs["independent_review_path"] == str(registered["controls"] / "review.json")

        def evaluator(task, patch):
            calls.append((task.task_id, patch))
            return {"evaluation_completed": True}

        return evaluator

    monkeypatch.setattr(MODULE + ".original_query_evaluator", factory)
    route = registry.route(registered["query"])
    assert not calls
    route.evaluator(registered["query"].task, "submission")
    assert calls == [(registered["query"].task.task_id, "submission")]
    registered["controls"].joinpath("completion.json").write_text("{}")
    with pytest.raises(ValueError):
        route.evaluator(registered["query"].task, "submission")
    assert len(calls) == 1


def runner(registered, monkeypatch):
    path = Path(__file__).resolve().parents[1] / "experiments/run_historical_ranker_supervision.py"
    spec = importlib.util.spec_from_file_location("original_registry_unit_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    class Encoder:
        def __init__(self, *args):
            pass

        def descriptor(self):
            return {"synthetic_unit_encoder": True}

        def encode(self, inputs):
            return [[1.0] for _ in inputs]

    monkeypatch.setattr(module, "TransformerEncoder", Encoder)
    references = registered["queries"].parent / "references.json"
    write_json(references, [])
    args = [
        "--queries",
        str(registered["queries"]),
        "--query-register",
        str(registered["register"]),
        "--references",
        str(references),
        "--embedding-model",
        "synthetic-unit-only",
        "--output-dir",
        str(registered["queries"].parent / "study"),
        "--model",
        "synthetic-unit-only",
        "--base-url",
        "https://example.invalid/v1",
        "--original-supervision-registry",
        str(registered["registry"]),
        "--candidate-kind",
        "plan",
    ]
    return module, args


def test_runner_preparation_retains_denominator_without_model_calls(registered, monkeypatch):
    load(registered)
    module, args = runner(registered, monkeypatch)
    monkeypatch.setattr(
        module, "transport_from_args", lambda *_: pytest.fail("model transport during preparation")
    )
    assert module.main([*args, "--prepare-only"]) == 0
    study = registered["queries"].parent / "study"
    assert len(json.loads((study / "query-population.json").read_text())) == 3
    assert len(json.loads((study / "controlled-schedule.json").read_text())) == 1
    assert (
        json.loads((study / "study-identity.json").read_text())["evaluation_route"]
        == "original_query"
    )


def test_runner_keeps_unreviewed_queries_unrun_with_zero_labels(registered, monkeypatch):
    bindings = deepcopy(registered["bindings"])
    bindings[registered["query"].task.task_id]["independent_review_path"] = None
    load(registered, bindings)
    module, args = runner(registered, monkeypatch)
    monkeypatch.setattr(
        module, "transport_from_args", lambda *_: pytest.fail("unqualified query model call")
    )
    assert module.main(args) == 0
    study = registered["queries"].parent / "study"
    results = json.loads((study / "study-results.json").read_text())
    assert results["registered_query_count"] == 3
    assert results["results"][0]["status"] == "qualification_pending_unrun"
    assert results["results"][0]["live_calls"] == 0
    assert json.loads((study / "labels.json").read_text()) == []


def test_runner_uses_original_route_and_per_query_runtime(registered, monkeypatch):
    load(registered)
    module, args = runner(registered, monkeypatch)
    seen = {}

    class Transport:
        calls = 0

    class Store:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def initialize(self):
            pass

    class Solver:
        SYSTEM = "synthetic-unit-only"

        def __init__(self, *args, **kwargs):
            seen["runtime"] = kwargs["dependency_root"]
            seen["required_hash"] = kwargs["required_runtime_sha256"]

        def run(self, task, *, evaluator, **kwargs):
            evaluation = evaluator(task, "unit-submission")
            return {
                "solver_terminated": True,
                "benchmark_resolved": False,
                "evaluation": evaluation,
            }

    monkeypatch.setattr(module, "transport_from_args", lambda *_: Transport())
    monkeypatch.setattr(module, "CatalogStore", Store)
    monkeypatch.setattr(module, "AdaptiveSolver", Solver)
    monkeypatch.setattr(
        module, "historical_evaluator", lambda *_a, **_k: pytest.fail("native-parent fallback")
    )

    def evaluator_factory(*args, **kwargs):
        seen["evaluator_runtime"] = args[1]
        return lambda task, patch: {"evaluation_completed": True, "causal_controls_passed": True}

    monkeypatch.setattr(MODULE + ".original_query_evaluator", evaluator_factory)
    assert module.main(args) == 0
    assert seen["runtime"] == registered["runtime"]
    assert seen["evaluator_runtime"] == str(registered["runtime"])
    assert seen["required_hash"] == registered["runtime_hash"]


def test_runner_rejects_concurrent_external_calls(registered, monkeypatch):
    load(registered)
    module, args = runner(registered, monkeypatch)
    with pytest.raises(SystemExit):
        module.main([*args, "--workers", "2"])
