#!/usr/bin/env python3
"""Collect all observable pre-cutoff issues; never treat current edits as history."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import GitHubCLI, HistoryCensus, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--repository", action="append")
    parser.add_argument("--gh-executable", default="gh")
    parser.add_argument("--phase", choices=["issues", "comments", "verify"], default="issues")
    args = parser.parse_args(argv)
    repositories = args.repository or ["pylint-dev/pylint", "PyCQA/pyflakes", "astral-sh/ruff"]
    api = GitHubCLI(args.gh_executable)
    summaries = []
    for repository in repositories:
        census = HistoryCensus(
            args.output_dir,
            repository,
            args.cutoff,
            api,
            progress=lambda text: print(text, flush=True),
        )
        if args.phase == "issues":
            result = census.census()
        elif args.phase == "comments":
            result = census.collect_comments()
        else:
            result = census.verify_identities()
        summaries.append(result)
        print(
            json.dumps(
                {
                    "repository": repository,
                    "issues": result["observable_pre_cutoff_issues"],
                    "body_statuses": result["body_statuses"],
                    "identity_verified": result["identity_second_pass_verified"],
                    "full_history_qualified": result["full_history_qualified"],
                }
            ),
            flush=True,
        )
    suffix = "-" + repositories[0].replace("/", "__") if len(repositories) == 1 else ""
    write_json(
        args.output_dir / f"{args.phase}-summary{suffix}.json",
        {
            "schema": "temporal-history-census-summary-v1",
            "cutoff_exclusive": args.cutoff,
            "repositories": summaries,
            "api_calls": api.calls,
            "full_history_qualified": False,
            "remaining": [
                "All other timeline events and linked repair evidence",
                "Unavailable historical text versions",
                "Semantic disposition and resolution verification",
            ],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
