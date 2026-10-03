#!/usr/bin/env python3
"""Synthetic native/CrossBind/ranker/isolated-solver pipeline validation, not SWE efficacy."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tests")]
from adaptive_fixture import make_fixture
from test_adaptive_contracts import RankingReplay
from test_temporal_ranker_training import make_dataset, tiny_model
from arex_skill_graph.adaptive_cli import ReplayTransport, write_json, new_ledger
from arex_skill_graph.adaptive_guidance import index_native_package, prepare_adaptive_guidance
from arex_skill_graph.adaptive_runner import AdaptiveSolver, hidden_evaluator_from_file
from arex_skill_graph.crossbind import splice_workflows
from arex_skill_graph.ranker_training import train_ranker, TrainedRankerScorer
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.workflow_ranker import WorkflowRanker


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=ROOT / "tmp/adaptive-contract-smoke-v1")
    p.add_argument("--history-tokens", type=int, default=6000)
    p.add_argument(
        "--history-tokenizer", choices=["cl100k_base", "utf8_upper_bound"], default="cl100k_base"
    )
    a = p.parse_args(argv)
    output = a.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        p.error("output directory exists; use a fresh versioned directory")
    output.mkdir(parents=True, exist_ok=True)
    package, task, policy = make_fixture(output / "core")

    def budget():
        return new_ledger({"history_tokens": a.history_tokens}, a.history_tokenizer)

    crossbind = splice_workflows(
        *package.workflows, ["detect:a"], ["guard:b"], task, package.pattern, budget(), policy
    )
    data, *_ = make_dataset(output / "training")
    write_json(output / "temporal-dataset.json", data)
    tiny_model(output / "tiny-transformer")
    training = train_ranker(data, output / "tiny-transformer", output / "checkpoint", epochs=3)
    scorer = TrainedRankerScorer(output / "checkpoint")
    with CatalogStore(output / "catalog.sqlite") as store:
        store.initialize()
        indexing = index_native_package(store, package.reference, policy.temporal)
        arms = {}
        for arm in ("E0", "E1", "E2", "E3"):
            ranker = WorkflowRanker(
                RankingReplay(),
                scorer=scorer if arm == "E3" else None,
                model=scorer.model_version if arm == "E3" else "synthetic-ranking-replay",
            )
            result = prepare_adaptive_guidance(task, store, policy, ranker, budget(), arm=arm)
            arms[arm] = {
                "retrieved_workflows": len(result["retrieved_ids"]),
                "plans": len(result["plans"]),
                "selected": result["selected_plan"] is not None,
                "fallback": result["fallback"],
                "behavior_verified": result["behavior_verified"],
                "budget": result["budget"],
            }
        before = Path(task.root, "checker.py").read_text()
        requests = [
            {
                "operation": "run_public_command",
                "arguments": {"argv": ["python3", "checker.py"]},
                "rationale": "Public reproduction",
            },
            {
                "operation": "write_file",
                "arguments": {
                    "path": "checker.py",
                    "content": before.replace("return True", "return context != 'type'"),
                },
                "rationale": "Synthetic narrow repair replay",
            },
            {
                "operation": "run_public_command",
                "arguments": {"argv": ["python3", "checker.py"]},
                "rationale": "Public regression check",
            },
            {
                "operation": "finish",
                "arguments": {},
                "rationale": "End solver before independent evaluation",
            },
        ]
        private = output / "synthetic-evaluator.json"
        private.write_text(
            json.dumps(
                {
                    "task_id": task.task_id,
                    "base_commit": task.base_commit,
                    "evaluator_version": "synthetic-independent-v1",
                    "benchmark_commands": [["python3", "checker.py"]],
                    "regression_commands": [
                        [
                            "python3",
                            "-c",
                            "from checker import diagnostic; assert diagnostic('runtime')",
                        ]
                    ],
                }
            )
        )
        solver = AdaptiveSolver(
            ReplayTransport(requests), WorkflowRanker(), store, policy, budget(), arm="B0"
        )
        solved = solver.run(task, evaluator=hidden_evaluator_from_file(private))
    integrity = subprocess.run(
        [sys.executable, str(Path(package.root) / "scripts/verify_package.py")],
        capture_output=True,
        text=True,
    )
    report = {
        "schema": "adaptive-contract-synthetic-smoke-v1",
        "synthetic": True,
        "live_llm_calls": 0,
        "fixture_authorship": "authored-file protocol replay, synthetic independent sources",
        "native_package_integrity": integrity.returncode == 0,
        "indexing": indexing,
        "crossbind": {
            "parent_workflows": crossbind.plans[0].parent_workflow_ids,
            "status": crossbind.reports[0].status,
            "behavior_verified": False,
        },
        "ranker_training": {
            key: training[key]
            for key in (
                "training_pairs",
                "training_queries",
                "development_queries",
                "tokens_processed",
                "checkpoint_sha256",
                "loss_history",
            )
        },
        "arms": arms,
        "isolated_solver": {
            "public_reproduction_exit": solved["public_observations"][0]["exit_code"],
            "public_post_repair_exit": solved["public_observations"][2]["exit_code"],
            "independent_acceptance": solved["validated_resolved"],
            "isolation": solved["isolation"],
            "budget": solved["budget"],
            "original_checkout_changed": Path(task.root, "checker.py").read_text() != before,
        },
        "history_token_cap": a.history_tokens,
        "history_tokenizer": a.history_tokenizer,
        "formal_default_history_cap_used": a.history_tokens == 6000,
        "repair_effectiveness_proven": False,
        "formal_swe_runs": 0,
        "limitations": [
            "Synthetic workflow and ranking replay",
            "Random initialized tiny Transformer is a training/reload check",
            "No full-history corpus, temporal SWE cohort or repair effectiveness claim",
        ],
    }
    write_json(output / "smoke-report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if integrity.returncode == 0 and solved["validated_resolved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
