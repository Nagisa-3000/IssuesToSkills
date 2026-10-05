#!/usr/bin/env python3
"""Qualify all registered original public queries with private replay controls."""

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.historical_replay_controls import run_original_query_controls
from arex_skill_graph.history_census import fingerprint, redact_history, write_json
from arex_skill_graph.task_context import TaskContext


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("queries", "query-register", "verifications", "runtime-map", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve existing replay controls; use a new output version")
    queries = json.loads(args.queries.read_text())
    register = json.loads(args.query_register.read_text())
    inventory = json.loads(args.verifications.read_text())
    runtimes = json.loads(args.runtime_map.read_text())
    if (
        register["queries_sha256"] != fingerprint(queries)
        or register["query_count"] != len(queries)
        or register["selected_targets"] != len(register["audits"])
        or len({row["task"]["task_id"] for row in queries}) != len(queries)
    ):
        raise ValueError("original public replay population differs from its register")
    authorities = {}
    for row in inventory["results"]:
        if row.get("verified_resolution"):
            key = (row["issue_id"], row["fix_id"])
            if key in authorities:
                raise ValueError("duplicate qualified native replay identity")
            authorities[key] = row
    query_ids = {row["task"]["task_id"] for row in queries}
    registered = {row["query_id"] for row in register["audits"]}
    if not query_ids <= registered or len(registered) != register["selected_targets"]:
        raise ValueError("registered original query denominator changed")
    args.output_dir.mkdir(parents=True)
    identity = {
        "schema": "original-query-replay-control-study-v1",
        "prepared_at_utc": datetime.now(UTC).isoformat(),
        "queries_sha256": fingerprint(queries),
        "query_register_sha256": fingerprint(register),
        "native_verification_inventory_sha256": fingerprint(inventory),
        "runtime_map_sha256": fingerprint(runtimes),
        "implementation_sha256": fingerprint(
            {
                name: (Path(__file__).resolve().parents[1] / name).read_text()
                for name in (
                    "experiments/qualify_original_release_controls.py",
                    "src/arex_skill_graph/historical_replay_controls.py",
                    "src/arex_skill_graph/adaptive_runner.py",
                    "src/arex_skill_graph/copied_sandbox.py",
                    "src/arex_skill_graph/copied_sandbox_worker.py",
                )
            }
        ),
        "selected_targets": register["selected_targets"],
        "registered_queries": len(queries),
        "known_repair_policy": "unchanged native production diff",
        "replay_cohort_frozen_before_known_repair": True,
        "all_model_calls": 0,
        "solver_branches": 0,
        "formal_SWE_runs": 0,
    }
    write_json(args.output_dir / "study-identity.json", identity)
    rows = [
        {
            "query_id": row["query_id"],
            "status": "original_input_unrecovered",
            "mechanical_controls_passed": False,
            "utility_labels_created": 0,
        }
        for row in register["audits"]
        if row["query_id"] not in query_ids
    ]
    for query in queries:
        task = TaskContext.from_dict(query["task"])
        case = task.task_id.replace("/", "__").replace(":", "-")
        try:
            authority = authorities[(task.task_id, query["fix_id"])]
            verification = Path(authority["verification_path"])
            if not verification.is_absolute():
                verification = Path(__file__).resolve().parents[1] / verification
            runtime = Path(runtimes[task.task_id.rsplit(":", 1)[0]])
            # The temporary process configuration permits the root-owned control
            # executor to verify this user-owned source Git identity.
            os.environ["GIT_CONFIG_COUNT"] = "1"
            os.environ["GIT_CONFIG_KEY_0"] = "safe.directory"
            os.environ["GIT_CONFIG_VALUE_0"] = task.root
            result = run_original_query_controls(
                task, verification, runtime, args.output_dir / "cases" / case
            )
            row = {
                "query_id": task.task_id,
                "status": "mechanical_pass"
                if result["mechanical_controls_passed"]
                else "controls_unqualified",
                "mechanical_controls_passed": result["mechanical_controls_passed"],
                "control_status": result["control_status"],
                "completion_path": str(
                    (args.output_dir / "cases" / case / "completion.json").resolve()
                ),
                "completion_sha256": fingerprint(result),
                "current_fail_to_pass_count": result["current_fail_to_pass_count"],
                "current_pass_to_pass_count": result["current_pass_to_pass_count"],
                "missing_native_pass_to_pass": result["missing_native_pass_to_pass"],
                "failed_checks": [
                    check["name"] for check in result["checks"] if check["status"] != "PASS"
                ],
                "independent_review_complete": False,
                "utility_labels_created": 0,
            }
        except (ValueError, OSError, KeyError) as error:
            row = {
                "query_id": task.task_id,
                "status": "execution_or_input_gap",
                "mechanical_controls_passed": False,
                "failure_class": type(error).__name__,
                "failure_reason": redact_history(str(error)),
                "utility_labels_created": 0,
            }
        rows.append(row)
        write_json(
            args.output_dir / "progress.json",
            {
                "status": "running",
                "completed_targets": len(rows),
                "selected_targets": register["selected_targets"],
                "mechanical_controls_passed": sum(
                    row["mechanical_controls_passed"] for row in rows
                ),
                "results": rows,
                "actual_LLM_calls": 0,
                "new_utility_labels": 0,
            },
        )
        print(
            json.dumps(
                {
                    "query_id": task.task_id,
                    "status": row["status"],
                    "completed_targets": len(rows),
                    "mechanical_controls_passed": sum(
                        row["mechanical_controls_passed"] for row in rows
                    ),
                }
            ),
            flush=True,
        )
    completion = {
        **identity,
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "status": "terminal",
        "results": rows,
        "completed_targets": len(rows),
        "mechanical_controls_passed": sum(row["mechanical_controls_passed"] for row in rows),
        "complete_replay_acceptances": 0,
        "independent_review_complete": False,
        "new_utility_labels": 0,
        "actual_LLM_calls": 0,
        "native_source_records_replaced": False,
        "actor_may_read_known_repairs": False,
        "full_history_qualified": False,
    }
    if len(rows) != register["selected_targets"]:
        raise ValueError("replay control study lost registered targets")
    write_json(args.output_dir / "completion.json", completion)
    print(
        json.dumps(
            {
                "status": "terminal",
                "selected_targets": len(rows),
                "mechanical_controls_passed": completion["mechanical_controls_passed"],
                "new_utility_labels": 0,
                "formal_SWE_runs": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
