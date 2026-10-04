#!/usr/bin/env python3
"""Run a native Action definition exercise with explicit development provenance."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import (
    new_ledger,
    read_json,
    read_references,
    transport_from_args,
)
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.plan_validation import ResourcePolicy
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workflow_ranker import WorkflowRanker


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("references", "task-context", "output-dir"):
        parser.add_argument("--" + option, required=True, type=Path)
    parser.add_argument("--action-id", required=True)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--dependency-root", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key-env", default="AREX_LLM_API_KEY")
    parser.add_argument("--http-backend", default="native", choices=["native", "windows_pipe"])
    parser.add_argument("--public-read-only", action="store_true")
    parser.add_argument("--execution-unavailable-fixture", action="store_true")
    parser.add_argument("--enforce-action-prerequisites", action="store_true")
    parser.add_argument("--ground-current-action", action="store_true")
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve previous native Action exercise; use a new output directory")
    temporal = TemporalPolicy(args.cutoff)
    matches = []
    for ref in read_references(args.references):
        package = load_native_package(ref, temporal)
        for action in package.actions:
            if action.id == args.action_id:
                matches.append((package, action))
    if len(matches) != 1:
        raise ValueError("Action exercise must name one authoritative native Action")
    package, action = matches[0]
    task = TaskContext.from_dict(read_json(args.task_context))
    task.verify()
    args.output_dir.mkdir(parents=True)
    ledger = new_ledger(tokenizer="cl100k_base")
    ledger.approve_root(action.package_id)
    resources = []
    for relative in ("SKILL.md", action.resource):
        content = (Path(package.root) / relative).read_text()
        ledger.history(content, "native Action definition resource " + relative)
        resources.append(
            {
                "resource": relative,
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
                "chunks": [content[i : i + 4000] for i in range(0, len(content), 4000)],
            }
        )
    transport = transport_from_args(args)
    from dataclasses import replace

    transport.config = replace(
        transport.config, max_output_tokens=4000, timeout_seconds=180, stream_responses=True
    )
    policy = ResourcePolicy(temporal, (package.reference,))
    if args.ground_current_action:
        from arex_skill_graph.adaptive_guidance import current_grounding

        # Scope the request to the already loaded immutable Action; files remain unchanged.
        scope = replace(package, actions=(action,), workflows=(), pattern=None)
        try:
            task = current_grounding(task, (scope,), transport, ledger)
        except Exception as error:
            from arex_skill_graph.llm_http import safe_text

            failure = {
                "schema": "native-action-grounding-failure-v1",
                "failure_type": type(error).__name__,
                "failure_reason": safe_text(str(error), [transport.config.api_key]),
                "model_calls": len(transport.calls),
                "actual_action_records": 0,
                "authored_Action_executed": False,
                "formal_SWE_runs": 0,
                "formal_KB_admitted": False,
            }
            (args.output_dir / "calls.json").write_text(
                json.dumps(transport.calls, indent=2) + "\n"
            )
            (args.output_dir / "grounding-transcript.json").write_text(
                json.dumps(getattr(transport, "transcripts", []), ensure_ascii=False, indent=2)
                + "\n"
            )
            (args.output_dir / "exercise-failure.json").write_text(
                json.dumps(failure, indent=2) + "\n"
            )
            print(json.dumps(failure))
            return 1
        (args.output_dir / "grounded-task.json").write_text(
            json.dumps(task.to_dict(), ensure_ascii=False, indent=2) + "\n"
        )
    tools_factory = None
    if args.execution_unavailable_fixture:
        from arex_skill_graph.adaptive_runner import make_namespace_tools

        class UnavailableExecution:
            def __init__(self, checkout, budget):
                self.inner = make_namespace_tools(
                    checkout, budget, args.dependency_root, backend="namespace-copy"
                )
                self.budget = budget
                self.isolation = self.inner.isolation
                self.runtime_sha256 = self.inner.runtime_sha256

            def preflight(self):
                return self.inner.preflight()

            def close(self):
                self.inner.close()

            def run(self, argv, **kwargs):
                if kwargs.get("charge", True):
                    self.budget.charge(
                        "tool_calls", 1, "controlled unavailable public execution attempt"
                    )
                self.budget.check_time()
                return {
                    "argv": list(argv),
                    "exit_code": None,
                    "output": "Public command execution is unavailable in this controlled "
                    "evidence fixture; no analyzer command was executed.",
                    "execution_available": False,
                    "workspace_adopted": False,
                    "timed_out": False,
                    "isolation": self.isolation,
                    "runtime_sha256": self.runtime_sha256,
                    "fixture_policy": "native-command-execution-unavailable-v1",
                }

        tools_factory = UnavailableExecution
    with CatalogStore(args.output_dir / "development-catalog.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(),
            store,
            policy,
            ledger,
            dependency_root=args.dependency_root,
            sandbox_backend="namespace-copy",
            tools_factory=tools_factory,
        ).run(
            task,
            use_frozen_selection=True,
            recordable_actions=(action,),
            read_only_workspace=args.public_read_only,
            enforce_catalog_prerequisites=args.enforce_action_prerequisites,
            initial_observations=(
                {
                    "operation": "native_action_instruction",
                    "package_id": action.package_id,
                    "action_id": action.id,
                    "resources": resources,
                },
            ),
        )
    (args.output_dir / "trajectory.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    (args.output_dir / "calls.json").write_text(json.dumps(transport.calls, indent=2) + "\n")
    (args.output_dir / "model-transcripts.json").write_text(
        json.dumps(getattr(transport, "transcripts", []), ensure_ascii=False, indent=2) + "\n"
    )
    audit = {
        "schema": "native-action-definition-exercise-v1",
        "task_id": task.task_id,
        "package_id": action.package_id,
        "package_sha256": action.package_hash,
        "action_id": action.id,
        "same_author_model_definition_exercise": True,
        "independent_generalization_established": False,
        "functional_cases_passed": None,
        "semantic_validation": "pending_independent_functional_review",
        "formal_SWE_runs": 0,
        "formal_KB_admitted": False,
        "public_read_only": args.public_read_only,
        "controlled_execution_unavailable": args.execution_unavailable_fixture,
        "strict_functional_action_catalog": args.enforce_action_prerequisites,
        "current_action_grounded": args.ground_current_action,
        "resources": [{k: v for k, v in r.items() if k != "chunks"} for r in resources],
        "model": args.model,
        "base_url": args.base_url,
        "model_calls": len(transport.calls),
        "actual_action_records": len(result["action_observations"]),
        "solver_ended": result["solver_ended"],
        "failure": result["failure"],
    }
    (args.output_dir / "exercise-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
