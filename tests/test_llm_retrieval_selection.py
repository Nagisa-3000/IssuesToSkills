from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "run_llm_retrieval_selection.py"
SPEC = importlib.util.spec_from_file_location("llm_retrieval_selection", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_query_uses_table_note_when_issue_title_and_body_are_absent() -> None:
    assert MODULE.query_for_case({
        "table_note": "proxy premature stream ending is not recognized, so no retry occurs",
    }) == "proxy premature stream ending is not recognized, so no retry occurs"


def test_router_plan_is_bounded_and_hnsw_is_not_selected_when_unavailable() -> None:
    plan, errors = MODULE.bounded_plan({
        "vector_backend": "hnsw",
        "query_mode": "solve",
        "top_k": 999,
        "seed_k": 0,
        "expand_hops": 99,
        "hnsw_ef_search": 1,
        "hnsw_oversample": 99,
        "rationale": "bounded decision",
    }, hnsw_available=False)
    assert plan["vector_backend"] == "exact"
    assert plan["top_k"] == 20
    assert plan["seed_k"] == 20
    assert plan["expand_hops"] == 3
    assert plan["hnsw_ef_search"] == 16
    assert plan["hnsw_oversample"] == 16
    assert errors

