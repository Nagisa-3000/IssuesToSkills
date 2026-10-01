#!/usr/bin/env python3
"""Let an LLM choose bounded retrieval parameters, then execute the plan.

The model is a router, not the source of truth for graph membership.  It sees
the query and a candidate pool produced by independent sparse/dense searches,
chooses a bounded plan, and the deterministic retriever executes that plan.
Without an API key the script records an explicit ``unavailable`` decision and
uses a fixed fallback; it never silently presents the fallback as an LLM win.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import NodeType
from arex_skill_graph.store import CatalogStore

PLAN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "vector_backend", "top_k", "seed_k", "expand_hops", "hnsw_ef_search",
        "hnsw_oversample", "query_mode", "rationale",
    ],
    "properties": {
        "vector_backend": {"enum": ["exact", "hnsw"]},
        "top_k": {"type": "integer", "minimum": 1, "maximum": 20},
        "seed_k": {"type": "integer", "minimum": 1, "maximum": 100},
        "expand_hops": {"type": "integer", "minimum": 0, "maximum": 3},
        "hnsw_ef_search": {"type": "integer", "minimum": 16, "maximum": 512},
        "hnsw_oversample": {"type": "integer", "minimum": 1, "maximum": 16},
        "query_mode": {"enum": ["solve", "audit"]},
        "rationale": {"type": "string"},
    },
}


def cases_from_manifest(path: Path, role: str) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise TypeError("manifest must contain a cases array")
    return [dict(case) for case in cases if str(case.get("role") or case.get("split")) == role]


def query_for_case(case: dict[str, Any]) -> str:
    problem = case.get("problem_class") or {}
    generic = str(problem.get("problem") or "") if isinstance(problem, dict) else ""
    workflow = " ".join(str(item) for item in problem.get("workflow", [])) if isinstance(problem, dict) else ""
    return " ".join(
        part for part in (
            str(case.get("issue_title") or case.get("title") or ""),
            str(case.get("table_note") or ""),
            str(case.get("issue_body") or "")[:1200],
            generic,
            workflow,
        ) if part
    ).strip()


def candidate_pool(store: CatalogStore, query: str, limit: int) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for source, ranked in (
        ("sparse", store.search_lexical(query, limit=limit)),
        ("dense_exact", store.search_vector(query, limit=limit, vector_backend="exact")),
    ):
        for rank, (node, score) in enumerate(ranked, start=1):
            if node.node_type not in {NodeType.ACTION, NodeType.WORKFLOW, NodeType.PATTERN}:
                continue
            row = by_id.setdefault(node.id, {
                "id": node.id,
                "node_type": node.node_type.value,
                "title": node.title,
                "summary": node.summary,
                "repository": node.repository,
                "facets": node.facets,
                "sources": {},
            })
            row["sources"][source] = {"rank": rank, "score": score}
    return sorted(by_id.values(), key=lambda row: (-len(row["sources"]), row["id"]))[:limit]


def fallback_plan(hnsw_available: bool) -> dict[str, Any]:
    return {
        "vector_backend": "hnsw" if hnsw_available else "exact",
        "top_k": 8,
        "seed_k": 40,
        "expand_hops": 2,
        "hnsw_ef_search": 64,
        "hnsw_oversample": 4,
        "query_mode": "solve",
        "rationale": "deterministic fallback; no LLM decision was available",
    }


def hnsw_status(store: CatalogStore, path: Path | None) -> tuple[bool, str | None]:
    if path is None or not path.exists():
        return False, "index path was not supplied or does not exist"
    try:
        store.search_vector("hnsw preflight", limit=1, vector_backend="hnsw", hnsw_path=str(path))
    except Exception as exc:  # noqa: BLE001 - optional backend/index failures are reported as data
        return False, f"{type(exc).__name__}: {exc}"
    return True, None


def bounded_plan(value: Any, *, hnsw_available: bool) -> tuple[dict[str, Any], list[str]]:
    fallback = fallback_plan(hnsw_available)
    if not isinstance(value, dict):
        return fallback, ["LLM response was not an object"]
    errors: list[str] = []
    plan = dict(fallback)
    allowed_values = {
        "vector_backend": {"exact", "hnsw"},
        "query_mode": {"solve", "audit"},
    }
    for key in ("vector_backend", "query_mode"):
        if value.get(key) in allowed_values[key]:
            plan[key] = value[key]
        else:
            errors.append(f"invalid {key}")
    if not hnsw_available and plan["vector_backend"] == "hnsw":
        errors.append("LLM selected hnsw but no HNSW index is available")
        plan["vector_backend"] = "exact"
    bounds = {
        "top_k": (1, 20),
        "seed_k": (1, 100),
        "expand_hops": (0, 3),
        "hnsw_ef_search": (16, 512),
        "hnsw_oversample": (1, 16),
    }
    for key, (lower, upper) in bounds.items():
        try:
            number = int(value.get(key, fallback[key]))
        except (TypeError, ValueError):
            errors.append(f"invalid {key}")
            number = int(fallback[key])
        if not lower <= number <= upper:
            errors.append(f"out-of-range {key}")
            number = min(upper, max(lower, number))
        plan[key] = number
    if plan["seed_k"] < plan["top_k"]:
        errors.append("seed_k was below top_k; clamped to top_k")
        plan["seed_k"] = plan["top_k"]
    rationale = value.get("rationale")
    if isinstance(rationale, str) and rationale.strip():
        plan["rationale"] = rationale.strip()
    else:
        errors.append("missing rationale")
    return plan, errors


def run_case(store: CatalogStore, case: dict[str, Any], args: argparse.Namespace, transport: Any, hnsw_available: bool) -> dict[str, Any]:
    query = query_for_case(case)
    candidates = candidate_pool(store, query, args.candidate_k)
    fallback = fallback_plan(hnsw_available)
    decision = "fallback_no_api_key" if transport is None else "llm"
    llm_result: dict[str, Any] | None = None
    llm_error: str | None = None
    if transport is not None:
        try:
            llm_result = dict(transport.complete(
                system=(
                    "You are a retrieval router for an evidence-grounded resolution graph. "
                    "Choose only bounded retrieval parameters. Do not claim a candidate is a "
                    "correct repair; use the candidate pool only to select search breadth, "
                    "graph expansion, and exact versus HNSW backend. Return JSON only."
                ),
                user=json.dumps({
                    "query": query,
                    "problem_class": case.get("category"),
                    "candidate_pool": candidates,
                    "constraints": {
                        "hnsw_available": hnsw_available,
                        "exact_dense_is_correctness_oracle": True,
                        "candidate_pool_is_not_ground_truth": True,
                    },
                }, ensure_ascii=False),
                response_schema=PLAN_SCHEMA,
            ))
        except Exception as exc:  # noqa: BLE001 - transport failures trigger an explicit fallback
            decision = "fallback_llm_error"
            llm_error = f"{type(exc).__name__}: {exc}"
    plan, guardrail_errors = bounded_plan(llm_result if llm_result is not None else fallback, hnsw_available=hnsw_available)
    started = time.perf_counter()
    response = SkillRetriever(store).search(
        query,
        top_k=plan["top_k"],
        seed_k=plan["seed_k"],
        expand_hops=plan["expand_hops"],
        query_mode=plan["query_mode"],
        vector_backend=plan["vector_backend"],
        hnsw_path=str(args.hnsw) if plan["vector_backend"] == "hnsw" else None,
        hnsw_ef_search=plan["hnsw_ef_search"],
        hnsw_oversample=plan["hnsw_oversample"],
        include_inactive=False,
    )
    retrieval_ms = (time.perf_counter() - started) * 1000
    return {
        "case_id": case.get("case_id") or f"{case.get('repository')}#{case.get('issue')}",
        "repository": case.get("repository"),
        "issue": case.get("issue"),
        "category": case.get("category"),
        "query": query,
        "decision": decision,
        "llm_error": llm_error,
        "llm_plan_raw": llm_result,
        "plan": plan,
        "guardrail_errors": guardrail_errors,
        "candidate_pool": candidates,
        "retrieval_ms": round(retrieval_ms, 3),
        "seed_count": response.seed_count,
        "expanded_count": response.expanded_count,
        "unresolved": response.unresolved,
        "hits": [
            {
                "rank": rank,
                "id": hit.node.id,
                "node_type": hit.node.node_type.value,
                "title": hit.node.title,
                "repository": hit.node.repository,
                "score": hit.score,
                "sources": dict(hit.sources),
                "trace": list(hit.trace),
            }
            for rank, hit in enumerate(response.hits, start=1)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--role", default="holdout_candidate")
    parser.add_argument("--candidate-k", type=int, default=20)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    args = parser.parse_args()
    if args.candidate_k <= 0:
        raise ValueError("candidate-k must be positive")
    cases = cases_from_manifest(args.cases, args.role)
    transport = None
    if args.api_key:
        transport = OpenAICompatibleTransport(OpenAICompatibleConfig(
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
            timeout_seconds=180,
            max_output_tokens=1200,
            retries=2,
        ))
    with CatalogStore(args.db) as store:
        store.initialize()
        hnsw_available, hnsw_error = hnsw_status(store, args.hnsw)
        rows = [run_case(store, case, args, transport, hnsw_available) for case in cases]
        payload = {
            "schema_version": "llm-retrieval-parameter-selection-v1",
            "cases": len(cases),
            "model": args.model if transport is not None else None,
            "llm_available": transport is not None,
            "hnsw_available": hnsw_available,
            "hnsw_error": hnsw_error,
            "rows": rows,
            "calls": transport.calls if transport is not None else [],
            "transcripts": transport.transcripts if transport is not None else [],
            "limitations": [
                "The LLM chooses retrieval parameters; applicability and repair correctness require the separate evaluator.",
                "Fallback rows are not LLM evidence.",
            ],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "llm_available": payload["llm_available"], "calls": len(payload["calls"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
