#!/usr/bin/env python3
"""Build a six-harness, ten-class issue manifest without collapsing evidence into labels.

The seed file contains only candidate issue numbers.  This command can enrich
them with GitHub issue metadata and linked pull requests, but it deliberately
does not promote a closed issue to an extractable episode.  That decision is
made later by the evidence extractor after the implementation, call sites, and
tests have been inspected.
"""
from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSES = DEFAULT_ROOT / "experiments" / "manifests" / "universal-problem-classes-v1.json"
DEFAULT_SEEDS = DEFAULT_ROOT / "experiments" / "manifests" / "universal-issue-seeds-v1.json"
DEFAULT_OUTPUT = DEFAULT_ROOT / "experiments" / "manifests" / "universal-issue-manifest-v1.json"

CHECKOUTS = {
    "earendil-works/pi": "/home/chenyujia/tritonToLlvm/pi-agent",
    "Aider-AI/aider": "/home/chenyujia/tritonToLlvm/aider-agent",
    "NousResearch/hermes-agent": "/home/chenyujia/tritonToLlvm/hermes-agent",
    "openai/codex": "/home/chenyujia/tritonToLlvm/codex-agent",
    "google-gemini/gemini-cli": "/home/chenyujia/tritonToLlvm/gemini-cli",
    "QwenLM/qwen-code": "/home/chenyujia/tritonToLlvm/qwen-code",
}


def gh_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "arex-universal-resolution-study",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def linked_pr_numbers(issue: dict[str, Any]) -> list[int]:
    values: set[int] = set()
    pull_request = issue.get("pull_request")
    if isinstance(pull_request, dict):
        match = re.search(r"/pull/(\d+)", str(pull_request.get("url", "")))
        if match:
            values.add(int(match.group(1)))
    return sorted(values)


def enrich_case(case: dict[str, Any], classes: dict[str, dict[str, Any]], token: str | None, fetch: bool) -> dict[str, Any]:
    repository = str(case["repository"])
    issue_number = int(case["issue"])
    category = str(case["category"])
    result: dict[str, Any] = {
        "case_id": f"{repository}#{issue_number}:{category}:{case['role']}",
        "repository": repository,
        "issue": issue_number,
        "issue_url": f"https://github.com/{repository}/issues/{issue_number}",
        "category": category,
        "role": str(case["role"]),
        "split": "train_candidate" if case["role"] == "train_candidate" else "holdout_candidate",
        "checkout": CHECKOUTS.get(repository, ""),
        "problem_class": classes[category],
        "source": {
            "selection_query": "GitHub REST issues endpoint with state=closed; candidate only until linked implementation evidence is fetched",
            "retrieved_at": None,
        },
        "verification": {
            "issue_state": "unverified",
            "closed_at": None,
            "linked_pull_requests": [],
            "merged_resolution": None,
            "implementation_evidence": "pending_extraction",
        },
    }
    if not fetch:
        return result
    url = f"https://api.github.com/repos/{repository}/issues/{issue_number}"
    try:
        issue = gh_json(url, token)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        result["verification"]["error"] = f"{type(exc).__name__}: {exc}"
        return result
    result["title"] = str(issue.get("title", ""))
    result["body_present"] = bool(issue.get("body"))
    result["labels"] = [str(item.get("name", "")) for item in issue.get("labels", []) if isinstance(item, dict)]
    result["source"]["retrieved_at"] = datetime.now(UTC).isoformat()
    result["verification"]["issue_state"] = str(issue.get("state", "unknown"))
    result["verification"]["closed_at"] = issue.get("closed_at")
    result["verification"]["issue_is_pull_request"] = bool(issue.get("pull_request"))
    result["verification"]["linked_pull_requests"] = linked_pr_numbers(issue)
    if issue.get("state") != "closed":
        result["verification"]["rejection_reason"] = "seed is not closed at enrichment time"
    return result


def validate_seed_shape(seeds: list[dict[str, Any]], classes: dict[str, dict[str, Any]], repositories: list[str]) -> None:
    expected_roles = {"train_candidate", "holdout_candidate"}
    seen: set[tuple[str, int]] = set()
    by_bucket: dict[tuple[str, str], set[str]] = {}
    for case in seeds:
        key = (str(case["repository"]), int(case["issue"]))
        if key in seen:
            raise ValueError(f"duplicate repository/issue seed: {key}")
        seen.add(key)
        if str(case["repository"]) not in repositories:
            raise ValueError(f"repository outside six-harness scope: {case['repository']}")
        if str(case["category"]) not in classes:
            raise ValueError(f"unknown universal class: {case['category']}")
        if str(case["role"]) not in expected_roles:
            raise ValueError(f"unknown candidate role: {case['role']}")
        bucket = (str(case["repository"]), str(case["category"]))
        by_bucket.setdefault(bucket, set()).add(str(case["role"]))
    expected_buckets = {(repo, category) for repo in repositories for category in classes}
    if set(by_bucket) != expected_buckets:
        missing = sorted(expected_buckets - set(by_bucket))
        extra = sorted(set(by_bucket) - expected_buckets)
        raise ValueError(f"bucket mismatch; missing={missing[:5]} extra={extra[:5]}")
    incomplete = {bucket: roles for bucket, roles in by_bucket.items() if roles != expected_roles}
    if incomplete:
        raise ValueError(f"each repository/class bucket needs train and holdout candidates: {incomplete}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classes", type=Path, default=DEFAULT_CLASSES)
    parser.add_argument("--seeds", type=Path, default=DEFAULT_SEEDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--fetch", action="store_true", help="fetch issue state/title from GitHub; otherwise preserve unverified candidates")
    parser.add_argument("--fetch-role", choices=("all", "train_candidate", "holdout_candidate"), default="all", help="when fetching, restrict API calls to one candidate role while preserving all manifest rows")
    parser.add_argument("--max-fetch-cases", type=int, help="optional cap on API calls; uncapped rows remain unverified")
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"))
    args = parser.parse_args()
    class_doc = json.loads(args.classes.read_text(encoding="utf-8"))
    seed_doc = json.loads(args.seeds.read_text(encoding="utf-8"))
    classes = {str(item["id"]): dict(item) for item in class_doc["classes"]}
    repositories = [str(item) for item in seed_doc["repositories"]]
    seeds = [dict(item) for item in seed_doc["cases"]]
    validate_seed_shape(seeds, classes, repositories)
    fetch_count = 0
    manifest = []
    for case in seeds:
        role = str(case.get("role", ""))
        fetch_this = bool(args.fetch and (args.fetch_role == "all" or role == args.fetch_role))
        if args.max_fetch_cases is not None and fetch_count >= max(0, args.max_fetch_cases):
            fetch_this = False
        if fetch_this:
            fetch_count += 1
        manifest.append(enrich_case(case, classes, args.github_token, fetch_this))
    manifest.sort(key=lambda item: (item["category"], item["repository"], item["role"]))
    output = {
        "schema_version": "universal-issue-manifest-v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "repositories": repositories,
        "classes": list(classes.values()),
        "cases": manifest,
        "policy": {
            "train_candidates_are_not_automatically_admitted": True,
            "holdout_candidates_are_never_sent_to_action_or_pattern_extraction": True,
            "closed_state_is_necessary_but_not_sufficient": True,
            "implementation_test_and_linked_resolution_evidence_required": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    states: dict[str, int] = {}
    for item in manifest:
        state = str(item["verification"]["issue_state"])
        states[state] = states.get(state, 0) + 1
    print(json.dumps({"output": str(args.output), "cases": len(manifest), "fetched": fetch_count, "states": states}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
