#!/usr/bin/env python3
"""Register every qualified historical query and every missing/aliased input."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import utc
from arex_skill_graph.history_census import fingerprint, redact_history, write_json
from arex_skill_graph.history_learning import observable_evidence
from arex_skill_graph.history_ranker_queries import prepare_historical_query

EXPOSED_DEVELOPMENT_IDS = frozenset({"PyCQA/pyflakes:" + str(n) for n in (633, 671, 674, 728, 771)})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--verifications", type=Path, required=True)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--text-recovery", type=Path)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--training-cutoff", default="2021-01-01T00:00:00Z")
    parser.add_argument(
        "--environment",
        action="append",
        default=[],
        help="Verified runtime observation; omit when not observed.",
    )
    args = parser.parse_args(argv)
    inventory = json.loads(args.verifications.read_text())
    requests = json.loads(args.requests.read_text())
    by_request = {(r["issue_id"], r["metadata"]["fix_id"]): r for r in requests}
    records = {
        r["issue_id"]: r
        for repository in {r["issue_id"].rsplit(":", 1)[0] for r in requests}
        for r in observable_evidence(
            args.census,
            repository,
            args.cutoff,
            text_recovery=args.text_recovery,
            strict_metadata=True,
            repair_locator_mode="all_pre_cutoff_mentions",
        )
    }
    queries, audits, seen_fixes, seen_issues = [], [], {}, set()
    for row in inventory["results"]:
        qid = row["issue_id"]
        audit = {"query_id": qid, "fix_id": row.get("fix_id")}
        if qid in EXPOSED_DEVELOPMENT_IDS:
            audits.append({**audit, "status": "excluded_exposed_development_query"})
            continue
        if not row["verified_resolution"]:
            audits.append({**audit, "status": "not_qualified_resolution"})
            continue
        request = by_request[(qid, row["fix_id"])]
        report = json.loads(Path(row["verification_path"]).read_text())
        revision = report["identity"]["merge_commit"]
        if qid in seen_issues or revision in seen_fixes:
            audits.append(
                {
                    **audit,
                    "status": "alias_of_registered_issue_or_repair",
                    "canonical_query_id": seen_fixes.get(revision, qid),
                }
            )
            continue
        case = qid.replace("/", "__").replace(":", "-")
        try:
            task, source_audit = prepare_historical_query(
                records[qid],
                report,
                request,
                args.output_dir / "public-bases" / case,
                environment=args.environment,
            )
        except (ValueError, OSError) as error:
            audits.append(
                {
                    **audit,
                    "status": "public_input_or_environment_gap",
                    "reason": redact_history(str(error)),
                }
            )
            continue
        seen_issues.add(qid)
        seen_fixes[revision] = qid
        queries.append(
            {
                "task": task.to_dict(),
                "bug_cluster_id": qid,
                "fix_id": row["fix_id"],
                "aliases": [records[qid]["identity"]["url"]],
                "copied_from": [],
                "exposed": False,
            }
        )
        audits.append(
            {
                **audit,
                **source_audit,
                "status": "registered_public_query",
                "split": "train"
                if utc(task.input_available_at) < utc(args.training_cutoff)
                else "development",
            }
        )
    write_json(args.output_dir / "queries.json", queries)
    write_json(
        args.output_dir / "query-register.json",
        {
            "schema": "historical-public-ranker-query-register-v1",
            "audits": audits,
            "queries_sha256": fingerprint(queries),
            "verification_inventory_sha256": fingerprint(inventory),
            "training_cutoff": args.training_cutoff,
            "main_cutoff": args.cutoff,
            "query_count": len(queries),
            "formal_SWE_queries": 0,
            "semantic_bug_cluster_review": "pending",
            "base_publication_time_limit": True,
            "real_ranker_training_completed": False,
        },
    )
    print(
        json.dumps(
            {
                "public_queries": len(queries),
                "train": sum(a.get("split") == "train" for a in audits),
                "development": sum(a.get("split") == "development" for a in audits),
                "formal_SWE_queries": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
