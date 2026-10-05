#!/usr/bin/env python3
"""Reconcile accepted causal reviews with immutable native source identities."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import read_references
from arex_skill_graph.historical_isolation import reconcile_cluster_reviews
from arex_skill_graph.history_census import write_json
from arex_skill_graph.pattern_contracts import load_native_package


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-dir", type=Path, action="append", required=True)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--cutoff", default="2024-01-01T00:00:00Z")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        raise ValueError("isolation output exists; preserve it and use a new version")
    packages = [
        load_native_package(r, TemporalPolicy(args.cutoff))
        for r in read_references(args.references)
    ]
    sources = {s.id: s for p in packages for s in p.sources}
    index = reconcile_cluster_reviews(args.review_dir, tuple(sources.values()))
    write_json(args.output, index.to_dict())
    print(
        json.dumps(
            {
                "native_source_records": len(sources),
                "reviewed_issue_ids": len(index.reviewed_issue_ids),
                "conservative_identity_components": len(index.components),
                "isolation_sha256": index.sha256,
                "full_corpus_causal_review_complete": index.full_corpus_causal_review_complete,
                "actual_LLM_calls": 0,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
