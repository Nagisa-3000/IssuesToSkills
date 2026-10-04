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
