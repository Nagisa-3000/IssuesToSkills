#!/usr/bin/env python3
"""Build audited historical supervision; never turn unrun candidates into failures."""

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import digest
from arex_skill_graph.adaptive_cli import read_json, read_references, write_json
from arex_skill_graph.historical_isolation import HistoricalIsolation
from arex_skill_graph.plan_validation import ResourcePolicy, TaskWorkflowPlan
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.temporal_ranker_data import (
    HistoricalQuery,
    SupervisionLabel,
    build_examples,
    pair_preferences,
    validate_training_snapshot,
)
from arex_skill_graph.workflow_ranker import workflow_capsule


def source_input_hashes(args):
    names = ("queries", "references", "labels", "plans", "excluded_query_ids", "causal_isolation")
    return {
        name: digest(read_json(path))
        for name in names
        if (path := getattr(args, name, None)) is not None
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("queries", "references", "labels", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--training-cutoff", required=True)
    parser.add_argument("--main-cutoff", required=True)
    parser.add_argument("--excluded-query-ids", type=Path)
    parser.add_argument(
        "--causal-isolation", type=Path, help="Accepted host-only causal identity index"
    )
    parser.add_argument(
        "--plans",
        type=Path,
        help="Current public Task Plans by query ID, including hard-negative contracts",
    )
    args = parser.parse_args(argv)
    isolation = HistoricalIsolation.load(args.causal_isolation) if args.causal_isolation else None
    queries = [
        HistoricalQuery(
            task=TaskContext.from_dict(r["task"]),
            bug_cluster_id=r["bug_cluster_id"],
            fix_id=r["fix_id"],
            aliases=tuple(r.get("aliases", [])),
            copied_from=tuple(r.get("copied_from", [])),
            exposed=r.get("exposed", False),
        )
        for r in read_json(args.queries)
    ]
    labels = [
        SupervisionLabel(**{**r, "evidence_refs": tuple(r["evidence_refs"])})
        for r in read_json(args.labels)
    ]
    plans = read_json(args.plans) if args.plans else {}

    def candidates(task, references, policy):
        resource_policy = ResourcePolicy(policy, references)
        return [
            workflow_capsule(w, task, resource_policy)
            for p in resource_policy.load()
            for w in p.workflows
        ] + [TaskWorkflowPlan.from_dict(p) for p in plans.get(task.task_id, [])]

    examples, audits = build_examples(
        queries,
        read_references(args.references),
        labels,
        candidates,
        training_cutoff=args.training_cutoff,
        main_cutoff=args.main_cutoff,
        excluded_query_ids=read_json(args.excluded_query_ids) if args.excluded_query_ids else (),
        isolation=isolation,
    )
    result = {
        "schema": "temporal-workflow-ranker-data-v1",
        "training_cutoff": args.training_cutoff,
        "main_cutoff": args.main_cutoff,
        "examples": [asdict(e) for e in examples],
        "pairs": list(pair_preferences(examples)),
        "audits": audits,
        "source_input_hashes": source_input_hashes(args),
        "repair_effectiveness_proven": False,
    }
    result["dataset_sha256"] = digest(result)
    validate_training_snapshot(result)
    write_json(args.output, result)
    print(f"Audited {len(examples)} observations; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
