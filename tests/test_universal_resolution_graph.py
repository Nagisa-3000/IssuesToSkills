from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "build_universal_resolution_graph.py"
SPEC = importlib.util.spec_from_file_location("universal_graph", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _manifest() -> dict[str, object]:
    classes = json.loads(
        (ROOT / "experiments/manifests/universal-problem-classes-v1.json").read_text()
    )
    return {
        "cases": [
            {
                "repository": "org/a",
                "issue": 1,
                "category": "state-continuity-reconstruction",
                "role": "train_candidate",
            },
            {
                "repository": "org/b",
                "issue": 2,
                "category": "state-continuity-reconstruction",
                "role": "train_candidate",
            },
            {
                "repository": "org/c",
                "issue": 3,
                "category": "state-continuity-reconstruction",
                "role": "holdout_candidate",
            },
        ],
        "classes": classes["classes"],
    }


def _episode(repo: str, issue: int, episode_id: str) -> dict[str, object]:
    action = {
        "name": "reconcile state",
        "title": "Reconcile the authoritative state",
        "description": "Reconcile the authoritative state after a boundary.",
        "evidence_ids": ["impl", "test"],
        "semantic_action": {
            "intent": "reconstruct authoritative state after a boundary",
            "module_role": "state owner",
            "operation": "reconcile",
            "pre_state": "derived state can disagree with the authoritative record",
            "post_state": "derived state matches the authoritative record",
            "validation": "round-trip replay test proves the state is retained",
            "parameters": ["state snapshot"],
            "evidence_ids": ["impl", "test"],
        },
    }
    return {
        "episode_id": episode_id,
        "repository": repo,
        "revision": "test",
        "title": "state repair",
        "before": "state is lost after a boundary",
        "after": "state is restored",
        "diff": "reconcile the state owner and add a replay oracle",
        "evidence_ids": ["impl", "test"],
        "metadata": {
            "issue": issue,
            "candidate_atomics": [action],
            "candidate_workflows": [
                {
                    "name": "reconstruct and validate",
                    "title": "Reconstruct state and validate replay",
                    "description": "Restore state and validate a replay.",
                    "atomic_names": ["reconcile state"],
                    "evidence_ids": ["impl", "test"],
                    "workflow_graph": {
                        "goal": "restore state",
                        "when_to_use": ["Persisted state exists but reconstructed state diverges."],
                        "anti_goals": ["Do not replace the authoritative state source."],
                        "not_applicable_when": ["No authoritative persisted state exists."],
                        "inputs": ["authoritative state snapshot"],
                        "entry_state": "state is lost",
                        "exit_state": "state is restored",
                        "steps": [
                            {
                                "action_name": "reconcile state",
                                "role": "reconcile",
                                "required": True,
                                "depends_on": [],
                                "condition": "when reconstructed state diverges",
                                "validation": "round-trip replay test",
                            }
                        ],
                        "edges": [],
                        "validation_ladder": ["run the focused round-trip replay test"],
                        "stop_conditions": ["stop if no authoritative snapshot is available"],
                        "unresolved_or_deferred": [],
                    },
                }
            ],
        },
    }


def test_same_grounded_action_is_reused_across_repositories() -> None:
    result = MODULE.build([_episode("org/a", 1, "e1"), _episode("org/b", 2, "e2")], _manifest())
    assert result["summary"]["actions"] == 1
    assert result["summary"]["grounded_actions"] == 1
    assert result["summary"]["workflows"] == 2
    assert result["summary"]["patterns_with_cross_repository_support"] == 1
    pattern = result["patterns"][0]
    assert pattern["promotion_status"] == "candidate"
    assert len(pattern["supporting_repositories"]) == 2
    workflow = result["workflows"][0]
    assert workflow["when_to_use"]
    assert workflow["anti_goals"]
    assert workflow["not_applicable_when"]
    assert workflow["validation_ladder"]
    assert workflow["stop_conditions"]
    assert workflow["steps"][0]["required"] is True
    assert workflow["steps"][0]["validation"] == "round-trip replay test"


def test_holdout_episode_is_refused_and_not_used_for_pattern_support() -> None:
    result = MODULE.build([_episode("org/a", 1, "e1"), _episode("org/c", 3, "e3")], _manifest())
    assert result["summary"]["episodes_used"] == 1
    assert any("holdout" in item["reason"] for item in result["rejected"])
    assert result["patterns"][0]["supporting_workflows"]
    assert all("org/c" not in item.get("source_case", "") for item in result["workflows"])


def test_unknown_semantics_do_not_collapse_episode_local_actions() -> None:
    manifest = _manifest()
    first = _episode("org/a", 1, "e1")
    second = _episode("org/b", 2, "e2")
    for episode in (first, second):
        action = episode["metadata"]["candidate_atomics"][0]
        action.pop("semantic_action")
    result = MODULE.build([first, second], manifest)
    assert result["summary"]["actions"] == 2
    assert result["summary"]["grounded_actions"] == 0
