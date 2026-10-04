import copy
from dataclasses import replace
from pathlib import Path

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import Predicate
from arex_skill_graph.action_grounding import review_action_observation
from arex_skill_graph.action_observations import record_action_observation
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.execution_frontier import action_execution_checks
from arex_skill_graph.task_context import ObservedFact, SemanticCheck


def observed(tmp_path, *, exit_code=0, effects=None, kind=None):
    package, task, _policy = make_fixture(tmp_path)
    action = package.actions[0]
    if effects is not None:
        action = replace(action, effects=effects)
    if kind is not None:
        action = replace(action, kind=kind)
    broker = {
        "observation_id": "public:observation:0",
        "operation": "run_public_command",
        "argv": ["python3", "-c", "from context import type_only; assert type_only('type')"],
        "exit_code": exit_code,
        "output": "Actual context probe output",
        "context_revision": task.revision,
    }
    observations = {broker["observation_id"]: broker}
    record = record_action_observation(
        action,
        {
            "action_id": action.id,
            "context_revision": task.revision,
            "summary": "Claim requiring independent evidence review.",
            "outputs": [
                {
                    "port_name": p.name,
                    "observation_ids": [broker["observation_id"]],
                    "artifact_paths": ["context.py"],
                }
                for p in action.outputs
            ],
        },
        task,
        observations,
        record_id="action-result:0",
    )
    refs = [record["witnesses"][0]["id"]]
    keys = (
        {"output:" + p.name for p in action.outputs}
        | {"effect:" + p.key for p in action.effects}
        | {"preserve:" + p.key for p in action.preserves}
        | {"oracle:" + o.id for o in action.oracle}
    )
    response = {
        "checks": [
            {
                "key": key,
                "status": "PASS",
                "rationale": "Independent synthetic current-evidence review",
                "evidence_refs": refs,
            }
            for key in sorted(keys)
        ]
    }
    return package, task, action, record, observations, response


def review(task, action, record, observations, response):
    return review_action_observation(
        task,
        action,
        record,
        observations,
        ReplayTransport([response]),
        BudgetLedger(BudgetCaps(history_tokens=200000)),
    )


def test_only_independently_reviewed_actual_outputs_can_enable_next_action(tmp_path):
    package, task, action, record, observations, response = observed(tmp_path)
    guard = next(a for a in package.actions if a.id == "guard:a")
    assert not action_execution_checks(guard, task)["ready"]
    assert not task.port_values
    current, audit = review(task, action, record, observations, response)
    assert len(current.port_values) == 1
    assert current.condition(Predicate("context_known", True)) == "PASS"
    # The reviewer establishes an output; a separate current connection check is still required.
    assert not action_execution_checks(guard, current)["ready"]
    current = current.update(
        checks=(
            SemanticCheck(
                "current-connect:context:guard:a:context",
                "PASS",
                "Current synthetic port semantics reviewed",
                current.port_values[0].evidence_refs,
                "fixture-review",
            ),
        )
    )
    assert action_execution_checks(guard, current)["ready"]
    assert not audit["repair_success_established"] and not audit["formal_KB_admitted"]
    assert record["semantic_validation"] == "unreviewed"


def test_unknown_review_does_not_turn_expected_outputs_into_facts(tmp_path):
    _package, task, action, record, observations, response = observed(tmp_path)
    for row in response["checks"]:
        row["status"], row["evidence_refs"] = "UNKNOWN", []
    current, audit = review(task, action, record, observations, response)
    assert current.port_values == ()
    assert current.condition(Predicate("context_known", True)) == "UNKNOWN"
    assert audit["current_ports_promoted"] == []


def test_recorded_failure_can_be_an_outcome_without_becoming_success(tmp_path):
    _package, task, action, record, observations, response = observed(
        tmp_path, exit_code=1, effects=(Predicate("validated", True),)
    )
    for row in response["checks"]:
        if row["key"].startswith(("effect:", "oracle:")):
            row["status"] = "FAIL"
    current, audit = review(task, action, record, observations, response)
    assert current.condition(Predicate("validated", True)) == "FAIL"
    assert not audit["repair_success_established"]
    assert current.port_values  # The synthetic port records observations, not acceptance.


@pytest.mark.parametrize(
    "bad", ["claim_success_after_failed_probe", "missing_oracle", "unknown_oracle"]
)
def test_goal_effect_needs_successful_execution_and_complete_oracle_review(tmp_path, bad):
    _package, task, action, record, observations, response = observed(
        tmp_path,
        exit_code=1 if bad == "claim_success_after_failed_probe" else 0,
        effects=(Predicate("validated", True),),
    )
    if bad != "claim_success_after_failed_probe":
        for row in response["checks"]:
            if row["key"].startswith("oracle:"):
                row["status"] = "UNKNOWN" if bad == "unknown_oracle" else "FAIL"
    with pytest.raises(ValueError, match="passing Oracles"):
        review(task, action, record, observations, response)


@pytest.mark.parametrize(
    "bad",
    ["missing_key", "extra_key", "duplicate_key", "future_evidence", "claim_only", "extra_field"],
)
def test_reviewer_cannot_invent_conditions_or_evidence(tmp_path, bad):
    _package, task, action, record, observations, response = observed(tmp_path)
    if bad == "missing_key":
        response["checks"].pop()
    elif bad == "extra_key":
        response["checks"].append({**response["checks"][0], "key": "effect:invented"})
    elif bad == "duplicate_key":
        response["checks"].append(copy.deepcopy(response["checks"][0]))
    elif bad == "future_evidence":
        response["checks"][0]["evidence_refs"] = ["future:oracle"]
    elif bad == "claim_only":
        response["checks"][0]["evidence_refs"] = ["current:issue"]
    else:
        response["checks"][0]["confidence"] = 1.0
    with pytest.raises(ValueError):
        review(task, action, record, observations, response)


@pytest.mark.parametrize(
    "bad",
    [
        "changed_unanchored_file",
        "changed_artifact",
        "changed_broker",
        "changed_port",
        "legacy_record",
        "different_task",
    ],
)
def test_stale_forged_or_unsealed_record_is_not_current_state(tmp_path, bad):
    _package, task, action, record, observations, response = observed(tmp_path)
    if bad == "changed_unanchored_file":
        Path(task.root, "unanchored.py").write_text("changed = True\n")
    elif bad == "changed_artifact":
        Path(task.root, "context.py").write_text("changed = True\n")
    elif bad == "changed_broker":
        record["witnesses"][0]["record"]["exit_code"] = 99
    elif bad == "changed_port":
        record["outputs"][0]["port"]["state"] = "invented-pass"
    elif bad == "legacy_record":
        record.pop("schema")
    else:
        record["task_id"] = "different-task"
    with pytest.raises(ValueError):
        review(task, action, record, observations, response)


def test_whole_workspace_seal_invalidates_ports_even_for_unanchored_changes(tmp_path):
    _package, task, action, record, observations, response = observed(tmp_path)
    current, _audit = review(task, action, record, observations, response)
    Path(task.root, "unanchored.py").write_text("changed = True\n")
    with pytest.raises(ValueError, match="reviewed Action state is stale"):
        current.verify()


def test_expected_predecessor_effects_are_not_executable_prerequisites(tmp_path):
    package, task, _policy = make_fixture(tmp_path)
    guard = next(a for a in package.actions if a.id == "guard:a")
    current = task.update(facts=(ObservedFact("context_known", True, ("current:context",)),))
    assert not action_execution_checks(guard, current)["ready"]
    assert any(
        row["key"] == "input:context" and row["status"] == "UNKNOWN"
        for row in action_execution_checks(guard, current)["checks"]
    )


def test_diagnostic_probe_can_confirm_cause_without_establishing_repaired_behavior(tmp_path):
    _package, task, action, record, observations, response = observed(
        tmp_path, exit_code=1, kind="probe"
    )
    current, audit = review(task, action, record, observations, response)
    assert current.condition(Predicate("context_known", True)) == "PASS"
    assert current.condition(Predicate("validated", True)) == "UNKNOWN"
    assert current.port_values
    assert record["witnesses"][0]["record"]["exit_code"] == 1
    assert not audit["repair_success_established"]


def test_permission_only_change_invalidates_record_and_reviewed_inputs(tmp_path):
    _package, task, action, record, observations, response = observed(tmp_path)
    current, _audit = review(task, action, record, observations, response)
    target = Path(task.root, "context.py")
    target.chmod(0o755 if target.stat().st_mode & 0o111 == 0 else 0o644)
    with pytest.raises(ValueError, match="stale"):
        current.verify()
    with pytest.raises(ValueError, match="stale"):
        review(task, action, record, observations, response)


def test_content_only_v2_receipt_is_not_silently_promoted(tmp_path):
    _package, task, action, record, observations, response = observed(tmp_path)
    record["schema"] = "arex-action-observation-v2"
    record.pop("workspace_execution_sha256")
    with pytest.raises(ValueError, match="v3"):
        review(task, action, record, observations, response)


@pytest.mark.parametrize(
    "bad", ["wrong_command", "unexecuted", "failed", "stale", "missing_binding", "timed_out"]
)
def test_validation_oracle_cannot_pass_without_current_bound_execution(tmp_path, bad):
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256

    _, task, action, _, observations, response = observed(tmp_path, kind="validate")
    command = next(o.command for o in task.oracles if o.action_id == action.id)
    broker = observations["public:observation:0"]
    broker.update(
        argv=list(command), workspace_execution_sha256=public_workspace_execution_sha256(task.root)
    )
    if bad == "wrong_command":
        broker["argv"] = ["python3", "-V"]
    elif bad == "unexecuted":
        broker.update(exit_code=None, execution_available=False)
    elif bad == "failed":
        broker["exit_code"] = 1
    elif bad == "stale":
        broker["workspace_execution_sha256"] = "0" * 64
    elif bad == "missing_binding":
        task = replace(task, oracles=())
    else:
        broker["timed_out"] = True
    record = record_action_observation(
        action,
        {
            "action_id": action.id,
            "context_revision": task.revision,
            "summary": "Synthetic attempted validation, not acceptance.",
            "outputs": [
                {
                    "port_name": p.name,
                    "observation_ids": [broker["observation_id"]],
                    "artifact_paths": ["context.py"],
                }
                for p in action.outputs
            ],
        },
        task,
        observations,
        record_id="action-result:0",
    )
    with pytest.raises(ValueError, match="bound command"):
        review(task, action, record, observations, response)


def test_current_validation_oracle_and_outcome_record_remain_separate(tmp_path):
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256

    _, task, action, _, observations, response = observed(tmp_path, kind="validate")
    command = next(o.command for o in task.oracles if o.action_id == action.id)
    broker = observations["public:observation:0"]
    broker.update(
        argv=list(command), workspace_execution_sha256=public_workspace_execution_sha256(task.root)
    )
    record = record_action_observation(
        action,
        {
            "action_id": action.id,
            "context_revision": task.revision,
            "summary": "Current executed public command, separately reviewed semantic obligations.",
            "outputs": [
                {
                    "port_name": p.name,
                    "observation_ids": [broker["observation_id"]],
                    "artifact_paths": [],
                }
                for p in action.outputs
            ],
        },
        task,
        observations,
        record_id="action-result:0",
    )
    current, audit = review(task, action, record, observations, response)
    assert current.port_values and not audit["repair_success_established"]
    for row in response["checks"]:
        if row["key"].startswith("oracle:"):
            row.update(status="UNKNOWN", evidence_refs=[])
    current, audit = review(task, action, record, observations, response)
    assert current.port_values and not audit["repair_success_established"]
    assert any(c["key"].startswith("oracle:") and c["status"] == "UNKNOWN" for c in audit["checks"])
