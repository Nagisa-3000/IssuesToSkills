#!/usr/bin/env python3
"""Evaluate flat versus graph retrieval on the leave-one-project-out cases."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import statistics
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import NodeType
from arex_skill_graph.store import CatalogStore


def safe(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)


def load_cases(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("case manifest must be an array")
    return value


def category_for_node(node_id: str, workflow_to_category: dict[str, str], pattern_to_categories: dict[str, set[str]]) -> set[str]:
    if node_id in workflow_to_category:
        return {workflow_to_category[node_id]}
    return pattern_to_categories.get(node_id, set())


def build_category_maps(admission_summary: Path, episodes: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    values = json.loads(episodes.read_text(encoding="utf-8"))
    episode_categories = {str(item["episode_id"]): str(item.get("category") or item.get("metadata", {}).get("manifest_metadata", {}).get("category") or "") for item in values}
    summary = json.loads(admission_summary.read_text(encoding="utf-8"))
    workflow_to_category: dict[str, str] = {}
    for row in summary.get("episode_results", []):
        category = episode_categories.get(str(row.get("episode_id")), "")
        for workflow_id in row.get("workflows", []):
            workflow_to_category[str(workflow_id)] = category
    pattern_to_categories: dict[str, set[str]] = {}
    for pattern_id in summary.get("patterns", []):
        pattern_to_categories[str(pattern_id)] = set()
    # Pattern payloads are read from the database later; this map is filled by
    # the caller when supporting workflow IDs are available.
    return workflow_to_category, pattern_to_categories


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--admission-summary", type=Path, required=True)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--seed-k", type=int, default=40)
    parser.add_argument("--expand-hops", type=int, default=2)
    args = parser.parse_args()
    cases = load_cases(args.cases)
    workflow_to_category, pattern_to_categories = build_category_maps(args.admission_summary, args.episodes)
    with CatalogStore(args.db) as store:
        store.initialize()
        # Recover Pattern -> Workflow category support from persisted payloads.
        for node in store.list_nodes(node_types=[NodeType.PATTERN]):
            support = node.payload.get("workflow_ids", []) if isinstance(node.payload, dict) else []
            categories = set()
            for workflow_id in support if isinstance(support, list) else []:
                categories.update({workflow_to_category.get(str(workflow_id), "")})
            categories.discard("")
            pattern_to_categories[node.id] = categories
        retriever = SkillRetriever(store)
        rows: list[dict[str, Any]] = []
        for case in cases:
            source = case.get("manifest_source") or {}
            category = str(case.get("category") or source.get("category") or "")
            families = " ".join(str(item) for item in source.get("module_families", []))
            query = " ".join(filter(None, (category.replace("-", " "), str(case.get("issue_title", "")), families)))
            arms = ("bm25", "embedding", "hybrid", "hnsw", "graph")
            for arm in arms:
                expanded_count = 0
                unresolved = []
                seed_count = 0
                if arm == "bm25":
                    ranked = store.search_lexical(query, limit=args.top_k)
                    hit_rows = [(node, score, {"bm25": score}, []) for node, score in ranked]
                elif arm in {"embedding", "hnsw"}:
                    backend = "hnsw" if arm == "hnsw" and args.hnsw and args.hnsw.exists() else "exact"
                    ranked = store.search_vector(query, limit=args.top_k, vector_backend=backend, hnsw_path=str(args.hnsw) if args.hnsw and args.hnsw.exists() else None)
                    hit_rows = [(node, score, {"embedding" if backend == "exact" else "hnsw": score}, []) for node, score in ranked]
                else:
                    response = retriever.search(query, top_k=args.top_k, seed_k=args.seed_k, expand_hops=args.expand_hops if arm == "graph" else 0, query_mode="solve", vector_backend="hnsw" if args.hnsw and args.hnsw.exists() else "exact", hnsw_path=str(args.hnsw) if args.hnsw and args.hnsw.exists() else None, include_inactive=False)
                    seed_count, expanded_count, unresolved = response.seed_count, response.expanded_count, list(response.unresolved)
                    hit_rows = [(hit.node, hit.score, dict(hit.sources), list(hit.trace)) for hit in response.hits]
                if not seed_count:
                    seed_count = len(hit_rows)
                hits = []
                ranks: list[int] = []
                for rank, (node, score, sources, trace) in enumerate(hit_rows, 1):
                    categories = category_for_node(node.id, workflow_to_category, pattern_to_categories)
                    hit_row = {"rank": rank, "id": node.id, "node_type": node.node_type.value, "title": node.title, "score": score, "categories": sorted(categories), "sources": sources, "trace": trace}
                    hits.append(hit_row)
                    if category and category in categories:
                        ranks.append(rank)
                rows.append({"case_id": case["id"], "category": category, "query": query, "arm": arm, "seed_count": seed_count, "expanded_count": expanded_count, "unresolved": unresolved, "hits": hits, "first_relevant_rank": min(ranks) if ranks else None})
    aggregate: dict[str, Any] = {}
    for arm in sorted({row["arm"] for row in rows}):
        items = [row for row in rows if row["arm"] == arm]
        relevant = [row["first_relevant_rank"] for row in items if row["first_relevant_rank"] is not None]
        aggregate[arm] = {"cases": len(items), "recall_at_k": len(relevant) / len(items) if items else 0.0, "mrr": statistics.mean(1.0 / rank for rank in relevant) if relevant else 0.0, "mean_first_relevant_rank": statistics.mean(relevant) if relevant else None, "mean_seed_count": statistics.mean(row["seed_count"] for row in items) if items else 0.0, "mean_expanded_count": statistics.mean(row["expanded_count"] for row in items) if items else 0.0}
    output = {"schema_version": "held-out-retrieval-evaluation-v1", "cases": len(cases), "aggregate": aggregate, "rows": rows, "workflow_category_count": len(workflow_to_category), "pattern_count": len(pattern_to_categories)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "aggregate": aggregate}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
