#!/usr/bin/env python3
"""Map every benchmark PR to original issue dates without returning solution text."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.benchmark_identity import (
    classify_original_issue_group,
    connect_issue_alias_clusters,
    dataset_issue_identities,
    original_issue_identities,
    reconcile_dataset_issue_references,
)
from arex_skill_graph.history_census import GitHubCLI, fingerprint, now, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--union", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--gh-executable", default="gh")
    args = parser.parse_args(argv)
    union = json.loads(args.union.read_text())
    api, mapped = GitHubCLI(args.gh_executable), []
    for start in range(0, len(union["records"]), 25):
        batch = union["records"][start : start + 25]
        path = args.output_dir / f"mapping-{start // 25 + 1:04}.json"
        config = {
            "union_sha256": fingerprint(union),
            "cutoff": args.cutoff,
            "pull_numbers": [g["pull_number"] for g in batch],
        }
        if path.exists():
            saved = json.loads(path.read_text())
            if saved["config"] != config or fingerprint(saved["records"]) != saved["sha256"]:
                raise ValueError("benchmark mapping checkpoint configuration/integrity mismatch")
            records = saved["records"]
        else:
            mapping = original_issue_identities(
                api, union["target_repository"], config["pull_numbers"]
            )
            declared = {
                number
                for group in batch
                for alias in group["aliases"]
                for number in alias.get("dataset_original_issue_numbers", [])
            }
            issue_identities = dataset_issue_identities(api, union["target_repository"], declared)
            records = [
                classify_original_issue_group(
                    g,
                    reconcile_dataset_issue_references(
                        g, mapping[g["pull_number"]], issue_identities
                    ),
                    args.cutoff,
                )
                for g in batch
            ]
            write_json(path, {"config": config, "records": records, "sha256": fingerprint(records)})
        mapped.extend(records)
        print(f"Mapped {len(mapped)}/{len(union['records'])} PR identities", flush=True)
    connect_issue_alias_clusters(mapped)
    result = {
        "schema": "temporal-benchmark-original-issue-union-v2",
        "observed_at": now(),
        "cutoff_exclusive": args.cutoff,
        "source_union_sha256": fingerprint(union),
        "records": mapped,
        "distinct_pr_count": len(mapped),
        "issue_alias_cluster_count": len({g["issue_alias_cluster_id"] for g in mapped}),
        "temporal_classifications": dict(Counter(g["temporal_classification"] for g in mapped)),
        "unmapped_PRs": [g["pull_number"] for g in mapped if not g["original_issues"]],
        "reference_conflict_PRs": [
            g["pull_number"] for g in mapped if g.get("mapping_reference_conflict")
        ],
        "exposed_PRs_in_union": [
            g["pull_number"] for g in mapped if g["exposed_gold_development_only"]
        ],
        "benchmark_qualification_complete": False,
        "qualified_N": None,
        "original_issue_union_complete": all(g["original_issue_mapping_verified"] for g in mapped),
        "solution_text_returned": False,
        "semantic_duplicate_review_complete": False,
        "api_calls": api.calls,
    }
    write_json(args.output_dir / "benchmark-original-issue-union.json", result)
    print(json.dumps({k: v for k, v in result.items() if k not in {"records"}}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
