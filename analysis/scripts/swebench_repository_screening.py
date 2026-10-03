#!/usr/bin/env python3
"""Collect public GitHub maintenance and PR evidence without reading credentials.

Uses an already authenticated GitHub CLI; the token remains inside that CLI.
Benchmark membership comes only from the frozen census, never GitHub topics.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from datetime import UTC, date, datetime, timedelta
from pathlib import Path


def now() -> str:
    return datetime.now(UTC).isoformat()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def github_query(executable: str, query: str) -> dict:
    for attempt in range(3):
        try:
            result = subprocess.run(
                [executable, "api", "graphql", "--input", "-"],
                input=json.dumps({"query": query}), capture_output=True, text=True, timeout=40, check=False,
            )
            break
        except subprocess.TimeoutExpired:
            if attempt == 2:
                raise RuntimeError("GitHub read request timed out after three attempts") from None
            print(json.dumps({"github_read_retry": attempt + 1, "reason": "transport timeout"}), flush=True)
            time.sleep(1 + attempt)
    if not result.stdout.strip():
        raise RuntimeError(f"GitHub CLI request failed (exit {result.returncode})")
    value = json.loads(result.stdout)
    if "data" not in value:
        raise RuntimeError("GitHub GraphQL response has no data")
    return value


REPOSITORY_FIELDS = """
  nameWithOwner url description homepageUrl isArchived isDisabled isPrivate isFork
  stargazerCount pushedAt updatedAt
  licenseInfo { spdxId name }
  primaryLanguage { name }
  defaultBranchRef { name target { ... on Commit { committedDate oid } } }
  latestRelease { tagName publishedAt isPrerelease }
  allPR: pullRequests { totalCount }
  mergedPR: pullRequests(states: MERGED) { totalCount }
  openPR: pullRequests(states: OPEN) { totalCount }
  parent { nameWithOwner }
"""


def repository_phase(args: argparse.Namespace, repositories: list[str]) -> None:
    path = args.output / "github-repositories.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    collected = existing.get("projects", {}) if existing.get("snapshot_date") == args.date else {}
    pending = [repository for repository in repositories if repository not in collected]
    for offset in range(0, len(pending), args.batch_size):
        batch = pending[offset:offset + args.batch_size]
        fields = []
        for index, repository in enumerate(batch):
            owner, name = repository.split("/", 1)
            fields.append(f"r{index}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{ {REPOSITORY_FIELDS} }}")
        observed = now()
        response = github_query(args.gh, "query { " + "\n".join(fields) + " rateLimit { remaining resetAt cost } }")
        for index, repository in enumerate(batch):
            value = response["data"].get(f"r{index}")
            collected[repository] = {"observed_at": observed, "repository": value, "resolved": value is not None}
        print(json.dumps({"repository_batch_completed": offset + len(batch), "pending_total": len(pending), "total_cached": len(collected), "rate_limit": response["data"].get("rateLimit")}), flush=True)
        write_json(args.output / "github-repositories.json", {
            "schema": "swebench-github-repositories-v1", "snapshot_date": args.date,
            "observed_at": now(), "projects": collected,
        })


def activity_phase(args: argparse.Namespace) -> None:
    metadata = json.loads((args.output / "github-repositories.json").read_text(encoding="utf-8"))
    canonical = {}
    for raw, value in metadata["projects"].items():
        repository = value["repository"]
        if repository is None:
            continue
        canonical[repository["nameWithOwner"]] = repository
    extra_names = set()
    if args.extra_repositories:
        for raw in json.loads(args.extra_repositories.read_text(encoding="utf-8")):
            record = metadata["projects"].get(raw, {}).get("repository")
            if record:
                extra_names.add(record["nameWithOwner"])
    # Collect recent PR evidence even for the lower historical-volume tier.
    chosen = sorted(name for name, value in canonical.items() if
                    (value["allPR"]["totalCount"] >= 500 or name in extra_names) and not value["isArchived"]
                    and not value["isDisabled"] and not value["isPrivate"])
    snapshot = date.fromisoformat(args.date)
    end = (snapshot + timedelta(days=1)).isoformat()
    start90 = (snapshot - timedelta(days=89)).isoformat()
    start365 = (snapshot - timedelta(days=364)).isoformat()
    activity_path = args.output / "github-pr-activity.json"
    existing = json.loads(activity_path.read_text(encoding="utf-8")) if activity_path.exists() else {}
    expected_windows = {"start90_inclusive": start90, "start365_inclusive": start365, "end_exclusive": end}
    contract = "single_inclusive_github_date_range_v1"
    collected = existing.get("projects", {}) if (existing.get("windows") == expected_windows
                                                and existing.get("query_contract") == contract) else {}
    pending = [name for name in chosen if name not in collected]
    for offset in range(0, len(pending), args.batch_size):
        batch = pending[offset:offset + args.batch_size]
        fields = []
        for index, name in enumerate(batch):
            searches = {
                "created90": f"repo:{name} is:pr created:{start90}..{args.date}",
                "merged90": f"repo:{name} is:pr is:merged merged:{start90}..{args.date} sort:updated-desc",
                "merged365": f"repo:{name} is:pr is:merged merged:{start365}..{args.date}",
            }
            for metric, search in searches.items():
                sample = " first:25," if metric == "merged90" else " first:1,"
                if metric == "merged90":
                    detail = "nodes { ... on PullRequest { number url mergedAt author { login __typename } } }"
                elif metric == "created90":
                    detail = "nodes { ... on PullRequest { number url createdAt } }"
                else:
                    detail = "nodes { ... on PullRequest { number url mergedAt } }"
                fields.append(f"r{index}_{metric}: search(query:{json.dumps(search)}, {sample} type:ISSUE) {{ issueCount {detail} }}")
        observed = now()
        response = github_query(args.gh, "query { " + "\n".join(fields) + " rateLimit { remaining resetAt cost } }")
        for index, name in enumerate(batch):
            metrics = {}
            for metric in ("created90", "merged90", "merged365"):
                result = response["data"].get(f"r{index}_{metric}")
                if result is None:
                    raise RuntimeError(f"Missing activity evidence: {name}/{metric}")
                metrics[metric] = result["issueCount"]
                lower = start365 if metric == "merged365" else start90
                date_field = "createdAt" if metric == "created90" else "mergedAt"
                for item in result.get("nodes", []):
                    stamp = item.get(date_field)
                    if stamp is None or not (lower <= stamp[:10] < end):
                        raise RuntimeError(f"Search date window was not honored: {name}/{metric}")
                if metric == "merged90":
                    sample = result.get("nodes", [])
                    metrics["merged90_sample"] = sample
                    metrics["sample_non_bot_prs"] = sum(1 for item in sample if item.get("author", {}) and item["author"].get("__typename") == "User")
                else:
                    metrics[metric + "_validation_sample"] = result.get("nodes", [])
            collected[name] = {"observed_at": observed, **metrics}
        print(json.dumps({"activity_batch_completed": offset + len(batch), "pending_total": len(pending), "total_cached": len(collected), "rate_limit": response["data"].get("rateLimit")}), flush=True)
        write_json(args.output / "github-pr-activity.json", {
            "schema": "swebench-github-pr-activity-v1", "snapshot_date": args.date,
            "query_contract": contract,
            "observed_at": now(), "windows": expected_windows,
            "sample_order": "GitHub search sort:updated-desc, up to 25 merged PRs per repo",
            "projects": collected,
        })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--date", default="2026-10-03")
    parser.add_argument("--phase", choices=("repositories", "activity"), required=True)
    parser.add_argument("--batch-size", type=int, default=15)
    parser.add_argument("--extra-repositories", type=Path)
    parser.add_argument("--gh", default=shutil.which("gh") or "/mnt/c/Users/W/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe")
    args = parser.parse_args()
    if args.phase == "repositories":
        census = json.loads((args.output / "benchmark-project-census.json").read_text(encoding="utf-8"))
        repositories = set(census["projects"])
        if args.extra_repositories:
            repositories.update(json.loads(args.extra_repositories.read_text(encoding="utf-8")))
        repository_phase(args, sorted(repositories, key=str.lower))
    else:
        activity_phase(args)


if __name__ == "__main__":
    main()
