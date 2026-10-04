"""Broker protocol tests use a local fixture backend, never a production isolation claim."""

import json
import subprocess
from pathlib import Path

from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.workflow_ranker import WorkflowRanker


class FixtureTools:
    isolation = "test-only-local-fixture"
    runtime_sha256 = "test-only"

    def __init__(self, root, _ledger):
        self.root = root

    def preflight(self):
        pass

    def close(self):
        pass

    def run(self, argv, **_kwargs):
        p = subprocess.run(argv, cwd=self.root, capture_output=True, text=True, check=False)
        return {"argv": argv, "exit_code": p.returncode, "output": p.stdout + p.stderr}


def test_broker_retains_actual_failed_probe_and_does_not_promote_recorded_ports(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    action = package.actions[0]
    steps = [
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Execute actual public fixture probe.",
        },
        {
            "operation": "record_action_observation",
            "arguments": {
                "action_id": action.id,
                "context_revision": task.revision + 1,
                "summary": "Record the actual public probe and inspected source without claiming validation.",
                "outputs": [
                    {
                        "port_name": p.name,
                        "observation_ids": ["public:observation:0"],
                        "artifact_paths": ["checker.py"],
                    }
                    for p in action.outputs
                ],
            },
            "rationale": "Preserve actual output evidence for independent review.",
        },
        {"operation": "finish", "arguments": {}, "rationale": "End protocol fixture."},
    ]

    class CheckingReplay(ReplayTransport):
        def complete(self, **kwargs):
            current = json.loads(kwargs["user"])["current"]
            assert current["port_values"] == json.loads(json.dumps(task.to_dict()["port_values"]))
            return super().complete(**kwargs)

    with CatalogStore(tmp_path / "store.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            CheckingReplay(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=FixtureTools,
        ).run(task, use_frozen_selection=True, recordable_actions=(action,))
    assert result["solver_ended"] and not result["failure"], result
    (record,) = result["action_observations"]
    assert record["semantic_validation"] == "unreviewed"
    assert not record["current_ports_promoted"]
    assert record["witnesses"][0]["record"]["argv"] == ["python3", "checker.py"]
    assert result["explicit_functional_action_catalog"]
    assert result["budget"]["history_tokens"] > 0
    assert Path(task.root, "checker.py").is_file()


def test_unapproved_action_cannot_fabricate_a_broker_port_record(tmp_path):
    _package, task, policy = make_fixture(tmp_path)
    steps = [
        {
            "operation": "record_action_observation",
            "arguments": {
                "action_id": "unapproved",
                "context_revision": task.revision,
                "summary": "Unsupported output.",
                "outputs": [
                    {
                        "port_name": "success",
                        "observation_ids": [],
                        "artifact_paths": ["checker.py"],
                    }
                ],
            },
            "rationale": "Protocol rejection fixture.",
        }
    ]
    with CatalogStore(tmp_path / "store.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            ReplayTransport(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(),
            arm="B0",
            tools_factory=FixtureTools,
        ).run(task)
    assert result["failure"] and not result["solver_ended"]
    assert result["action_observations"] == []


def test_read_only_action_exercise_denies_source_writes(tmp_path):
    _package, task, policy = make_fixture(tmp_path)
    original = Path(task.root, "checker.py").read_text()
    steps = [
        {
            "operation": "write_file",
            "arguments": {"path": "checker.py", "content": "changed"},
            "rationale": "Read-only rejection fixture.",
        },
        {"operation": "finish", "arguments": {}, "rationale": "End fixture."},
    ]
    with CatalogStore(tmp_path / "store.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            ReplayTransport(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(),
            arm="B0",
            tools_factory=FixtureTools,
        ).run(task, read_only_workspace=True)
    assert result["solver_ended"] and not result["patch"]
    assert result["public_workspace_read_only"]
    assert "read-only" in result["public_observations"][0]["denied"]
    assert Path(task.root, "checker.py").read_text() == original
