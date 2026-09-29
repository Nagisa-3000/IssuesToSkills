from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "validate_universal_episodes.py"
SPEC = importlib.util.spec_from_file_location("universal_episode_validation", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def episode(issue: int, *, holdout: bool = False) -> dict[str, object]:
    return {
        "episode_id": f"episode-{issue}",
        "repository": "org/a",
        "metadata": {
            "issue": issue,
            "github_bundle": {
                "source": "github_api",
                "issue": {"state": "closed"},
                "linked_pull_requests": [{"pull_request": {"merged": True}}],
            },
            "codex_response": {
                "evidence_units": [
                    {"id": "impl", "kind": "implementation", "claim": "implementation changed", "source": "checkout"},
                    {"id": "test", "kind": "test", "claim": "regression test", "source": "checkout"},
                ]
            },
            "candidate_atomics": [{
                "semantic_action": {
                    "intent": "reconcile state",
                    "module_role": "state owner",
                    "operation": "reconcile",
                    "pre_state": "old",
                    "post_state": "new",
                    "validation": "test",
                }
            }],
            "candidate_workflows": [{"workflow_graph": {"steps": []}}],
        },
    }


def test_merged_training_episode_passes() -> None:
    report = MODULE.validate(
        [episode(1)],
        {("org/a", 1): {"category": "state", "role": "train_candidate"}},
    )
    assert report["accepted_for_graph"] == 1
    assert report["rejected"] == 0


def test_holdout_episode_is_rejected_even_when_merged() -> None:
    report = MODULE.validate(
        [episode(2)],
        {("org/a", 2): {"category": "state", "role": "holdout_candidate"}},
    )
    assert report["accepted_for_graph"] == 0
    assert "holdout/non-training" in report["rows"][0]["errors"][0]

