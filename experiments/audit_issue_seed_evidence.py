#!/usr/bin/env python3
"""Audit issue seeds against GitHub resolution metadata and local checkouts.

This is intentionally a qualification gate, not an extractor.  A closed
issue is retained as a seed even when it has no implementation-bearing
resolution; only a merged PR plus a locally resolvable implementation ref is
eligible for ChangeEpisode extraction.  Holdout rows are reported but never
converted into training candidates.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request
from typing import Any


def gh(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "arex-skill-graph-issue-seed-audit",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def git_exists(checkout: str, ref: str) -> bool:
    if not checkout or not ref:
        return False
    try:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
            cwd=checkout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def pr_numbers(value: Any) -> set[int]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return {int(number) for number in re.findall(r"/(?:pulls|pull)/(\d+)", text)}


def linked_pr_numbers(issue: dict[str, Any], timeline: list[Any]) -> set[int]:
    numbers = pr_numbers(issue)
    for event in timeline:
        if not isinstance(event, dict):
            continue
        numbers |= pr_numbers(event)
        source = event.get("source") if isinstance(event.get("source"), dict) else {}
        source_issue = source.get("issue") if isinstance(source.get("issue"), dict) else {}
        if source_issue.get("pull_request"):
            numbers.add(int(source_issue.get("number", 0)))
    if issue.get("pull_request"):
        numbers.add(int(issue.get("number", 0)))
    return {number for number in numbers if number > 0}


def file_summary(files: list[Any]) -> dict[str, Any]:
    names = [str(item.get("filename")) for item in files if isinstance(item, dict) and item.get("filename")]
    implementation = [name for name in names if not re.search(r"(^|/)(test|tests|spec|specs|fixtures?)(/|$)|(_test|\.test\.|\.spec\.)", name, re.I)]
    tests = [name for name in names if name not in implementation]
    return {
        "file_count": len(names),
        "implementation_file_count": len(implementation),
        "test_file_count": len(tests),
        "file_sample": names[:40],
    }


def audit_case(case: dict[str, Any], token: str | None, fetch_files: bool, max_linked_prs: int) -> dict[str, Any]:
    repo = str(case["repository"])
    issue_number = int(case["issue"])
    api = f"https://api.github.com/repos/{repo}"
    result: dict[str, Any] = {
        "case_id": case.get("case_id"),
        "repository": repo,
        "issue": issue_number,
        "issue_url": case.get("issue_url") or f"https://github.com/{repo}/issues/{issue_number}",
        "category": case.get("category"),
        "role": case.get("role") or case.get("split"),
        "checkout": case.get("checkout"),
        "source": case.get("source"),
        "table_note": case.get("table_note"),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        issue = gh(f"{api}/issues/{issue_number}", token)
        timeline = gh(f"{api}/issues/{issue_number}/timeline?per_page=100", token)
    except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        result.update({"evidence_status": "audit-error", "error": f"{type(exc).__name__}: {exc}"})
        return result
    timeline = timeline if isinstance(timeline, list) else []
    numbers = sorted(linked_pr_numbers(issue if isinstance(issue, dict) else {}, timeline))
    preferred = int(case.get("preferred_resolution_pr") or 0)
    inspected_numbers = sorted(
        numbers,
        key=lambda number: (0 if number == preferred else 1, abs(number - issue_number), number),
    )
    if max_linked_prs > 0:
        inspected_numbers = inspected_numbers[:max_linked_prs]
    if preferred and preferred not in inspected_numbers:
        inspected_numbers.insert(0, preferred)
    prs: list[dict[str, Any]] = []
    errors: list[str] = []
    for number in inspected_numbers:
        try:
            pr = gh(f"{api}/pulls/{number}", token)
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            errors.append(f"pull/{number}: {type(exc).__name__}: {exc}")
            continue
        if not isinstance(pr, dict):
            continue
        row = {
            "number": number,
            "title": pr.get("title"),
            "state": pr.get("state"),
            "merged": bool(pr.get("merged") or pr.get("merged_at")),
            "merged_at": pr.get("merged_at"),
            "merge_commit_sha": pr.get("merge_commit_sha"),
            "head_sha": ((pr.get("head") or {}).get("sha")),
            "html_url": pr.get("html_url"),
            "changed_files": pr.get("changed_files"),
            "additions": pr.get("additions"),
            "deletions": pr.get("deletions"),
        }
        if fetch_files and row["merged"]:
            try:
                files = gh(f"{api}/pulls/{number}/files?per_page=100", token)
                row["files"] = file_summary(files if isinstance(files, list) else [])
            except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
                errors.append(f"pull/{number}/files: {type(exc).__name__}: {exc}")
        prs.append(row)
    merged = [row for row in prs if row.get("merged")]
    merged.sort(key=lambda row: str(row.get("merged_at") or ""), reverse=True)
    chosen = next((row for row in merged if row.get("number") == preferred), None) if preferred else None
    if chosen is None and len(merged) == 1:
        chosen = merged[0]
    ref = str(case.get("ref") or case.get("extraction_ref") or "")
    if not ref and chosen:
        ref = str(chosen.get("merge_commit_sha") or chosen.get("head_sha") or "")
    local_ref = git_exists(str(case.get("checkout") or ""), ref)
    role = str(case.get("role") or case.get("split") or "")
    if role == "holdout_candidate":
        status = "holdout-seed-not-extracted"
    elif chosen and local_ref:
        files = chosen.get("files") or {}
        if files and files.get("implementation_file_count", 0) == 0:
            status = "merged-but-documentation-or-test-only"
        else:
            status = "implementation-bearing-candidate"
    elif chosen:
        status = "merged-resolution-but-local-ref-missing"
    elif len(merged) > 1:
        status = "ambiguous-linked-resolutions"
    else:
        status = "closed-without-merged-resolution" if issue.get("state") == "closed" else "open-or-unresolved"
    result.update({
        "title": issue.get("title"),
        "state": issue.get("state"),
        "state_reason": issue.get("state_reason"),
        "closed_at": issue.get("closed_at"),
        "labels": [item.get("name") for item in issue.get("labels", []) if isinstance(item, dict)],
        "linked_pr_numbers": numbers,
        "preferred_resolution_pr": preferred or None,
        "inspected_pr_numbers": inspected_numbers,
        "pull_requests": prs,
        "selected_resolution": chosen,
        "ref": ref,
        "local_ref_resolvable": local_ref,
        "evidence_status": status,
        "api_errors": errors,
        "timeline_event_count": len(timeline),
        "policy_note": (
            "Holdout row is reported for audit only and must not enter training extraction."
            if role == "holdout_candidate" else
            "Eligible for extraction only after the extractor independently verifies before/after state and validation oracle."
            if status == "implementation-bearing-candidate" else
            "Do not create a ChangeEpisode from issue closure alone."
        ),
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--category")
    parser.add_argument("--include-holdout", action="store_true")
    parser.add_argument("--fetch-files", action="store_true")
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--max-linked-prs", type=int, default=12)
    args = parser.parse_args()
    raw = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = raw.get("cases", raw) if isinstance(raw, (dict, list)) else []
    selected = [dict(case) for case in cases if isinstance(case, dict)]
    if args.category:
        selected = [case for case in selected if case.get("category") == args.category]
    if not args.include_holdout:
        selected = [case for case in selected if (case.get("role") or case.get("split")) != "holdout_candidate"]
    if args.max_cases > 0:
        selected = selected[:args.max_cases]
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    rows = [audit_case(case, token, args.fetch_files, args.max_linked_prs) for case in selected]
    summary = {
        "cases": len(rows),
        "implementation_bearing_candidates": sum(row.get("evidence_status") == "implementation-bearing-candidate" for row in rows),
        "holdout_seeds": sum(row.get("evidence_status") == "holdout-seed-not-extracted" for row in rows),
        "closed_without_merged_resolution": sum(row.get("evidence_status") == "closed-without-merged-resolution" for row in rows),
        "merged_resolution_but_local_ref_missing": sum(row.get("evidence_status") == "merged-resolution-but-local-ref-missing" for row in rows),
        "ambiguous_linked_resolutions": sum(row.get("evidence_status") == "ambiguous-linked-resolutions" for row in rows),
        "audit_errors": sum(row.get("evidence_status") == "audit-error" for row in rows),
    }
    payload = {
        "schema_version": "issue-seed-evidence-audit-v1",
        "source_manifest": str(args.manifest),
        "category": args.category,
        "policy": {
            "closure_is_not_resolution": True,
            "merged_pr_and_local_ref_required_for_candidate": True,
            "holdout_excluded_from_training": not args.include_holdout,
            "api_bodies_not_persisted": True,
        },
        "summary": summary,
        "cases": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
