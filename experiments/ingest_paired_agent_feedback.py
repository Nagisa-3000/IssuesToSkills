#!/usr/bin/env python3
"""Ingest qualified paired-agent Skill usage into a derived lifecycle registry.

The source catalog and HNSW index are treated as immutable serving artifacts. This
script copies the SQLite catalog once, records only validated guided-arm usage, and
keeps promotion, revision, merge, quarantine, deprecation, and retirement decisions
outside this neutral feedback-ingestion step.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections.abc import Iterable, Mapping
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.lifecycle import (
    SkillLevel,
    SkillRecord,
    SkillStatus,
    UsageEvent,
    UsageResult,
)
from arex_skill_graph.schema import (
    Node,
    NodeType,
    RelationType,
    canonical_json,
    stable_id,
)
from arex_skill_graph.store import CatalogStore

SCHEMA_VERSION = "paired-agent-feedback-v1"
SOURCE_BINDING_KEY = "paired_agent_feedback_source_v1"
SERVING_TABLES = {
    "nodes": ("id",),
    "edges": ("id",),
    "embeddings": ("node_id", "embedding_kind", "model_version"),
}
SKILL_NODE_TYPES = {NodeType.ATOMIC, NodeType.WORKFLOW, NodeType.PATTERN}
INELIGIBLE_PATTERN_DECISIONS = {
    "defer",
    "deferred",
    "deferred_by_semantic_judge",
    "reject",
    "rejected",
    "rejected_by_semantic_judge",
}
TERMINAL_SKILL_STATUSES = {
    SkillStatus.QUARANTINED,
    SkillStatus.DEPRECATED,
    SkillStatus.RETIRED,
    SkillStatus.MERGED,
    SkillStatus.SUPERSEDED,
}


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def copy_sqlite_once(source: Path, target: Path, source_sha256: str) -> bool:
    """Create a durable derived copy once and verify its source on later runs."""
    target.parent.mkdir(parents=True, exist_ok=True)
    created = not target.exists()
    if created:
        source_uri = f"file:{source.resolve()}?mode=ro"
        with (
            sqlite3.connect(source_uri, uri=True) as source_db,
            sqlite3.connect(target) as target_db,
        ):
            source_db.backup(target_db)

    with CatalogStore(target) as store:
        store.initialize()
        row = store.connection.execute(
            "SELECT value_json FROM metadata WHERE key = ?", (SOURCE_BINDING_KEY,)
        ).fetchone()
        binding = {
            "schema_version": SCHEMA_VERSION,
            "source_db": display_path(source),
            "source_db_sha256": source_sha256,
        }
        if row is None:
            if not created:
                raise ValueError(
                    f"existing output catalog lacks {SOURCE_BINDING_KEY} metadata: {target}"
                )
            store.connection.execute(
                "INSERT INTO metadata(key, value_json) VALUES (?, ?)",
                (SOURCE_BINDING_KEY, canonical_json(binding)),
            )
            store.connection.commit()
        else:
            existing = json.loads(row["value_json"])
            if existing != binding:
                raise ValueError(
                    "existing output catalog was derived from a different source: "
                    f"expected={binding!r} actual={existing!r}"
                )
    return created


def table_fingerprint(
    connection: sqlite3.Connection,
    table: str,
    order_by: tuple[str, ...],
) -> dict[str, Any]:
    order_sql = ", ".join(order_by)
    rows = connection.execute(f"SELECT * FROM {table} ORDER BY {order_sql}").fetchall()
    digest = sha256()
    for row in rows:
        value = dict(zip(row.keys(), row, strict=True))
        digest.update(canonical_json(value).encode("utf-8"))
        digest.update(b"\n")
    return {"rows": len(rows), "sha256": digest.hexdigest()}


def serving_graph_fingerprints(store: CatalogStore) -> dict[str, dict[str, Any]]:
    return {
        table: table_fingerprint(store.connection, table, order_by)
        for table, order_by in SERVING_TABLES.items()
    }


def string_values(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        return (str(value),)
    if isinstance(value, Iterable):
        return tuple(str(item) for item in value)
    return (str(value),)


def deduplicated_strings(*values: Any) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        for item in string_values(value):
            if item and item not in seen:
                seen.add(item)
                result.append(item)
    return tuple(result)


def registry_status(lifecycle: str | None) -> SkillStatus:
    normalized = str(lifecycle or "").strip().lower()
    if not normalized or normalized == "provisional":
        return SkillStatus.CANDIDATE
    try:
        return SkillStatus(normalized)
    except ValueError as exc:
        raise ValueError(f"unsupported serving-node lifecycle: {lifecycle!r}") from exc


def incoming_parent_ids(store: CatalogStore, node_id: str) -> set[str]:
    return {
        edge.source_id
        for edge, _neighbor, direction in store.neighbors(
            node_id,
            relations=(RelationType.CONTAINS,),
            direction="in",
        )
        if direction == "in"
    }


def skill_record_from_node(store: CatalogStore, node: Node) -> SkillRecord:
    payload = dict(node.payload)
    facets = dict(node.facets)
    status = registry_status(node.lifecycle)
    if status in TERMINAL_SKILL_STATUSES:
        raise ValueError(f"selected Skill is terminal in the serving graph: {node.id}={status.value}")
    try:
        version = int(node.version)
    except (TypeError, ValueError):
        version = 1

    registry_payload = dict(payload)
    registry_payload["feedback_registry_source"] = {
        "serving_node_lifecycle": node.lifecycle,
        "serving_node_confidence": node.confidence,
        "serving_node_facets": facets,
        "serving_node_provenance": dict(node.provenance),
        "serving_graph_mutated": False,
    }
    return SkillRecord(
        skill_id=node.id,
        level=SkillLevel(node.node_type.value),
        title=node.title,
        summary=node.summary,
        version=version,
        status=status,
        canonical_id=str(payload.get("canonical_id") or node.id),
        aliases=set(string_values(payload.get("aliases"))),
        supersedes=set(string_values(payload.get("supersedes"))),
        merged_from=set(string_values(payload.get("merged_from"))),
        parent_ids=incoming_parent_ids(store, node.id),
        evidence_ids=set(
            deduplicated_strings(payload.get("evidence_ids"), facets.get("evidence_ids"))
        ),
        preconditions=deduplicated_strings(
            payload.get("preconditions"),
            facets.get("preconditions"),
            payload.get("when_to_use"),
        ),
        exclusions=deduplicated_strings(
            payload.get("exclusions"),
            facets.get("exclusions"),
            payload.get("not_applicable_when"),
        ),
        failure_modes=deduplicated_strings(
            payload.get("failure_modes"),
            facets.get("failure_modes"),
            payload.get("known_failure_modes"),
        ),
        payload=registry_payload,
    )


def existing_skill_record(store: CatalogStore, skill_id: str) -> SkillRecord | None:
    row = store.connection.execute(
        "SELECT skill_json FROM skill_versions WHERE skill_id = ?", (skill_id,)
    ).fetchone()
    if row is None:
        return None
    return SkillRecord.from_json(json.loads(row["skill_json"]))


def index_rows_by_case(
    document: Any,
    *,
    field: str = "rows",
) -> dict[str, Mapping[str, Any]]:
    if isinstance(document, Mapping):
        rows = document.get(field, [])
    else:
        rows = document
    if not isinstance(rows, list):
        raise TypeError(f"expected a list at {field!r}")
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        raw_case_id = row.get("case_id") or row.get("id")
        if not raw_case_id:
            continue
        case_id = str(raw_case_id)
        if case_id in result:
            raise ValueError(f"duplicate case_id: {case_id}")
        result[case_id] = row
    return result


def oracle_candidates_by_case(document: Any) -> dict[str, Mapping[str, Any]]:
    if document is None:
        return {}
    if isinstance(document, Mapping):
        return index_rows_by_case(document, field="rows")
    return index_rows_by_case(document)


def project_documents(evaluation_root: Path) -> list[dict[str, Any]]:
    manifest_dir = evaluation_root / "manifests"
    documents: list[dict[str, Any]] = []
    for project_dir in sorted(path for path in evaluation_root.iterdir() if path.is_dir()):
        report_path = project_dir / "report.json"
        weighted_path = project_dir / "weighted-evaluation.json"
        if not report_path.exists() and not weighted_path.exists():
            continue
        if not report_path.exists() or not weighted_path.exists():
            raise FileNotFoundError(
                f"paired evaluation project requires report and weighted evaluation: {project_dir}"
            )
        manifest_path = manifest_dir / f"{project_dir.name}.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"missing holdout manifest: {manifest_path}")

        guidance: dict[str, tuple[Path, Mapping[str, Any]]] = {}
        for path in sorted((project_dir / "runs").rglob("guided/guidance.json")):
            case_id = path.parent.parent.name
            if case_id in guidance:
                raise ValueError(f"duplicate guided guidance for {case_id}")
            value = load_json(path)
            if not isinstance(value, Mapping):
                raise TypeError(f"guidance must be an object: {path}")
            guidance[case_id] = (path, value)

        report = load_json(report_path)
        weighted = load_json(weighted_path)
        manifest = load_json(manifest_path)
        documents.append(
            {
                "project": project_dir.name,
                "report_path": report_path,
                "weighted_path": weighted_path,
                "manifest_path": manifest_path,
                "report": report,
                "weighted": weighted,
                "manifest": index_rows_by_case(manifest),
                "guidance": guidance,
            }
        )
    if not documents:
        raise ValueError(f"no paired evaluation projects found under {evaluation_root}")
    return documents


def require_true(reasons: list[str], value: Any, label: str) -> None:
    if value is not True:
        reasons.append(label)


def feedback_case_gate(
    *,
    guided_row: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    qualification: Mapping[str, Any] | None,
    manifest: Mapping[str, Any] | None,
    guidance: Mapping[str, Any] | None,
    selected_node: Node | None,
) -> list[str]:
    reasons: list[str] = []
    if qualification is None:
        reasons.append("missing_qualification")
    else:
        require_true(reasons, qualification.get("qualified"), "qualification_not_passed")
        require_true(reasons, qualification.get("oracle_qualified"), "oracle_not_qualified")
        if qualification.get("base_passes") is not False:
            reasons.append("parent_does_not_fail_visible_regression")
        require_true(reasons, qualification.get("solution_passes"), "candidate_does_not_pass_oracle")

    if manifest is None:
        reasons.append("missing_holdout_manifest")
    else:
        require_true(reasons, manifest.get("extraction_forbidden"), "holdout_extraction_not_forbidden")
        require_true(
            reasons,
            manifest.get("solution_hidden_from_agent"),
            "solution_not_hidden_from_agent",
        )
        if manifest.get("split") not in {"test", "held_out_test"}:
            reasons.append("case_not_in_test_split")

    if guided_row.get("arm") != "guided":
        reasons.append("not_guided_arm")
    if guided_row.get("status") != "passed":
        reasons.append("guided_status_not_passed")
    for key in (
        "setup_success",
        "agent_success",
        "patch_nonempty",
        "visible_tests_present",
        "raw_test_success",
        "test_success",
    ):
        require_true(reasons, guided_row.get(key), f"guided_{key}_not_true")
    if guided_row.get("test_edit_violation") is not False:
        reasons.append("visible_test_edit_violation")
    if guided_row.get("solution_ref_in_prompt") is not False:
        reasons.append("solution_ref_leaked_in_prompt")
    if guided_row.get("solution_ref_in_workspace_history") is not False:
        reasons.append("solution_ref_leaked_in_workspace_history")

    require_true(
        reasons,
        evaluation.get("eligible_for_causal_comparison"),
        "evaluation_not_causally_eligible",
    )
    guided_eval = evaluation.get("arms", {}).get("guided", {})
    for key in (
        "eligible",
        "setup_success",
        "test_success",
        "issue_postcondition_satisfied",
        "task_solved",
    ):
        require_true(reasons, guided_eval.get(key), f"guided_evaluation_{key}_not_true")
    leakage_gate = guided_eval.get("leakage_gate", {})
    require_true(reasons, leakage_gate.get("passed"), "guided_evaluation_leakage_gate_failed")

    if guidance is None:
        reasons.append("missing_guidance")
    else:
        require_true(reasons, guidance.get("guidance_applicable"), "guidance_not_applicable")
        judge = guidance.get("judge") or {}
        require_true(reasons, judge.get("applicable"), "retrieval_judge_not_applicable")
        selected_skill_id = judge.get("selected_skill_id")
        if not selected_skill_id:
            reasons.append("retrieval_judge_selected_no_skill")
        elif selected_skill_id not in set(string_values(guidance.get("judge_eligible_hit_ids"))):
            reasons.append("selected_skill_not_judge_eligible")
        if selected_skill_id not in set(string_values(guidance.get("approved_hit_ids"))):
            reasons.append("selected_skill_not_approved_for_guidance")
        excluded = {
            str(item.get("id"))
            for item in guidance.get("excluded_guidance_hits", [])
            if isinstance(item, Mapping)
        }
        if selected_skill_id in excluded:
            reasons.append("selected_skill_explicitly_excluded")

    if selected_node is None:
        reasons.append("selected_skill_missing_from_catalog")
    else:
        if selected_node.node_type not in SKILL_NODE_TYPES:
            reasons.append("selected_node_is_not_a_skill_level")
        decision = str(
            selected_node.payload.get("promotion_status")
            or selected_node.facets.get("promotion_status")
            or ""
        ).strip().lower()
        if selected_node.node_type is NodeType.PATTERN and decision in INELIGIBLE_PATTERN_DECISIONS:
            reasons.append("selected_pattern_deferred_or_rejected")
        try:
            status = registry_status(selected_node.lifecycle)
        except ValueError:
            reasons.append("selected_node_has_unknown_lifecycle")
        else:
            if status in TERMINAL_SKILL_STATUSES:
                reasons.append("selected_skill_has_terminal_lifecycle")
    return list(dict.fromkeys(reasons))


def selected_skill_id(guidance: Mapping[str, Any] | None) -> str | None:
    if not guidance:
        return None
    judge = guidance.get("judge") or {}
    value = judge.get("selected_skill_id")
    return str(value) if value else None


def event_timestamp(report: Mapping[str, Any]) -> str:
    value = str(report.get("generated_at") or "").strip()
    if not value:
        raise ValueError("paired report lacks generated_at")
    datetime.fromisoformat(value)
    return value


def registry_counts(store: CatalogStore) -> dict[str, int]:
    tables = (
        "skill_versions",
        "skill_usage_events",
        "skill_lifecycle_events",
        "skill_failure_incidents",
        "skill_dedup_proposals",
    )
    return {
        table: int(store.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        for table in tables
    }


def ingest_paired_agent_feedback(
    *,
    source_db: Path,
    source_index: Path,
    evaluation_root: Path,
    qualification_report: Path,
    aggregate_path: Path,
    oracle_candidates_path: Path | None,
    output_dir: Path,
) -> dict[str, Any]:
    source_db = source_db.resolve()
    source_index = source_index.resolve()
    evaluation_root = evaluation_root.resolve()
    qualification_report = qualification_report.resolve()
    aggregate_path = aggregate_path.resolve()
    oracle_candidates_path = oracle_candidates_path.resolve() if oracle_candidates_path else None
    output_dir = output_dir.resolve()
    output_db = output_dir / "catalog.sqlite"
    output_report = output_dir / "feedback-report.json"

    for required in (
        source_db,
        source_index,
        evaluation_root,
        qualification_report,
        aggregate_path,
    ):
        if not required.exists():
            raise FileNotFoundError(required)
    if oracle_candidates_path is not None and not oracle_candidates_path.exists():
        raise FileNotFoundError(oracle_candidates_path)

    source_db_sha_before = sha256_file(source_db)
    source_index_sha_before = sha256_file(source_index)
    output_created = copy_sqlite_once(source_db, output_db, source_db_sha_before)

    qualification_rows = index_rows_by_case(load_json(qualification_report))
    aggregate = load_json(aggregate_path)
    oracle_rows = oracle_candidates_by_case(
        load_json(oracle_candidates_path) if oracle_candidates_path else None
    )
    projects = project_documents(evaluation_root)

    cases: list[dict[str, Any]] = []
    accepted_event_ids: list[str] = []
    new_event_ids: list[str] = []
    lifecycle_status_mutations = 0

    with CatalogStore(output_db) as store:
        store.initialize()
        graph_before = serving_graph_fingerprints(store)
        registry_before = registry_counts(store)

        with store.transaction():
            for project in projects:
                report = project["report"]
                weighted = project["weighted"]
                evaluation_by_case = index_rows_by_case(weighted, field="evaluations")
                guided_rows = {
                    str(row["case_id"]): row
                    for row in report.get("rows", [])
                    if isinstance(row, Mapping) and row.get("arm") == "guided"
                }
                for case_id, guided_row in sorted(guided_rows.items()):
                    guidance_entry = project["guidance"].get(case_id)
                    guidance_path = guidance_entry[0] if guidance_entry else None
                    guidance = guidance_entry[1] if guidance_entry else None
                    evaluation = evaluation_by_case.get(case_id, {})
                    qualification = qualification_rows.get(case_id)
                    manifest = project["manifest"].get(case_id)
                    skill_id = selected_skill_id(guidance)
                    node = store.get_node(skill_id) if skill_id else None
                    reasons = feedback_case_gate(
                        guided_row=guided_row,
                        evaluation=evaluation,
                        qualification=qualification,
                        manifest=manifest,
                        guidance=guidance,
                        selected_node=node,
                    )
                    oracle = oracle_rows.get(case_id, {})
                    guided_eval = evaluation.get("arms", {}).get("guided", {})
                    case_result: dict[str, Any] = {
                        "case_id": case_id,
                        "project": project["project"],
                        "accepted": not reasons,
                        "rejection_reasons": reasons,
                        "selected_skill_id": skill_id,
                        "selected_node_type": node.node_type.value if node else None,
                        "serving_node_lifecycle": node.lifecycle if node else None,
                        "registry_status": (
                            registry_status(node.lifecycle).value if node and not reasons else None
                        ),
                        "evaluation_outcome": evaluation.get("outcome"),
                        "guided_overall_score": guided_eval.get("overall_score"),
                        "guided_usage_tokens": guided_eval.get("usage_tokens"),
                        "guided_wall_seconds": guided_eval.get("wall_seconds"),
                        "qualification": {
                            key: qualification.get(key) if qualification else None
                            for key in (
                                "qualified",
                                "oracle_qualified",
                                "base_passes",
                                "solution_passes",
                                "oracle_blocker",
                            )
                        },
                        "oracle_candidate_status": oracle.get("oracle_candidate_status"),
                        "oracle_authority": oracle.get("oracle_authority"),
                        "oracle_caveat": oracle.get("oracle_caveat"),
                        "source_artifacts": {
                            "report": display_path(project["report_path"]),
                            "weighted_evaluation": display_path(project["weighted_path"]),
                            "manifest": display_path(project["manifest_path"]),
                            "guidance": display_path(guidance_path) if guidance_path else None,
                        },
                    }
                    if reasons:
                        cases.append(case_result)
                        continue
                    assert node is not None
                    assert skill_id is not None

                    occurred_at = event_timestamp(report)
                    event_id = stable_id(
                        "usage",
                        "paired-agent-guided",
                        case_id,
                        skill_id,
                        str(manifest.get("base_ref")),
                    )
                    event = UsageEvent(
                        event_id=event_id,
                        skill_id=skill_id,
                        skill_version=int(node.version) if str(node.version).isdigit() else 1,
                        task_id=case_id,
                        result=UsageResult.SUCCESS,
                        independent_context_id=case_id,
                        validation_passed=True,
                        token_cost=(
                            int(guided_eval["usage_tokens"])
                            if guided_eval.get("usage_tokens") is not None
                            else None
                        ),
                        notes=(
                            "Qualified paired-agent guided arm solved the holdout; "
                            f"independent evaluator outcome={evaluation.get('outcome')}; "
                            "this event does not imply Skill promotion."
                        ),
                        occurred_at=occurred_at,
                    )
                    existed = store.connection.execute(
                        "SELECT 1 FROM skill_usage_events WHERE event_id = ?", (event_id,)
                    ).fetchone() is not None
                    record = existing_skill_record(store, skill_id)
                    if record is None:
                        record = skill_record_from_node(store, node)
                    prior_status = record.status
                    if not existed:
                        record.usage.record(
                            UsageResult.SUCCESS,
                            context_id=case_id,
                            occurred_at=occurred_at,
                        )
                        record.touch(occurred_at)
                        store.persist_skill_record(record)
                        store.record_usage_event(event)
                        new_event_ids.append(event_id)
                    elif existing_skill_record(store, skill_id) is None:
                        raise RuntimeError(
                            f"usage event exists without a Skill registry record: {event_id}"
                        )
                    if record.status is not prior_status:
                        lifecycle_status_mutations += 1

                    lifecycle_payload = {
                        "event_id": event_id,
                        "case_id": case_id,
                        "arm": "guided",
                        "result": UsageResult.SUCCESS.value,
                        "validation_passed": True,
                        "selected_skill_id": skill_id,
                        "selection_source": "retrieval_llm_judge",
                        "evaluation_outcome": evaluation.get("outcome"),
                        "serving_node_lifecycle": node.lifecycle,
                        "registry_status": record.status.value,
                        "lifecycle_status_changed": False,
                        "promotion_applied": False,
                        "merge_applied": False,
                        "retirement_applied": False,
                        "source_artifacts": case_result["source_artifacts"],
                    }
                    store.record_skill_lifecycle_event(
                        skill_id,
                        "paired_agent_feedback",
                        lifecycle_payload,
                        occurred_at,
                    )
                    accepted_event_ids.append(event_id)
                    case_result.update(
                        {
                            "event_id": event_id,
                            "event_already_present": existed,
                            "result": UsageResult.SUCCESS.value,
                            "validation_passed": True,
                            "registry_status": record.status.value,
                            "lifecycle_status_changed": False,
                        }
                    )
                    cases.append(case_result)

        graph_after = serving_graph_fingerprints(store)
        registry_after = registry_counts(store)
        if graph_after != graph_before:
            raise RuntimeError("feedback ingestion mutated serving nodes, edges, or embeddings")
        if accepted_event_ids:
            placeholders = ",".join("?" for _ in accepted_event_ids)
            accepted_success_events = int(
                store.connection.execute(
                    f"SELECT COUNT(*) FROM skill_usage_events WHERE event_id IN ({placeholders})",
                    accepted_event_ids,
                ).fetchone()[0]
            )
        else:
            accepted_success_events = 0

    source_db_sha_after = sha256_file(source_db)
    source_index_sha_after = sha256_file(source_index)
    if source_db_sha_after != source_db_sha_before:
        raise RuntimeError("source catalog changed during feedback ingestion")
    if source_index_sha_after != source_index_sha_before:
        raise RuntimeError("source HNSW index changed during feedback ingestion")

    accepted_cases = [case for case in cases if case["accepted"]]
    rejected_cases = [case for case in cases if not case["accepted"]]
    timestamps = [
        str(project["report"].get("generated_at"))
        for project in projects
        if project["report"].get("generated_at")
    ]
    generated_at = max(timestamps) if timestamps else None
    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "source": {
            "catalog": {
                "path": display_path(source_db),
                "sha256_before": source_db_sha_before,
                "sha256_after": source_db_sha_after,
                "unchanged": source_db_sha_before == source_db_sha_after,
            },
            "hnsw_index": {
                "path": display_path(source_index),
                "sha256_before": source_index_sha_before,
                "sha256_after": source_index_sha_after,
                "unchanged": source_index_sha_before == source_index_sha_after,
                "rebuilt": False,
            },
            "evaluation_root": display_path(evaluation_root),
            "qualification_report": display_path(qualification_report),
            "aggregate": display_path(aggregate_path),
            "oracle_candidates": (
                display_path(oracle_candidates_path) if oracle_candidates_path else None
            ),
        },
        "output": {
            "catalog": display_path(output_db),
            "catalog_sha256": sha256_file(output_db),
            "created_from_source": output_created,
            "report": display_path(output_report),
        },
        "serving_graph": {
            "before": graph_before,
            "after": graph_after,
            "unchanged": graph_before == graph_after,
            "hnsw_rebuilt": False,
        },
        "registry": {
            "before": registry_before,
            "after": registry_after,
            "provisional_serving_nodes_map_to_registry_status": SkillStatus.CANDIDATE.value,
        },
        "cases": cases,
        "summary": {
            "discovered_guided_cases": len(cases),
            "accepted_guided_cases": len(accepted_cases),
            "rejected_guided_cases": len(rejected_cases),
            "success_events": accepted_success_events,
            "new_success_events": len(new_event_ids),
            "failure_events": 0,
            "failure_incidents": 0,
            "lifecycle_status_mutations": lifecycle_status_mutations,
            "revision_mutations": 0,
            "merge_mutations": 0,
            "quarantine_mutations": 0,
            "deprecation_mutations": 0,
            "retirement_mutations": 0,
            "pattern_promotion_supported": bool(
                aggregate.get("pattern_promotion_supported", False)
            ),
            "pattern_promotion_applied": False,
            "promotion_blockers": list(aggregate.get("promotion_blockers", [])),
        },
        "policy_decisions": [
            "Only the guided arm can create a Skill usage event; the no-skill arm is a baseline.",
            "A success event requires a qualified fail-to-pass oracle, no leakage, a solved guided arm, and an eligible retrieval-judge selection.",
            "Deferred or rejected Patterns cannot be recorded as the used Skill.",
            "Usage feedback is neutral evidence and does not itself promote, merge, quarantine, deprecate, revise, or retire a Skill.",
            "Serving nodes, graph edges, embeddings, and the HNSW index remain unchanged.",
        ],
    }
    write_json(output_report, report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-db", type=Path, required=True)
    parser.add_argument("--source-index", type=Path, required=True)
    parser.add_argument("--evaluation-root", type=Path, required=True)
    parser.add_argument("--qualification-report", type=Path, required=True)
    parser.add_argument("--aggregate", type=Path)
    parser.add_argument("--oracle-candidates", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    aggregate_path = args.aggregate or args.evaluation_root / "aggregate.json"
    report = ingest_paired_agent_feedback(
        source_db=args.source_db,
        source_index=args.source_index,
        evaluation_root=args.evaluation_root,
        qualification_report=args.qualification_report,
        aggregate_path=aggregate_path,
        oracle_candidates_path=args.oracle_candidates,
        output_dir=args.output_dir,
    )
    print(
        json.dumps(
            {
                "output_catalog": report["output"]["catalog"],
                "feedback_report": report["output"]["report"],
                "success_events": report["summary"]["success_events"],
                "new_success_events": report["summary"]["new_success_events"],
                "lifecycle_status_mutations": report["summary"][
                    "lifecycle_status_mutations"
                ],
                "pattern_promotion_applied": report["summary"][
                    "pattern_promotion_applied"
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
