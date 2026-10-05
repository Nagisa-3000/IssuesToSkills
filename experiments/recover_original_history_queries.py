#!/usr/bin/env python3
"""Recover every supplied original opened Issue input from bounded public archive streams."""

import argparse
import gzip
import hashlib
import json
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.historical_opened_input import (
    OriginalIssueTarget,
    original_input_qualification,
    scan_original_opened_inputs,
)
from arex_skill_graph.history_census import fingerprint, redact_history, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-decompressed-bytes", type=int, default=1024**3)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve previous original-input recovery; use a new version")
    raw_targets = json.loads(args.targets.read_text())
    targets = [OriginalIssueTarget(**row) for row in raw_targets]
    if len({t.query_issue for t in targets}) != len(targets):
        raise ValueError("duplicate canonical original Issue target")
    groups = defaultdict(list)
    for target in targets:
        groups[target.archive_url].append(target)
    args.output_dir.mkdir(parents=True)
    rows, archive_audits = [], []
    for url, group in sorted(groups.items()):
        found, audit = {}, {}
        try:
            request = urllib.request.Request(
                url, headers={"User-Agent": "AREX historical-input-audit"}
            )
            with (
                urllib.request.urlopen(request, timeout=args.timeout) as response,
                gzip.GzipFile(fileobj=response) as stream,
            ):
                found, audit = scan_original_opened_inputs(
                    stream, group, url, max_bytes=args.max_decompressed_bytes
                )
            audit["status"] = "complete"
        except (ValueError, OSError, EOFError, urllib.error.URLError) as error:
            audit = {
                "archive_url": url,
                "status": "archive_scan_failed",
                "failure_type": type(error).__name__,
                "failure_reason": redact_history(str(error)),
                "unrelated_raw_events_persisted": False,
            }
        archive_audits.append(audit)
        for target in group:
            opened = found.get(target.query_issue)
            if opened is None:
                rows.append(
                    {
                        "query_issue": target.query_issue,
                        "status": "input_unrecovered",
                        "archive_url": url,
                        "reason": audit.get("invalid_targets", {}).get(
                            target.query_issue,
                            audit.get("failure_reason", "exact opened event not found"),
                        ),
                    }
                )
                continue
            case = target.query_issue.replace("/", "__").replace(":", "-")
            root = args.output_dir / "inputs" / case
            write_json(root / "opened-input.json", opened)
            input_sha = hashlib.sha256((root / "opened-input.json").read_bytes()).hexdigest()
            qualification = original_input_qualification(opened, input_sha)
            write_json(root / "qualification.json", qualification)
            rows.append(
                {
                    "query_issue": target.query_issue,
                    "status": "original_input_qualified",
                    "archive_url": url,
                    "event_id": opened["event_id"],
                    "input_available_at": opened["event_created_at"],
                    "input_path": str((root / "opened-input.json").resolve()),
                    "qualification_path": str((root / "qualification.json").resolve()),
                    "input_artifact_sha256": input_sha,
                }
            )
        write_json(
            args.output_dir / "progress.json",
            {
                "status": "running",
                "completed_targets": len(rows),
                "selected_targets": len(targets),
                "qualified_original_inputs": sum(
                    r["status"] == "original_input_qualified" for r in rows
                ),
                "actual_LLM_calls": 0,
            },
        )
        print(
            json.dumps(
                {
                    "archive": url,
                    "completed_targets": len(rows),
                    "qualified_inputs": sum(
                        r["status"] == "original_input_qualified" for r in rows
                    ),
                }
            ),
            flush=True,
        )
    inventory = {
        "schema": "original-public-history-query-recovery-v1",
        "targets_sha256": fingerprint(raw_targets),
        "selected_targets": len(targets),
        "qualified_original_inputs": sum(r["status"] == "original_input_qualified" for r in rows),
        "results": rows,
        "archive_audits": archive_audits,
        "unrelated_raw_events_persisted": False,
        "later_comments_and_repairs_persisted": False,
        "actual_LLM_calls": 0,
        "new_utility_labels": 0,
        "formal_SWE_runs": 0,
    }
    write_json(args.output_dir / "completion.json", inventory)
    print(
        json.dumps(
            {
                "status": "terminal",
                "selected_targets": len(targets),
                "qualified_original_inputs": inventory["qualified_original_inputs"],
                "actual_LLM_calls": 0,
                "formal_SWE_runs": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
