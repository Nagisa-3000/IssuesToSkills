#!/usr/bin/env python3
"""Summarize a paired no-skill/guided holdout agent comparison.

The report treats correctness and leakage as gates, then reports input/output
tokens and wall time separately.  A single holdout is explicitly directional;
it is not presented as a statistically significant skill effect.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def metric(row: dict[str, Any]) -> dict[str, Any]:
    usage = row.get("usage") if isinstance(row.get("usage"), dict) else {}
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    reasoning_tokens = int(usage.get("reasoning_output_tokens") or 0)
    return {
        "arm": row.get("arm"),
        "status": row.get("status"),
        "test_success": bool(row.get("test_success")),
        "total_wall_seconds": row.get("total_wall_seconds"),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "reasoning_output_tokens": reasoning_tokens,
        "visible_test_edits": list(row.get("edited_visible_tests") or []),
        "changed_files": list(row.get("changed_files") or []),
        "solution_ref_hidden": bool((row.get("snapshot") or {}).get("solution_ref_hidden")),
    }


def summarize(report: dict[str, Any], *, holdout_case_id: str | None = None) -> dict[str, Any]:
    rows = [metric(row) for row in report.get("rows", []) if isinstance(row, dict)]
    by_arm = {str(row.get("arm")): row for row in rows}
    baseline = by_arm.get("no_skill")
    guided = by_arm.get("guided")
    if baseline is None or guided is None:
        raise ValueError("report must contain both no_skill and guided rows")
    case_ids = sorted({str(row.get("case_id")) for row in report.get("rows", []) if row.get("case_id")})
    if holdout_case_id and holdout_case_id not in case_ids:
        raise ValueError(f"case {holdout_case_id} is absent from report")
    input_delta = guided["input_tokens"] - baseline["input_tokens"]
    output_delta = guided["output_tokens"] - baseline["output_tokens"]
    wall_delta = float(guided["total_wall_seconds"] or 0) - float(baseline["total_wall_seconds"] or 0)
    correctness = {
        "no_skill_passed": baseline["test_success"],
        "guided_passed": guided["test_success"],
        "guided_correctness_win": guided["test_success"] and not baseline["test_success"],
        "correctness_tie": guided["test_success"] == baseline["test_success"],
    }
    leakage = all(row["solution_ref_hidden"] and not row["visible_test_edits"] for row in rows)
    return {
        "schema_version": "guided-agent-comparison-summary-v1",
        "case_ids": case_ids,
        "holdout_case_id": holdout_case_id,
        "paired_arms": {"no_skill": baseline, "guided": guided},
        "deltas_guided_minus_no_skill": {
            "input_tokens": input_delta,
            "output_tokens": output_delta,
            "reasoning_output_tokens": guided["reasoning_output_tokens"] - baseline["reasoning_output_tokens"],
            "total_wall_seconds": wall_delta,
        },
        "correctness": correctness,
        "leakage_gate": {
            "passed": leakage,
            "solution_ref_hidden_all_arms": all(row["solution_ref_hidden"] for row in rows),
            "visible_test_edits_absent_all_arms": all(not row["visible_test_edits"] for row in rows),
        },
        "interpretation": (
            "Guided arm improved the visible-test result in this paired holdout; collect more independent holdouts before claiming a general effect."
            if correctness["guided_correctness_win"] else
            "Both arms have the same visible-test result in this paired holdout; the comparison measures cost/style differences, not a correctness improvement."
            if correctness["correctness_tie"] else
            "The no-skill arm passed while the guided arm did not; inspect retrieval/prompt applicability before adding more skills."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--holdout-case-id")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = summarize(report, holdout_case_id=args.holdout_case_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **result["deltas_guided_minus_no_skill"], **result["correctness"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
