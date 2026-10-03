#!/usr/bin/env python3
"""Evaluate E0-E3 or prompted/trained ranking on a frozen shared public pool."""

import argparse
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy, digest
from arex_skill_graph.adaptive_cli import (
    new_ledger,
    read_json,
    read_references,
    transport_from_args,
    write_json,
)
from arex_skill_graph.adaptive_guidance import prepare_adaptive_guidance
from arex_skill_graph.adaptive_runner import AdaptiveSolver, hidden_evaluator_from_file
from arex_skill_graph.embeddings import TransformerEncoder
from arex_skill_graph.experiment_metrics import ndcg, summarize_runs
from arex_skill_graph.plan_validation import ResourcePolicy, TaskWorkflowPlan
from arex_skill_graph.ranker_training import TrainedRankerScorer
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workflow_ranker import WorkflowRanker


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("tasks", "references", "db", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--cutoff", required=True)
    p.add_argument("--mode", choices=["guidance", "solver", "shared-pool"], default="guidance")
    p.add_argument("--arm", action="append", choices=["B0", "E0", "E1", "E2", "E3"])
    p.add_argument(
        "--pool",
        type=Path,
        help="Frozen public TaskContext and validated Plans, indexed by task ID",
    )
    p.add_argument(
        "--ranking-labels", type=Path, help="Independent grades loaded after ranking only"
    )
    p.add_argument("--checkpoint", type=Path)
    p.add_argument("--embedding-model", type=Path)
    p.add_argument(
        "--dependency-root",
        type=Path,
        help="Pinned isolated virtualenv mounted read-only to solver/evaluator",
    )
    p.add_argument("--budget", type=Path)
    p.add_argument(
        "--history-tokenizer", choices=["cl100k_base", "utf8_upper_bound"], default="cl100k_base"
    )
    p.add_argument("--replay", type=Path)
    p.add_argument("--model")
    p.add_argument("--base-url")
    p.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    p.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    p.add_argument("--seed", type=int, default=20261003)
    a = p.parse_args(argv)
    refs = read_references(a.references)
    tasks = read_json(a.tasks)
    arms = a.arm or ["E0", "E1", "E2"]
    scorer = TrainedRankerScorer(a.checkpoint) if a.checkpoint else None
    if ("E3" in arms or a.mode == "shared-pool") and scorer is None:
        p.error("E3/shared-pool needs a trained checkpoint; no silent fallback")
    if a.mode == "shared-pool" and not a.pool:
        p.error("shared-pool needs frozen --pool")
    if a.mode == "guidance" and "B0" in arms:
        p.error("B0 is a solver baseline")
    pool = read_json(a.pool) if a.pool else None
    encoder = TransformerEncoder(str(a.embedding_model)) if a.embedding_model else None
    rows, decisions = [], []
    with CatalogStore(a.db, encoder=encoder) as store:
        store.connection.execute("PRAGMA query_only=ON")
        frozen_db = hashlib.sha256(store.connection.serialize()).hexdigest()
        frozen = {
            "cutoff": a.cutoff,
            "arms": arms,
            "mode": a.mode,
            "references": refs,
            "tasks_sha256": digest(tasks),
            "catalog_sha256": frozen_db,
            "pool_sha256": digest(pool) if pool else None,
            "seed": a.seed,
            "encoder": store.encoder.descriptor(),
            "budget": read_json(a.budget) if a.budget else {},
            "history_tokenizer": a.history_tokenizer,
            "checkpoint": scorer.model_version if scorer else None,
            "prompt_version": WorkflowRanker.PROMPT_VERSION,
            "offline_replay": a.replay is not None,
            "http_backend": a.http_backend,
            "population_completion_audited": False,
        }
        for record in tasks:
            task = TaskContext.from_dict(record["task"])
            modes = ["prompted", "trained"] if a.mode == "shared-pool" else arms
            for arm in modes:
                ledger = new_ledger(frozen["budget"], a.history_tokenizer)
                transport = transport_from_args(a, replay_key=arm, task_id=task.task_id)
                trained = arm in {"E3", "trained"}
                ranker = WorkflowRanker(
                    transport,
                    scorer=scorer if trained else None,
                    model=scorer.model_version if trained else a.model or "offline-replay",
                    seed=a.seed,
                )
                policy = ResourcePolicy(TemporalPolicy(a.cutoff), tuple(refs))
                try:
                    selected = None
                    if a.mode == "shared-pool":
                        item = pool[task.task_id]
                        task = TaskContext.from_dict(item["task"])
                        plans = [TaskWorkflowPlan.from_dict(plan) for plan in item["plans"]]
                        decision = ranker.rank_plans(task, plans, policy, ledger)
                        selected = next(
                            (plan for plan in plans if plan.id in decision.selected_ids), None
                        )
                        decisions.append(
                            {
                                "task_id": task.task_id,
                                "arm": arm,
                                "decision": decision.to_dict(),
                                "pool_sha256": digest(item),
                                "budget": ledger.snapshot(),
                            }
                        )
                    if a.mode == "guidance":
                        result = prepare_adaptive_guidance(
                            task, store, policy, ranker, ledger, arm=arm, ground_with_model=True
                        )
                        result.update(
                            {
                                "task_id": task.task_id,
                                "benchmark_resolved": None,
                                "validated_resolved": None,
                            }
                        )
                    else:
                        evaluator = (
                            hidden_evaluator_from_file(
                                record["evaluator_manifest"], dependency_root=a.dependency_root
                            )
                            if record.get("evaluator_manifest")
                            else None
                        )
                        solver_arm = (
                            "E3" if arm == "trained" else "E2" if arm == "prompted" else arm
                        )
                        result = AdaptiveSolver(
                            transport,
                            ranker,
                            store,
                            policy,
                            ledger,
                            arm=solver_arm,
                            dependency_root=a.dependency_root,
                        ).run(
                            task,
                            evaluator=evaluator,
                            use_frozen_selection=a.mode == "shared-pool",
                            initial_plan=selected,
                        )
                    result.update({"arm": arm, "bug_cluster_id": record["bug_cluster_id"]})
                except Exception as exc:  # noqa: BLE001 -- Population boundary retains failed requests for audit.
                    # A failed run stays in the denominator; suppress potentially sensitive exception values.
                    result = {
                        "task_id": task.task_id,
                        "arm": arm,
                        "bug_cluster_id": record["bug_cluster_id"],
                        "failure_type": type(exc).__name__,
                        "budget": ledger.snapshot(),
                        "benchmark_resolved": False if a.mode != "guidance" else None,
                        "validated_resolved": False if a.mode != "guidance" else None,
                    }
                rows.append(result)
        if hashlib.sha256(store.connection.serialize()).hexdigest() != frozen_db:
            raise ValueError("frozen catalog changed during evaluation")
    grades = read_json(a.ranking_labels) if a.ranking_labels else {}
    for decision in decisions:
        relevant = grades.get(decision["task_id"], {})
        decision["nDCG@8"] = (
            ndcg(decision["decision"]["ranked_ids"], relevant) if relevant else None
        )
    output = {
        "schema": "pattern-crossbind-ranker-eval-v1",
        "configuration": frozen,
        "configuration_sha256": digest(frozen),
        "runs": rows,
        "shared_pool_decisions": decisions,
        "metrics": summarize_runs(rows),
        "repair_effectiveness_proven": False,
        "effectiveness_claim_requires_full_temporal_cohort_and_independent_evaluation": True,
    }
    write_json(a.output, output)
    print(f"Recorded {len(rows)} attempts including failures; wrote {a.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
