#!/usr/bin/env python3
"""Execute a registered temporal development population with controlled candidate guidance.

This preliminary execution study uses validated probe-only initial task plans.
It retains no-match queries, hard-rejected/unrun candidates and all failures.
It does not mark M4/full-history learning or formal SWE evaluation complete.
"""

import argparse
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_cli import new_ledger, read_references, transport_from_args
from arex_skill_graph.adaptive_guidance import index_native_package
from arex_skill_graph.adaptive_runner import TOOL_BACKENDS, AdaptiveSolver
from arex_skill_graph.embeddings import TransformerEncoder
from arex_skill_graph.historical_solver_evaluator import historical_evaluator
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.plan_validation import ResourcePolicy, validate_task_plan
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.temporal_ranker_data import (
    HistoricalQuery,
    eligible_catalog,
    execution_label_from_run,
)
from arex_skill_graph.workflow_ranker import WorkflowRanker, workflow_capsule
from arex_skill_graph.workflow_rewriter import bind_selection


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in (
        "queries",
        "query-register",
        "references",
        "verifications",
        "dependency-root",
        "embedding-model",
        "output-dir",
    ):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    parser.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    parser.add_argument("--sandbox-backend", choices=TOOL_BACKENDS, default="namespace-bind")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261004)
    args = parser.parse_args(argv)
    import torch

    torch.set_num_threads(1)
    raw_queries = json.loads(args.queries.read_text())
    register = json.loads(args.query_register.read_text())
    if register["queries_sha256"] != fingerprint(raw_queries):
        raise ValueError("historical public query population changed")
    references = read_references(args.references)
    qualified = {
        (r["issue_id"], r["fix_id"]): r
        for r in json.loads(args.verifications.read_text())["results"]
        if r["verified_resolution"]
    }
    encoder = TransformerEncoder(str(args.embedding_model))
    queries = [
        HistoricalQuery(
            TaskContext.from_dict(r["task"]),
            r["bug_cluster_id"],
            r["fix_id"],
            tuple(r.get("aliases", [])),
            tuple(r.get("copied_from", [])),
            r.get("exposed", False),
        )
        for r in raw_queries
    ]
    identity = {
        "queries_sha256": fingerprint(raw_queries),
        "references_sha256": fingerprint(references),
        "model": args.model,
        "endpoint": args.base_url,
        "encoder": encoder.descriptor(),
        "solver_system_sha256": fingerprint(AdaptiveSolver.SYSTEM),
        "seed": args.seed,
        "sandbox_backend": args.sandbox_backend,
        "execution_policy_sha256": fingerprint(
            {
                p: (Path(__file__).resolve().parents[1] / p).read_text()
                for p in (
                    "experiments/run_historical_ranker_supervision.py",
                    "src/arex_skill_graph/adaptive_runner.py",
                    "src/arex_skill_graph/copied_sandbox.py",
                    "src/arex_skill_graph/copied_sandbox_worker.py",
                    "src/arex_skill_graph/historical_solver_evaluator.py",
                    "src/arex_skill_graph/temporal_ranker_data.py",
                )
            }
        ),
        "training_cutoff": register["training_cutoff"],
        "main_cutoff": register["main_cutoff"],
        "sampling": "top two embedding candidates; add best hard-gate survivors until two runnable; one uniform remaining candidate; no-match retained",
        "initial_plan_policy": "current unknown conditions authorize probes only",
        "development_population": True,
        "full_history_qualified": False,
    }
    checkpoint = args.output_dir / "study-identity.json"
    if checkpoint.exists() and json.loads(checkpoint.read_text()) != identity:
        raise ValueError("controlled historical study identity changed; use a new version")
    write_json(checkpoint, identity)
    scheduled, coverage = [], []
    for query in queries:
        policy, eligible, catalog_hash, rejected = eligible_catalog(
            query,
            references,
            training_cutoff=register["training_cutoff"],
            main_cutoff=register["main_cutoff"],
        )
        resources = ResourcePolicy(policy, eligible)
        candidates = [(p, w) for p in resources.load() for w in p.workflows]
        similarities = encoder.encode(
            [query.task.public_problem]
            + [
                workflow_capsule(w, query.task, resources).summary + " " + w.mechanism
                for _, w in candidates
            ]
        )
        ordered = sorted(
            range(len(candidates)),
            key=lambda i: (
                -sum(a * b for a, b in zip(similarities[0], similarities[i + 1])),
                candidates[i][1].id,
            ),
        )
        chosen = [(i, 1.0) for i in ordered[:2]]
        reports = {
            i: validate_task_plan(
                bind_selection(query.task, None, candidates[i][1].actions, (candidates[i][1],)),
                query.task,
                resources,
            )
            for i in ordered
        }
        runnable_count = sum(reports[i].status != "FAIL" for i, _ in chosen)
        for index in ordered[2:]:
            if runnable_count >= 2:
                break
            if reports[index].status != "FAIL":
                chosen.append((index, 1.0))
                runnable_count += 1
        rng = random.Random(str(args.seed) + query.task.task_id)
        remaining = [i for i in ordered if i not in {index for index, _ in chosen}]
        if remaining:
            chosen.append((rng.choice(remaining), 1.0 / len(remaining)))
        case = query.task.task_id.replace("/", "__").replace(":", "-")
        scheduled.append((query, None, None, policy, 1.0, case + "/baseline"))
        for number, (index, probability) in enumerate(chosen, 1):
            package, workflow = candidates[index]
            scheduled.append(
                (
                    query,
                    package.reference,
                    workflow,
                    policy,
                    probability,
                    case + "/candidate-" + str(number),
                )
            )
        coverage.append(
            {
                "query_id": query.task.task_id,
                "catalog_sha256": catalog_hash,
                "eligible_workflows": len(candidates),
                "selected_candidate_ids": [candidates[i][1].id for i, _ in chosen],
                "rejected_packages": rejected,
                "structurally_runnable_candidates": sum(
                    r.status != "FAIL" for r in reports.values()
                ),
                "unrun_candidates_are_failure_labels": False,
            }
        )
    write_json(args.output_dir / "candidate-coverage.json", coverage)

    def run_branch(branch):
        query, reference, workflow, policy, probability, relative = branch
        directory = args.output_dir / relative
        saved_path = directory / "run.json"
        if saved_path.exists():
            return json.loads(saved_path.read_text())
        transport = transport_from_args(args)
        ledger = new_ledger(tokenizer="cl100k_base")
        branch_encoder = TransformerEncoder(str(args.embedding_model))
        with CatalogStore(directory / "controlled-catalog.sqlite", encoder=branch_encoder) as store:
            store.initialize()
            if reference:
                index_native_package(store, reference, policy)
            resources = ResourcePolicy(policy, (reference,) if reference else ())
            initial = (
                bind_selection(query.task, None, workflow.actions, (workflow,))
                if workflow
                else None
            )
            report = validate_task_plan(initial, query.task, resources) if initial else None
            if report and report.status == "FAIL":
                row = {
                    "query_id": query.task.task_id,
                    "candidate_id": workflow.id,
                    "status": "hard_rejected_unrun",
                    "report": report.to_dict(),
                    "failure_label_created": False,
                    "live_calls": transport.calls,
                }
            else:
                verification = qualified[(query.task.task_id, query.fix_id)]
                result = AdaptiveSolver(
                    transport,
                    WorkflowRanker(transport, model=args.model),
                    store,
                    resources,
                    ledger,
                    arm="E1" if reference else "B0",
                    dependency_root=args.dependency_root,
                    sandbox_backend=args.sandbox_backend,
                ).run(
                    query.task,
                    evaluator=historical_evaluator(
                        verification["verification_path"],
                        args.dependency_root,
                        sandbox_backend=args.sandbox_backend,
                    ),
                    use_frozen_selection=True,
                    initial_plan=initial,
                )
                row = {
                    "query_id": query.task.task_id,
                    "candidate_id": workflow.id if workflow else None,
                    "status": "executed",
                    "run": result,
                    "live_calls": transport.calls,
                    "sampling_probability": probability,
                    "label": None,
                }
                if (
                    workflow
                    and result.get("solver_terminated")
                    and result.get("evaluation", {}).get("evaluation_completed") is True
                ):
                    label = execution_label_from_run(
                        query, workflow.id, "workflow", result, sampling_probability=probability
                    )
                    label = replace(
                        label,
                        applicability="probe_only"
                        if report.mode == "probe_only"
                        else "adaptively_usable",
                    )
                    row["label"] = asdict(label)
        write_json(saved_path, row)
        print(
            json.dumps(
                {
                    "query_id": query.task.task_id,
                    "candidate_id": row["candidate_id"],
                    "status": row["status"],
                    "resolved": row.get("run", {}).get("benchmark_resolved"),
                    "label_created": bool(row.get("label")),
                }
            ),
            flush=True,
        )
        return row

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = {executor.submit(run_branch, branch): branch for branch in scheduled}
        for future in as_completed(pending):
            try:
                results.append(future.result())
            except Exception as error:  # noqa: BLE001 -- Population boundary retains failed requests for audit.
                branch = pending[future]
                row = {
                    "query_id": branch[0].task.task_id,
                    "candidate_id": branch[2].id if branch[2] else None,
                    "status": "infrastructure_or_protocol_failure",
                    "failure_type": type(error).__name__,
                    "failure_label_created": False,
                    "native_output_suppressed": True,
                }
                write_json(args.output_dir / branch[-1] / "branch-failure.json", row)
                results.append(row)
            write_json(
                args.output_dir / "study-results.json",
                {
                    "results": results,
                    "scheduled_count": len(scheduled),
                    "completed_count": len(results),
                    "real_ranker_training_completed": False,
                    "full_history_qualified": False,
                    "formal_SWE_runs": 0,
                },
            )
    write_json(args.output_dir / "labels.json", [r["label"] for r in results if r.get("label")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
