#!/usr/bin/env python3
"""Resolve linked/closing PRs from the rendered GitHub issue evidence.

Issue pages identify linked and closing PR numbers, while PR pages expose the
head and merge commit metadata.  This bounded pass records both without using
the REST core API.  A merge commit is still only a candidate implementation
ref; the extractor and admission validator must inspect its diff and tests.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
import json
from pathlib import Path
import re
import subprocess
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MERGE_RE = re.compile(r'\"mergeCommitSha\":(null|\"([0-9a-f]{40})\")', re.I)
HEAD_RE = re.compile(r'\"headSha\":\"([0-9a-f]{40})\"', re.I)
STATE_RE = re.compile(r'\"state\":\"(OPEN|CLOSED|MERGED)\"', re.I)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.I | re.S)


def git_resolves(checkout: str, ref: str) -> bool:
    if not checkout or not ref:
        return False
    try:
        proc = subprocess.run(["git", "-C", checkout, "cat-file", "-e", f"{ref}^{{commit}}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def fetch_pr(case: dict[str, Any], number: int) -> dict[str, Any]:
    repository = str(case["repository"])
    url = f"https://github.com/{repository}/pull/{number}"
    result: dict[str, Any] = {
        "number": number,
        "url": url,
        "source": "github_rendered_pull_request_html",
        "retrieved_at": datetime.now(UTC).isoformat(),
    }
    try:
        request = Request(url, headers={"User-Agent": "arex-universal-resolution-study/1.0", "Accept": "text/html"})
        with urlopen(request, timeout=45) as response:
            page = response.read().decode("utf-8", "replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    merge_match = MERGE_RE.search(page)
    result["merge_commit_sha"] = merge_match.group(2).lower() if merge_match and merge_match.group(2) else None
    head_match = HEAD_RE.search(page)
    result["head_sha"] = head_match.group(1).lower() if head_match else None
    result["state_candidates"] = sorted({item.lower() for item in STATE_RE.findall(page)})
    title_match = TITLE_RE.search(page)
    result["title"] = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
    result["merged"] = bool(result["merge_commit_sha"])
    checkout = str(case.get("checkout", ""))
    refs = [ref for ref in (result.get("merge_commit_sha"), result.get("head_sha")) if ref]
    result["resolved_checkout_refs"] = [ref for ref in refs if git_resolves(checkout, ref)]
    result["page_bytes"] = len(page.encode("utf-8"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", choices=("all", "train_candidate", "holdout_candidate"), default="train_candidate")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list):
        raise ValueError("manifest must be an object with cases")
    cases = [dict(case) for case in document["cases"] if args.role == "all" or str(case.get("role") or case.get("split")) == args.role]
    jobs: dict[tuple[str, int, int], tuple[dict[str, Any], int]] = {}
    for case in cases:
        verification = case.get("verification") or {}
        details = list(verification.get("html_linked_pull_request_details", [])) + list(verification.get("html_closed_by_pull_request_details", []))
        numbers = {
            int(item["number"])
            for item in details
            if isinstance(item, dict) and item.get("number") is not None
        }
        numbers.update(
            int(number)
            for number in verification.get("html_linked_pull_requests", [])
            if str(number).isdigit()
        )
        numbers.update(
            int(number)
            for number in verification.get("api_timeline_pull_requests", [])
            if str(number).isdigit()
        )
        for number in numbers:
            jobs[(str(case["repository"]), int(case["issue"]), number)] = (case, number)
    evidence: dict[tuple[str, int], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(fetch_pr, case, number): (str(case["repository"]), number) for case, number in jobs.values()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                evidence[key] = future.result()
            except Exception as exc:
                evidence[key] = {"number": key[1], "error": f"{type(exc).__name__}: {exc}"}
    updated_cases: list[dict[str, Any]] = []
    merged_case_count = 0
    local_ref_count = 0
    for original in document["cases"]:
        case = dict(original)
        if args.role != "all" and str(case.get("role") or case.get("split")) != args.role:
            updated_cases.append(case)
            continue
        repo = str(case["repository"])
        verification = dict(case.get("verification") or {})
        numbers = set()
        for item in list(verification.get("html_linked_pull_request_details", [])) + list(verification.get("html_closed_by_pull_request_details", [])):
            if isinstance(item, dict) and item.get("number") is not None:
                numbers.add(int(item["number"]))
        numbers.update(
            int(number)
            for number in verification.get("html_linked_pull_requests", [])
            if str(number).isdigit()
        )
        numbers.update(
            int(number)
            for number in verification.get("api_timeline_pull_requests", [])
            if str(number).isdigit()
        )
        pr_rows = [evidence[(repo, number)] for number in sorted(numbers) if (repo, number) in evidence]
        case["html_pr_evidence"] = pr_rows
        merged = [row for row in pr_rows if row.get("merged")]
        verification["html_merged_pull_requests"] = [int(row["number"]) for row in merged]
        verification["html_merged_resolution"] = bool(merged)
        verification["html_pr_resolution_evidence"] = "merged_commit_found" if merged else ("pr_pages_checked_no_merge" if pr_rows else verification.get("html_resolution_evidence", "unverified"))
        case["verification"] = verification
        case["resolution_commit_refs"] = [str(row["merge_commit_sha"]) for row in merged if row.get("merge_commit_sha")]
        candidate_refs: list[str] = []
        for row in pr_rows:
            candidate_refs.extend(str(ref) for ref in row.get("resolved_checkout_refs", []) if ref)
        existing = str(case.get("extraction_ref") or "")
        if existing and git_resolves(str(case.get("checkout", "")), existing):
            candidate_refs.insert(0, existing)
        for ref in candidate_refs:
            if ref:
                case["extraction_ref"] = ref
                break
        if merged:
            merged_case_count += 1
        if any(row.get("resolved_checkout_refs") for row in pr_rows):
            local_ref_count += 1
        updated_cases.append(case)
    document["cases"] = updated_cases
    document["pr_html_evidence"] = {
        "role": args.role,
        "pr_pages": len(evidence),
        "merged_case_count": merged_case_count,
        "local_ref_count": local_ref_count,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(document["pr_html_evidence"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
