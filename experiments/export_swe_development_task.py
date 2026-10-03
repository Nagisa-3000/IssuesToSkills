#!/usr/bin/env python3
"""Independent export of public benchmark input for an already-exposed development task."""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.benchmark_identity import EXPOSED_PULL_NUMBERS
from arex_skill_graph.history_census import write_json
from arex_skill_graph.official_swe import load_private_registered_instance
from arex_skill_graph.task_context import EvidenceAnchor, TaskContext


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--preparation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if int(args.instance_id.rsplit("-", 1)[1]) not in EXPOSED_PULL_NUMBERS:
        raise ValueError("this exporter is restricted to registered exposed development tasks")
    instance, provenance = load_private_registered_instance(
        json.loads(args.register.read_text()), args.variant, args.instance_id
    )
    prepared = json.loads(args.preparation.read_text())
    if instance["base_commit"] != prepared["base_commit"]:
        raise ValueError("public development base differs from the benchmark identity")
    raw_time = instance["created_at"]
    at = raw_time if isinstance(raw_time, datetime) else datetime.fromisoformat(raw_time)
    if at.tzinfo is None:
        at = at.replace(tzinfo=UTC)
    available = at.isoformat()
    task = TaskContext(
        instance["instance_id"],
        "pylint-dev/pylint",
        instance["base_commit"],
        prepared["checkout"],
        instance["problem_statement"],
        available,
        (
            EvidenceAnchor(
                "current:issue",
                "public_issue",
                instance["problem_statement"],
                instance["base_commit"],
                available_at=available,
            ),
        ),
        environment=("Pinned official SWE-bench-Live runtime",),
    )
    task.verify()
    write_json(
        args.output,
        {
            "task": task.to_dict(),
            "source": provenance,
            "development_only": True,
            "public_input_chronology_qualified_for_formal_evaluation": False,
            "solution_fields_exported": False,
            "formal_SWE_solver_runs": 0,
        },
    )
    print(
        json.dumps(
            {
                "instance_id": args.instance_id,
                "public_task_exported": True,
                "development_only": True,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
