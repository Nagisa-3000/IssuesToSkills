from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "audit_action_factorization.py"
SPEC = importlib.util.spec_from_file_location("action_factorization", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _action(action_id: str, repo: str, *, post: str = "state is valid", oracle: str = "focused test") -> dict[str, object]:
    return {
        "id": action_id,
        "module_role": "provider contract boundary",
        "operation": "adapt",
        "pre_state": "generic contract is insufficient",
        "post_state": post,
        "validation": oracle,
        "description": "Adapt the boundary and preserve caller behavior.",
        "intent": "adapt the provider contract",
        "grounded_semantics": True,
        "supporting_repositories": [repo],
    }


def _workflow(workflow_id: str, repo: str, actions: list[str], roles: list[str]) -> dict[str, object]:
    return {
        "id": workflow_id,
        "repository": repo,
        "issue": 1,
        "steps": [{"step_id": f"s{index}", "action_id": action, "role": role} for index, (action, role) in enumerate(zip(actions, roles))],
    }


def test_same_contract_is_a_safe_reuse_candidate() -> None:
    graph = {
        "actions": [_action("a", "org/a"), _action("b", "org/b")],
        "workflows": [
            _workflow("w1", "org/a", ["a"], ["implement"]),
            _workflow("w2", "org/b", ["b"], ["implement"]),
        ],
    }
    report = MODULE.audit(graph)
    assert report["summary"]["safe_reuse_candidates"] == 1
    assert report["summary"]["hypothesis"] == "some-action-reuse-is-supported"


def test_same_verb_different_contract_is_not_action_reuse() -> None:
    graph = {
        "actions": [
            _action("a", "org/a"),
            _action("b", "org/b", post="request is endpoint-specific", oracle="strict HTTP oracle"),
        ],
        "workflows": [
            _workflow("w1", "org/a", ["a"], ["implement"]),
            _workflow("w2", "org/b", ["b"], ["implement"]),
        ],
    }
    report = MODULE.audit(graph)
    assert report["summary"]["safe_reuse_candidates"] == 0
    assert report["summary"]["same_owner_operation_contract_divergences"] == 1
    assert report["cross_repository_pair_analysis"][0]["decision"] == "same-owner-operation-but-contract-diverges"


def test_role_skeleton_is_reported_separately_from_action_reuse() -> None:
    graph = {
        "actions": [_action("a", "org/a"), _action("b", "org/b")],
        "workflows": [
            _workflow("w1", "org/a", ["a"], ["establish-contract"]),
            _workflow("w2", "org/b", ["b"], ["establish-contract"]),
        ],
    }
    report = MODULE.audit(graph)
    assert report["summary"]["already_reused_actions"] == 0
    assert report["summary"]["workflow_role_segments"] == 0

