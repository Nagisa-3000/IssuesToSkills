#!/usr/bin/env python3
"""Fetch issue-facing holdout text without fetching any resolution evidence.

This produces evaluation input only. It deliberately avoids comments,
timelines, linked pull requests, commits, patches, and tests so untouched
holdouts remain excluded from Skill extraction and Pattern induction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.DOTALL),
)


def redact_sensitive_text(value: str) -> tuple[str, int]:
    redacted = value
    count = 0
    for pattern in SECRET_PATTERNS:
        redacted, replacements = pattern.subn("<redacted-public-issue-secret>", redacted)
        count += replacements
    return redacted, count


def fetch_issue(repository: str, issue: int) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repository}/issues/{issue}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "arex-holdout-evaluation-input",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise TypeError(f"GitHub issue response is not an object: {repository}#{issue}")
    if value.get("pull_request"):
        raise ValueError(f"holdout input unexpectedly points to a pull request: {repository}#{issue}")
    return value


def enrich_case(case: dict[str, Any], issue: dict[str, Any]) -> dict[str, Any]:
    result = dict(case)
    title, title_redactions = redact_sensitive_text(str(issue.get("title") or ""))
    body, body_redactions = redact_sensitive_text(str(issue.get("body") or ""))
    result.update({
        "issue_title": title,
        "issue_body": body,
        "issue_body_length": len(body),
        "issue_body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "issue_state": issue.get("state"),
        "issue_created_at": issue.get("created_at"),
        "issue_updated_at": issue.get("updated_at"),
        "issue_labels": [
            str(label.get("name"))
            for label in issue.get("labels", [])
            if isinstance(label, dict) and label.get("name")
        ],
        "public_issue_secret_redactions": title_redactions + body_redactions,
        "evaluation_input_source": {
            "kind": "github_issue_title_and_body_only",
            "api_url": issue.get("url"),
            "html_url": issue.get("html_url"),
        },
        "extraction_forbidden": True,
    })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = json.loads(args.input.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise TypeError("input manifest must contain a cases array")

    enriched: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for raw_case in cases:
        case = dict(raw_case)
        repository = str(case["repository"])
        issue_number = int(case["issue"])
        try:
            issue = fetch_issue(repository, issue_number)
            enriched.append(enrich_case(case, issue))
        except (OSError, TimeoutError, urllib.error.HTTPError, urllib.error.URLError, ValueError) as exc:
            errors.append({
                "case_id": case.get("case_id"),
                "error": f"{type(exc).__name__}: {exc}",
            })

    payload = {
        "schema_version": "agent-core-holdout-evaluation-input-v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "source_manifest": str(args.input),
        "policy": {
            "extract": False,
            "issue_title_and_body_only": True,
            "comments_fetched": False,
            "timeline_fetched": False,
            "linked_pull_requests_fetched": False,
            "commits_or_patches_fetched": False,
            "purpose": "retrieval and applicability evaluation input",
        },
        "counts": {
            "requested": len(cases),
            "enriched": len(enriched),
            "errors": len(errors),
            "secret_redactions": sum(int(case["public_issue_secret_redactions"]) for case in enriched),
        },
        "errors": errors,
        "cases": enriched,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["counts"], ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
