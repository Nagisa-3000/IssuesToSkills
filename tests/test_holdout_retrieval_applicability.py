from __future__ import annotations

import importlib.util
import json
from argparse import Namespace
from pathlib import Path

from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "run_holdout_retrieval_applicability.py"
SPEC = importlib.util.spec_from_file_location("holdout_retrieval_applicability", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FirstCandidateTransport:
    def complete(self, *, system: str, user: str, response_schema: dict) -> dict:
        del system, response_schema
        payload = json.loads(user)["payload"]
        selected = payload["candidates"][0]["skill_id"]
        return {
            "selected_skill_id": selected,
            "applicable": True,
            "confidence": 0.9,
            "rationale": "The first candidate has the requested state transition.",
            "missing_preconditions": [],
        }


def test_applicability_case_uses_table_note_and_records_selected_metadata(tmp_path: Path) -> None:
    db = tmp_path / "catalog.sqlite"
    with CatalogStore(db) as store:
        store.initialize()
        store.upsert_node(Node(
            id="pattern:deferred",
            node_type=NodeType.PATTERN,
            title="Generic resume pattern",
            summary="A deferred abstraction about restoring state.",
            facets={"problem_class": "state-continuity-and-resume"},
            payload={"promotion_status": "deferred_by_semantic_judge"},
        ))
        store.upsert_node(Node(
            id="workflow:resume",
            node_type=NodeType.WORKFLOW,
            title="Preserve caller-owned state during resume",
            summary="Scope restored state to the selected caller context.",
            facets={"problem_class": "state-continuity-and-resume"},
            payload={"when_to_use": ["resume crosses a persisted-state boundary"]},
        ))
        case = {
            "case_id": "org/holdout#1",
            "repository": "org/holdout",
            "issue": 1,
            "category": "state-continuity-and-resume",
            "table_note": "resume mixes a sibling worktree session",
        }
        args = Namespace(
            top_k=4,
            seed_k=8,
            expand_hops=0,
            vector_backend="exact",
            hnsw=None,
            hnsw_ef_search=64,
            hnsw_oversample=4,
        )
        governance = LLMGovernanceAdapter(
            FirstCandidateTransport(),
            GovernanceContext(repository="org/holdout", model="test"),
        )
        row = MODULE.evaluate_case(store, case, args, governance)

    assert row["query"] == "resume mixes a sibling worktree session"
    assert row["query_source"] == "table-note"
    assert row["judgment"]["selected_skill_id"] == "workflow:resume"
    assert row["judge_candidate_ids"] == ["workflow:resume"]
    assert row["judge_excluded_hits"][0]["id"] == "pattern:deferred"
    assert row["selected_category_matches_holdout_proxy"] is True
    assert row["holdout_solution_data_sent"] is False
