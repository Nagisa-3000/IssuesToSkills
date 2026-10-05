"""Effect-only Actions need real witnesses and the same independent semantic gates."""

import copy
from dataclasses import replace

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import Predicate
from arex_skill_graph.action_grounding import review_action_observation
from arex_skill_graph.action_observations import record_action_observation
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.workspace_state import public_workspace_execution_sha256


def exercise(tmp_path, *, kind="probe", exit_code=1, artifact_only=False):
    package, task, _ = make_fixture(tmp_path)
    action = replace(package.actions[0], outputs=(), kind=kind)
    command = next(o.command for o in task.oracles if o.action_id == action.id)
    observation = {
        "operation": "run_public_command",
        "observation_id": "public:observed:0",
        "argv": list(command),
        "exit_code": exit_code,
        "output": "Actual synthetic public probe observation",
        "context_revision": task.revision,
        "workspace_execution_sha256": public_workspace_execution_sha256(task.root),
    }
    observations = {observation["observation_id"]: observation}
    request = {
        "action_id": action.id,
        "context_revision": task.revision,
        "summary": "Observed current behavior; effects need independent review.",
        "outputs": [],
        "observation_ids": [] if artifact_only else [observation["observation_id"]],
        "artifact_paths": ["context.py"],
    }
    record = record_action_observation(
        action, request, task, observations, record_id="action-result:0"
    )
    response = {
        "checks": [
            {
                "key": key,
                "status": "PASS",
                "rationale": "Synthetic independent witnessed review",
                "evidence_refs": [record["witnesses"][0]["id"]],
            }
            for key in sorted(
                {"effect:" + p.key for p in action.effects}
                | {"preserve:" + p.key for p in action.preserves}
                | {"oracle:" + o.id for o in action.oracle}
            )
        ]
    }
    return task, action, request, observations, record, response


def review(task, action, observations, record, response):
    return review_action_observation(
        task,
        action,
        record,
        observations,
        ReplayTransport([response]),
        BudgetLedger(BudgetCaps(history_tokens=200000)),
    )


def test_actual_witness_without_ports_never_promotes_claim_before_independent_review(tmp_path):
    task, action, _, observations, record, response = exercise(tmp_path)
    before = task.to_dict()
    assert record["schema"] == "arex-action-observation-v4"
    assert record["outputs"] == []
    assert record["execution_evidence_refs"]
    assert record["current_facts_promoted"] is False
    assert record["current_ports_promoted"] is False
    assert record["witnesses"][0]["record"]["exit_code"] == 1
    assert task.to_dict() == before
    current, audit = review(task, action, observations, record, response)
    assert current.condition(Predicate("context_known", True)) == "PASS"
    assert current.port_values == ()
    assert audit["repair_success_established"] is False
    assert not any(c["key"].startswith("output:") for c in audit["checks"])


@pytest.mark.parametrize("status", ["UNKNOWN", "FAIL"])
def test_portless_uncertainty_and_counterevidence_remain_not_authorized(tmp_path, status):
    task, action, _, observations, record, response = exercise(tmp_path)
    for check in response["checks"]:
        check["status"] = status
        if status == "UNKNOWN":
            check["evidence_refs"] = []
    current, audit = review(task, action, observations, record, response)
    assert current.condition(Predicate("context_known", True)) == status
    assert current.port_values == ()
    assert not audit["repair_success_established"]


@pytest.mark.parametrize(
    "defect", ["no_witness", "future_tool", "invented_port", "duplicate_tool", "summary_only"]
)
def test_portless_request_cannot_record_predicted_or_fabricated_execution(tmp_path, defect):
    task, action, request, observations, _, _ = exercise(tmp_path)
    if defect == "no_witness":
        request.update(observation_ids=[], artifact_paths=[])
    elif defect == "future_tool":
        request["observation_ids"] = ["public:future"]
    elif defect == "invented_port":
        request["outputs"] = [
            {"port_name": "fabricated", "observation_ids": [], "artifact_paths": []}
        ]
    elif defect == "duplicate_tool":
        request["observation_ids"] *= 2
    else:
        request.pop("observation_ids")
        request.pop("artifact_paths")
    with pytest.raises(ValueError):
        record_action_observation(action, request, task, observations, record_id="action-result:1")


@pytest.mark.parametrize(
    "defect",
    ["downgrade_schema", "missing_ref", "duplicate_ref", "unused_witness", "invented_output"],
)
def test_portless_record_still_enforces_identity_and_exact_witness_closure(tmp_path, defect):
    task, action, _, observations, record, response = exercise(tmp_path)
    if defect == "downgrade_schema":
        record["schema"] = "arex-action-observation-v3"
    elif defect == "missing_ref":
        record["execution_evidence_refs"] = []
    elif defect == "duplicate_ref":
        record["execution_evidence_refs"] *= 2
    elif defect == "unused_witness":
        extra = copy.deepcopy(record["witnesses"][0])
        extra["id"] = "unused:broker:witness"
        record["witnesses"].append(extra)
    else:
        record["outputs"] = [{"port": {}, "evidence_refs": []}]
    with pytest.raises((ValueError, TypeError)):
        review(task, action, observations, record, response)


def test_required_artifact_ports_cannot_be_bypassed_with_portless_request(tmp_path):
    task, action, request, observations, _, _ = exercise(tmp_path)
    package, _, _ = make_fixture(tmp_path / "other")
    action = replace(action, outputs=package.actions[0].outputs)
    with pytest.raises(ValueError, match="exact documented fields"):
        record_action_observation(action, request, task, observations, record_id="action-result:1")


@pytest.mark.parametrize("exit_code", [None, 1])
def test_portless_validation_cannot_pass_on_unavailable_or_failed_command(tmp_path, exit_code):
    task, action, _, observations, record, response = exercise(
        tmp_path, kind="validate", exit_code=exit_code
    )
    with pytest.raises(ValueError, match="bound command"):
        review(task, action, observations, record, response)


def test_portless_validation_does_not_accept_artifact_as_successful_execution(tmp_path):
    task, action, _, observations, record, response = exercise(
        tmp_path, kind="validate", exit_code=0, artifact_only=True
    )
    with pytest.raises(ValueError, match="bound command"):
        review(task, action, observations, record, response)


def test_portless_validation_requires_actual_current_bound_command(tmp_path):
    task, action, _, observations, record, response = exercise(
        tmp_path, kind="validate", exit_code=0
    )
    current, audit = review(task, action, observations, record, response)
    assert current.port_values == ()
    assert audit["current_fact_keys"]
    assert not audit["repair_success_established"]
