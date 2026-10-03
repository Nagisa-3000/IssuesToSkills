#!/usr/bin/env python3
"""Fetch sanitized PR metadata and patches for explicitly selected study cases."""

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

from research_issue_skill_suitability import graphql, sanitizer, scrub


def collect(gh: str, case: dict, patterns: list) -> dict:
    owner, name = case["repository"].split("/")
    number = case["PR"]
    fields = """
      number title url body createdAt merged mergedAt additions deletions changedFiles
      baseRefOid headRefOid mergeCommit { oid }
      closingIssuesReferences(first:20) {
        nodes { number title url body createdAt closedAt labels(first:15) { nodes { name } } }
      }
    """
    query = f"query {{ repository(owner:{json.dumps(owner)},name:{json.dumps(name)}) {{ pullRequest(number:{number}) {{ {fields} }} }} }}"
    value = graphql(gh, query, patterns)["repository"]["pullRequest"]
    path = f"repos/{case['repository']}/pulls/{number}/files?per_page=100"
    response = subprocess.run([gh, "api", path], text=True, capture_output=True, timeout=45, check=False)
    if response.returncode:
        raise RuntimeError(f"Public PR files request failed (exit {response.returncode})")
    raw_files = scrub(json.loads(response.stdout), patterns)
    files = [{key: item.get(key) for key in ("filename", "status", "additions", "deletions", "patch", "sha")}
             for item in raw_files]
    record = {**case, "observed_at": datetime.now(UTC).isoformat(), "PR_metadata": value,
              "files": files, "all_file_metadata_returned": len(files) == value["changedFiles"],
              "credential_literals_redacted": True}
    if case.get("source_cutoff_exclusive") and (
        not value["merged"] or value["mergedAt"][:10] >= case["source_cutoff_exclusive"]
    ):
        raise ValueError(f"Source repair is outside cutoff: {case['repository']}#{number}")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gh", default="/mnt/c/Users/W/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe")
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text())
    patterns = sanitizer()
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(lambda case: collect(args.gh, case, patterns), cases))
    result = {"schema": "reviewed-issue-repair-evidence-v1", "records": records,
              "scope": "Exploratory historical sources and development examples. Reviewed later repairs must be excluded from future blind holdouts. No Agent effectiveness result is claimed.",
              "patch_limit": "GitHub may omit/truncate large/binary diffs; missing patches are explicitly null."}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in records:
        print(json.dumps({"repository": row["repository"], "PR": row["PR"],
                          "purpose": row["purpose"], "changed_files": len(row["files"]),
                          "test_files": [file["filename"] for file in row["files"]
                                         if "test" in file["filename"].lower() or "fixture" in file["filename"].lower()]},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
