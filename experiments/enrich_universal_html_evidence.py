#!/usr/bin/env python3
"""Enrich universal issue candidates from public GitHub HTML pages.

The REST core quota is intentionally not a prerequisite for this bounded
evidence pass.  GitHub's rendered issue page contains the issue state and the
timeline's referenced commit/PR links.  This command records those links as
discovery evidence only; it never promotes an issue to a ChangeEpisode.  The
actual checkout/diff/test gate remains in ``validate_universal_episodes.py``.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
import html
import json
from pathlib import Path
import re
import subprocess
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


COMMIT_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/commit/([0-9a-f]{7,40})", re.I)
PR_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", re.I)
STATE_RE = re.compile(r'\"state\":\"(OPEN|CLOSED)\"', re.I)
LINKED_BLOCK_RE = re.compile(r'\"linkedPullRequests\":\{\"nodes\":\[(.*?)\]\},\"agentAssignments\"', re.S)
CLOSED_BY_BLOCK_RE = re.compile(r'\"closedByPullRequestsReferences\":\{\"nodes\":\[(.*?)\]\},\"labels\"', re.S)
PR_DETAIL_RE = re.compile(r'\"number\":(\d+),\"url\":\"([^\"]+/pull/\d+)\",\"state\":\"(OPEN|CLOSED|MERGED)\"', re.I)


def load_cases(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("cases"), list):
        raise ValueError("manifest must be an object with a cases array")
    return value, [dict(item) for item in value["cases"]]


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


def fetch_html(case: dict[str, Any]) -> dict[str, Any]:
    repository = str(case["repository"])
    issue = int(case["issue"])
    url = f"https://github.com/{repository}/issues/{issue}"
    result: dict[str, Any] = {
        "url": url,
        "retrieved_at": datetime.now(UTC).isoformat(),
        "source": "github_rendered_issue_html",
        "issue_state": None,
        "commit_refs": [],
        "pull_requests": [],
        "resolved_checkout_refs": [],
    }
    try:
        request = Request(url, headers={"User-Agent": "arex-universal-resolution-study/1.0", "Accept": "text/html"})
        with urlopen(request, timeout=45) as response:
            page = response.read().decode("utf-8", "replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    states = [item.upper() for item in STATE_RE.findall(page)]
    if "CLOSED" in states:
        result["issue_state"] = "closed"
    elif "OPEN" in states:
        result["issue_state"] = "open"
    commit_refs = sorted({sha.lower() for repo, sha in COMMIT_RE.findall(page) if repo.lower() == repository.lower()}, key=len, reverse=True)
    pull_requests = sorted({int(number) for repo, number in PR_RE.findall(page) if repo.lower() == repository.lower()})
    linked_block = LINKED_BLOCK_RE.search(page)
    closed_by_block = CLOSED_BY_BLOCK_RE.search(page)
    linked_details = [
        {"number": int(number), "url": url, "state": state.lower()}
        for number, url, state in PR_DETAIL_RE.findall(linked_block.group(1) if linked_block else "")
    ]
    closed_by_details = [
        {"number": int(number), "url": url, "state": state.lower()}
        for number, url, state in PR_DETAIL_RE.findall(closed_by_block.group(1) if closed_by_block else "")
    ]
    result["commit_refs"] = commit_refs[:20]
    result["pull_requests"] = pull_requests[:20]
    result["linked_pull_request_details"] = linked_details[:20]
    result["closed_by_pull_request_details"] = closed_by_details[:20]
    checkout = str(case.get("checkout", ""))
    result["resolved_checkout_refs"] = [ref for ref in commit_refs if git_resolves(checkout, ref)]
    result["has_resolution_reference"] = bool(commit_refs or pull_requests)
    result["page_bytes"] = len(page.encode("utf-8"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", choices=("all", "train_candidate", "holdout_candidate"), default="train_candidate")
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    document, cases = load_cases(args.manifest)
    selected = [case for case in cases if args.role == "all" or str(case.get("role") or case.get("split")) == args.role]
    if args.max_cases is not None:
        selected = selected[: max(0, args.max_cases)]
    by_key = {(str(case["repository"]), int(case["issue"])): case for case in selected}
    evidence: dict[tuple[str, int], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(fetch_html, case): key for key, case in by_key.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                evidence[key] = future.result()
            except Exception as exc:  # keep one failed page from losing the batch
                evidence[key] = {"source": "github_rendered_issue_html", "error": f"{type(exc).__name__}: {exc}"}
    for case in cases:
        key = (str(case["repository"]), int(case["issue"]))
        record = evidence.get(key)
        if record is None:
            continue
        verification = dict(case.get("verification") or {})
        verification["html_issue_state"] = record.get("issue_state") or "unverified"
        verification["html_linked_pull_requests"] = record.get("pull_requests", [])
        verification["html_linked_pull_request_details"] = record.get("linked_pull_request_details", [])
        verification["html_closed_by_pull_request_details"] = record.get("closed_by_pull_request_details", [])
        verification["html_commit_refs"] = record.get("commit_refs", [])
        verification["html_resolved_checkout_refs"] = record.get("resolved_checkout_refs", [])
        verification["html_resolution_evidence"] = "reference_found" if record.get("has_resolution_reference") else "no_reference_found"
        if record.get("error"):
            verification["html_error"] = record["error"]
        case["verification"] = verification
        case["html_evidence"] = record
        resolved = record.get("resolved_checkout_refs", [])
        if resolved:
            case["extraction_ref"] = resolved[0]
    document["cases"] = cases
    document["html_evidence"] = {
        "role": args.role,
        "selected": len(selected),
        "fetched": len(evidence),
        "reference_cases": sum(bool(item.get("has_resolution_reference")) for item in evidence.values()),
        "checkout_resolvable_cases": sum(bool(item.get("resolved_checkout_refs")) for item in evidence.values()),
        "generated_at": datetime.now(UTC).isoformat(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(document["html_evidence"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
