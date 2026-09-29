#!/usr/bin/env python3
"""Evaluate sparse, dense, HNSW, hybrid, and graph retrieval on holdout cases.

The labels are category-level transfer labels, not issue-title string matches:
for a holdout case, every training-derived catalog node carrying the same
universal problem class is relevant.  This makes the evaluation explicit about
what is measured (cross-repository problem-class transfer) and avoids claiming
that a hit is a valid repair merely because it shares a word with an issue.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
import time
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.retrieval import SearchHit, SkillRetriever
from arex_skill_graph.schema import NodeType
from arex_skill_graph.store import CatalogStore


def load_cases(path: Path, role: str) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    return [dict(case) for case in cases if str(case.get("role") or case.get("split")) == role]


def category_for_node(node: Any) -> str:
    for container in (getattr(node, "facets", {}), getattr(node, "payload", {})):
        if isinstance(container, dict):
            value = container.get("problem_class") or container.get("category")
            if value:
                return str(value)
    return ""


def query_for_case(case: dict[str, Any]) -> tuple[str, str]:
    problem = case.get("problem_class") or {}
    if isinstance(problem, dict):
        generic = str(problem.get("problem") or "")
        workflow = " ".join(str(item) for item in problem.get("workflow", []))
    else:
        generic, workflow = "", ""
    issue_title = str(case.get("issue_title") or case.get("title") or "")
    issue_body = str(case.get("issue_body") or "")
    query = " ".join(part for part in (issue_title, issue_body[:1200], generic, workflow) if part).strip()
    source = "issue+class" if issue_title else "class-only-unverified"
    return query, source


def context_tokens(hits: Iterable[SearchHit]) -> int:
    text = "\n".join(
        f"{hit.node.node_type.value} {hit.node.id} {hit.node.title} {hit.node.summary}"
        for hit in hits
    )
    return (len(text) + 3) // 4 if text else 0


def compact_hit(hit: SearchHit, rank: int, relevant: bool) -> dict[str, Any]:
    return {
        "rank": rank,
        "id": hit.node.id,
        "node_type": hit.node.node_type.value,
        "title": hit.node.title,
        "repository": hit.node.repository,
        "category": category_for_node(hit.node),
        "score": hit.score,
        "relevant": relevant,
        "sources": dict(hit.sources),
        "trace": list(hit.trace),
    }


def evaluate_case(store: CatalogStore, case: dict[str, Any], args: argparse.Namespace, hnsw_available: bool) -> list[dict[str, Any]]:
    query, query_source = query_for_case(case)
    category = str(case.get("category") or "")
    relevant_ids = {
        node.id for node in store.list_nodes()
        if category
        and node.node_type in {NodeType.ACTION, NodeType.WORKFLOW, NodeType.PATTERN}
        and category_for_node(node) == category
    }
    retriever = SkillRetriever(store)
    plans = [
        {"arm": "sparse", "kind": "sparse"},
        {"arm": "dense_exact", "kind": "dense_exact"},
        {"arm": "hybrid_exact", "kind": "hybrid", "backend": "exact", "hops": 0},
        {"arm": "graph_exact", "kind": "hybrid", "backend": "exact", "hops": args.expand_hops},
    ]
    if hnsw_available:
        plans.extend([
            {"arm": "dense_hnsw", "kind": "dense_hnsw"},
            {"arm": "hybrid_hnsw", "kind": "hybrid", "backend": "hnsw", "hops": 0},
            {"arm": "graph_hnsw", "kind": "hybrid", "backend": "hnsw", "hops": args.expand_hops},
        ])
    rows: list[dict[str, Any]] = []
    for plan in plans:
        started = time.perf_counter()
        if plan["kind"] == "sparse":
            ranked = store.search_lexical(query, limit=args.top_k)
            hits = [SearchHit(node=node, score=score, sources={"sparse": score}) for node, score in ranked]
            seed_count, expanded_count, unresolved = len(hits), 0, []
        elif plan["kind"] == "dense_exact":
            ranked = store.search_vector(query, limit=args.top_k, vector_backend="exact")
            hits = [SearchHit(node=node, score=score, sources={"dense_exact": score}) for node, score in ranked]
            seed_count, expanded_count, unresolved = len(hits), 0, []
        else:
            response = retriever.search(
                query,
                top_k=args.top_k,
                seed_k=args.seed_k,
                expand_hops=int(plan.get("hops", 0)),
                query_mode="solve",
                vector_backend=str(plan.get("backend", "exact")),
                hnsw_path=str(args.hnsw) if plan.get("backend") == "hnsw" else None,
                hnsw_ef_search=args.hnsw_ef_search,
                hnsw_oversample=args.hnsw_oversample,
                include_inactive=False,
            )
            hits = response.hits
            seed_count, expanded_count, unresolved = response.seed_count, response.expanded_count, list(response.unresolved)
        latency_ms = (time.perf_counter() - started) * 1000
        hit_rows = [compact_hit(hit, rank, hit.node.id in relevant_ids) for rank, hit in enumerate(hits, start=1)]
        relevant_ranks = [row["rank"] for row in hit_rows if row["relevant"]]
        rows.append({
            "case_id": case.get("case_id") or f"{case.get('repository')}#{case.get('issue')}",
            "repository": case.get("repository"),
            "issue": case.get("issue"),
            "category": category,
            "query": query,
            "query_source": query_source,
            "gold_definition": "same universal problem class in training-derived catalog",
            "gold_count": len(relevant_ids),
            "arm": plan["arm"],
            "latency_ms": round(latency_ms, 3),
            "seed_count": seed_count,
            "expanded_count": expanded_count,
            "unresolved": unresolved,
            "context_tokens_proxy": context_tokens(hits),
            "hits": hit_rows,
            "first_relevant_rank": min(relevant_ranks) if relevant_ranks else None,
        })
    return rows


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for arm in sorted({str(row["arm"]) for row in rows}):
        items = [row for row in rows if row["arm"] == arm]
        ranks = [int(row["first_relevant_rank"]) for row in items if row["first_relevant_rank"] is not None]
        result[arm] = {
            "cases": len(items),
            "recall_at_k": len(ranks) / len(items) if items else 0.0,
            "mrr": statistics.mean(1.0 / rank for rank in ranks) if ranks else 0.0,
            "mean_first_relevant_rank": statistics.mean(ranks) if ranks else None,
            "mean_latency_ms": statistics.mean(float(row["latency_ms"]) for row in items) if items else None,
            "p95_latency_ms": sorted(float(row["latency_ms"]) for row in items)[max(0, int(len(items) * 0.95) - 1)] if items else None,
            "mean_context_tokens_proxy": statistics.mean(int(row["context_tokens_proxy"]) for row in items) if items else 0.0,
            "mean_seed_count": statistics.mean(int(row["seed_count"]) for row in items) if items else 0.0,
            "mean_expanded_count": statistics.mean(int(row["expanded_count"]) for row in items) if items else 0.0,
        }
    return result


def hnsw_status(store: CatalogStore, path: Path | None) -> tuple[bool, str | None]:
    if path is None or not path.exists():
        return False, "index path was not supplied or does not exist"
    try:
        store.search_vector("hnsw preflight", limit=1, vector_backend="hnsw", hnsw_path=str(path))
    except Exception as exc:  # optional dependency/index validity is environment-specific
        return False, f"{type(exc).__name__}: {exc}"
    return True, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", default="holdout_candidate")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--seed-k", type=int, default=40)
    parser.add_argument("--expand-hops", type=int, default=2)
    parser.add_argument("--hnsw-ef-search", type=int, default=64)
    parser.add_argument("--hnsw-oversample", type=int, default=4)
    args = parser.parse_args()
    if args.top_k <= 0 or args.seed_k < args.top_k or args.expand_hops < 0:
        raise ValueError("require top_k > 0, seed_k >= top_k, expand_hops >= 0")
    cases = load_cases(args.cases, args.role)
    with CatalogStore(args.db) as store:
        store.initialize()
        hnsw_available, hnsw_error = hnsw_status(store, args.hnsw)
        rows: list[dict[str, Any]] = []
        for case in cases:
            rows.extend(evaluate_case(store, case, args, hnsw_available))
        payload = {
            "schema_version": "universal-holdout-retrieval-evaluation-v1",
            "catalog": str(args.db),
            "hnsw": str(args.hnsw) if args.hnsw else None,
            "hnsw_available": hnsw_available,
            "hnsw_error": hnsw_error,
            "embedding": {"kind": "routing", "model_version": "hash-v1", "exact_is_oracle": True},
            "role": args.role,
            "cases": len(cases),
            "arms": sorted({row["arm"] for row in rows}),
            "aggregate": aggregate(rows),
            "rows": rows,
            "limitations": [
                "Labels measure category transfer, not repair correctness.",
                "HNSW is an optional acceleration cache; exact dense is the correctness oracle.",
                "context_tokens_proxy is serialized text length divided by four, not a model tokenizer.",
            ],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "aggregate": payload["aggregate"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
