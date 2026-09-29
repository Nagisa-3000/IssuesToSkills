from __future__ import annotations

import importlib.util
from argparse import Namespace
from pathlib import Path

from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "run_universal_retrieval_eval.py"
SPEC = importlib.util.spec_from_file_location("universal_retrieval_eval", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


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

