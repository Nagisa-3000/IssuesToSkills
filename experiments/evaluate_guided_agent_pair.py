#!/usr/bin/env python3
"""Run an independent weighted evaluator over paired holdout agent artifacts."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.paired_evaluation import DEFAULT_WEIGHTS, score_pair

JUDGE_SCHEMA: Mapping[str, Any] = {
    "type": "object",
    "required": [
        "semantic_completion",
        "patch_scope_precision",
        "maintainability_style",
        "validation_quality",
        "issue_postcondition_satisfied",
        "rationale",
        "concerns",
    ],
    "properties": {
        "semantic_completion": {"type": "number", "minimum": 0, "maximum": 100},
        "patch_scope_precision": {"type": "number", "minimum": 0, "maximum": 100},
        "maintainability_style": {"type": "number", "minimum": 0, "maximum": 100},
        "validation_quality": {"type": "number", "minimum": 0, "maximum": 100},
        "issue_postcondition_satisfied": {"type": "boolean"},
        "rationale": {"type": "string"},
        "concerns": {"type": "array", "items": {"type": "string"}},
    },
}

SYSTEM = """You are an independent software-engineering evaluation agent. You judge a completed patch; you do not repair it. Regression-test results are authoritative for executable correctness. Compare the candidate patch with the issue contract, current test evidence, and the hidden reference change only after the agent run has ended. Score semantic completion, patch scope precision, maintainability/style, and validation quality from 0 to 100. Do not reward verbosity, repository-name overlap, or similarity alone. Return JSON only."""


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)


def _bounded_text(value: str, limit: int = 50000) -> str:
    if len(value) <= limit:
        return value
    half = limit // 2
    return value[:half] + "\n...<truncated>...\n" + value[-half:]


def _solution_diff(case: Mapping[str, Any]) -> str:
    repo = Path(str(case["repository_path"])).expanduser().resolve()
    proc = subprocess.run(
        ["git", "-C", str(repo), "diff", "--no-ext-diff", "--binary", str(case["base_ref"]), str(case["solution_ref"])],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if proc.returncode:
        return f"<solution diff unavailable: {proc.stderr.strip()}>"
    return _bounded_text(proc.stdout)


def _test_evidence(row: Mapping[str, Any]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for item in row.get("tests", []):
        if not isinstance(item, Mapping):
            continue
        record = {key: item.get(key) for key in ("command", "returncode", "wall_seconds", "timed_out")}
        for stream in ("stdout_path", "stderr_path"):
            path = Path(str(item.get(stream) or ""))
            if path.is_file():
                record[stream.removesuffix("_path")] = _bounded_text(path.read_text(encoding="utf-8", errors="replace"), 12000)
        evidence.append(record)
    return evidence


def _agent_validation_evidence(
    report_root: Path,
    case_id: str,
    arm: str,
) -> dict[str, Any]:
    run_dir = report_root / "runs" / _safe_name(case_id) / arm
    final_path = run_dir / "agent-last.txt"
    final_message = (
        _bounded_text(final_path.read_text(encoding="utf-8", errors="replace"), 12000)
        if final_path.is_file()
        else ""
    )
    events_path = run_dir / "agent-events.jsonl"
    commands: list[dict[str, Any]] = []
    if events_path.is_file():
        for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            item = event.get("item") if isinstance(event, Mapping) else None
            if event.get("type") != "item.completed" or not isinstance(item, Mapping):
                continue
            if item.get("type") != "command_execution":
                continue
            command = str(item.get("command") or "")
            lower_command = command.lower()
            is_validation = any(
                marker in lower_command
                for marker in ("vitest", "pytest", "typecheck", "git diff --check")
            ) or bool(
                re.search(
                    r"\b(?:npm|pnpm|yarn|bun)\b[^;&|\n]*\b(?:test|check|lint)\b",
                    lower_command,
                )
                or re.search(r"(?:^|[\s/])(?:tsc|tsgo)(?:\s|$)", lower_command)
            )
            if not is_validation:
                continue
            commands.append(
                {
                    "command": command,
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                    "output": _bounded_text(str(item.get("aggregated_output") or ""), 10000),
                }
            )
    return {"final_message": final_message, "validation_commands": commands[-10:]}


def _retrieval_judgment(report_root: Path, case_id: str) -> Mapping[str, Any] | None:
    guidance_path = report_root / "runs" / _safe_name(case_id) / "guided" / "guidance.json"
    if not guidance_path.is_file():
        return None
    guidance = _read_json(guidance_path)
    judge = guidance.get("judge") if isinstance(guidance, Mapping) else None
    return judge if isinstance(judge, Mapping) else None


def _fallback_judgment(row: Mapping[str, Any]) -> dict[str, Any]:
    passed = bool(row.get("test_success"))
    clean = not bool(row.get("test_edit_violation"))
    return {
        "semantic_completion": 100 if passed else 0,
        "patch_scope_precision": 70 if row.get("patch_nonempty") and clean else 0,
        "maintainability_style": 50 if row.get("patch_nonempty") and clean else 0,
        "validation_quality": 100 if passed else 0,
        "issue_postcondition_satisfied": passed,
        "rationale": "Deterministic fallback; no independent LLM evaluator was configured.",
        "concerns": ["llm_evaluator_unavailable"],
        "fallback": True,
    }


def _judge(
    transport: OpenAICompatibleTransport | None,
    *,
    case: Mapping[str, Any],
    row: Mapping[str, Any],
    report_root: Path,
    solution_diff: str,
) -> dict[str, Any]:
    if transport is None:
        return _fallback_judgment(row)
    patch_path = report_root / "runs" / _safe_name(str(row["case_id"])) / str(row["arm"]) / "model.patch"
    candidate_patch = patch_path.read_text(encoding="utf-8", errors="replace") if patch_path.is_file() else ""
    payload = {
        "case": {
            "id": case.get("id"),
            "repository": case.get("repository"),
            "category": case.get("category"),
            "issue_title": case.get("issue_title"),
            "issue_body": case.get("issue_body"),
            "visible_test_paths": case.get("visible_test_paths", []),
        },
        "arm": row.get("arm"),
        "execution": {
            "test_success": row.get("test_success"),
            "agent_success": row.get("agent_success"),
            "changed_files": row.get("changed_files", []),
            "changed_untracked_files": row.get("changed_untracked_files", []),
            "edited_visible_tests": row.get("edited_visible_tests", []),
            "test_evidence": _test_evidence(row),
            "agent_validation_evidence": _agent_validation_evidence(
                report_root,
                str(row["case_id"]),
                str(row["arm"]),
            ),
        },
        "candidate_patch": _bounded_text(candidate_patch),
        "hidden_reference_diff_for_post_run_evaluation_only": solution_diff,
        "instruction": (
            "The candidate need not copy the reference implementation. Judge whether it satisfies "
            "the issue contract with a precise, maintainable, well-validated patch. Passing tests "
            "are necessary but inspect scope and hidden postconditions for accidental or incomplete fixes."
        ),
    }
    result = transport.complete(system=SYSTEM, user=json.dumps(payload, ensure_ascii=False), response_schema=JUDGE_SCHEMA)
    return dict(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--qualification", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    args = parser.parse_args()

    report = _read_json(args.report)
    cases = {str(item["id"]): item for item in _read_json(args.cases)}
    qualification: dict[str, bool] = {}
    if args.qualification:
        raw = _read_json(args.qualification)
        qualification = {str(item["case_id"]): bool(item.get("qualified")) for item in raw.get("rows", [])}
    transport = None
    if args.api_key:
        transport = OpenAICompatibleTransport(
            OpenAICompatibleConfig(
                api_key=args.api_key,
                base_url=args.base_url,
                model=args.model,
                timeout_seconds=240,
                max_output_tokens=2200,
                retries=2,
            )
        )

    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in report.get("rows", []):
        if isinstance(row, Mapping):
            grouped.setdefault(str(row.get("case_id")), []).append(row)
    evaluations = []
    judgments_artifact: dict[str, Any] = {}
    for case_id, rows in sorted(grouped.items()):
        case = cases.get(case_id)
        if case is None:
            raise ValueError(f"case {case_id} is missing from case manifest")
        reference = _solution_diff(case)
        judgments = {
            str(row["arm"]): _judge(
                transport,
                case=case,
                row=row,
                report_root=args.report.parent,
                solution_diff=reference,
            )
            for row in rows
        }
        judgments_artifact[case_id] = judgments
        scored = score_pair(
            rows,
            judgments,
            oracle_qualified=qualification.get(case_id) if args.qualification else None,
            retrieval_judgment=_retrieval_judgment(args.report.parent, case_id),
            weights=DEFAULT_WEIGHTS,
        )
        scored["case_id"] = case_id
        evaluations.append(scored)

    output = {
        "schema_version": "weighted-guided-agent-evaluation-v1",
        "source_report": str(args.report),
        "cases": len(evaluations),
        "model": args.model if transport else None,
        "independent_llm_evaluator_used": transport is not None,
        "evaluations": evaluations,
        "llm_calls": list(transport.calls) if transport else [],
        "judgments": judgments_artifact,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "cases": len(evaluations), "outcomes": [item["outcome"] for item in evaluations]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
