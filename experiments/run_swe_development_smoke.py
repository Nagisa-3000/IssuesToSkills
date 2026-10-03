#!/usr/bin/env python3
"""Run the real common public solver on an exposed official development task."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import new_ledger, transport_from_args
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.docker_public_tools import DockerPublicTools
from arex_skill_graph.history_census import write_json
from arex_skill_graph.plan_validation import ResourcePolicy
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workflow_ranker import WorkflowRanker


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in (
        "task",
        "qualification",
        "register",
        "harness-root",
        "harness-python",
        "output-dir",
    ):
        parser.add_argument("--" + option, type=Path, required=True)
    parser.add_argument("--docker-host", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    parser.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    args = parser.parse_args(argv)
    import docker

    public = json.loads(args.task.read_text())
    if public["development_only"] is not True:
        raise ValueError("this smoke runner does not execute formal tasks")
    if args.output_dir.exists():
        raise ValueError("development smoke output exists; preserve it and use a new version")
    args.output_dir.mkdir(parents=True)
    task = TaskContext.from_dict(public["task"])
    qualification = json.loads(args.qualification.read_text())
    if (
        qualification["identity"]["development_only"] is not True
        or qualification["identity"]["base_commit"] != task.base_commit
    ):
        raise ValueError("development qualification/base mismatch")
    image = qualification["image"]
    client = docker.DockerClient(base_url=args.docker_host, timeout=180)

    def tools(checkout, ledger):
        return DockerPublicTools(
            checkout,
            ledger,
            client=client,
            image_id=image["image_id"],
            repository_digest=image["repository_digest"],
        )

    def evaluator(task, patch):
        patch_path = args.output_dir.resolve() / "solver.patch"
        patch_path.write_text(patch)
        command = [
            str(args.harness_python.resolve()),
            "experiments/evaluate_official_swe_patch.py",
            "--register",
            str(args.register),
            "--qualification",
            str(args.qualification),
            "--patch",
            str(patch_path),
            "--output-dir",
            str(args.output_dir / "independent-evaluation"),
            "--harness-root",
            str(args.harness_root),
            "--docker-host",
            args.docker_host,
        ]
        environment = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": "/tmp"}
        completed = subprocess.run(
            command, env=environment, capture_output=True, text=True, timeout=900, check=False
        )
        if completed.returncode:
            return {
                "benchmark_resolved": False,
                "validated_resolved": False,
                "reason": "independent official evaluator failed; native output suppressed",
            }
        return json.loads(completed.stdout)

    transport = transport_from_args(args)
    with CatalogStore(args.output_dir / "empty-baseline.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(transport, model=args.model),
            store,
            ResourcePolicy(TemporalPolicy("2024-01-01T00:00:00Z"), ()),
            new_ledger(tokenizer="cl100k_base"),
            arm="B0",
            tools_factory=tools,
        ).run(task, evaluator=evaluator)
    result.update(
        {
            "development_only": True,
            "formal_SWE_solver_runs": 0,
            "full_history_qualified": False,
            "live_calls": transport.calls,
        }
    )
    write_json(args.output_dir / "run.json", result)
    print(
        json.dumps(
            {
                "instance_id": task.task_id,
                "solver_ended": result["solver_ended"],
                "benchmark_resolved": result["benchmark_resolved"],
                "validated_resolved": result["validated_resolved"],
                "budget": result["budget"],
                "formal_SWE_solver_runs": 0,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
