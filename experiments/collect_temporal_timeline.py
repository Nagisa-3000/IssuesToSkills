#!/usr/bin/env python3
"""Resume complete timeline identity/metadata pagination for the historical population."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_census import GitHubCLI
from arex_skill_graph.history_timeline import TimelineCensus


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--gh-executable", default="gh")
    args = parser.parse_args(argv)
    result = TimelineCensus(
        args.output_dir,
        args.repository,
        args.cutoff,
        GitHubCLI(args.gh_executable),
        progress=lambda message: print(message, flush=True),
    ).collect()
    print(json.dumps({k: v for k, v in result.items() if k != "batches"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
