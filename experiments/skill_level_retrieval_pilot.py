from __future__ import annotations

"""Level-aware retrieval pilot on an extracted Atomic/Workflow/Pattern catalog.

This is intentionally an offline retrieval experiment.  It compares lexical
BM25, exact hash embeddings, HNSW, and BM25+vector graph retrieval without
calling an LLM in the query path.  The catalog is tiny, so results are a
sanity check rather than a generalization claim.
"""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import statistics
import time

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore


LEVELS = (NodeType.ATOMIC, NodeType.WORKFLOW, NodeType.PATTERN)


@dataclass(frozen=True)
class QueryCase:
    case_id: str
    level: str
    query: str
    expected_id: str


@dataclass
class Result:
    case_id: str
    level: str
    backend: str
    mode: str
    expected_id: str
    expected_rank: int | None
    hit_ids: list[str]
    same_level_hits: int
    seed_count: int
    expanded_count: int
    context_tokens_proxy: int
    latency_ms: float


def level_from_id(node_id: str) -> str:
    return node_id.split(":", 1)[0]


def make_cases(nodes: list[Node]) -> list[QueryCase]:
    cases: list[QueryCase] = []
    for node in nodes:
        # Prefixes are evidence-derived case namespaces in this pilot.  Do not
        # use the ID as the query: that would measure identifier matching.
        prefix = node.id.split(":", 1)[0]
        query = f"{node.title}. {node.summary}"
        cases.append(QueryCase(f"{prefix}:{node.node_type.value}", node.node_type.value, query, node.id))
    return cases


def token_proxy(ids: list[str], nodes: dict[str, Node]) -> int:
    text = "\n".join(
        f"{nodes[item].node_type.value} {nodes[item].title} {nodes[item].summary}"
        for item in ids if item in nodes
    )
    return (len(text) + 3) // 4 if text else 0


def result_for(store: CatalogStore, case: QueryCase, backend: str, mode: str, index: Path | None, nodes: dict[str, Node]) -> Result:
    started = time.perf_counter()
    if mode == "bm25":
        hits = store.search_lexical(case.query, node_types=[NodeType(case.level)], limit=8)
        hit_ids = [node.id for node, _ in hits]
        seed_count = len(hit_ids)
        expanded_count = 0
    elif mode == "vector":
        hits = store.search_vector(case.query, node_types=[NodeType(case.level)], limit=8, vector_backend=backend, hnsw_path=index)
        hit_ids = [node.id for node, _ in hits]
        seed_count = len(hit_ids)
        expanded_count = 0
    elif mode in {"hybrid", "graph"}:
        response = SkillRetriever(store).search(
            case.query,
            node_types=[NodeType(case.level)],
            top_k=8,
            seed_k=12,
            expand_hops=2 if mode == "graph" else 0,
            vector_backend=backend,
            hnsw_path=str(index) if index else None,
            hnsw_ef_search=128,
            hnsw_oversample=8,
            # Graph neighbors are still traversed, but only same-level peers
            # are returned as candidates for the level-aware gold ranking.
            same_level_only=True,
        )
        hit_ids = [hit.node.id for hit in response.hits]
        seed_count = response.seed_count
        expanded_count = response.expanded_count
    else:
        raise ValueError(mode)
    elapsed = (time.perf_counter() - started) * 1000
    rank = hit_ids.index(case.expected_id) + 1 if case.expected_id in hit_ids else None
    same_level_hits = sum(nodes[item].node_type.value == case.level for item in hit_ids if item in nodes)
    return Result(case.case_id, case.level, backend, mode, case.expected_id, rank, hit_ids, same_level_hits, seed_count, expanded_count, token_proxy(hit_ids, nodes), elapsed)


def _metrics(subset: list[Result]) -> dict[str, float | int | None]:
    ranks = [r.expected_rank for r in subset if r.expected_rank is not None]
    return {
        "cases": len(subset),
        "recall_at_8": len(ranks) / len(subset) if subset else 0.0,
        "mrr": statistics.mean((1 / rank) for rank in ranks) if ranks else 0.0,
        "mean_expected_rank": statistics.mean(ranks) if ranks else None,
        "mean_latency_ms": statistics.mean(r.latency_ms for r in subset) if subset else 0.0,
        "mean_context_tokens_proxy": statistics.mean(r.context_tokens_proxy for r in subset) if subset else 0.0,
        "mean_same_level_hits": statistics.mean(r.same_level_hits for r in subset) if subset else 0.0,
        "mean_seed_count": statistics.mean(r.seed_count for r in subset) if subset else 0.0,
        "mean_expanded_count": statistics.mean(r.expanded_count for r in subset) if subset else 0.0,
    }


def summarize(results: list[Result]) -> dict[str, dict[str, float | int | None]]:
    return {
        f"{backend}:{mode}": _metrics(
            [r for r in results if r.backend == backend and r.mode == mode]
        )
        for backend in ("exact", "hnsw")
        for mode in ("bm25", "vector", "hybrid", "graph")
    }


def summarize_by_level(results: list[Result]) -> dict[str, dict[str, float | int | None]]:
    return {
        f"{level}:{backend}:{mode}": _metrics(
            [
                r for r in results
                if r.level == level and r.backend == backend and r.mode == mode
            ]
        )
        for level in ("atomic", "workflow", "pattern")
        for backend in ("exact", "hnsw")
        for mode in ("bm25", "vector", "hybrid", "graph")
    }


def diagnostics(results: list[Result]) -> dict[str, object]:
    seed_level_ok = all(
        r.mode in {"bm25", "vector"}
        or r.same_level_hits <= r.seed_count
        for r in results
    )
    graph = [r for r in results if r.mode == "graph"]
    hybrid = [r for r in results if r.mode == "hybrid"]
    graph_tokens = statistics.mean(r.context_tokens_proxy for r in graph) if graph else 0.0
    hybrid_tokens = statistics.mean(r.context_tokens_proxy for r in hybrid) if hybrid else 0.0
    graph_expansion = statistics.mean(r.expanded_count for r in graph) if graph else 0.0
    return {
        "seed_level_filter_holds_for_flat_channels": seed_level_ok,
        "graph_expansion_mean_count": graph_expansion,
        "graph_vs_hybrid_context_token_proxy_delta": graph_tokens - hybrid_tokens,
        "graph_expansion_increases_context_token_proxy": graph_tokens > hybrid_tokens,
        "llm_judge_not_called": True,
        "candidate_budget_is_top_k": 8,
        "interpretation": "Graph mode is an expansion/context experiment; its self-retrieval rank is not an end-task success metric.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with CatalogStore(args.db) as store:
        store.initialize()
        store.build_hnsw_index(args.index, ef_search=128)
        nodes = {node.id: node for node in store.list_nodes(node_types=list(LEVELS))}
        cases = make_cases(list(nodes.values()))
        results: list[Result] = []
        for backend in ("exact", "hnsw"):
            for mode in ("bm25", "vector", "hybrid", "graph"):
                for case in cases:
                    results.append(result_for(store, case, backend, mode, args.index, nodes))

    payload = {
        "kind": "level-aware-skill-retrieval-pilot",
        "db": str(args.db),
        "index": str(args.index),
        "cases": [asdict(case) for case in cases],
        "summary": summarize(results),
        "summary_by_level": summarize_by_level(results),
        "diagnostics": diagnostics(results),
        "results": [asdict(result) for result in results],
        "limitations": [
            "The catalog contains only four evidence-grounded cases and one Pattern.",
            "Expected targets are node-level self-retrieval, not end-task success.",
            "Token counts are serialized title/summary characters divided by four, not model tokenizer counts.",
            "No LLM is called during retrieval; semantic judging remains an admission/offline operation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
