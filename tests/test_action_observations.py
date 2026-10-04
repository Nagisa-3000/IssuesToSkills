import copy
from dataclasses import asdict

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_observations import record_action_observation


def exercise(tmp_path):
    package, task, _policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[0]
    observation = {
        "operation": "run_public_command",
        "observation_id": "public:observation:0",
        "argv": ["python3", "checker.py"],
        "exit_code": 1,
        "output": "observed target failure",
        "context_revision": task.revision,
    }
    request = {
        "action_id": action.id,
        "context_revision": task.revision,
        "summary": "Inspected actual current implementation and failing public probe.",
        "outputs": [
            {
                "port_name": port.name,
                "observation_ids": [observation["observation_id"]],
                "artifact_paths": ["checker.py"],
            }
            for port in action.outputs
        ],
    }
    return action, task, request, {observation["observation_id"]: observation}


def test_actual_port_witnesses_do_not_promote_semantics_or_turn_failure_into_pass(tmp_path):
    action, task, request, observations = exercise(tmp_path)
    before = task.to_dict()
    result = record_action_observation(
        action, request, task, observations, record_id="action-result:0"
    )
    assert task.to_dict() == before
    assert result["outputs"][0]["port"] == asdict(action.outputs[0])
    assert result["semantic_validation"] == "unreviewed"
    assert not result["current_facts_promoted"] and not result["current_ports_promoted"]
    assert not result["repair_success_established"]
    recorded = next(w for w in result["witnesses"] if w["kind"] == "broker_observation")
    assert recorded["record"]["exit_code"] == 1
    assert result["outputs"][0]["evidence_refs"]


@pytest.mark.parametrize(
    "mutation",
    [
        "predicted",
        "unknown_observation",
        "wrong_port",
        "duplicate_port",
        "stale_revision",
        "wrong_action",
        "missing_artifact",
        "escape",
        "hidden",
    ],
)
def test_forged_stale_missing_or_unobserved_output_is_rejected(tmp_path, mutation):
    action, task, request, observations = exercise(tmp_path)
    request = copy.deepcopy(request)
    output = request["outputs"][0]
    if mutation == "predicted":
        output["observation_ids"], output["artifact_paths"] = [], []
    elif mutation == "unknown_observation":
        output["observation_ids"] = ["public:future-result"]
    elif mutation == "wrong_port":
        output["port_name"] = "invented-success"
    elif mutation == "duplicate_port":
        request["outputs"].append(copy.deepcopy(output))
    elif mutation == "stale_revision":
        request["context_revision"] -= 1
    elif mutation == "wrong_action":
        request["action_id"] = "unapproved-action"
    elif mutation == "missing_artifact":
        output["artifact_paths"] = ["missing-artifact.json"]
    elif mutation == "escape":
        output["artifact_paths"] = ["../private-evaluator.json"]
    else:
        request["gold_patch"] = "evaluator-only material"
    with pytest.raises(ValueError):
        record_action_observation(action, request, task, observations, record_id="action-result:0")


def test_plans_and_previous_output_claims_cannot_witness_new_outputs(tmp_path):
    action, task, request, observations = exercise(tmp_path)
    observation = observations["public:observation:0"]
    observation["operation"] = "record_action_observation"
    with pytest.raises(ValueError, match="unobserved or non-tool"):
        record_action_observation(action, request, task, observations, record_id="action-result:0")
