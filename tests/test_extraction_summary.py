from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "summarize_issue_episode_extraction.py"
SPEC = importlib.util.spec_from_file_location("extraction_summary", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_parse_usage_uses_the_last_completed_turn(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10}}),
                "not-json",
                json.dumps(
                    {
                        "type": "turn.completed",
                        "usage": {
                            "input_tokens": 20,
                            "cached_input_tokens": 5,
                            "output_tokens": 3,
                            "reasoning_output_tokens": 2,
                        },
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    assert MODULE.parse_usage(path) == {
        "input_tokens": 20,
        "cached_input_tokens": 5,
        "output_tokens": 3,
        "reasoning_output_tokens": 2,
    }


def test_cases_from_manifest_accepts_wrapped_cases(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"cases": [{"repository": "org/repo", "issue": 1}]}))

    assert MODULE.cases_from_manifest(path) == [{"repository": "org/repo", "issue": 1}]
