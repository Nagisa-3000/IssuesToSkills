import importlib.util
from pathlib import Path

import pytest

from arex_skill_graph.adaptive_budget import BudgetLedger

_spec = importlib.util.spec_from_file_location(
    "native_policy_review_cli",
    Path(__file__).resolve().parents[1] / "experiments/review_native_action_functional_cases.py",
)
_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cli)


def policy_response(status="PASS"):
    return {
        "checks": [
            {
                "key": key,
                "status": status,
                "rationale": "Actual controlled observation",
                "evidence_refs": ["observed:one"],
            }
            for key in sorted(_cli.CHECKS)
        ],
        "domain_state": "UNKNOWN",
        "behavior": "correct_refusal",
        "verdict": status,
        "rationale": "An unavailable domain check remains UNKNOWN; refusal follows actual evidence.",
    }


def test_honest_unknown_domain_can_pass_refusal_policy_without_claiming_repair():
    value = policy_response()
    assert (
        _cli.validate_policy_review(value, {"observed:one"}, actual_refs={"observed:one"})[
            "domain_state"
        ]
        == "UNKNOWN"
    )
    value["checks"][0]["status"] = "UNKNOWN"
    with pytest.raises(ValueError, match="contradicts"):
        _cli.validate_policy_review(value, {"observed:one"}, actual_refs={"observed:one"})


def test_contract_or_fabricated_refs_cannot_prove_current_case_pass():
    value = policy_response()
    with pytest.raises(ValueError, match="nonexistent"):
        _cli.validate_policy_review(value, {"authored:contract"}, actual_refs={"observed:one"})
    for check in value["checks"]:
        check["evidence_refs"] = ["authored:contract"]
    with pytest.raises(ValueError, match="actual run"):
        _cli.validate_policy_review(value, {"authored:contract"}, actual_refs={"observed:one"})


def test_policy_review_uses_shared_budget_adapter_with_actual_transport_interface():
    class Transport:
        def __init__(self):
            self.calls = []

        def complete(self, *, system, user, response_schema):
            assert response_schema == _cli.SCHEMA and "allowed_refs" in user
            self.calls.append({"usage": {"total_tokens": 23}})
            return policy_response()

    transport, ledger = Transport(), BudgetLedger()
    result = _cli.review_policy(transport, ledger, {"allowed_refs": ["observed:one"]})
    assert result["verdict"] == "PASS" and ledger.model_calls == 1 and ledger.model_tokens == 23


@pytest.mark.parametrize("bad_checks", [[None] * 4, {"applicability_reasoning": "PASS"}])
def test_invalid_check_shapes_remain_protocol_failures(bad_checks):
    value = policy_response()
    value["checks"] = bad_checks
    with pytest.raises(ValueError, match="required checks"):
        _cli.validate_policy_review(value, {"observed:one"}, actual_refs={"observed:one"})


def test_confirmation_cannot_be_accepted_with_unknown_domain():
    value = policy_response()
    value["behavior"] = "correct_confirmation"
    with pytest.raises(ValueError, match="confirmed reviewed domain"):
        _cli.validate_policy_review(value, {"observed:one"}, actual_refs={"observed:one"})


def test_complete_response_schema_requires_evidence_and_check_shapes():
    from jsonschema import validate, ValidationError

    value = policy_response()
    validate(value, _cli.SCHEMA)
    value["checks"][0].pop("evidence_refs")
    with pytest.raises(ValidationError):
        validate(value, _cli.SCHEMA)


def test_accepted_observed_task_is_preserved_for_downstream_action(tmp_path):
    import json

    from test_action_grounding import observed
    from arex_skill_graph.adaptive_budget import BudgetCaps
    from arex_skill_graph.adaptive_cli import ReplayTransport
    from arex_skill_graph.task_context import TaskContext

    _package, task, action, record, observations, response = observed(tmp_path)
    path = tmp_path / "reviewed-task.json"
    current, audits = _cli.review_records(
        task, action, [record], observations, ReplayTransport([response]),
        BudgetLedger(BudgetCaps(history_tokens=200000)), output_path=path,
    )
    saved = TaskContext.from_dict(json.loads(path.read_text()))
    assert saved.to_dict() == current.to_dict()
    assert saved.port_values and not task.port_values
    assert audits[0]["current_ports_promoted"]
    assert not audits[0]["repair_success_established"]


def test_rejected_record_never_creates_reviewed_state(tmp_path):
    from test_action_grounding import observed
    from arex_skill_graph.adaptive_budget import BudgetCaps
    from arex_skill_graph.adaptive_cli import ReplayTransport

    _package, task, action, record, observations, response = observed(tmp_path)
    response["checks"][0]["evidence_refs"] = ["unobserved:future"]
    path = tmp_path / "reviewed-task.json"
    with pytest.raises(ValueError, match="never observed"):
        _cli.review_records(
            task, action, [record], observations, ReplayTransport([response]),
            BudgetLedger(BudgetCaps(history_tokens=200000)), output_path=path,
        )
    assert not path.exists()


def test_execution_input_is_verified_and_namespaced_separately_from_post_state(tmp_path):
    import json
    import hashlib
    from dataclasses import replace
    from adaptive_fixture import make_fixture

    _package, task, _policy = make_fixture(tmp_path)
    path = tmp_path / "execution-input.json"
    path.write_text(json.dumps(task.to_dict()))
    case = {"execution_input_task_context": str(path),
            "execution_input_task_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    public, ref, refs = _cli.execution_input_view(case, task)
    assert "root" not in public
    assert all(a["id"].startswith("execution-input:") for a in public["anchors"])
    assert all(b["anchor_id"] in refs for b in public["bindings"])
    assert ref.startswith("native-execution-input:")
    assert not refs.intersection(a.id for a in task.anchors)
    with pytest.raises(ValueError, match="identity mismatch"):
        _cli.execution_input_view(case, replace(task, task_id="different"))
    path.write_text(path.read_text() + "\n")
    with pytest.raises(ValueError, match="changed after dispatch"):
        _cli.execution_input_view(case, task)


def test_policy_accepts_authentic_record_witness_reference():
    value = policy_response()
    for row in value["checks"]:
        row["evidence_refs"] = ["action-result:0:tool:public:observation:0"]
    _cli.validate_policy_review(value, {"action-result:0:tool:public:observation:0"},
                                actual_refs={"action-result:0:tool:public:observation:0"})
