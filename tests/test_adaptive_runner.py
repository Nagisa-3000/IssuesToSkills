import json
from pathlib import Path

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.adaptive_runner import (
    AdaptiveSolver,
    IsolationUnavailable,
    NamespaceTools,
    bounded_public_view,
    hidden_evaluator_from_file,
    request_history_view,
)
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.workflow_ranker import WorkflowRanker


def isolated_tools_or_skip(root):
    tools = NamespaceTools(root, BudgetLedger())
    try:
        tools.preflight()
    except IsolationUnavailable:
        pytest.skip(
            "Linux namespace capability unavailable; production runner refuses unsafe fallback"
        )
    return tools


def test_enforced_filesystem_network_environment_and_write_isolation(tmp_path):
    root = tmp_path / "public"
    root.mkdir()
    host_only = tmp_path / "hidden-evaluator.txt"
    host_only.write_text("private evaluator material")
    tools = isolated_tools_or_skip(root)
    code = """import os,socket,pathlib
assert not pathlib.Path('/home').exists()
assert not pathlib.Path('/run').exists()
assert not pathlib.Path(HOST_PATH).exists()
assert sorted(os.environ)==['HOME','LANG','LC_CTYPE','PATH','PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED'] or set(os.environ)<=set(['HOME','LANG','LC_CTYPE','PATH','PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED'])
s=socket.socket(); s.settimeout(0.2)
try:
 s.connect(('1.1.1.1',80)); raise AssertionError('network escaped')
except OSError: pass
try:
 pathlib.Path('/usr/arex-write-test').write_text('forbidden'); raise AssertionError('runtime writable')
except OSError: pass
pathlib.Path('/workspace/public-result.txt').write_text('allowed')
print('ISOLATION_PASS')
""".replace("HOST_PATH", repr(str(host_only)))
    result = tools.run(["python3", "-c", code])
    assert result["exit_code"] == 0, result
    assert (root / "public-result.txt").read_text() == "allowed"
    assert host_only.read_text() == "private evaluator material"


def test_hidden_evaluator_only_after_solver_finishes(tmp_path):
    _p, task, policy = make_fixture(tmp_path)
    isolated_tools_or_skip(Path(task.root))
    marker = tmp_path / "private-evaluation.json"
    old = Path(task.root, "checker.py").read_text()
    fixed = old.replace("return True", "return context != 'type'")
    steps = [
        {
            "operation": "read_file",
            "arguments": {"path": "checker.py"},
            "rationale": "Inspect current public implementation",
        },
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Reproduce public defect",
        },
        {
            "operation": "write_file",
            "arguments": {"path": "checker.py", "content": fixed},
            "rationale": "Narrow current diagnostic guard",
        },
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Verify public repaired and runtime cases",
        },
        {"operation": "finish", "arguments": {}, "rationale": "Public behavior verified"},
    ]

    class CheckingReplay(ReplayTransport):
        def complete(self, **kwargs):
            assert not marker.exists()
            assert "hidden_test_patch" not in kwargs["user"]
            return super().complete(**kwargs)

    evaluated = []

    def evaluator(task, patch):
        # Creating this private file now proves it was absent during every model call.
        marker.write_text(
            json.dumps(
                {
                    "task_id": task.task_id,
                    "base_commit": task.base_commit,
                    "hidden_test_patch": "",
                    "evaluator_version": "synthetic-independent-v1",
                    "benchmark_commands": [["python3", "checker.py"]],
                    "regression_commands": [
                        [
                            "python3",
                            "-c",
                            "from checker import diagnostic; assert diagnostic('runtime')",
                        ]
                    ],
                }
            )
        )
        evaluated.append(True)
        return hidden_evaluator_from_file(marker)(task, patch)

    with CatalogStore(tmp_path / "catalog.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            CheckingReplay(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            arm="B0",
        ).run(task, evaluator=evaluator)
    assert evaluated and result["solver_ended"]
    assert result["benchmark_resolved"] is True and result["validated_resolved"] is True, result
    assert len(result["public_observations"]) == 4
    assert result["budget"]["model_calls"] == 5
    assert "hidden_test_patch" not in json.dumps(result)
    assert Path(task.root, "checker.py").read_text() == old


def test_paired_metrics_include_failures():
    from arex_skill_graph.experiment_metrics import ndcg, summarize_runs

    rows = [
        {
            "task_id": str(i),
            "bug_cluster_id": str(i),
            "arm": arm,
            "validated_resolved": i == 0 and arm == "E2",
            "benchmark_resolved": i == 0 and arm == "E2",
        }
        for arm in ("E1", "E2")
        for i in range(2)
    ]
    report = summarize_runs(rows)
    assert report["arms"]["E2"]["ValidatedResolved@1"] == 0.5
    assert report["paired"][0]["paired_issues"] == 2
    assert ndcg(["bad", "good"], {"bad": 0, "good": 2}) < 1


def test_prompt_excerpts_keep_boundaries_and_do_not_replay_full_writes():
    content = "BEGIN\n" + "x" * 20000 + "\nEND"
    original = {"output": content}
    excerpt = bounded_public_view(original, text_limit=1000)["output"]
    assert excerpt.startswith("BEGIN") and excerpt.endswith("END")
    assert len(excerpt) < 1300 and "sha256=" in excerpt
    assert original["output"] == content
    requests = [
        {
            "operation": "write_file",
            "arguments": {"path": "source.py", "content": content},
            "rationale": "Repair current source",
        }
    ]
    viewed = request_history_view(requests)
    assert "content" not in viewed[0]["arguments"]
    assert viewed[0]["arguments"]["content_characters"] == len(content)
    assert requests[0]["arguments"]["content"] == content


def test_budget_stop_is_evaluated_but_never_counted_as_solver_success(tmp_path):
    _, task, policy = make_fixture(tmp_path)
    isolated_tools_or_skip(Path(task.root))
    evaluated = []

    def evaluate(task, patch):
        evaluated.append(True)
        return {"benchmark_resolved": True, "validated_resolved": True}

    with CatalogStore(tmp_path / "empty.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            ReplayTransport([]),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(model_tokens=1)),
            arm="B0",
        ).run(task, evaluator=evaluate)
    assert evaluated and result["solver_terminated"]
    assert not result["solver_ended"]
    assert result["benchmark_resolved"] is False
    assert result["validated_resolved"] is False
    assert result["failure"] == "model request cannot fit remaining token budget"


def test_probe_workspace_is_actually_readonly(tmp_path):
    root = tmp_path / "public"
    root.mkdir()
    (root / "source.txt").write_text("base")
    tools = isolated_tools_or_skip(root)
    result = tools.run(
        ["python3", "-c", "from pathlib import Path; Path('source.txt').write_text('modified')"],
        readonly_workspace=True,
    )
    assert result["exit_code"] != 0
    assert (root / "source.txt").read_text() == "base"


def test_frozen_pool_cli_compares_prompted_and_trained_with_isolated_branches(tmp_path):
    import importlib.util

    from adaptive_fixture import CUTOFF, make_fixture
    from test_adaptive_contracts import RankingReplay, good_plan
    from test_temporal_ranker_training import make_dataset, tiny_model

    from arex_skill_graph.adaptive_cli import write_json
    from arex_skill_graph.adaptive_guidance import index_native_package
    from arex_skill_graph.ranker_training import train_ranker
    from arex_skill_graph.workflow_ranker import plan_capsule

    package, task, policy = make_fixture(tmp_path / "native")
    isolated_tools_or_skip(Path(task.root))
    dataset, *_ = make_dataset(tmp_path / "training")
    tiny_model(tmp_path / "model")
    train_ranker(dataset, tmp_path / "model", tmp_path / "checkpoint", epochs=1)
    plan = good_plan(package, task)
    capsule, _ = plan_capsule(plan, task, policy)
    prompted = RankingReplay().complete(user=json.dumps({"candidates": [capsule.to_dict()]}))
    original = Path(task.root, "checker.py").read_text()
    fixed = original.replace("return True", "return context != 'type'")
    solver_steps = [
        {
            "operation": "write_file",
            "arguments": {"path": "checker.py", "content": fixed},
            "rationale": "Synthetic current repair",
        },
        {"operation": "finish", "arguments": {}, "rationale": "End before evaluation"},
    ]
    private = tmp_path / "evaluator.json"
    private.write_text(
        json.dumps(
            {
                "task_id": task.task_id,
                "base_commit": task.base_commit,
                "evaluator_version": "synthetic-shared-pool-v1",
                "benchmark_commands": [["python3", "checker.py"]],
                "regression_commands": [
                    [
                        "python3",
                        "-c",
                        "from checker import diagnostic; assert diagnostic('runtime')",
                    ]
                ],
            }
        )
    )
    write_json(
        tmp_path / "tasks.json",
        [
            {
                "task": task.to_dict(),
                "bug_cluster_id": "synthetic:current",
                "evaluator_manifest": str(private),
            }
        ],
    )
    write_json(tmp_path / "references.json", [package.reference])
    write_json(
        tmp_path / "pool.json", {task.task_id: {"task": task.to_dict(), "plans": [plan.to_dict()]}}
    )
    write_json(
        tmp_path / "replay.json",
        {task.task_id: {"prompted": [prompted, *solver_steps], "trained": solver_steps}},
    )
    db = tmp_path / "catalog.sqlite"
    with CatalogStore(db) as store:
        store.initialize()
        index_native_package(store, package.reference, policy.temporal)
    script = Path(__file__).resolve().parents[1] / "experiments/eval_pattern_crossbind_ranker.py"
    spec = importlib.util.spec_from_file_location("shared_pool_cli", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = [
        "--tasks",
        str(tmp_path / "tasks.json"),
        "--references",
        str(tmp_path / "references.json"),
        "--db",
        str(db),
        "--output",
        str(tmp_path / "results.json"),
        "--cutoff",
        CUTOFF,
        "--mode",
        "shared-pool",
        "--pool",
        str(tmp_path / "pool.json"),
        "--checkpoint",
        str(tmp_path / "checkpoint"),
        "--replay",
        str(tmp_path / "replay.json"),
    ]
    assert module.main(args) == 0
    result = json.loads((tmp_path / "results.json").read_text())
    assert len(result["runs"]) == 2
    assert all(row.get("validated_resolved") is True for row in result["runs"]), result["runs"]
    decisions = result["shared_pool_decisions"]
    assert {row["arm"] for row in decisions} == {"prompted", "trained"}
    assert len({row["pool_sha256"] for row in decisions}) == 1
    assert result["configuration"]["offline_replay"] is True
    assert result["repair_effectiveness_proven"] is False
    assert Path(task.root, "checker.py").read_text() == original


def test_snapshot_preserves_reviewed_execution_modes(tmp_path):
    from dataclasses import replace
    from arex_skill_graph.adaptive_runner import snapshot_base
    from arex_skill_graph.task_context import EvidenceAnchor
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256

    _, task, _ = make_fixture(tmp_path)
    Path(task.root).chmod(0o750)
    Path(task.root, "checker.py").chmod(0o664)
    Path(task.root, "context.py").chmod(0o640)
    seal = public_workspace_execution_sha256(task.root)
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor(
                "reviewed:workspace",
                "workspace_execution_snapshot",
                "Reviewed public state",
                task.base_commit,
                sha256=seal,
            ),
        ),
    )
    copied = snapshot_base(task, tmp_path / "snapshot")
    copied.verify(verify_head=False)
    assert public_workspace_execution_sha256(copied.root) == seal
    assert not Path(copied.root, ".git").exists()


def test_snapshot_does_not_transfer_reviewed_modes_to_different_content(tmp_path):
    import hashlib
    from dataclasses import replace
    from arex_skill_graph.adaptive_runner import snapshot_base
    from arex_skill_graph.task_context import EvidenceAnchor
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256

    _, task, _ = make_fixture(tmp_path)
    path = Path(task.root, "checker.py")
    path.write_text(path.read_text().replace("return True", "return False"))
    anchors = tuple(
        replace(a, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        if a.path == "checker.py"
        else a
        for a in task.anchors
    )
    task = replace(
        task,
        anchors=(
            *anchors,
            EvidenceAnchor(
                "reviewed:workspace",
                "workspace_execution_snapshot",
                "Reviewed changed state",
                task.base_commit,
                sha256=public_workspace_execution_sha256(task.root),
            ),
        ),
    )
    task.verify()
    with pytest.raises(ValueError, match="content differs from the pinned base archive"):
        snapshot_base(task, tmp_path / "snapshot")


@pytest.mark.parametrize("exit_code,expected", [(0, True), (1, False), (None, None)])
def test_unexecuted_public_probe_is_unknown_and_drops_the_old_fact(tmp_path, exit_code, expected):
    from arex_skill_graph.task_context import ObservedFact

    _, task, policy = make_fixture(tmp_path)
    task = task.update(
        facts=(ObservedFact("last_public_probe_passed", True, ("current:checker",)),)
    )

    class ProbeTools:
        isolation = "test-only-probe-fixture"
        runtime_sha256 = "test-only"

        def __init__(self, root, ledger):
            pass

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **options):
            return {
                "argv": argv,
                "exit_code": exit_code,
                "execution_available": exit_code is not None,
                "output": "Fixture outcome",
            }

    class CapturingReplay(ReplayTransport):
        def __init__(self, steps):
            super().__init__(steps)
            self.contexts = []

        def complete(self, **kwargs):
            self.contexts.append(json.loads(kwargs["user"])["current"])
            return super().complete(**kwargs)

    replay = CapturingReplay(
        [
            {
                "operation": "run_public_command",
                "arguments": {"argv": ["python3", "-V"]},
                "rationale": "Observe an execution availability control",
            },
            {"operation": "finish", "arguments": {}, "rationale": "Finish broker fixture"},
        ]
    )
    with CatalogStore(tmp_path / "probe.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            replay,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            arm="B0",
            tools_factory=ProbeTools,
        ).run(task)
    assert result["solver_ended"] and not result["failure"]
    latest = [f for f in replay.contexts[-1]["facts"] if f["key"] == "last_public_probe_passed"]
    assert ([f["value"] for f in latest] == [expected]) if expected is not None else not latest


def test_frozen_refresh_rebinds_without_running_candidate_generation(tmp_path, monkeypatch):
    import arex_skill_graph.adaptive_runner as runner
    from test_adaptive_contracts import good_plan

    package, task, policy = make_fixture(tmp_path)
    initial = good_plan(package, task)
    before = initial.to_dict()

    def reject_generation(*_args, **_kwargs):
        raise AssertionError("fixed candidate refresh invoked retrieval/rewrite/composition")

    monkeypatch.setattr(runner, "prepare_adaptive_guidance", reject_generation)

    class EmptyTestTools:
        isolation = "test-only-no-command-execution"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            pass

        def preflight(self):
            pass

        def close(self):
            pass

    replay = ReplayTransport(
        [
            {
                "operation": "refresh_guidance",
                "arguments": {},
                "rationale": "Renew fixed current binding",
            },
            {"operation": "finish", "arguments": {}, "rationale": "End fixed-scope protocol test"},
        ]
    )
    with CatalogStore(tmp_path / "frozen.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            replay,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=EmptyTestTools,
        ).run(task, use_frozen_selection=True, initial_plan=initial)
    assert result["solver_ended"] and not result["failure"]
    assert result["candidate_generation_frozen"] is True
    assert result["nominated_plan_id"] == initial.id
    refresh = result["guidance_runs"][0]
    assert refresh["candidate_generation_frozen"] is True
    refreshed = refresh["selected_plan"]
    assert tuple(refreshed["parent_workflow_ids"]) == initial.parent_workflow_ids
    assert {i["action"]["id"] for i in refreshed["instances"]} == {
        i.action.id for i in initial.instances
    }
    assert all(
        row.get("nominated_plan_id", initial.id) == initial.id for row in result["guidance_usage"]
    )
    assert initial.to_dict() == before


def test_frozen_rebinding_retains_actions_and_rejects_tampered_contract(tmp_path):
    from dataclasses import replace
    from test_adaptive_contracts import good_plan
    from arex_skill_graph.workflow_rewriter import rebind_frozen_plan

    package, task, policy = make_fixture(tmp_path)
    initial = good_plan(package, task)
    updated = task.update()
    rebound = rebind_frozen_plan(initial, updated, policy)
    assert rebound.context_revision == updated.revision
    assert rebound.parent_workflow_ids == initial.parent_workflow_ids
    assert tuple(i.action for i in rebound.instances) == tuple(i.action for i in initial.instances)
    assert set(initial.required_effects).issubset(rebound.required_effects)
    assert set(initial.invariants).issubset(rebound.invariants)
    changed = replace(initial.instances[0].action, operation="invented unsourced operation")
    corrupted = replace(
        initial, instances=(replace(initial.instances[0], action=changed), *initial.instances[1:])
    )
    with pytest.raises(ValueError, match="authoritative"):
        rebind_frozen_plan(corrupted, updated, policy)


def test_solver_finishes_after_large_record_without_replaying_nested_witnesses(tmp_path):
    from dataclasses import replace
    from arex_skill_graph.task_context import EvidenceAnchor

    package, task, policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[-1]
    output = "BEGIN public evidence\n" + "x" * 30000 + "\nEND public evidence"
    prior = {
        "argv": ["python3", "-V"],
        "exit_code": 1,
        "output": output,
        "isolation": "test-only-projection-fixture",
    }
    task = replace(
        task,
        anchors=(
            *task.anchors,
            *(
                EvidenceAnchor(
                    "current:probe:" + str(i),
                    "probe",
                    json.dumps(prior),
                    task.base_commit,
                    exit_code=1,
                )
                for i in range(18)
            ),
        ),
    )

    class ProjectionTools:
        isolation = "test-only-projection-fixture"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            pass

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **_options):
            return {**prior, "argv": argv}

    class RecordingTransport:
        def __init__(self):
            self.frames = []

        def complete(self, **kwargs):
            frame = json.loads(kwargs["user"])
            self.frames.append(frame)
            if len(self.frames) == 1:
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": ["python3", "-V"]},
                    "rationale": "Observe a failed fixture command; no repair claim",
                }
            if len(self.frames) == 2:
                return {
                    "operation": "record_action_observation",
                    "arguments": {
                        "action_id": action.id,
                        "context_revision": frame["current"]["revision"],
                        "summary": "Recorded failed public evidence, not semantic success.",
                        "outputs": [],
                        "observation_ids": [frame["observations"][-1]["observation_id"]],
                        "artifact_paths": [],
                    },
                    "rationale": "Retain actual unreviewed execution evidence",
                }
            return {
                "operation": "finish",
                "arguments": {},
                "rationale": "Finish this broker protocol fixture without a repair claim",
            }

    transport = RecordingTransport()
    with CatalogStore(tmp_path / "projection.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(model_tokens=145000, history_tokens=200000)),
            arm="B0",
            tools_factory=ProjectionTools,
        ).run(task, use_frozen_selection=True, recordable_actions=(action,))
    assert result["solver_ended"] and not result["failure"], {
        "failure": result["failure"],
        "budget": result["budget"]["model_tokens"],
        "frames": [{k: len(json.dumps(v)) for k, v in frame.items()} for frame in transport.frames],
    }
    assert result["budget"]["model_tokens"] <= 145000
    assert len(transport.frames) == 3
    record = result["action_observations"][0]
    assert record["witnesses"][0]["record"]["output"] == output
    assert record["witnesses"][0]["record"]["exit_code"] == 1
    assert record["semantic_validation"] == "unreviewed"
    assert record["repair_success_established"] is False
    assert result["benchmark_resolved"] is None
    assert result["public_observations"][0]["output"] == output


def test_solver_receipt_views_preserve_failed_witnesses_and_original_hashes(tmp_path):
    import copy
    import hashlib
    from dataclasses import replace
    from test_action_observations import exercise
    from arex_skill_graph.action_contracts import digest
    from arex_skill_graph.action_observations import record_action_observation
    from arex_skill_graph.adaptive_runner import solver_current_view, solver_observation_view
    from arex_skill_graph.task_context import EvidenceAnchor

    action, task, request, observations = exercise(tmp_path)
    broker = observations["public:observation:0"]
    broker["output"] = "BEGIN\n" + "x" * 30000 + "\nEND"
    record = record_action_observation(
        action, request, task, observations, record_id="action-result:0"
    )
    observation = {
        "operation": "record_action_observation",
        "observation_id": "public:observation:1",
        "context_revision": task.revision,
        "record": record,
    }
    original = copy.deepcopy(observation)
    viewed = solver_observation_view(observation)
    assert observation == original
    assert viewed["record"]["full_action_record_sha256"] == digest(record)
    assert json.dumps(viewed["record"]["outputs"]) == json.dumps(record["outputs"])
    assert viewed["record"]["semantic_validation"] == "unreviewed"
    assert not viewed["record"]["repair_success_established"]
    witnesses = viewed["record"]["witnesses"]
    tool = next(w for w in witnesses if w["kind"] == "broker_observation")
    assert "record" not in tool
    assert tool["record_sha256"] == digest(broker)
    assert tool["broker_summary"]["argv"] == broker["argv"]
    assert tool["broker_summary"]["observation_id"] == broker["observation_id"]
    assert tool["broker_summary"]["exit_code"] == 1
    assert "output" not in tool["broker_summary"]
    assert (
        tool["broker_summary"]["output_sha256"]
        == hashlib.sha256(broker["output"].encode()).hexdigest()
    )
    assert len(json.dumps(viewed)) < len(json.dumps(bounded_public_view(observation))) / 2
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor(
                "current:probe:0", "probe", json.dumps(broker), task.base_commit, exit_code=1
            ),
        ),
    )
    before = task.to_dict()
    context = solver_current_view(task)
    assert task.to_dict() == before
    assert "root" not in context
    assert json.dumps(context["facts"]) == json.dumps(before["facts"])
    assert json.dumps(context["bindings"]) == json.dumps(before["bindings"])
    assert json.dumps(context["oracles"]) == json.dumps(before["oracles"])
    probe = context["anchors"][-1]["broker_summary"]
    assert probe["argv"] == broker["argv"] and probe["exit_code"] == 1
    assert "output_excerpt" not in probe
    assert probe["output_characters"] == len(broker["output"])
    assert (
        context["anchors"][-1]["full_observation_sha256"]
        == hashlib.sha256(json.dumps(broker).encode()).hexdigest()
    )


@pytest.mark.parametrize("observation", ["plain public probe", "[]", "{", '{"note":"public"}'])
def test_solver_context_handles_non_broker_probe_evidence_without_changing_it(
    tmp_path, observation
):
    from dataclasses import replace
    from arex_skill_graph.adaptive_runner import solver_current_view
    from arex_skill_graph.task_context import EvidenceAnchor

    _, task, _ = make_fixture(tmp_path)
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor("current:probe:0", "probe", observation, task.base_commit),
        ),
    )
    viewed = solver_current_view(task)
    assert viewed["anchors"][-1]["observation"] == observation
    assert "full_observation_sha256" not in viewed["anchors"][-1]


def _journal_fixture(tmp_path):
    from dataclasses import replace
    from arex_skill_graph.task_context import CurrentOracle
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256

    _, task, _ = make_fixture(tmp_path)
    command = ["python3", "-V"]
    task = replace(
        task,
        oracles=(
            CurrentOracle(
                "validate:a",
                "oracle:a",
                "Observe Python version",
                tuple(command),
                ("current:issue",),
            ),
        ),
    )
    broker = {
        "operation": "run_public_command",
        "argv": command,
        "observation_id": "public:observation:0",
        "context_revision": task.revision,
        "exit_code": 0,
        "execution_available": True,
        "workspace_execution_sha256": public_workspace_execution_sha256(task.root),
        "output": "An actual process exit is not a semantic repair verdict.",
    }
    return task, broker


@pytest.mark.parametrize(
    "updates,expected",
    [
        ({}, "passed_process"),
        ({"workspace_adopted": False}, "passed_process"),  # A read-only sandbox need not adopt.
        ({"exit_code": 1}, "failed_process"),
        ({"exit_code": 124}, "timed_out"),
        ({"timed_out": True}, "timed_out"),
        ({"execution_available": False}, "execution_unavailable"),
        ({"exit_code": None}, "execution_unavailable"),
        ({"context_revision": True}, "execution_unavailable"),
        ({"context_revision": 1000000}, "execution_unavailable"),
        ({"workspace_execution_sha256": "0" * 64}, "stale_workspace"),
        ({"write_scope_accepted": False}, "failed_process"),
        ({"denied": "Out of scope result rejected"}, "failed_process"),
        ({"observation_id": "public:observation:other"}, "execution_unavailable"),
    ],
)
def test_current_run_journal_does_not_turn_invalid_process_evidence_into_success(
    tmp_path, updates, expected
):
    import copy
    from arex_skill_graph.action_contracts import digest
    from arex_skill_graph.adaptive_runner import solver_run_view

    task, broker = _journal_fixture(tmp_path)
    broker.update(updates)
    observations = {"public:observation:0": broker}
    before = copy.deepcopy((task.to_dict(), observations))
    view = solver_run_view(task, observations, [])
    row = view["oracle_executions"][0]
    assert row["status"] == expected
    assert row["command"] == broker["argv"]
    assert row["full_broker_record_sha256"] == digest(broker)
    assert row["current_passing_process_witness_id"] == (
        "public:observation:0" if expected == "passed_process" else None
    )
    assert (task.to_dict(), observations) == before
    assert "PASS" not in row.values()
    assert "no semantic acceptance" in view["assurance"]


def test_current_run_journal_matches_exact_argv_and_ignores_retained_evidence(tmp_path):
    from dataclasses import replace
    from arex_skill_graph.adaptive_runner import solver_run_view
    from arex_skill_graph.task_context import EvidenceAnchor

    task, broker = _journal_fixture(tmp_path)
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor(
                "current:probe:old", "probe", json.dumps(broker), task.base_commit, exit_code=0
            ),
        ),
    )
    wrapped = {
        **broker,
        "argv": ["bash", "-c", "python3 -V"],
    }
    for actual in ({}, {"public:observation:0": wrapped}):
        row = solver_run_view(task, actual, [])["oracle_executions"][0]
        assert row["status"] == "not_executed_in_this_run"
        assert row["current_passing_process_witness_id"] is None


def test_current_run_latest_failure_supersedes_a_passing_process(tmp_path):
    from arex_skill_graph.adaptive_runner import solver_run_view

    task, broker = _journal_fixture(tmp_path)
    failed = {**broker, "observation_id": "public:observation:1", "exit_code": 1}
    observations = {"public:observation:0": broker, "public:observation:1": failed}
    row = solver_run_view(task, observations, [])["oracle_executions"][0]
    assert row["latest_observation_id"] == "public:observation:1"
    assert row["status"] == "failed_process"
    assert row["current_passing_process_witness_id"] is None
    malformed = {**failed, "observation_id": "public:observation:2", "context_revision": None}
    observations["public:observation:2"] = malformed
    assert (
        solver_run_view(task, observations, [])["oracle_executions"][0]["status"]
        == "execution_unavailable"
    )


def test_current_run_old_workspace_witness_is_stale_after_edit(tmp_path):
    from arex_skill_graph.adaptive_runner import solver_run_view

    task, broker = _journal_fixture(tmp_path)
    observations = {"public:observation:0": broker}
    assert (
        solver_run_view(task, observations, [])["oracle_executions"][0]["status"]
        == "passed_process"
    )
    Path(task.root, "checker.py").write_text(
        "Changed public state invalidates old command evidence.\n"
    )
    view = solver_run_view(task, observations, [])
    assert view["oracle_executions"][0]["status"] == "stale_workspace"
    assert view["oracle_executions"][0]["current_passing_process_witness_id"] is None


def test_solver_context_indexes_long_broker_scripts_and_keeps_full_safety_records(tmp_path):
    import copy
    import hashlib
    from dataclasses import replace
    from arex_skill_graph.action_contracts import digest
    from arex_skill_graph.adaptive_runner import solver_current_view, solver_observation_view
    from arex_skill_graph.task_context import EvidenceAnchor, SemanticCheck

    _, task, _ = make_fixture(tmp_path)
    broker = {
        "operation": "run_public_command",
        "argv": ["python3", "-c", "print('probe')\n" * 2000],
        "exit_code": 125,
        "output": "FULL PUBLIC OUTPUT\n" * 3000,
        "workspace_adopted": False,
        "workspace_rollback": True,
        "write_scope_accepted": False,
        "out_of_scope_paths": ["forbidden.py"],
        "denied": "Rejected scope",
        "incidental_duplicate_body": "body" * 20000,
    }
    read = {"operation": "read_file", "path": "checker.py", "output": "READ\n" * 2000}
    anchors = tuple(
        EvidenceAnchor("current:probe:" + str(i), "probe", json.dumps(item), task.base_commit)
        for i, item in enumerate([broker, read])
    )
    check = SemanticCheck("probe-note", "UNKNOWN", "Reason " * 2000, (), "fixture")
    task = replace(task, anchors=(*task.anchors, *anchors), checks=(*task.checks, check))
    original = copy.deepcopy((task.to_dict(), broker))
    view = solver_current_view(task)
    indexed = view["anchors"][-2]["broker_summary"]
    assert indexed["argv_sha256"] == digest(broker["argv"])
    assert indexed["full_broker_record_sha256"] == digest(broker)
    assert "output_excerpt" not in indexed and "incidental_duplicate_body" not in indexed
    assert indexed["workspace_rollback"] and not indexed["write_scope_accepted"]
    assert indexed["out_of_scope_paths"] == broker["out_of_scope_paths"]
    assert view["anchors"][-1]["broker_summary"]["path"] == "checker.py"
    assert (
        view["anchors"][-1]["full_observation_sha256"]
        == hashlib.sha256(json.dumps(read).encode()).hexdigest()
    )
    assert view["checks"][-1]["status"] == "UNKNOWN"
    assert len(view["checks"][-1]["rationale"]) < 1000
    recent = solver_observation_view(broker, output_limit=600)
    assert recent["output_sha256"] == hashlib.sha256(broker["output"].encode()).hexdigest()
    assert "FULL PUBLIC OUTPUT" in recent["output_excerpt"]
    assert len(json.dumps(recent)) < 2500
    assert (task.to_dict(), broker) == original


def test_solver_frames_deliver_fresh_journal_witness_for_record_and_explicit_finish(tmp_path):
    from dataclasses import replace
    from arex_skill_graph.task_context import CurrentOracle, EvidenceAnchor

    package, task, policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[-1]
    command = ["python3", "-V"]
    prior = {
        "operation": "run_public_command",
        "argv": ["python3", "-c", "print('retained old command')\n" * 1000],
        "output": "Old public evidence\n" * 2000,
        "exit_code": 0,
    }
    task = replace(
        task,
        anchors=(
            *task.anchors,
            *(
                EvidenceAnchor(
                    "current:probe:" + str(i),
                    "probe",
                    json.dumps(prior),
                    task.base_commit,
                    exit_code=0,
                )
                for i in range(40)
            ),
        ),
        oracles=(
            CurrentOracle(
                action.id,
                action.oracle[0].id,
                "Process protocol control",
                tuple(command),
                ("current:issue",),
            ),
        ),
    )

    class JournalTools:
        isolation = "test-only-journal-protocol"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            pass

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **_options):
            return {
                "argv": argv,
                "output": "Current this-run process witness; no semantic verdict.",
                "exit_code": 0,
                "workspace_adopted": False,
            }

    class JournalTransport:
        def __init__(self):
            self.frames = []

        def complete(self, **kwargs):
            frame = json.loads(kwargs["user"])
            self.frames.append(frame)
            journal = frame["current_run"]
            assert "no semantic acceptance" in journal["assurance"]
            row = journal["oracle_executions"][0]
            if len(self.frames) == 1:
                assert row["status"] == "not_executed_in_this_run"
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": command},
                    "rationale": "Execute an exact public protocol control",
                }
            if len(self.frames) == 2:
                assert row["status"] == "passed_process"
                assert row["current_passing_process_witness_id"] == "public:observation:40"
                return {
                    "operation": "record_action_observation",
                    "arguments": {
                        "action_id": action.id,
                        "context_revision": frame["current"]["revision"],
                        "summary": "Actual protocol control recorded, not a semantic repair claim.",
                        "outputs": [],
                        "observation_ids": [row["current_passing_process_witness_id"]],
                        "artifact_paths": [],
                    },
                    "rationale": "Reuse the current exact process witness without rerunning it",
                }
            assert len(journal["recorded_actions"]) == 1
            assert journal["recorded_actions"][0]["semantic_validation"] == "unreviewed"
            assert journal["recorded_actions"][0]["repair_success_established"] is False
            return {
                "operation": "finish",
                "arguments": {},
                "rationale": "Explicitly finish the recording protocol control",
            }

    transport = JournalTransport()
    with CatalogStore(tmp_path / "journal.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(model_tokens=145000, history_tokens=200000)),
            arm="B0",
            tools_factory=JournalTools,
        ).run(task, use_frozen_selection=True, recordable_actions=(action,))
    assert result["solver_ended"] and not result["failure"], {
        "failure": result["failure"],
        "budget": result["budget"]["model_tokens"],
        "frame_sizes": [
            {k: len(json.dumps(v).encode()) for k, v in f.items()} for f in transport.frames
        ],
    }
    assert len(transport.frames) == 3 and result["budget"]["model_tokens"] <= 145000
    assert len(result["action_observations"]) == 1
    assert result["action_observations"][0]["semantic_validation"] == "unreviewed"
    assert result["public_observations"][0]["observation_id"] == "public:observation:40"
    assert (
        result["public_observations"][0]["output"]
        == "Current this-run process witness; no semantic verdict."
    )
    assert result["benchmark_resolved"] is None


def test_public_evidence_reader_recovers_omitted_middle_without_executing_or_promoting(tmp_path):
    import copy
    import hashlib
    from dataclasses import replace

    from arex_skill_graph.adaptive_runner import solver_current_view, solver_run_view
    from arex_skill_graph.public_evidence import read_public_evidence
    from arex_skill_graph.task_context import EvidenceAnchor

    _, task, _ = make_fixture(tmp_path)
    output = json.dumps(
        {
            "first": "start" * 3000,
            "cases": [{"status": "FAIL", "detail": "middle"}],
            "last": "end" * 3000,
        }
    )
    broker = {
        "operation": "run_public_command",
        "observation_id": "public:observation:4",
        "argv": ["python3", "-V"],
        "output": output,
        "exit_code": 1,
        "context_revision": task.revision,
    }
    retained = EvidenceAnchor(
        "retained:probe", "probe", json.dumps(broker), task.base_commit, exit_code=1
    )
    task = replace(task, anchors=(*task.anchors, retained))
    actual = {broker["observation_id"]: broker}
    before = copy.deepcopy((task.to_dict(), actual))
    view = solver_current_view(task)
    assert "middle" not in json.dumps(view["anchors"][-1])
    page = read_public_evidence(
        task,
        actual,
        {"evidence_id": broker["observation_id"], "field": "output", "json_pointer": "/cases/0"},
    )
    assert json.loads(page["content"]) == {"status": "FAIL", "detail": "middle"}
    assert page["source"] == "current_run_broker_record" and page["next_offset"] is None
    assert page["field_sha256"] == hashlib.sha256(output.encode()).hexdigest()
    for offset in (0, 4000, 8000):
        read = read_public_evidence(
            task, actual, {"evidence_id": "retained:probe", "field": "output", "offset": offset}
        )
        assert read["content"] == output[offset : offset + 4000]
        assert read["source"] == "retained_task_anchor_representation"
        assert "not fresh execution" in read["assurance"]
    assert (task.to_dict(), actual) == before
    assert solver_run_view(task, actual, [])["recorded_actions"] == []


@pytest.mark.parametrize(
    "arguments",
    [
        {"evidence_id": "/tmp/hidden-evaluator.json"},
        {"evidence_id": "current:issue", "field": "host_path"},
        {"evidence_id": "current:issue", "field": []},
        {"evidence_id": "current:issue", "limit": True},
        {"evidence_id": "current:issue", "limit": 4001},
        {"evidence_id": "current:issue", "offset": -1},
        {"evidence_id": "current:issue", "offset": False},
        {"evidence_id": "current:issue", "path": "/etc/passwd"},
        {"evidence_id": "public:observation:0", "field": "output", "json_pointer": "cases"},
        {"evidence_id": "public:observation:0", "field": "output", "json_pointer": "/missing"},
        {"evidence_id": "public:observation:0", "field": "output", "json_pointer": "/bad~2escape"},
        {"evidence_id": "public:observation:0", "field": "output", "json_pointer": "/cases/01"},
        {"evidence_id": "public:observation:0", "field": "output", "json_pointer": "/cases/-"},
    ],
)
def test_public_evidence_reader_rejects_host_access_and_invalid_selection(tmp_path, arguments):
    from arex_skill_graph.public_evidence import read_public_evidence

    _, task, _ = make_fixture(tmp_path)
    actual = {
        "public:observation:0": {
            "observation_id": "public:observation:0",
            "output": '{"cases":[false],"a/b~c":true}',
        }
    }
    with pytest.raises(ValueError):
        read_public_evidence(task, actual, arguments)
    assert (
        json.loads(
            read_public_evidence(
                task,
                actual,
                {
                    "evidence_id": "public:observation:0",
                    "field": "output",
                    "json_pointer": "/a~1b~0c",
                },
            )["content"]
        )
        is True
    )


def test_public_evidence_reader_does_not_treat_excerpt_as_complete_json(tmp_path):
    from dataclasses import replace

    from arex_skill_graph.public_evidence import read_public_evidence
    from arex_skill_graph.task_context import EvidenceAnchor

    _, task, _ = make_fixture(tmp_path)
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor("retained:text", "probe", "incomplete {", task.base_commit),
        ),
    )
    assert (
        read_public_evidence(task, {}, {"evidence_id": "retained:text", "field": "observation"})[
            "content"
        ]
        == "incomplete {"
    )
    with pytest.raises(ValueError, match="anchor contains text"):
        read_public_evidence(task, {}, {"evidence_id": "retained:text"})
    with pytest.raises(ValueError, match="complete stored JSON"):
        read_public_evidence(
            task, {}, {"evidence_id": "retained:text", "field": "observation", "json_pointer": ""}
        )


def test_solver_reader_keeps_actual_failed_oracle_and_semantic_state_unchanged(tmp_path):
    from dataclasses import replace

    from arex_skill_graph.task_context import CurrentOracle, EvidenceAnchor

    package, task, policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[-1]
    command = ["python3", "-V"]
    task = replace(
        task,
        anchors=(
            *task.anchors,
            EvidenceAnchor("retained:note", "probe", "stored public note", task.base_commit),
        ),
        oracles=(
            CurrentOracle(
                action.id, action.oracle[0].id, "Control", tuple(command), ("current:issue",)
            ),
        ),
    )

    class Tools:
        isolation = "test-only-evidence-reader"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            self.executions = 0

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **_options):
            self.executions += 1
            assert self.executions == 1
            return {"argv": argv, "output": '{"cases":[{"status":"FAIL"}]}', "exit_code": 1}

    class Transport:
        def __init__(self):
            self.frames = []

        def complete(self, **kwargs):
            frame = json.loads(kwargs["user"])
            self.frames.append(frame)
            n = len(self.frames)
            if n == 1:
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": command},
                    "rationale": "Control",
                }
            oracle = frame["current_run"]["oracle_executions"][0]
            assert oracle["status"] == "failed_process"
            witness = oracle["latest_observation_id"]
            if n == 2:
                return {
                    "operation": "read_public_evidence",
                    "arguments": {
                        "evidence_id": witness,
                        "field": "output",
                        "json_pointer": "/cases/0",
                    },
                    "rationale": "Read stored failed domain result",
                }
            previous = self.frames[1]["current"]
            assert frame["current"] == previous
            assert frame["current_run"]["broker_observation_ids"] == [witness]
            if n == 3:
                page = frame["observations"][-1]
                assert json.loads(page["content"]) == {"status": "FAIL"}
                assert "not fresh execution" in page["assurance"]
                return {
                    "operation": "read_public_evidence",
                    "arguments": {"evidence_id": "/tmp/hidden-evaluator.json"},
                    "rationale": "Unknown ID must be denied",
                }
            assert frame["observations"][-1]["denied"] == "unknown public evidence ID"
            return {
                "operation": "finish",
                "arguments": {},
                "rationale": "End control, no success claim",
            }

    transport = Transport()
    with CatalogStore(tmp_path / "reader.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(),
            arm="B0",
            tools_factory=Tools,
        ).run(task, use_frozen_selection=True, recordable_actions=(action,))
    assert result["solver_ended"] and not result["failure"]
    assert len(transport.frames) == 4
    assert not result["action_observations"]
    assert result["validated_resolved"] is None
    assert result["budget"]["tool_calls"] >= 4
    assert all(
        f["current"]["facts"] == transport.frames[1]["current"]["facts"]
        for f in transport.frames[2:]
    )


def test_solver_view_preserves_full_task_obligations_and_rejects_other_base(tmp_path):
    import hashlib
    from dataclasses import replace

    from arex_skill_graph.adaptive_runner import solver_current_view
    from arex_skill_graph.task_context import EvidenceAnchor

    _, task, _ = make_fixture(tmp_path)
    problem = "begin " * 1000 + "MIDDLE_REQUIRED_OBLIGATION" + " end" * 1000
    task = replace(
        task,
        public_problem=problem,
        anchors=(
            *task.anchors,
            EvidenceAnchor("current:repeat-problem", "public_issue", problem, task.base_commit),
        ),
    )
    view = solver_current_view(task)
    assert view["public_problem"] == problem
    assert view["anchors"][-1]["observation"] == "See current.public_problem (identical text)."
    assert (
        view["anchors"][-1]["full_observation_sha256"]
        == hashlib.sha256(problem.encode()).hexdigest()
    )
    with pytest.raises(ValueError, match="different base"):
        replace(
            task,
            anchors=(
                *task.anchors,
                EvidenceAnchor("invalid:other-base", "probe", "other base", "f" * 40),
            ),
        )
    for field in ("facts", "bindings", "port_values", "goals", "environment", "oracles"):
        assert view[field] == task.to_dict()[field]


def test_public_evidence_reader_rejects_mismatched_broker_identity(tmp_path):
    from arex_skill_graph.public_evidence import read_public_evidence

    _, task, _ = make_fixture(tmp_path)
    with pytest.raises(ValueError, match="identity mismatch"):
        read_public_evidence(
            task,
            {
                "public:observation:0": {
                    "observation_id": "public:observation:1",
                    "output": "wrong identity",
                }
            },
            {"evidence_id": "public:observation:0", "field": "output"},
        )
