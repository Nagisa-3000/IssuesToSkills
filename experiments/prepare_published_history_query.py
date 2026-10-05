#!/usr/bin/env python3
"""Prepare an original historical query from a previously published PyPI sdist."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import write_json
from arex_skill_graph.published_history_query import prepare_published_query


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("input", "qualification", "metadata", "archive", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument(
        "--environment",
        action="append",
        default=[],
        help="Verified runtime observation; omit when the runtime is not yet observed.",
    )
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve existing query preparation; choose a new output directory")
    task, audit = prepare_published_query(
        args.input,
        args.qualification,
        args.metadata,
        args.archive,
        args.output_dir / "public-base",
        environment=args.environment,
    )
    write_json(args.output_dir / "task.json", task.to_dict())
    write_json(args.output_dir / "audit.json", audit)
    print(
        json.dumps(
            {
                "query_id": task.task_id,
                "input_available_at": task.input_available_at,
                "archive_sha256": audit["archive_sha256"],
                "published_index_artifacts_verified": audit["published_index_artifacts_verified"],
                "base_commit": task.base_commit,
                "runtime_environment": task.environment,
                "formal_SWE_queries": 0,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
