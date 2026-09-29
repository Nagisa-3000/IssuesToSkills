#!/usr/bin/env python3
"""Build a conservative, evidence-backed extraction manifest.

The universal issue manifest is a discovery table.  This adapter turns only
training rows with a locally resolvable implementation ref into extraction
cases.  A local ref by itself is not enough: it must be backed either by a
merged linked PR or by a commit reference present on the rendered issue page.
Closed-but-unmerged PR heads are retained in the rejection report and are not
silently treated as resolutions.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
from typing import Any


def git_resolves(checkout: str, ref: str) -> bool:
    if not checkout or not ref:
        return False
    try:
        result = subprocess.run(
            ["git", "-C", checkout, "cat-file", "-e", f"{ref}^{{commit}}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def cases_from(value: Any) -> list[dict[str, Any]]:
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    return [dict(item) for item in cases if isinstance(item, dict)]


def extraction_basis(case: dict[str, Any]) -> tuple[str | None, str | None]:
    verification = case.get("verification") or {}
    html = case.get("html_evidence") or {}
    ref = str(case.get("extraction_ref") or case.get("ref") or "").strip()
    if str(verification.get("html_issue_state") or "").lower() != "closed":
        return None, "issue is not verified closed by rendered HTML"
    if not ref:
        return None, "no local extraction_ref"
    if not git_resolves(str(case.get("checkout") or ""), ref):
        return None, "extraction_ref is not resolvable in checkout"
    if verification.get("html_merged_resolution"):
        return "merged_pull_request", None
    direct_refs = {
        str(item).lower()
        for item in (html.get("commit_refs") or [])
        if str(item).strip()
    }
    direct_refs.update(
        str(item).lower()
        for item in (verification.get("api_timeline_commit_refs") or [])
        if str(item).strip()
    )
    resolved_refs = {
        str(item).lower()
        for item in (html.get("resolved_checkout_refs") or [])
        if str(item).strip()
    }
    resolved_refs.update(
        str(item).lower()
        for item in (verification.get("api_timeline_resolved_checkout_refs") or [])
        if str(item).strip()
    )
    if direct_refs and (ref.lower() in direct_refs or ref.lower() in resolved_refs):
        return "issue_direct_commit", None
    return None, "local ref comes only from a non-merged PR or unclassified reference"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", choices=("train_candidate", "holdout_candidate"), default="train_candidate")
    parser.add_argument("--max-cases", type=int)
    args = parser.parse_args()

    source = json.loads(args.manifest.read_text(encoding="utf-8"))
    all_cases = cases_from(source)
    candidates = [
        case for case in all_cases
        if str(case.get("role") or case.get("split") or "") == args.role
    ]
    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for case in candidates:
        basis, reason = extraction_basis(case)
        identity = {
            "case_id": case.get("case_id"),
            "repository": case.get("repository"),
            "issue": case.get("issue"),
            "category": case.get("category"),
        }
        if reason:
            rejected.append({**identity, "reason": reason})
            continue
        enriched = dict(case)
        enriched["ref"] = str(case.get("extraction_ref") or case.get("ref"))
        enriched["extraction_basis"] = basis
        enriched["extraction_manifest_source"] = str(args.manifest)
        selected.append(enriched)

    if args.max_cases is not None:
        selected = selected[: max(0, args.max_cases)]
    output = {
        "schema_version": "universal-extraction-manifest-v1",
        "source_manifest": str(args.manifest),
        "role": args.role,
        "selection_policy": {
            "requires_closed_issue": True,
            "requires_local_ref": True,
            "accepted_resolution_bases": ["merged_pull_request", "issue_direct_commit"],
            "rejects_closed_unmerged_pr_head": True,
        },
        "cases": selected,
        "selection_report": {
            "candidate_rows": len(candidates),
            "selected_rows": len(selected),
            "rejected_rows": len(rejected),
            "selected_by_repository": dict(Counter(str(item["repository"]) for item in selected)),
            "selected_by_category": dict(Counter(str(item["category"]) for item in selected)),
            "rejected": rejected,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "candidate_rows": len(candidates),
        "selected_rows": len(selected),
        "rejected_rows": len(rejected),
        "selected_by_repository": output["selection_report"]["selected_by_repository"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
