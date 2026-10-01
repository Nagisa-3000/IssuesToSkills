from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from evaluate_guided_agent_pair import _agent_validation_evidence


def test_agent_validation_evidence_collects_only_completed_validation_commands(
    tmp_path: Path,
) -> None:
    run_dir = tmp_path / "runs" / "owner__repo__1" / "guided"
    run_dir.mkdir(parents=True)
    (run_dir / "agent-last.txt").write_text(
        "Implemented the fix and ran the focused resolver tests.",
        encoding="utf-8",
    )
    events = [
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": "npm test -- resolver.test.ts",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "27 tests passed",
            },
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": "rg -n resolver packages/coding-agent/test -g '*.ts'",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "packages/coding-agent/test/model-resolver.test.ts",
            },
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": "git status --short",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "M resolver.ts",
            },
        },
        {
            "type": "item.started",
            "item": {
                "type": "command_execution",
                "command": "git diff --check",
            },
        },
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": "git diff --check",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "",
            },
        },
    ]
    event_text = "\n".join(json.dumps(event) for event in events)
    (run_dir / "agent-events.jsonl").write_text(
        event_text + "\n{malformed json\n",
        encoding="utf-8",
    )

    evidence = _agent_validation_evidence(tmp_path, "owner__repo__1", "guided")

    assert evidence["final_message"] == (
        "Implemented the fix and ran the focused resolver tests."
    )
    assert [item["command"] for item in evidence["validation_commands"]] == [
        "npm test -- resolver.test.ts",
        "git diff --check",
    ]
    assert evidence["validation_commands"][0]["output"] == "27 tests passed"
