#!/usr/bin/env python3
"""Enrich unresolved training rows from GitHub issue timeline events.

Rendered issue HTML is useful for discovery but does not expose every
``referenced`` commit or cross-referenced pull request.  This bounded pass
uses one REST timeline request per selected row, records the raw identifiers,
and only marks a local commit as a candidate ref when the checkout resolves it.
It never treats a cross-reference as merged resolution; PR-page enrichment
and the extraction-manifest gate still decide that.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.I)


def gh_json(url: str, token: str | None) -> Any:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "arex-universal-resolution-study/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=45) as response:
        return json.load(response)


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


def pull_number_from_event(event: dict[str, Any], repository: str) -> int | None:
    source = event.get("source") or {}
    issue = source.get("issue") if isinstance(source, dict) else None
    if not isinstance(issue, dict):
        return None
    pull = issue.get("pull_request")
    html_url = str(issue.get("html_url") or "")
    api_url = str(pull.get("url") or "") if isinstance(pull, dict) else ""
    if f"github.com/{repository}/pull/" not in html_url and f"api.github.com/repos/{repository}/pulls/" not in api_url:
        return None
    number = issue.get("number")
    return int(number) if str(number).isdigit() else None


def fetch_timeline(case: dict[str, Any], token: str | None) -> dict[str, Any]:
    repository = str(case["repository"])
    issue = int(case["issue"])
    url = f"https://api.github.com/repos/{repository}/issues/{issue}/timeline?per_page=100"
    result: dict[str, Any] = {
        "source": "github_rest_issue_timeline",
        "url": url,
        "retrieved_at": datetime.now(UTC).isoformat(),
        "commit_refs": [],
        "pull_requests": [],
    }
    try:
        events = gh_json(url, token)
        if not isinstance(events, list):
            raise ValueError("timeline response is not an array")
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        return result
    commits = sorted({str(event.get("commit_id")).lower() for event in events if isinstance(event, dict) and SHA_RE.fullmatch(str(event.get("commit_id") or ""))})
    pulls = sorted({number for event in events if isinstance(event, dict) for number in [pull_number_from_event(event, repository)] if number is not None})
    result["commit_refs"] = commits
    result["pull_requests"] = pulls
    result["event_count"] = len(events)
    result["resolved_checkout_refs"] = [ref for ref in commits if git_resolves(str(case.get("checkout") or ""), ref)]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", choices=("train_candidate", "holdout_candidate"), default="train_candidate")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--only-missing-ref", action="store_true", default=True)
    args = parser.parse_args()

    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("cases"), list):
        raise ValueError("manifest must be an object with cases")
    selected = [
        dict(case) for case in document["cases"]
        if str(case.get("role") or case.get("split") or "") == args.role
        and (not args.only_missing_ref or not case.get("extraction_ref"))
    ]
    token = os.environ.get("GITHUB_TOKEN")
    evidence: dict[tuple[str, int], dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(fetch_timeline, case, token): (str(case["repository"]), int(case["issue"]))
            for case in selected
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                evidence[key] = future.result()
            except Exception as exc:
                evidence[key] = {"source": "github_rest_issue_timeline", "error": f"{type(exc).__name__}: {exc}"}

    timeline_meta = {"role": args.role, "selected": len(selected), "fetched": len(evidence), "generated_at": datetime.now(UTC).isoformat()}
    for original in document["cases"]:
        case = dict(original)
        key = (str(case["repository"]), int(case["issue"]))
        row = evidence.get(key)
        if row is None:
            continue
        verification = dict(case.get("verification") or {})
        verification["api_timeline_commit_refs"] = row.get("commit_refs", [])
        verification["api_timeline_pull_requests"] = row.get("pull_requests", [])
        verification["api_timeline_resolved_checkout_refs"] = row.get("resolved_checkout_refs", [])
        verification["api_timeline_resolution_evidence"] = "reference_found" if row.get("commit_refs") or row.get("pull_requests") else "no_reference_found"
        if row.get("error"):
            verification["api_timeline_error"] = row["error"]
        case["verification"] = verification
        case["api_timeline_evidence"] = row
        if row.get("resolved_checkout_refs") and not case.get("extraction_ref"):
            case["extraction_ref"] = row["resolved_checkout_refs"][0]
        document["cases"][document["cases"].index(original)] = case
    document["api_timeline_evidence"] = timeline_meta
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(timeline_meta, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
