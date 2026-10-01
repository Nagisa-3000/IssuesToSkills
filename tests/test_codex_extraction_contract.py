from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "run_codex_issue_episode_extraction.py"
SPEC = importlib.util.spec_from_file_location("codex_episode_extractor", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _response() -> dict[str, object]:
    return {
        "episode": {
            "episode_id": "episode-1",
            "title": "Keep selected endpoint semantics",
            "before": "The follow-up request loses the selected endpoint contract.",
            "after": "The follow-up request preserves the selected endpoint contract.",
            "diff": "Propagate the selected endpoint contract and add a regression test.",
        },
        "evidence_units": [
            {
                "id": "E1",
                "kind": "implementation",
                "claim": "The selected endpoint contract is propagated.",
                "source": "src/client.py:10-30",
            },
            {
                "id": "E2",
                "kind": "test",
                "claim": "The regression test checks follow-up routing.",
                "source": "tests/test_client.py:20-45",
            },
        ],
        "candidate_atomics": [
            {
                "name": "propagate-selected-endpoint-contract",
                "title": "Propagate the selected endpoint contract",
                "description": "Carry the selected endpoint contract across follow-up requests.",
                "evidence_ids": ["E1", "E2"],
                "semantic_action": {
                    "intent": "Preserve provider selection across request boundaries.",
                    "module_role": "follow-up request adapter",
                    "operation": "propagate",
                    "pre_state": "A follow-up request is created without the selected endpoint.",
                    "post_state": "The follow-up request uses the selected endpoint.",
                    "validation": "A focused follow-up routing regression passes.",
                    "parameters": ["selected endpoint", "follow-up request"],
                    "evidence_ids": ["E1", "E2"],
                },
            }
        ],
        "candidate_workflows": [
            {
                "name": "preserve-provider-selection-across-follow-ups",
                "title": "Preserve provider selection across follow-up requests",
                "description": "Repair a request boundary that drops provider routing state.",
                "atomic_names": ["propagate-selected-endpoint-contract"],
                "evidence_ids": ["E1", "E2"],
                "workflow_graph": {
                    "goal": "Every follow-up request preserves the selected provider contract.",
                    "when_to_use": [
                        "Initial requests work but follow-up requests lose routing state."
                    ],
                    "anti_goals": ["Do not replace global provider defaults."],
                    "not_applicable_when": ["The initial request also fails to select a provider."],
                    "inputs": ["selected endpoint", "follow-up request construction path"],
                    "entry_state": "A valid initial request has selected an endpoint.",
                    "exit_state": "Follow-up requests retain that endpoint.",
                    "steps": [
                        {
                            "action_name": "propagate-selected-endpoint-contract",
                            "role": "implement",
                            "required": True,
                            "depends_on": [],
                            "condition": "when constructing a follow-up request",
                            "validation": "Run the focused follow-up routing regression.",
                        }
                    ],
                    "edges": [],
                    "validation_ladder": [
                        "Run the focused follow-up routing test.",
                        "Run provider client regressions.",
                    ],
                    "stop_conditions": ["Stop if the selected endpoint cannot be established."],
                    "unresolved_or_deferred": [],
                },
            }
        ],
        "unresolved_questions": [],
    }


def test_v2_schema_accepts_actionable_workflow_contract() -> None:
    from jsonschema import Draft202012Validator

    response = _response()
    schema = json.loads((ROOT / "schemas" / "codex-change-episode-v2.schema.json").read_text())

    Draft202012Validator(schema).validate(response)
    assert MODULE.validate_response(response) == (True, [])


def test_validator_rejects_dangling_workflow_action() -> None:
    response = _response()
    workflow = response["candidate_workflows"][0]
    workflow["workflow_graph"]["steps"][0]["action_name"] = "missing-action"

    valid, errors = MODULE.validate_response(response)

    assert valid is False
    assert any(error.endswith("references unknown action: missing-action") for error in errors)


def test_validator_requires_when_to_use_and_anti_goals() -> None:
    response = _response()
    graph = response["candidate_workflows"][0]["workflow_graph"]
    graph["when_to_use"] = []
    graph["anti_goals"] = []

    valid, errors = MODULE.validate_response(response)

    assert valid is False
    assert any(error.endswith("workflow_graph.when_to_use is empty") for error in errors)
    assert any(error.endswith("workflow_graph.anti_goals is empty") for error in errors)
