#!/usr/bin/env python3
"""Judge whether retrieved training-only Skills apply to untouched holdouts.

The holdout input is limited to the issue-facing text already present in the
manifest. Retrieval runs against the training-only catalog, then the LLM may
select exactly one returned Action, Workflow, or Pattern, or reject the whole
candidate set. The judge never receives a holdout patch, target test, commit,
or extracted holdout episode.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.retrieval import SearchHit, SkillRetriever
from arex_skill_graph.store import CatalogStore

BLOCKED_PATTERN_DECISIONS = {
    "defer",
    "deferred_by_semantic_judge",
    "reject",
    "rejected_by_semantic_judge",
}


def load_cases(path: Path, role: str, max_cases: int | None) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise TypeError("manifest must contain a cases array")
    selected = [
        dict(case)
        for case in cases
        if str(case.get("role") or case.get("split")) == role
    ]
    return selected[:max_cases] if max_cases is not None else selected


def query_for_case(case: Mapping[str, Any]) -> tuple[str, str]:
    problem = case.get("problem_class") or {}
    if isinstance(problem, Mapping):
        generic = str(problem.get("problem") or "")
        workflow = " ".join(str(item) for item in problem.get("workflow", []))
    else:
        generic, workflow = "", ""
    issue_title = str(case.get("issue_title") or case.get("title") or "")
    table_note = str(case.get("table_note") or "")
    issue_body = str(case.get("issue_body") or "")[:1200]
    query = " ".join(
        part for part in (issue_title, table_note, issue_body, generic, workflow) if part
    ).strip()
    if issue_title:
        source = "issue+class"
    elif table_note:
        source = "table-note+class" if generic or workflow else "table-note"
    else:
        source = "class-only-unverified"
    return query, source


def category_for_hit(hit: SearchHit) -> str:
    for container in (hit.node.facets, hit.node.payload):
        if isinstance(container, Mapping):
            value = container.get("problem_class") or container.get("category")
            if value:
                return str(value)
    return ""


def compact_hit(hit: SearchHit, rank: int) -> dict[str, Any]:
    payload = hit.node.payload if isinstance(hit.node.payload, Mapping) else {}
    return {
        "rank": rank,
        "id": hit.node.id,
        "node_type": hit.node.node_type.value,
        "title": hit.node.title,
        "summary": hit.node.summary,
        "repository": hit.node.repository,
        "category": category_for_hit(hit),
        "lifecycle": hit.node.lifecycle,
        "promotion_status": payload.get("promotion_status") or payload.get("decision"),
        "score": hit.score,
        "sources": dict(hit.sources),
        "trace": list(hit.trace),
    }


def split_judge_hits(hits: list[SearchHit]) -> tuple[list[SearchHit], list[dict[str, Any]]]:
    eligible: list[SearchHit] = []
    excluded: list[dict[str, Any]] = []
    for rank, hit in enumerate(hits, start=1):
        payload = hit.node.payload if isinstance(hit.node.payload, Mapping) else {}
        decision = str(payload.get("promotion_status") or payload.get("decision") or "")
        if hit.node.node_type.value == "pattern" and decision in BLOCKED_PATTERN_DECISIONS:
            excluded.append({
                "rank": rank,
                "id": hit.node.id,
                "title": hit.node.title,
                "decision": decision,
                "reason": "semantic Pattern decision is not eligible for guided use",
            })
        else:
            eligible.append(hit)
    return eligible, excluded


def evaluate_case(
    store: CatalogStore,
    case: Mapping[str, Any],
    args: argparse.Namespace,
    governance: LLMGovernanceAdapter,
) -> dict[str, Any]:
    query, query_source = query_for_case(case)
    if not query:
        raise ValueError(f"holdout case has no usable query text: {case.get('case_id')}")
    started = time.perf_counter()
    response = SkillRetriever(store).search(
        query,
        top_k=args.top_k,
        seed_k=args.seed_k,
        expand_hops=args.expand_hops,
        query_mode="solve",
        vector_backend=args.vector_backend,
        hnsw_path=str(args.hnsw) if args.vector_backend == "hnsw" else None,
        hnsw_ef_search=args.hnsw_ef_search,
        hnsw_oversample=args.hnsw_oversample,
        include_inactive=False,
    )
    retrieval_ms = (time.perf_counter() - started) * 1000
    judge_hits, judge_excluded_hits = split_judge_hits(response.hits)
    judge_started = time.perf_counter()
    if judge_hits:
        judgment = dict(governance.judge_retrieval_use(query, judge_hits))
    else:
        judgment = {
            "selected_skill_id": None,
            "applicable": False,
            "confidence": 1.0,
            "rationale": "No retrieved candidate was eligible for guided use after lifecycle and semantic-decision gates.",
            "missing_preconditions": [],
        }
    judge_ms = (time.perf_counter() - judge_started) * 1000

    selected_id = judgment.get("selected_skill_id")
    selected_rank = None
    selected_hit = None
    for rank, hit in enumerate(response.hits, start=1):
        if hit.node.id == selected_id:
            selected_rank = rank
            selected_hit = hit
            break
    selected_category = category_for_hit(selected_hit) if selected_hit is not None else ""
    selected_payload = (
        selected_hit.node.payload
        if selected_hit is not None and isinstance(selected_hit.node.payload, Mapping)
        else {}
    )
    category = str(case.get("category") or "")
    return {
        "case_id": case.get("case_id") or f"{case.get('repository')}#{case.get('issue')}",
        "repository": case.get("repository"),
        "issue": case.get("issue"),
        "category": category,
        "query": query,
        "query_source": query_source,
        "holdout_solution_data_sent": False,
        "retrieval_ms": round(retrieval_ms, 3),
        "judge_ms": round(judge_ms, 3),
        "seed_count": response.seed_count,
        "expanded_count": response.expanded_count,
        "unresolved": list(response.unresolved),
        "hits": [compact_hit(hit, rank) for rank, hit in enumerate(response.hits, start=1)],
        "judge_candidate_ids": [hit.node.id for hit in judge_hits],
        "judge_excluded_hits": judge_excluded_hits,
        "judgment": judgment,
        "selected_rank": selected_rank,
        "selected_category": selected_category or None,
        "selected_category_matches_holdout_proxy": bool(
            selected_hit is not None and category and selected_category == category
        ),
        "selected_node_type": selected_hit.node.node_type.value if selected_hit is not None else None,
        "selected_lifecycle": selected_hit.node.lifecycle if selected_hit is not None else None,
        "selected_promotion_status": (
            selected_payload.get("promotion_status") or selected_payload.get("decision")
            if selected_hit is not None
            else None
        ),
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    applicable = [row for row in rows if row["judgment"].get("applicable") is True]
    selected_types = Counter(
        str(row["selected_node_type"]) for row in applicable if row["selected_node_type"]
    )
    selected_statuses = Counter(
        str(row["selected_promotion_status"])
        for row in applicable
        if row["selected_promotion_status"]
    )
    return {
        "cases": len(rows),
        "applicable": len(applicable),
        "not_applicable": len(rows) - len(applicable),
        "selected_category_matches_holdout_proxy": sum(
            bool(row["selected_category_matches_holdout_proxy"]) for row in rows
        ),
        "selected_node_types": dict(sorted(selected_types.items())),
        "selected_promotion_statuses": dict(sorted(selected_statuses.items())),
        "judge_excluded_hits": sum(len(row["judge_excluded_hits"]) for row in rows),
        "mean_selected_rank": (
            statistics.mean(int(row["selected_rank"]) for row in applicable if row["selected_rank"])
            if any(row["selected_rank"] for row in applicable)
            else None
        ),
        "mean_retrieval_ms": statistics.mean(float(row["retrieval_ms"]) for row in rows),
        "mean_judge_ms": statistics.mean(float(row["judge_ms"]) for row in rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", default="holdout_candidate")
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--seed-k", type=int, default=40)
    parser.add_argument("--expand-hops", type=int, default=1)
    parser.add_argument("--vector-backend", choices=("exact", "hnsw"), default="exact")
    parser.add_argument("--hnsw-ef-search", type=int, default=64)
    parser.add_argument("--hnsw-oversample", type=int, default=4)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--max-output-tokens", type=int, default=1600)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()
    if not args.api_key:
        raise ValueError("--api-key or OPENAI_API_KEY is required")
    if args.top_k <= 0 or args.seed_k < args.top_k or args.expand_hops < 0:
        raise ValueError("require top_k > 0, seed_k >= top_k, expand_hops >= 0")
    if args.vector_backend == "hnsw" and (args.hnsw is None or not args.hnsw.exists()):
        raise ValueError("--hnsw must exist when vector-backend=hnsw")

    cases = load_cases(args.cases, args.role, args.max_cases)
    transport = OpenAICompatibleTransport(OpenAICompatibleConfig(
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        timeout_seconds=args.timeout_seconds,
        max_output_tokens=args.max_output_tokens,
        retries=args.retries,
    ))
    rows: list[dict[str, Any]] = []
    with CatalogStore(args.db) as store:
        store.initialize()
        for case in cases:
            governance = LLMGovernanceAdapter(
                transport,
                GovernanceContext(
                    repository=str(case.get("repository") or "holdout"),
                    model=args.model,
                    prompt_version="holdout-retrieval-applicability-v1",
                    code_context={
                        "experiment": "run_holdout_retrieval_applicability",
                        "training_only_catalog": True,
                        "holdout_solution_data_sent": False,
                    },
                ),
            )
            rows.append(evaluate_case(store, case, args, governance))

    payload = {
        "schema_version": "holdout-retrieval-applicability-v1",
        "model": args.model,
        "base_url": args.base_url,
        "training_only_catalog": True,
        "holdout_solution_data_sent": False,
        "retrieval": {
            "vector_backend": args.vector_backend,
            "top_k": args.top_k,
            "seed_k": args.seed_k,
            "expand_hops": args.expand_hops,
            "hnsw": str(args.hnsw) if args.hnsw else None,
        },
        "summary": summarize(rows),
        "rows": rows,
        "calls": list(transport.calls),
        "transcripts": list(transport.transcripts),
        "limitations": [
            "The judge sees issue-facing holdout text, not the hidden fix or target tests.",
            "Category agreement is a diagnostic proxy, not proof that the selected Skill repairs the holdout.",
            "A selected candidate remains guidance only until a separate agent run and executable oracle validate it.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
