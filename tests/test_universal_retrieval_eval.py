from __future__ import annotations

import importlib.util
from argparse import Namespace
from pathlib import Path

import pytest

from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "run_universal_retrieval_eval.py"
SPEC = importlib.util.spec_from_file_location("universal_retrieval_eval", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_query_uses_table_note_when_holdout_has_no_issue_payload() -> None:
    query, source = MODULE.query_for_case({
        "table_note": "compaction does not reserve output-token space",
        "category": "context-budget-and-compaction",
    })

    assert query == "compaction does not reserve output-token space"
    assert source == "table-note"


def test_mrr_counts_missed_cases_as_zero() -> None:
    result = MODULE.aggregate([
        {
            "arm": "dense_exact",
            "first_relevant_rank": 2,
            "latency_ms": 1.0,
            "context_tokens_proxy": 10,
            "seed_count": 2,
            "expanded_count": 0,
        },
        {
            "arm": "dense_exact",
            "first_relevant_rank": None,
            "latency_ms": 1.0,
            "context_tokens_proxy": 10,
            "seed_count": 2,
            "expanded_count": 0,
        },
    ])

    assert result["dense_exact"]["recall_at_k"] == 0.5
    assert result["dense_exact"]["mrr"] == 0.25
    assert result["dense_exact"]["mean_first_relevant_rank"] == 2


def test_category_transfer_metrics_have_sparse_dense_hybrid_and_graph_arms(tmp_path: Path) -> None:
    db = tmp_path / "catalog.sqlite"
    with CatalogStore(db) as store:
        store.initialize()
        store.upsert_node(Node(
            id="action:state",
            node_type=NodeType.ACTION,
            title="Reconcile authoritative state",
            summary="Restore state after a boundary and validate replay.",
            facets={"problem_class": "state-continuity-reconstruction"},
        ))
        store.upsert_node(Node(
            id="workflow:state",
            node_type=NodeType.WORKFLOW,
            title="Restore and validate state",
            summary="Reconcile then validate a round trip.",
            facets={"problem_class": "state-continuity-reconstruction"},
        ))
        case = {
            "case_id": "org/holdout#1",
            "repository": "org/holdout",
            "issue": 1,
            "category": "state-continuity-reconstruction",
            "problem_class": {"problem": "preserve authoritative state", "workflow": ["reconcile", "validate"]},
        }
        args = Namespace(
            top_k=3,
            seed_k=5,
            expand_hops=1,
            hnsw_ef_search=64,
            hnsw_oversample=4,
            hnsw=None,
        )
        rows = MODULE.evaluate_case(store, case, args, False)
    assert {row["arm"] for row in rows} == {"sparse", "dense_exact", "hybrid_exact", "graph_exact"}
    assert any(row["first_relevant_rank"] is not None for row in rows)
    assert all(row["gold_same_repository_count"] == 0 for row in rows)


def test_dense_hnsw_arm_executes_vector_only_search(tmp_path: Path) -> None:
    pytest.importorskip("hnswlib")
    db = tmp_path / "catalog.sqlite"
    index = tmp_path / "catalog.hnsw"
    with CatalogStore(db) as store:
        store.initialize()
        for number in range(8):
            store.upsert_node(Node(
                id=f"action:{number}",
                node_type=NodeType.ACTION,
                title=f"Retry a prematurely closed stream {number}",
                summary="Classify a truncated stream and retry within policy.",
                facets={"problem_class": "failure-recovery-and-streaming"},
            ))
        store.build_hnsw_index(index)
        case = {
            "case_id": "org/holdout#2",
            "repository": "org/holdout",
            "issue": 2,
            "category": "failure-recovery-and-streaming",
            "table_note": "proxy premature stream ending is not recognized, so no retry occurs",
        }
        args = Namespace(
            top_k=3,
            seed_k=5,
            expand_hops=1,
            hnsw_ef_search=64,
            hnsw_oversample=4,
            hnsw=index,
        )
        rows = MODULE.evaluate_case(store, case, args, True)

    dense_hnsw = next(row for row in rows if row["arm"] == "dense_hnsw")
    assert dense_hnsw["seed_count"] == 3
    assert dense_hnsw["expanded_count"] == 0
    assert all(set(hit["sources"]) == {"dense_hnsw"} for hit in dense_hnsw["hits"])

