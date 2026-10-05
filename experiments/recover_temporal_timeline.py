#!/usr/bin/env python3
"""Recover known state/title omissions without replacing the original census."""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import GitHubCLI
from arex_skill_graph.history_http import GitHubHTTP
from arex_skill_graph.history_timeline_recovery import recover_timeline_coverage


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--gh-executable", default="gh")
    parser.add_argument("--github-backend", choices=["http", "cli"], default="http")
    parser.add_argument("--github-token-env", default="GH_TOKEN")
    args = parser.parse_args(argv)
    api = (
        GitHubHTTP(os.environ.get(args.github_token_env, ""))
        if args.github_backend == "http"
        else GitHubCLI(args.gh_executable)
    )
    result = recover_timeline_coverage(
        args.source,
        args.output_dir,
        args.cutoff,
        api,
        batch_size=args.batch_size,
    )
    print(json.dumps(result), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
