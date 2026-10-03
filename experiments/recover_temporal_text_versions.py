#!/usr/bin/env python3
"""Recover pre-cutoff versions without persisting current future-edited text."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import GitHubCLI
from arex_skill_graph.history_text_recovery import recover_text_versions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--gh-executable", default="gh")
    args = parser.parse_args(argv)
    result = recover_text_versions(
        args.census, args.output_dir, args.cutoff, GitHubCLI(args.gh_executable)
    )
    print(
        json.dumps({k: v for k, v in result.items() if k not in {"records", "pages"}}), flush=True
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
