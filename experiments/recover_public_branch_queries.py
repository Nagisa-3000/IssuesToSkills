#!/usr/bin/env python3
"""Recover all registered original queries on independently archived public Git heads."""

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import fingerprint, redact_history, write_json
from arex_skill_graph.public_branch_source import (
    PublicPushTarget,
    archive_hour,
    latest_archived_push,
    prepare_public_branch_query,
    scan_public_pushes,
)
from arex_skill_graph.skill_packages import _resolve
from arex_skill_graph.task_context import TaskContext


class CountedRead:
    def __init__(self, stream):
        self.stream, self.count, self.hash = stream, 0, hashlib.sha256()

    def read(self, size=-1):
        data = self.stream.read(size)
        self.count += len(data)
        if self.count > 256 * 1024**2:
            raise ValueError("compressed public archive read bound reached")
        self.hash.update(data)
        return data


def scan_hour(url, rows):
    started = time.monotonic()
    archive_hour(url)
    targets = [
        PublicPushTarget(r["query_issue"], r["repository_id"], r["before_input_at"], r["ref"])
        for r in rows
    ]
    request = urllib.request.Request(url, headers={"User-Agent": "AREX historical-input-audit"})
    with urllib.request.urlopen(request, timeout=90) as response:
        counted = CountedRead(response)
        with gzip.GzipFile(fileobj=counted) as stream:
            found, audit = scan_public_pushes(stream, targets, url)
    audit.update(
        compressed_bytes_read=counted.count,
        compressed_archive_sha256=counted.hash.hexdigest(),
        elapsed_seconds=time.monotonic() - started,
    )
    return found, audit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "work-items",
        "original-queries",
        "query-register",
        "input-recovery",
        "native-repositories",
        "output-dir",
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args(argv)
    if args.output_dir.exists() or not 1 <= args.workers <= 4:
        raise ValueError("preserve existing source recovery and use one to four archive workers")
    work = json.loads(args.work_items.read_text())
    queries = json.loads(args.original_queries.read_text())
    register = json.loads(args.query_register.read_text())
    recovery = json.loads(args.input_recovery.read_text())
    native = json.loads(args.native_repositories.read_text())
    by_query = {q["task"]["task_id"]: q for q in queries}
    by_input = {r["query_issue"]: r for r in recovery["results"]}
    if (
        register["queries_sha256"] != fingerprint(queries)
        or register["query_count"] != len(queries)
        or len(by_query) != len(queries)
        or {r["query_issue"] for r in work} != set(by_query)
        or len(work) != len(by_query)
        or register["selected_targets"] != len(register["audits"])
        or recovery.get("later_comments_and_repairs_persisted") is not False
    ):
        raise ValueError("public source recovery changed registered original population")
    for row in work:
        task = TaskContext.from_dict(by_query[row["query_issue"]]["task"])
        task.verify()
        if task.input_available_at != row["before_input_at"] or not row["branch_evidence"]:
            raise ValueError(
                "source lookup differs from original query or lacks public branch evidence"
            )
        for evidence in row["branch_evidence"]:
            path = _resolve(Path(task.root), evidence["path"])
            content = path.read_bytes()
            line = content.decode().splitlines()[evidence["line"] - 1]
            if (
                hashlib.sha256(content).hexdigest() != evidence["file_sha256"]
                or line != evidence["text"]
                or "branch=master" not in line
                or row["ref"] != "refs/heads/master"
            ):
                raise ValueError("public released branch evidence changed")
        if row["source_selection_uses_gold_outcomes"] is not False:
            raise ValueError("public source lookup may not use gold outcomes")
    args.output_dir.mkdir(parents=True)
    identity = {
        "schema": "original-query-public-branch-source-study-v1",
        "prepared_at_utc": datetime.now(UTC).isoformat(),
        "work_items_sha256": fingerprint(work),
        "original_queries_sha256": fingerprint(queries),
        "original_query_register_sha256": fingerprint(register),
        "input_recovery_sha256": fingerprint(recovery),
        "native_repository_map_sha256": fingerprint(native),
        "selected_targets": register["selected_targets"],
        "recovered_original_inputs": len(queries),
        "source_selection_policy": "latest archived public head within frozen-locator-selected hour; corroborate locator event and stable repository ID",
        "locator_index_is_not_publication_proof": True,
        "complete_GitHub_push_history_claimed": False,
        "source_or_runtime_selected_using_gold_outcomes": False,
        "commit_dates_used_as_publication_proof": False,
        "implementation_sha256": fingerprint(
            {
                name: (Path(__file__).resolve().parents[1] / name).read_text()
                for name in [
                    "experiments/recover_public_branch_queries.py",
                    "src/arex_skill_graph/public_branch_source.py",
                    "src/arex_skill_graph/published_history_query.py",
                ]
            }
        ),
        "actual_LLM_calls": 0,
        "formal_SWE_runs": 0,
    }
    write_json(args.output_dir / "study-identity.json", identity)
    grouped = {}
    for row in work:
        grouped.setdefault(row["archive_url"], []).append(row)
    publications, archive_audits, source_errors = {}, [], {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = {
            executor.submit(scan_hour, url, rows): (url, rows) for url, rows in grouped.items()
        }
        for future in as_completed(pending):
            url, rows = pending[future]
            try:
                found, audit = future.result()
                for row in rows:
                    qid, candidates = row["query_issue"], found[row["query_issue"]]
                    if not any(
                        c["event_created_at"] == row["locator_event_at"] for c in candidates
                    ):
                        source_errors[qid] = (
                            "locator event not corroborated in matching raw archive"
                        )
                        continue
                    try:
                        publications[qid] = latest_archived_push(candidates)
                    except ValueError as error:
                        source_errors[qid] = str(error)
                key = archive_hour(url).strftime("%Y%m%d-%H")
                write_json(
                    args.output_dir / "archive-audits" / (key + ".json"),
                    {"audit": audit, "qualified_projections": found},
                )
                archive_audits.append(audit)
            except (ValueError, OSError, KeyError, TypeError, EOFError) as error:
                for row in rows:
                    source_errors[row["query_issue"]] = redact_history(str(error))
                archive_audits.append(
                    {
                        "archive_url": url,
                        "archive_scan_complete": False,
                        "failure_class": type(error).__name__,
                        "failure_reason": redact_history(str(error)),
                    }
                )
            write_json(
                args.output_dir / "scan-progress.json",
                {
                    "completed_archive_hours": len(archive_audits),
                    "selected_archive_hours": len(grouped),
                    "publications_recovered": len(publications),
                    "source_errors": source_errors,
                    "actual_LLM_calls": 0,
                },
            )
            print(
                json.dumps(
                    {
                        "completed_archive_hours": len(archive_audits),
                        "selected_archive_hours": len(grouped),
                        "publications_recovered": len(publications),
                    }
                ),
                flush=True,
            )
    output_queries = []
    audits = [
        {"query_id": r["query_id"], "status": "original_input_unrecovered"}
        for r in register["audits"]
        if r["query_id"] not in by_query
    ]
    for row in work:
        qid = row["query_issue"]
        try:
            if qid not in publications:
                raise ValueError(source_errors.get(qid, "qualified archived head unavailable"))
            original = by_input[qid]
            if original["status"] != "original_input_qualified":
                raise ValueError("original query input has not been qualified")
            case = qid.replace("/", "__").replace(":", "-")
            case_dir = args.output_dir / "cases" / case
            write_json(case_dir / "public-source-publication.json", publications[qid])
            task, audit = prepare_public_branch_query(
                original["input_path"],
                original["qualification_path"],
                publications[qid],
                native[qid.rsplit(":", 1)[0]],
                case_dir / "public-base",
            )
            write_json(case_dir / "task.json", task.to_dict())
            write_json(case_dir / "source-preparation-audit.json", audit)
            output_queries.append({**by_query[qid], "task": task.to_dict()})
            audits.append(
                {
                    "query_id": qid,
                    "status": "registered_original_public_branch_query",
                    "input_available_at": task.input_available_at,
                    "base_commit": task.base_commit,
                    "source_publication_at": publications[qid]["event_created_at"],
                    "source_publication_sha256": fingerprint(publications[qid]),
                    "historical_causal_controls_completed": False,
                }
            )
        except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
            audits.append(
                {
                    "query_id": qid,
                    "status": "public_branch_source_or_input_gap",
                    "failure_class": type(error).__name__,
                    "reason": redact_history(str(error)),
                }
            )
        write_json(
            args.output_dir / "query-progress.json",
            {
                "completed_targets": len(audits),
                "selected_targets": register["selected_targets"],
                "registered_queries": len(output_queries),
                "audits": audits,
                "actual_LLM_calls": 0,
            },
        )
    if len(audits) != register["selected_targets"]:
        raise ValueError("public source study lost registered targets")
    write_json(args.output_dir / "queries.json", output_queries)
    completion = {
        **identity,
        "status": "terminal",
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "audits": audits,
        "query_count": len(output_queries),
        "queries_sha256": fingerprint(output_queries),
        "archive_audits": archive_audits,
        "archive_audits_sha256": fingerprint(archive_audits),
        "historical_causal_controls_completed": False,
        "new_utility_labels": 0,
        "native_source_records_replaced": False,
        "full_history_qualified": False,
    }
    write_json(args.output_dir / "query-register.json", completion)
    print(
        json.dumps(
            {
                "status": "terminal",
                "selected_targets": len(audits),
                "registered_queries": len(output_queries),
                "source_gaps": len(audits) - len(output_queries),
                "new_utility_labels": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
