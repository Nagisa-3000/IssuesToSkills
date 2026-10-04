#!/usr/bin/env python3
"""Reconcile historical execution labels against actual failing-base/known-repair controls.

All acceptance material is read after the original solver terminated. This is
historical evaluator validation; it neither creates a new solver run nor freezes
or evaluates a formal SWE population.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_runner import TOOL_BACKENDS
from arex_skill_graph.historical_solver_evaluator import (
    calibrate_historical_evaluator,
    historical_evaluator,
)
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.temporal_ranker_data import HistoricalQuery, execution_label_from_run


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("queries", "verifications", "dependency-root", "output-dir"):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--submissions-from", type=Path)
    parser.add_argument("--sandbox-backend", choices=TOOL_BACKENDS, default="namespace-copy")
    args = parser.parse_args(argv)
    queries = json.loads(args.queries.read_text())
    inventory = json.loads(args.verifications.read_text())
    qualified = {
        (r["issue_id"], r["fix_id"]): r for r in inventory["results"] if r["verified_resolution"]
    }
    identity = {
        "schema": "historical-causal-reconciliation-study-v1",
        "queries_sha256": fingerprint(queries),
        "verification_inventory_sha256": fingerprint(inventory),
        "dependency_root": str(args.dependency_root.resolve()),
        "sandbox_backend": args.sandbox_backend,
        "evaluator_code_sha256": fingerprint(
            (
                Path(__file__).resolve().parents[1]
                / "src/arex_skill_graph/historical_solver_evaluator.py"
            ).read_text()
        ),
        "prior_study_sha256": fingerprint(
            json.loads((args.submissions_from / "study-identity.json").read_text())
        )
        if args.submissions_from
        else None,
        "new_solver_runs": 0,
        "formal_SWE_runs": 0,
    }
    existing = args.output_dir / "identity.json"
    if existing.exists() and json.loads(existing.read_text()) != identity:
        raise ValueError(
            "reconciliation inputs changed; preserve old outputs and use a new directory"
        )
    write_json(existing, identity)
    results = []
    for raw in queries:
        task = TaskContext.from_dict(raw["task"])
        query = HistoricalQuery(
            task,
            raw["bug_cluster_id"],
            raw["fix_id"],
            tuple(raw.get("aliases", [])),
            tuple(raw.get("copied_from", [])),
            raw.get("exposed", False),
        )
        if query.exposed:
            raise ValueError("exposed evaluation query cannot supervise training")
        verification = qualified[(task.task_id, query.fix_id)]["verification_path"]
        case = task.task_id.replace("/", "__").replace(":", "-")
        destination = args.output_dir / case
        controls_path = destination / "controls.json"
        if controls_path.exists():
            controls = json.loads(controls_path.read_text())
        else:
            controls = calibrate_historical_evaluator(
                task, verification, args.dependency_root, sandbox_backend=args.sandbox_backend
            )
            write_json(controls_path, controls)
        reconciled = []
        if controls["passed"] and args.submissions_from:
            for saved in sorted((args.submissions_from / case).glob("*/run.json")):
                output = destination / saved.parent.name / "run.json"
                if output.exists():
                    reconciled.append(json.loads(output.read_text()))
                    continue
                prior = json.loads(saved.read_text())
                run = prior.get("run")
                if not run or not (run.get("solver_ended") or run.get("solver_terminated")):
                    continue
                evaluated = historical_evaluator(
                    verification, args.dependency_root, sandbox_backend=args.sandbox_backend
                )(task, run["patch"])
                updated = {**run, "evaluation": evaluated}
                updated["benchmark_resolved"] = bool(
                    run.get("solver_ended")
                    and not run.get("failure")
                    and evaluated.get("benchmark_resolved")
                )
                updated["validated_resolved"] = bool(
                    run.get("solver_ended")
                    and not run.get("failure")
                    and evaluated.get("validated_resolved")
                )
                row = {
                    **prior,
                    "run": updated,
                    "label": None,
                    "original_trajectory_sha256": fingerprint(run),
                    "reconciliation_not_new_solver_run": True,
                }
                if prior.get("candidate_id"):
                    try:
                        from dataclasses import asdict

                        row["label"] = asdict(
                            execution_label_from_run(
                                query,
                                prior["candidate_id"],
                                prior.get("candidate_kind", "workflow"),
                                updated,
                                sampling_probability=prior["sampling_probability"],
                            )
                        )
                    except ValueError as error:
                        row["supervision_exclusion_reason"] = str(error)
                write_json(output, row)
                reconciled.append(row)
        summary = {
            "query_id": task.task_id,
            "controls_passed": controls["passed"],
            "base_target_failed": controls["base_target_failed"],
            "known_repair_passed": controls["known_repair_passed"],
            "reconciled_submissions": len(reconciled),
            "utility_labels": sum(bool(r.get("label")) for r in reconciled),
        }
        results.append(summary)
        write_json(
            args.output_dir / "progress.json",
            {
                "completed_queries": len(results),
                "requested_queries": len(queries),
                "results": results,
                "formal_SWE_runs": 0,
            },
        )
        print(json.dumps(summary), flush=True)
    labels = [
        row["label"]
        for saved in args.output_dir.glob("*/*/run.json")
        if (row := json.loads(saved.read_text())).get("label")
    ]
    write_json(args.output_dir / "labels.json", labels)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
