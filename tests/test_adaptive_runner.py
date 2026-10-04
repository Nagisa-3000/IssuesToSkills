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
