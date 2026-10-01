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


def test_render_markdown_handles_nested_holdout_record() -> None:
    inventory = {
        "counts": {
            "training_cases": 1,
            "admitted_episodes": 1,
            "candidate_atomics": 1,
            "candidate_workflows": 1,
            "jsonschema_validation_pass": 1,
            "holdout_leaks": 0,
        },
        "category_summaries": [
            {
                "category": "provider-interface-adaptation",
                "admitted_episodes": 1,
                "atomic_count": 1,
                "workflow_count": 1,
                "exact_table_rows": 1,
                "verified_substitutes": 0,
                "holdout": {"repository": "org/holdout", "issue": 42},
            }
        ],
        "records": [],
        "validation_errors": [],
    }

    markdown = MODULE.render_markdown(inventory)

    assert "| provider-interface-adaptation | 1 | 1 | 1 | 1 | 0 | org/holdout #42 |" in markdown
