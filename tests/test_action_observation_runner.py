"""Broker protocol tests use a local fixture backend, never a production isolation claim."""

import json
import subprocess
from dataclasses import asdict, replace

import pytest
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


def test_invalid_approved_witness_is_rejected_and_can_be_corrected(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    action = package.actions[0]

    def record_step(identity):
        return {
            "operation": "record_action_observation",
            "arguments": {
                "action_id": action.id,
                "context_revision": task.revision + 1,
                "summary": "Record actual failed probe outcomes without accepting the repair.",
                "outputs": [
                    {"port_name": p.name, "observation_ids": [identity], "artifact_paths": []}
                    for p in action.outputs
                ],
            },
            "rationale": "Preserve witnessed outputs for separate review.",
        }

    steps = [
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Observe a real public fixture failure.",
        },
        record_step("public:non-tool-guidance-refresh"),
        record_step("public:observation:0"),
        {"operation": "finish", "arguments": {}, "rationale": "Finish corrected record fixture."},
    ]
    with CatalogStore(tmp_path / "store.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            ReplayTransport(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=FixtureTools,
        ).run(task, use_frozen_selection=True, recordable_actions=(action,))
    assert result["solver_ended"] and not result["failure"]
    denied = result["public_observations"][1]
    assert not denied["recorded"]
    assert denied["available_tool_observation_ids"] == ["public:observation:0"]
    assert denied["current_context_revision"] == task.revision + 1
    assert "non-tool" in denied["denied"]
    assert len(result["action_observations"]) == 1
    assert result["action_observations"][0]["witnesses"][0]["record"]["exit_code"] != 0
    assert not result["action_observations"][0]["current_ports_promoted"]


@pytest.mark.parametrize("retained_public_id", [None, 12])
def test_resumed_observation_ids_preserve_old_bindings_and_oracles(tmp_path, retained_public_id):
    from arex_skill_graph.task_context import (
        CurrentOracle,
        EvidenceAnchor,
        ObservedFact,
        SemanticCheck,
    )

    package, task, policy = make_fixture(tmp_path)
    action = package.actions[0]
    old_probe = EvidenceAnchor(
        "current:probe:0", "probe", "Retained reviewed fixture probe", task.base_commit, exit_code=0
    )
    old_record = EvidenceAnchor(
        "action-result:4:tool:public:observation:8",
        "probe",
        "Retained fixture Action witness",
        task.base_commit,
        exit_code=0,
    )
    binding = replace(
        task.bindings[0], evidence_refs=(*task.bindings[0].evidence_refs, old_probe.id)
    )
    oracle = CurrentOracle(
        action.id,
        action.oracle[0].id,
        "Retained fixture Oracle, not a historical repair success claim",
        ("python3", "checker.py"),
        (old_probe.id,),
    )
    task = task.update(
        anchors=(old_probe, old_record),
        facts=(ObservedFact("retained_review", True, (old_probe.id,)),),
        checks=(
            SemanticCheck("retained_review", "PASS", "Fixture review", (old_probe.id,), "fixture"),
        ),
        bindings=(binding,),
        oracles=(oracle,),
    )
    initial = (
        ()
        if retained_public_id is None
        else ({"observation_id": f"public:observation:{retained_public_id}"},)
    )
    next_public = 9 if retained_public_id is None else 13
    steps = [
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Obtain a new actual failed probe without replacing the retained witness.",
        },
        {
            "operation": "record_action_observation",
            "arguments": {
                "action_id": action.id,
                "context_revision": task.revision + 1,
                "summary": "Record this actual fixture failure without promoting it.",
                "outputs": [
                    {
                        "port_name": port.name,
                        "observation_ids": [f"public:observation:{next_public}"],
                        "artifact_paths": ["checker.py"],
                    }
                    for port in action.outputs
                ],
            },
            "rationale": "Keep the new Action record in a distinct namespace.",
        },
        {"operation": "finish", "arguments": {}, "rationale": "End resumed protocol fixture."},
    ]

    class RetentionReplay(ReplayTransport):
        def complete(self, **kwargs):
            current = json.loads(kwargs["user"])["current"]
            assert next(a for a in current["anchors"] if a["id"] == old_probe.id) == asdict(
                old_probe
            )
            assert next(a for a in current["anchors"] if a["id"] == old_record.id) == asdict(
                old_record
            )
            assert binding.role in {v["role"] for v in current["bindings"]}
            assert oracle.source_oracle_id in {v["source_oracle_id"] for v in current["oracles"]}
            assert any(v["key"] == "retained_review" for v in current["facts"])
            assert any(v["key"] == "retained_review" for v in current["checks"])
            return super().complete(**kwargs)

    with CatalogStore(tmp_path / "resumed.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            RetentionReplay(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=FixtureTools,
        ).run(
            task,
            use_frozen_selection=True,
            recordable_actions=(action,),
            initial_observations=initial,
        )
    assert result["solver_ended"] and not result["failure"], result
    (record,) = result["action_observations"]
    assert record["id"] == "action-result:5"
    assert record["witnesses"][0]["id"] == f"action-result:5:tool:public:observation:{next_public}"
    assert record["witnesses"][0]["record"]["exit_code"] != 0
    assert record["semantic_validation"] == "unreviewed" and not record["current_ports_promoted"]
