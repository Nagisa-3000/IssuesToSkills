from __future__ import annotations

"""Small deterministic retrieval pilot for exact-vs-HNSW and graph expansion.

This is an offline retrieval/context study, not an agent success-rate or LLM
cost experiment.  Token figures are context-size proxies (serialized node
characters / 4), useful for deciding what to measure with a real runtime.
"""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import statistics
import time

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import NodeType
from arex_skill_graph.store import CatalogStore


@dataclass
class CaseResult:
    query: str
    expected_id: str
    expected_repository: str | None
    backend: str
    mode: str
    expected_rank: int | None
    hit_ids: list[str]
    hit_repositories: list[str | None]
    seed_count: int
    expanded_count: int
    context_tokens_proxy: int
    latency_ms: float


def context_tokens(response) -> int:
    # Conservative, dependency-free approximation; real runtime must use the
    # model tokenizer and separately record prompt/input/output tokens.
    text = "\n".join(
        f"{hit.node.node_type.value} {hit.node.id} {hit.node.title} {hit.node.summary}"
        for hit in response.hits
    )
    return max(1, (len(text) + 3) // 4) if text else 0


def run_case(store, query: str, expected_id: str, expected_repository: str | None, backend: str, mode: str, index: Path | None):
    if mode == "flat_skill":
        expand_hops = 0
        top_k = 8
    elif mode == "graph_skill":
        expand_hops = 2
        top_k = 8
    elif mode == "cross_repository_graph_skill":
        expand_hops = 2
        top_k = 8
    else:
        raise ValueError(mode)
    started = time.perf_counter()
    response = SkillRetriever(store).search(
        query,
        top_k=top_k,
        seed_k=20,
        expand_hops=expand_hops,
        vector_backend=backend,
        hnsw_path=str(index) if index else None,
        hnsw_ef_search=128,
        hnsw_oversample=8,
    )
    elapsed = (time.perf_counter() - started) * 1000
    hit_ids = [hit.node.id for hit in response.hits]
    rank = hit_ids.index(expected_id) + 1 if expected_id in hit_ids else None
    return CaseResult(
        query=query,
        expected_id=expected_id,
        expected_repository=expected_repository,
        backend=backend,
        mode=mode,
        expected_rank=rank,
        hit_ids=hit_ids,
        hit_repositories=[hit.node.repository for hit in response.hits],
        seed_count=response.seed_count,
        expanded_count=response.expanded_count,
        context_tokens_proxy=context_tokens(response),
        latency_ms=elapsed,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", type=int, default=12)
    args = parser.parse_args()

    with CatalogStore(args.db) as store:
        store.initialize()
        store.build_hnsw_index(args.index, ef_search=128)
        candidates = store.list_nodes(node_types=[NodeType.ACTION], limit=args.cases)
        cases = [(node.title + " " + node.summary, node.id, node.repository) for node in candidates]
        results: list[CaseResult] = []
        for backend in ("exact", "hnsw"):
            for mode in ("flat_skill", "graph_skill", "cross_repository_graph_skill"):
                for query, expected_id, repository in cases:
                    results.append(run_case(store, query, expected_id, repository, backend, mode, args.index))

    payload = {
        "kind": "offline-retrieval-context-pilot",
        "db": str(args.db),
        "index": str(args.index),
        "cases": len(cases),
        "results": [asdict(result) for result in results],
        "summary": {},
        "limitations": [
            "No authenticated model runtime was used.",
            "success rate, model tokens, wall time, and dollar cost are not measured.",
            "context_tokens_proxy is serialized text length divided by four, not a model tokenizer.",
            "graph_skill and cross_repository_graph_skill currently share the same bounded graph implementation; repository-aware Pattern routing is not enabled in this pilot.",
        ],
    }
    for backend in ("exact", "hnsw"):
        for mode in ("flat_skill", "graph_skill", "cross_repository_graph_skill"):
            subset = [r for r in results if r.backend == backend and r.mode == mode]
            ranks = [r.expected_rank for r in subset if r.expected_rank is not None]
            payload["summary"][f"{backend}:{mode}"] = {
                "recall_at_8": len(ranks) / len(subset) if subset else 0.0,
                "mean_expected_rank": statistics.mean(ranks) if ranks else None,
                "mean_latency_ms": statistics.mean(r.latency_ms for r in subset) if subset else None,
                "mean_context_tokens_proxy": statistics.mean(r.context_tokens_proxy for r in subset) if subset else None,
                "mean_expanded_count": statistics.mean(r.expanded_count for r in subset) if subset else None,
            }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
