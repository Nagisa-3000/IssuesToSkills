from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "induce_human_resolution_pattern.py"
SPEC = importlib.util.spec_from_file_location("pattern_induction_contract", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MERGE_SCRIPT = ROOT / "experiments" / "merge_resolution_pattern_contracts.py"
MERGE_SPEC = importlib.util.spec_from_file_location("pattern_contract_merge", MERGE_SCRIPT)
assert MERGE_SPEC and MERGE_SPEC.loader
MERGE_MODULE = importlib.util.module_from_spec(MERGE_SPEC)
MERGE_SPEC.loader.exec_module(MERGE_MODULE)
SCHEMA = json.loads(
    (ROOT / "schemas" / "resolution-pattern-induction-v1.schema.json").read_text()
)


def graph() -> dict[str, object]:
    return {
        "summary": {"patterns": 1},
        "actions": [
            {"id": "a1", "evidence_ids": ["a1-impl", "a1-test"]},
            {"id": "a2", "evidence_ids": ["a2-impl", "a2-test"]},
        ],
        "workflows": [
            {
                "id": "w1",
                "repository": "org/one",
                "evidence_ids": ["w1-evidence"],
                "steps": [{"step_id": "s1", "action_id": "a1"}],
            },
            {
                "id": "w2",
                "repository": "org/two",
                "evidence_ids": ["w2-evidence"],
                "steps": [{"step_id": "s1", "action_id": "a2"}],
            },
        ],
        "patterns": [
            {
                "id": "pattern:one",
                "category": "provider-interface-adaptation",
                "intent": "structural placeholder",
                "supporting_workflows": ["w1", "w2"],
                "supporting_repositories": ["org/one", "org/two"],
                "promotion_status": "insufficient-structural-support",
            }
        ],
    }


def contract() -> dict[str, object]:
    return {
        "schema_version": "resolution-pattern-induction-v1",
        "pattern_id": "pattern:one",
        "category": "provider-interface-adaptation",
        "decision": "candidate_pending_holdout",
        "title": "Adapt compatible providers at the boundary",
        "summary": "Identify the provider contract and adapt only the boundary it owns.",
        "when_to_use": ["A compatible endpoint rejects or ignores a provider-specific field."],
        "anti_goals": ["Do not rewrite unrelated authentication or response behavior."],
        "not_applicable_when": ["The endpoint uses an incompatible protocol."],
        "invariants": ["Explicit configuration wins over inferred defaults."],
        "action_template": [
            {
                "role_id": "establish-contract",
                "title": "Establish the endpoint contract",
                "purpose": "Locate the real provider boundary and its accepted request shape.",
                "required": True,
                "condition": "Always",
                "validation": "A focused probe reproduces the boundary behavior.",
            }
        ],
        "decision_points": [
            {
                "question": "Is the mismatch in routing or request shape?",
                "branches": [
                    {"condition": "routing", "action_role_ids": ["establish-contract"]},
                    {"condition": "request shape", "action_role_ids": ["establish-contract"]},
                ],
            }
        ],
        "ordering_constraints": [],
        "validation_ladder": ["Run the focused contract probe, then affected regressions."],
        "known_failure_modes": [
            {
                "failure": "Provider detection is too broad.",
                "detection": "A hostile-suffix endpoint selects the adapter.",
                "mitigation": "Match the canonical boundary instead of a substring.",
            }
        ],
        "exclusions": ["Credential acquisition failures without an interface mismatch."],
        "supporting_workflow_ids": ["w1", "w2"],
        "workflow_realizations": [
            {
                "workflow_id": "w1",
                "repository": "org/one",
                "role_bindings": [{"role_id": "establish-contract", "action_ids": ["a1"]}],
                "evidence_ids": ["a1-impl", "a1-test"],
            },
            {
                "workflow_id": "w2",
                "repository": "org/two",
                "role_bindings": [{"role_id": "establish-contract", "action_ids": ["a2"]}],
                "evidence_ids": ["a2-impl", "a2-test"],
            },
        ],
        "confidence": 0.82,
        "rationale": "Both repositories establish the provider contract before adapting it.",
        "evidence_ids": ["w1-evidence", "w2-evidence"],
        "missing_probes": ["Run an untouched cross-project holdout repair."],
    }


def test_valid_contract_binds_generic_role_to_real_actions() -> None:
    source = graph()
    pattern = source["patterns"][0]
    errors = MODULE.validate_contract(contract(), source, pattern, SCHEMA)
    assert errors == []
    result = MODULE.apply_contract(source, "pattern:one", contract())
    updated = result["patterns"][0]
    assert updated["title"] == "Adapt compatible providers at the boundary"
    assert updated["promotion_status"] == "candidate_pending_holdout"
    assert updated["supporting_repositories"] == ["org/one", "org/two"]
    assert result["semantic_pattern_induction"]["holdout_loaded"] is False


def test_contract_rejects_action_from_another_workflow() -> None:
    source = graph()
    value = contract()
    value["workflow_realizations"][0]["role_bindings"][0]["action_ids"] = ["a2"]
    errors = MODULE.validate_contract(value, source, source["patterns"][0], SCHEMA)
    assert any("not Workflow steps" in error for error in errors)


def test_required_role_needs_two_repository_realizations() -> None:
    source = graph()
    value = contract()
    value["workflow_realizations"][1]["role_bindings"] = [
        {"role_id": "optional-repair", "action_ids": ["a2"]}
    ]
    value["action_template"].append(
        {
            "role_id": "optional-repair",
            "title": "Repair the boundary",
            "purpose": "Apply a repository-specific repair.",
            "required": False,
            "condition": "Only when the focused probe fails.",
            "validation": "The focused probe passes.",
        }
    )
    errors = MODULE.validate_contract(value, source, source["patterns"][0], SCHEMA)
    assert any("fewer than two repositories" in error for error in errors)


def test_realization_evidence_must_belong_to_its_workflow() -> None:
    source = graph()
    value = contract()
    value["workflow_realizations"][0]["evidence_ids"] = ["a2-test"]
    errors = MODULE.validate_contract(value, source, source["patterns"][0], SCHEMA)
    assert any("outside its Workflow" in error for error in errors)


def test_training_payload_bounds_factorization_audit_to_selected_pattern() -> None:
    source = graph()
    source["actions"].append({"id": "unrelated", "evidence_ids": ["other"]})
    audit = {
        "schema_version": "action-factorization-audit-v1",
        "action_grain": [
            {"id": "a1", "verdict": "atomic-review"},
            {"id": "unrelated", "verdict": "split-review"},
        ],
        "coarse_action_groups": [
            {"action_ids": ["a1"], "operation": "adapt"},
            {"action_ids": ["unrelated"], "operation": "repair"},
        ],
        "cross_repository_pair_analysis": [
            {"left": "a1", "right": "a2", "decision": "not-a-peer"},
            {"left": "a1", "right": "unrelated", "decision": "not-a-peer"},
        ],
        "workflow_role_segments": [
            {
                "segment_roles": ["implement", "validate"],
                "supporting_workflows": ["w1", "outside"],
                "occurrences": [
                    {"workflow_id": "w1", "repository": "org/one", "category": "cat"},
                    {
                        "workflow_id": "outside",
                        "repository": "org/three",
                        "category": "other",
                    },
                ],
            }
        ],
    }

    payload = MODULE.bounded_training_payload(source, source["patterns"][0], audit)
    bounded = payload["factorization_audit"]

    assert [item["id"] for item in bounded["action_grain"]] == ["a1"]
    assert [item["action_ids"] for item in bounded["coarse_action_groups"]] == [["a1"]]
    assert len(bounded["cross_repository_pair_analysis"]) == 1
    assert bounded["workflow_role_segments"][0]["supporting_workflows"] == ["w1"]
    assert bounded["workflow_role_segments"][0]["supporting_repositories"] == ["org/one"]


def test_merge_contracts_preserves_validated_decision_and_requires_unique_pattern() -> None:
    source = graph()
    merged, report = MERGE_MODULE.merge_contracts(
        source,
        [contract()],
        SCHEMA,
        require_complete=True,
    )

    assert merged["patterns"][0]["promotion_status"] == "candidate_pending_holdout"
    assert merged["semantic_pattern_induction"]["merged_pattern_ids"] == ["pattern:one"]
    assert report["decision_counts"]["candidate_pending_holdout"] == 1
