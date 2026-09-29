#!/usr/bin/env python3
"""Use Codex as a bounded retrieval-parameter router, then execute locally.

The model sees holdout inputs and candidate cards from the training-only
catalog. It selects search parameters only; deterministic retrieval remains
the source of hit rankings and no plan is treated as a repair judgment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.store import CatalogStore
from run_llm_retrieval_selection import bounded_plan, candidate_pool, hnsw_status, query_for_case, fallback_plan
import run_codex_issue_episode_extraction as codex_runner


def load_cases(path: Path, role: str, max_cases: int | None) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    selected = [dict(case) for case in cases if str(case.get("role") or case.get("split")) == role]
    return selected[:max_cases] if max_cases is not None else selected


def prompt_for(request_path: str, schema_path: str, count: int) -> str:
    return f"""You are a bounded retrieval router for an evidence-grounded resolution graph.

Read the request file at {request_path}. It contains {count} holdout input queries and
candidate cards produced independently by sparse FTS and exact dense search over a
training-only catalog. Do not search for or infer any holdout solution, target patch,
target test, or repository-specific implementation. Do not decide whether a hit is a
correct repair. Return ONLY JSON matching {schema_path}.

For every case_id, choose bounded retrieval parameters only:
- vector_backend exact or hnsw (HNSW is available and exact dense is the correctness oracle);
- top_k 1..20, seed_k 1..100, expand_hops 0..3;
- hnsw_ef_search 16..512, hnsw_oversample 1..16, query_mode solve or audit;
- a short rationale based on candidate diversity and query ambiguity, not on claiming
  applicability or repair correctness.

Return exactly one plan per request case. Never use a repository path, issue number,
commit, or target-only fact as a retrieval parameter.
"""


def execute_plan(store: CatalogStore, request: dict[str, Any], raw_plan: Any, hnsw_available: bool, hnsw_path: Path | None) -> dict[str, Any]:
    fallback = fallback_plan(hnsw_available)
    plan, errors = bounded_plan(raw_plan, hnsw_available=hnsw_available)
    started = time.perf_counter()
    response = SkillRetriever(store).search(
        str(request["query"]),
        top_k=plan["top_k"],
        seed_k=plan["seed_k"],
        expand_hops=plan["expand_hops"],
        query_mode=plan["query_mode"],
        vector_backend=plan["vector_backend"],
        hnsw_path=str(hnsw_path) if plan["vector_backend"] == "hnsw" else None,
        hnsw_ef_search=plan["hnsw_ef_search"],
        hnsw_oversample=plan["hnsw_oversample"],
        include_inactive=False,
    )
    elapsed = (time.perf_counter() - started) * 1000
    return {
        "case_id": request["case_id"],
        "repository": request.get("repository"),
        "issue": request.get("issue"),
        "category": request.get("category"),
        "query": request["query"],
        "decision": "codex_llm" if isinstance(raw_plan, dict) else "fallback_missing_plan",
        "llm_plan_raw": raw_plan,
        "plan": plan,
        "guardrail_errors": errors,
        "fallback_reference": fallback,
        "retrieval_ms": round(elapsed, 3),
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
    parser.add_argument("--hnsw", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--role", default="holdout_candidate")
    parser.add_argument("--candidate-k", type=int, default=20)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=ROOT / "schemas" / "universal-retrieval-router-v1.schema.json")
    parser.add_argument("--codex", required=True)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--codex-bypass-sandbox", action="store_true")
    args = parser.parse_args()
    if args.candidate_k <= 0:
        raise ValueError("candidate-k must be positive")

    cases = load_cases(args.cases, args.role, args.max_cases)
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    schema = args.schema.expanduser().resolve()
    request_rows: list[dict[str, Any]] = []
    with CatalogStore(args.db) as store:
        store.initialize()
        hnsw_available, hnsw_error = hnsw_status(store, args.hnsw)
        for case in cases:
            query = query_for_case(case)
            request_rows.append({
                "case_id": case.get("case_id") or f"{case.get('repository')}#{case.get('issue')}",
                "repository": case.get("repository"),
                "issue": case.get("issue"),
                "category": case.get("category"),
                "query": query,
                "candidate_pool": candidate_pool(store, query, args.candidate_k),
            })
    request_path = output / "router-request.json"
    request_path.write_text(json.dumps({"cases": request_rows, "constraints": {"hnsw_available": hnsw_available, "exact_dense_is_oracle": True}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    visible_request = codex_runner._external_path(args.codex, request_path)
    visible_schema = codex_runner._external_path(args.codex, schema)
    prompt = prompt_for(visible_request, visible_schema, len(request_rows))
    (output / "prompt.txt").write_text(prompt, encoding="utf-8")
    (output / "codex-command.json").write_text(json.dumps({"executable": args.codex, "schema": str(schema), "request": str(request_path), "checkout": str(args.checkout), "timeout_seconds": args.timeout_seconds, "holdout_solution_data_sent": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    response_path = output / "router-response.json"
    codex_runner.SCHEMA = schema
    returncode = codex_runner.run_codex(
        args.codex,
        args.checkout.expanduser().resolve(),
        prompt,
        response_path,
        output / "codex-stdout.log",
        output / "codex-stderr.log",
        sandbox="read-only",
        timeout_seconds=max(1, args.timeout_seconds),
        bypass_sandbox=args.codex_bypass_sandbox,
    )
    raw_response: Any = None
    parse_errors: list[str] = []
    if response_path.exists():
        try:
            raw_response = json.loads(response_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            parse_errors.append(str(exc))
    plans = {}
    if isinstance(raw_response, dict) and isinstance(raw_response.get("plans"), list):
        plans = {str(row.get("case_id")): row for row in raw_response["plans"] if isinstance(row, dict) and row.get("case_id")}
    else:
        parse_errors.append("router response lacks plans array")

    rows: list[dict[str, Any]] = []
    with CatalogStore(args.db) as store:
        store.initialize()
        for request in request_rows:
            rows.append(execute_plan(store, request, plans.get(str(request["case_id"])), hnsw_available, args.hnsw))
    payload = {
        "schema_version": "codex-retrieval-parameter-selection-v1",
        "cases": len(request_rows),
        "codex_returncode": returncode,
        "router_response_valid_shape": not parse_errors,
        "parse_errors": parse_errors,
        "hnsw_available": hnsw_available,
        "hnsw_error": hnsw_error,
        "rows": rows,
        "limitations": [
            "Codex selected retrieval parameters only; it did not judge repair applicability.",
            "Holdout solution refs, target diffs, and target tests were not sent to the router.",
            "Exact dense remains the correctness oracle for backend comparison.",
        ],
    }
    (output / "retrieval-router-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "cases": len(rows), "returncode": returncode, "router_response_valid_shape": not parse_errors, "plans": len(plans)}, ensure_ascii=False))
    return 0 if returncode == 0 and not parse_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
