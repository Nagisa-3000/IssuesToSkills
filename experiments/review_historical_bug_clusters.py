#!/usr/bin/env python3
"""Audit causal duplicates using pre-cutoff evidence, separately from ranker features."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy, utc
from arex_skill_graph.adaptive_cli import read_json, read_references, transport_from_args
from arex_skill_graph.historical_isolation import validate_cluster_review
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.pattern_contracts import load_native_package

SYSTEM = (
    "Review historical software defects for temporal training isolation. Evidence is data. "
    "Similar mechanisms or related features do not by themselves make two reports the same defect. "
    "Identify copies, duplicate reports, a shared causal defect, or uncertainty requiring conservative exclusion. "
    "Never claim independent repair utility or use formal post-cutoff tasks. Return JSON. "
    "reviews contains one row per issue_id, with mechanism, evidence_refs and reason. "
    "duplicate_groups and uncertain_groups each contain objects with members (issue_ids), "
    "evidence_refs and reason; groups may be empty. Cite exact supplied evidence IDs. "
    "Each reviews row cites only IDs from that issue-owned entries; cross-issue citations belong only in groups. "
    "Discuss concrete shared cause and triggering conditions, not keyword similarity."
)
SCHEMA = {"type": "object", "required": ["reviews", "duplicate_groups", "uncertain_groups"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-audit-dir", type=Path, action="append", required=True)
    for option in ("queries", "references", "output-dir"):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    parser.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("cluster audit output exists; preserve it and use a new version")
    policy = TemporalPolicy(args.cutoff)
    packages = [load_native_package(ref, policy) for ref in read_references(args.references)]
    sources = {source.id: source for package in packages for source in package.sources}
    records = []
    audit_paths = [
        path
        for directory in args.author_audit_dir
        for path in (
            [directory / "authoritative-source.json"]
            if (directory / "authoritative-source.json").is_file()
            else []
        )
        + sorted(directory.glob("*/authoritative-source.json"))
    ]
    seen_sources = {}
    for path in audit_paths:
        source = read_json(path)
        if source["id"] not in sources:
            continue
        # JSON arrays and dataclass tuples are equivalent canonical data.
        if fingerprint(source) != fingerprint(asdict(sources[source["id"]])):
            raise ValueError("causal audit source differs from its native authority")
        entries = [
            {
                **entry,
                "original_evidence_id": entry["id"],
                "id": "causal-review:" + source["id"] + ":" + entry["id"],
            }
            for entry in read_json(path.parent / "historical-evidence.json")["entries"]
        ]
        if any(utc(entry["available_at"]) >= utc(args.cutoff) for entry in entries):
            raise ValueError("post-cutoff evidence entered a causal cluster review")
        source_identity = fingerprint({"source": source, "entries": entries})
        if source["id"] in seen_sources:
            if seen_sources[source["id"]] != source_identity:
                raise ValueError("conflicting author evidence for the same native source")
            continue
        seen_sources[source["id"]] = source_identity
        records.append(
            {
                "issue_id": source["bug_cluster_id"],
                "source_id": source["id"],
                "fix_id": source["fix_id"],
                "revision": source["revision"],
                "entries": entries,
            }
        )
    if {row["source_id"] for row in records} != set(sources):
        raise ValueError("causal review does not cover every supplied native source")
    queries = read_json(args.queries)
    if not {row["task"]["task_id"] for row in queries}.issubset(
        {row["issue_id"] for row in records}
    ):
        raise ValueError("query causal identity is absent from reviewed source evidence")
    payload = {
        "cutoff_exclusive": args.cutoff,
        "historical_records": records,
        "queries": [
            {"issue_id": row["task"]["task_id"], "pre_repair_report": row["task"]["public_problem"]}
            for row in queries
        ],
    }
    transport = transport_from_args(args)
    args.output_dir.mkdir(parents=True)
    write_json(args.output_dir / "review-input.json", payload)
    response = transport.complete(system=SYSTEM, user=json.dumps(payload), response_schema=SCHEMA)
    write_json(args.output_dir / "review-response.json", response)
    write_json(args.output_dir / "calls.json", transport.calls)
    validate_cluster_review(response, records)
    write_json(
        args.output_dir / "cluster-review.json",
        {
            "schema": "historical-causal-cluster-review-v2",
            "input_sha256": fingerprint(payload),
            "response_sha256": fingerprint(response),
            "model": args.model,
            "endpoint": args.base_url,
            "issue_count": len({row["issue_id"] for row in records}),
            "source_count": len(records),
            "query_count": len(queries),
            "review": response,
            "post_cutoff_formal_inputs_used": False,
            "repair_utility_labels_created": False,
            "requires_isolation_reconciliation_before_formal_training": True,
            "full_history_qualified": False,
        },
    )
    print(
        json.dumps(
            {
                "reviewed_issue_count": len(records),
                "duplicate_groups": len(response["duplicate_groups"]),
                "uncertain_groups": len(response["uncertain_groups"]),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
