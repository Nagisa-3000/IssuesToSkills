from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore
from experiments.ingest_paired_agent_feedback import (
    ingest_paired_agent_feedback,
    sha256_file,
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_source(root: Path, node: Node) -> tuple[Path, Path]:
    source_db = root / "source.sqlite"
    source_index = root / "source.hnsw"
    source_index.write_bytes(b"stable-hnsw-index")
    with CatalogStore(source_db) as store:
        store.initialize()
        with store.transaction():
            store.upsert_node(node)
    return source_db, source_index


def make_artifacts(
    root: Path,
    *,
    case_id: str,
    selected_skill_id: str,
    qualified: bool = True,
    task_solved: bool = True,
    pattern_promotion_supported: bool = False,
) -> dict[str, Path]:
    evaluation_root = root / "evaluation"
    project = "project-a"
    generated_at = "2026-10-02T12:00:00+00:00"
    report = {
        "generated_at": generated_at,
        "rows": [
            {
                "case_id": case_id,
                "arm": "no_skill",
                "status": "passed",
                "setup_success": True,
                "agent_success": True,
                "patch_nonempty": True,
                "visible_tests_present": True,
                "raw_test_success": True,
                "test_success": True,
                "test_edit_violation": False,
                "solution_ref_in_prompt": False,
                "solution_ref_in_workspace_history": False,
            },
            {
                "case_id": case_id,
                "arm": "guided",
                "status": "passed",
                "setup_success": True,
                "agent_success": True,
                "patch_nonempty": True,
                "visible_tests_present": True,
                "raw_test_success": True,
                "test_success": True,
                "test_edit_violation": False,
                "solution_ref_in_prompt": False,
                "solution_ref_in_workspace_history": False,
            },
        ],
    }
    weighted = {
        "evaluations": [
            {
                "case_id": case_id,
                "eligible_for_causal_comparison": qualified,
                "outcome": "full_tie",
                "arms": {
                    "guided": {
                        "eligible": qualified,
                        "setup_success": True,
                        "test_success": task_solved,
                        "issue_postcondition_satisfied": task_solved,
                        "task_solved": task_solved,
                        "leakage_gate": {"passed": True, "violations": []},
                        "overall_score": 96.0,
                        "usage_tokens": 1234,
                        "wall_seconds": 12.5,
                    }
                },
            }
        ]
    }
    manifest = [
        {
            "id": case_id,
            "base_ref": "base-ref",
            "split": "held_out_test",
            "extraction_forbidden": True,
            "solution_hidden_from_agent": True,
        }
    ]
    guidance = {
        "guidance_applicable": True,
        "judge": {
            "selected_skill_id": selected_skill_id,
            "applicable": True,
            "confidence": 0.95,
        },
        "judge_eligible_hit_ids": [selected_skill_id],
        "approved_hit_ids": [selected_skill_id],
        "excluded_guidance_hits": [],
    }
    qualification = {
        "rows": [
            {
                "case_id": case_id,
                "qualified": qualified,
                "oracle_qualified": qualified,
                "base_passes": not qualified,
                "solution_passes": qualified,
                "oracle_blocker": None if qualified else "not causal",
            }
        ]
    }
    aggregate = {
        "pattern_promotion_supported": pattern_promotion_supported,
        "promotion_blockers": (
            []
            if pattern_promotion_supported
            else [
                "insufficient_independent_holdout_cases",
                "insufficient_independent_guided_advantage_cases",
            ]
        ),
    }
    oracle = [
        {
            "case_id": case_id,
            "oracle_candidate_status": "unmerged_reference_candidate",
            "oracle_authority": "non_authoritative_unmerged_pull_request_head",
            "oracle_caveat": "Executable candidate only; not an authoritative resolution.",
        }
    ]

    write_json(evaluation_root / project / "report.json", report)
    write_json(evaluation_root / project / "weighted-evaluation.json", weighted)
    write_json(evaluation_root / "manifests" / f"{project}.json", manifest)
    write_json(
        evaluation_root / project / "runs" / case_id / "guided" / "guidance.json",
        guidance,
    )
    qualification_path = root / "qualification.json"
    aggregate_path = evaluation_root / "aggregate.json"
    oracle_path = root / "oracle-candidates.json"
    write_json(qualification_path, qualification)
    write_json(aggregate_path, aggregate)
    write_json(oracle_path, oracle)
    return {
        "evaluation_root": evaluation_root,
        "qualification": qualification_path,
        "aggregate": aggregate_path,
        "oracle": oracle_path,
    }


def run_ingestion(
    root: Path,
    source_db: Path,
    source_index: Path,
    artifacts: dict[str, Path],
) -> dict:
    return ingest_paired_agent_feedback(
        source_db=source_db,
        source_index=source_index,
        evaluation_root=artifacts["evaluation_root"],
        qualification_report=artifacts["qualification"],
        aggregate_path=artifacts["aggregate"],
        oracle_candidates_path=artifacts["oracle"],
        output_dir=root / "feedback",
    )


def test_ingests_guided_success_idempotently_without_serving_mutation(tmp_path: Path) -> None:
    case_id = "owner__repo__123__context-budget"
    skill_id = "pattern:test-budget-policy"
    source_db, source_index = make_source(
        tmp_path,
        Node(
            id=skill_id,
            node_type=NodeType.PATTERN,
            title="Repair budget decisions at their policy boundary",
            summary="Repair the owning policy and lock precedence.",
            lifecycle="provisional",
            facets={"promotion_status": "candidate_pending_holdout"},
            payload={
                "promotion_status": "candidate_pending_holdout",
                "evidence_ids": ["E1", "E2"],
                "when_to_use": ["A budget policy resolves to an unsafe value."],
            },
        ),
    )
    artifacts = make_artifacts(
        tmp_path,
        case_id=case_id,
        selected_skill_id=skill_id,
    )
    source_sha = sha256_file(source_db)
    index_sha = sha256_file(source_index)

    first = run_ingestion(tmp_path, source_db, source_index, artifacts)
    second = run_ingestion(tmp_path, source_db, source_index, artifacts)

    assert first["summary"]["success_events"] == 1
    assert first["summary"]["new_success_events"] == 1
    assert second["summary"]["success_events"] == 1
    assert second["summary"]["new_success_events"] == 0
    assert second["cases"][0]["event_already_present"] is True
    assert second["serving_graph"]["unchanged"] is True
    assert second["summary"]["lifecycle_status_mutations"] == 0
    assert second["summary"]["pattern_promotion_supported"] is False
    assert second["summary"]["pattern_promotion_applied"] is False
    assert sha256_file(source_db) == source_sha
    assert sha256_file(source_index) == index_sha

    output_db = tmp_path / "feedback" / "catalog.sqlite"
    with sqlite3.connect(output_db) as connection:
        connection.row_factory = sqlite3.Row
        node = connection.execute(
            "SELECT lifecycle FROM nodes WHERE id = ?", (skill_id,)
        ).fetchone()
        skill = connection.execute(
            "SELECT status, skill_json FROM skill_versions WHERE skill_id = ?", (skill_id,)
        ).fetchone()
        assert node["lifecycle"] == "provisional"
        assert skill["status"] == "candidate"
        skill_json = json.loads(skill["skill_json"])
        assert skill_json["usage"]["attempts"] == 1
        assert skill_json["usage"]["successes"] == 1
        assert connection.execute("SELECT COUNT(*) FROM skill_usage_events").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM skill_lifecycle_events").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM skill_failure_incidents").fetchone()[0] == 0


def test_failed_causal_gate_does_not_write_success_event(tmp_path: Path) -> None:
    case_id = "owner__repo__456__streaming"
    skill_id = "workflow:test-stream-recovery"
    source_db, source_index = make_source(
        tmp_path,
        Node(
            id=skill_id,
            node_type=NodeType.WORKFLOW,
            title="Recover recognized stream termination",
            summary="Route a recognized premature close through bounded retry.",
            lifecycle="provisional",
        ),
    )
    artifacts = make_artifacts(
        tmp_path,
        case_id=case_id,
        selected_skill_id=skill_id,
        qualified=False,
    )

    report = run_ingestion(tmp_path, source_db, source_index, artifacts)

    assert report["summary"]["success_events"] == 0
    assert report["summary"]["new_success_events"] == 0
    assert report["cases"][0]["accepted"] is False
    assert "qualification_not_passed" in report["cases"][0]["rejection_reasons"]
    with sqlite3.connect(tmp_path / "feedback" / "catalog.sqlite") as connection:
        assert connection.execute("SELECT COUNT(*) FROM skill_versions").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM skill_usage_events").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM skill_failure_incidents").fetchone()[0] == 0


def test_deferred_pattern_cannot_be_recorded_as_used_skill(tmp_path: Path) -> None:
    case_id = "owner__repo__789__streaming"
    skill_id = "pattern:deferred-streaming-policy"
    source_db, source_index = make_source(
        tmp_path,
        Node(
            id=skill_id,
            node_type=NodeType.PATTERN,
            title="Defer a unified streaming recovery policy",
            summary="The evidence supports distinct policies rather than one Pattern.",
            lifecycle="provisional",
            facets={"promotion_status": "deferred_by_semantic_judge"},
            payload={"promotion_status": "deferred_by_semantic_judge"},
        ),
    )
    artifacts = make_artifacts(
        tmp_path,
        case_id=case_id,
        selected_skill_id=skill_id,
    )

    report = run_ingestion(tmp_path, source_db, source_index, artifacts)

    assert report["summary"]["success_events"] == 0
    assert report["cases"][0]["accepted"] is False
    assert "selected_pattern_deferred_or_rejected" in report["cases"][0][
        "rejection_reasons"
    ]
    with sqlite3.connect(tmp_path / "feedback" / "catalog.sqlite") as connection:
        assert connection.execute("SELECT COUNT(*) FROM skill_versions").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM skill_usage_events").fetchone()[0] == 0
