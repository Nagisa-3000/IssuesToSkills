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
    "Discuss concrete shared cause and triggering conditions, not keyword similarity."
)
SCHEMA = {"type": "object", "required": ["reviews", "duplicate_groups", "uncertain_groups"]}


def validate_cluster_review(response, records):
    allowed = {row["issue_id"]: {entry["id"] for entry in row["entries"]} for row in records}
    reviews = response.get("reviews")
    if not isinstance(reviews, list) or len(reviews) != len(allowed):
        raise ValueError("cluster review omitted or added historical issues")
    if {row.get("issue_id") for row in reviews} != set(allowed):
        raise ValueError("cluster review changed issue identities")
    for row in reviews:
        if (
            not row.get("mechanism")
            or not row.get("reason")
            or not row.get("evidence_refs")
            or not set(row["evidence_refs"]).issubset(allowed[row["issue_id"]])
        ):
            raise ValueError("causal review lacks issue-owned evidence")
    for kind in ("duplicate_groups", "uncertain_groups"):
        if not isinstance(response.get(kind), list):
            raise ValueError("cluster groups must be explicit arrays")  # noqa: TRY004 -- JSON contract errors use ValueError.
        for group in response[kind]:
            members = group.get("members", [])
            if (
                len(set(members)) < 2
                or len(set(members)) != len(members)
                or not set(members).issubset(allowed)
                or not group.get("reason")
            ):
                raise ValueError("cluster group members or rationale are invalid")
            refs = set(group.get("evidence_refs", []))
            if (
                not refs
                or not refs.issubset(set().union(*(allowed[member] for member in members)))
                or any(not refs.intersection(allowed[member]) for member in members)
            ):
                raise ValueError("cluster relation requires evidence for every member")
    return response


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("queries", "references", "author-audit-dir", "output-dir"):
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
    for path in sorted(args.author_audit_dir.glob("*/authoritative-source.json")):
        source = read_json(path)
        if source["id"] not in sources:
            continue
        # JSON arrays and dataclass tuples are equivalent canonical data.
        if fingerprint(source) != fingerprint(asdict(sources[source["id"]])):
            raise ValueError("causal audit source differs from its native authority")
        entries = read_json(path.parent / "historical-evidence.json")["entries"]
        if any(utc(entry["available_at"]) >= utc(args.cutoff) for entry in entries):
            raise ValueError("post-cutoff evidence entered a causal cluster review")
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
            "schema": "historical-causal-cluster-review-v1",
            "input_sha256": fingerprint(payload),
            "response_sha256": fingerprint(response),
            "model": args.model,
            "endpoint": args.base_url,
            "issue_count": len(records),
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
