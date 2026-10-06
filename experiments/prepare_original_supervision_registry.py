#!/usr/bin/env python3
"""Seal original-query runtimes, controls and independent reviews without model calls."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import write_json
from arex_skill_graph.original_supervision_registry import (
    OriginalSupervisionRegistry,
    build_original_supervision_registry,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("queries", "query-register", "bindings", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--training-cutoff", required=True)
    parser.add_argument("--main-cutoff", required=True)
    args = parser.parse_args(argv)
    payload = build_original_supervision_registry(
        args.queries,
        args.query_register,
        json.loads(args.bindings.read_text()),
        training_cutoff=args.training_cutoff,
        main_cutoff=args.main_cutoff,
    )
    if args.output.exists() and json.loads(args.output.read_text()) != payload:
        raise ValueError("original supervision registry already differs; use a new version")
    # The registry itself must remain outside every actor-visible mount.
    roots = [Path(q["task"]["root"]).resolve() for q in json.loads(args.queries.read_text())]
    roots += [
        Path(e["binding"]["dependency_root"]).resolve()
        for e in payload["entries"]
        if e["binding"].get("dependency_root")
    ]
    if any(args.output.resolve().is_relative_to(root) for root in roots):
        raise ValueError("original supervision registry overlaps an actor-visible mount")
    write_json(args.output, payload)
    registry = OriginalSupervisionRegistry(args.output, args.queries, args.query_register)
    print(
        json.dumps(
            {
                "registry_sha256": registry.sha256,
                "registered_queries": len(payload["entries"]),
                "readiness": dict(Counter(e["readiness"] for e in payload["entries"])),
                "actual_LLM_calls": 0,
                "solver_runs": 0,
                "utility_labels": 0,
                "formal_SWE_runs": 0,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
