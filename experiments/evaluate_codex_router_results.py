#!/usr/bin/env python3
"""Score Codex-selected retrieval plans against category-transfer labels."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.schema import NodeType
from arex_skill_graph.store import CatalogStore


def category_for_node(node: Any) -> str:
    for container in (getattr(node, "facets", {}), getattr(node, "payload", {})):
        if isinstance(container, dict):
            value = container.get("problem_class") or container.get("category")
            if value:
                return str(value)
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.results.read_text(encoding="utf-8"))
    rows = payload.get("rows", []) if isinstance(payload, dict) else []
    with CatalogStore(args.db) as store:
        store.initialize()
        nodes = store.list_nodes()
        relevant_by_category = {
            category: {
                node.id for node in nodes
                if node.node_type in {NodeType.ACTION, NodeType.WORKFLOW, NodeType.PATTERN}
                and category_for_node(node) == category
            }
            for category in {str(row.get("category") or "") for row in rows}
        }
    scored: list[dict[str, Any]] = []
    for row in rows:
        category = str(row.get("category") or "")
        relevant = relevant_by_category.get(category, set())
        ranks = [int(hit.get("rank")) for hit in row.get("hits", []) if str(hit.get("id")) in relevant]
        scored.append({
            "case_id": row.get("case_id"),
            "repository": row.get("repository"),
            "issue": row.get("issue"),
            "category": category,
            "decision": row.get("decision"),
            "first_relevant_rank": min(ranks) if ranks else None,
            "gold_count": len(relevant),
            "retrieval_ms": row.get("retrieval_ms"),
            "guardrail_errors": row.get("guardrail_errors", []),
        })
    ranks = [int(row["first_relevant_rank"]) for row in scored if row["first_relevant_rank"] is not None]
    aggregate = {
        "cases": len(scored),
        "recall_at_k": len(ranks) / len(scored) if scored else 0.0,
        "mrr": statistics.mean(1.0 / rank for rank in ranks) if ranks else 0.0,
        "mean_first_relevant_rank": statistics.mean(ranks) if ranks else None,
        "mean_latency_ms": statistics.mean(float(row["retrieval_ms"]) for row in scored) if scored else None,
        "guardrail_error_cases": sum(bool(row["guardrail_errors"]) for row in scored),
    }
    result = {
        "schema_version": "codex-router-retrieval-evaluation-v1",
        "source_results": str(args.results),
        "catalog": str(args.db),
        "label": "same universal problem class in training-derived catalog",
        "aggregate": aggregate,
        "rows": scored,
        "limitations": [
            "This is category transfer, not end-task repair correctness.",
            "No holdout solution ref, target diff, or target-only test was used for labels.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
