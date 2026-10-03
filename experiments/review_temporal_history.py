#!/usr/bin/env python3
"""Evidence-review all censused issues, preserving every failure and missing version."""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.history_learning import observable_evidence, review_population
from arex_skill_graph.llm_http import OpenAICompatibleConfig


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--http-backend", choices=["native", "windows_pipe"], default="native")
    parser.add_argument("--repository", action="append")
    parser.add_argument("--text-recovery", type=Path)
    parser.add_argument("--strict-metadata", action="store_true")
    parser.add_argument("--prior-review-dir", type=Path)
    parser.add_argument(
        "--repair-locator-mode",
        choices=["closing_only", "all_pre_cutoff_mentions"],
        default="closing_only",
    )
    args = parser.parse_args(argv)
    repositories = args.repository or ["pylint-dev/pylint", "PyCQA/pyflakes", "astral-sh/ruff"]
    records = [
        r
        for repository in repositories
        for r in observable_evidence(
            args.census,
            repository,
            args.cutoff,
            text_recovery=args.text_recovery,
            strict_metadata=args.strict_metadata,
            repair_locator_mode=args.repair_locator_mode,
        )
    ]
    prior_records = (
        [
            r
            for repository in repositories
            for r in observable_evidence(args.census, repository, args.cutoff)
        ]
        if args.prior_review_dir
        else None
    )
    config = OpenAICompatibleConfig(
        os.environ.get("AREX_LLM_API_KEY", ""),
        args.base_url,
        args.model,
        max_output_tokens=10000,
        retries=1,
        http_backend=args.http_backend,
    )
    result = review_population(
        records,
        args.output_dir,
        config,
        workers=args.workers,
        prior_records=prior_records,
        prior_output=args.prior_review_dir,
    )
    print(json.dumps(result), flush=True)
    return 0 if result["all_issues_reviewed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
