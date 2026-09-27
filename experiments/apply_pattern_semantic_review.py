#!/usr/bin/env python3
"""Apply an explicit LLM semantic Pattern review to a copied catalog.

This script does not infer semantic membership from names, keywords, or scores.
It validates and materializes the workflow IDs explicitly returned by the review,
while preserving the original catalog and transcript as separate artifacts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.schema import NodeType, RelationType
from arex_skill_graph.store import CatalogStore


def copy_sqlite(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    with sqlite3.connect(source) as src, sqlite3.connect(target) as dst:
        src.backup(dst)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-db", type=Path, required=True)
    parser.add_argument("--source-index", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output-db", type=Path, required=True)
    parser.add_argument("--output-index", type=Path, required=True)
    args = parser.parse_args()

    review = json.loads(args.review.read_text(encoding="utf-8"))
    if review.get("schema_version") != "pattern-semantic-review-v1":
        raise ValueError("unsupported review schema")
    pattern_id = str(review["pattern_id"])
    supported = list(dict.fromkeys(str(item) for item in review["supported_workflow_ids"]))
    if len(supported) < 2:
        raise ValueError("a Pattern review must support at least two Workflows")
    reviewed_ids = [str(item["workflow_id"]) for item in review["workflow_reviews"]]
    if set(reviewed_ids) != set(supported) | {
        str(item["workflow_id"])
        for item in review["workflow_reviews"]
        if item["classification"] != "same_pattern"
    }:
        raise ValueError("workflow review coverage is inconsistent")
    if {item["classification"] for item in review["workflow_reviews"]} - {
        "same_pattern", "partial_alignment", "related_but_distinct", "specialization"
    }:
        raise ValueError("unsupported semantic classification")

    copy_sqlite(args.source_db, args.output_db)
    with CatalogStore(args.output_db) as store:
        store.initialize()
        pattern = store.get_node(pattern_id)
        if pattern is None or pattern.node_type is not NodeType.PATTERN:
            raise KeyError(f"Pattern not found: {pattern_id}")
        current = {
            neighbor.id
            for edge, neighbor, direction in store.neighbors(
                pattern_id, relations=(RelationType.CONTAINS,), direction="out"
            )
            if neighbor.node_type is NodeType.WORKFLOW
        }
        if not set(supported) <= current:
            raise ValueError({"review_support_not_in_graph": sorted(set(supported) - current)})
        workflows = {node.id: node for node in store.list_nodes(node_types=[NodeType.WORKFLOW])}
        unknown = [item for item in supported if item not in workflows]
        if unknown:
            raise ValueError({"unknown_workflows": unknown})

        payload = dict(pattern.payload)
        payload["workflow_ids"] = supported
        payload["semantic_review"] = {
            "artifact": args.review.name,
            "decision": review["pattern_decision"],
            "reviewed_at": review["reviewed_at"],
            "reviewer_model": review["reviewer_model"],
        }
        provenance = dict(pattern.provenance)
        provenance["semantic_review"] = {
            "artifact": str(args.review),
            "source_pattern_call_index": review["source_pattern_call_index"],
            "raw_response_sha256": review["raw_pattern_extraction_response_sha256"],
        }
        pattern.payload = payload
        pattern.provenance = provenance
        with store.transaction():
            store.upsert_node(pattern)
            placeholders = ",".join("?" for _ in supported)
            store.connection.execute(
                f"DELETE FROM edges WHERE source_id = ? AND relation = ? AND target_id NOT IN ({placeholders})",
                [pattern_id, RelationType.CONTAINS.value, *supported],
            )
            store.record_skill_lifecycle_event(
                pattern_id,
                "semantic_review",
                {
                    "review_artifact": str(args.review),
                    "decision": review["pattern_decision"],
                    "supported_workflow_ids": supported,
                    "workflow_reviews": review["workflow_reviews"],
                    "rationale": review["rationale"],
                    "reviewer_model": review["reviewer_model"],
                },
                review["reviewed_at"],
            )
            row = store.connection.execute(
                "SELECT skill_json FROM skill_versions WHERE skill_id = ?", (pattern_id,)
            ).fetchone()
            if row:
                skill_json = json.loads(row["skill_json"])
                skill_json["payload"] = payload
                review_by_id = {
                    str(item["workflow_id"]): item
                    for item in review["workflow_reviews"]
                }
                skill_json["evidence_ids"] = sorted({
                    str(evidence_id)
                    for workflow_id in supported
                    for evidence_id in review_by_id[workflow_id].get("evidence_ids", [])
                })
                store.connection.execute(
                    "UPDATE skill_versions SET skill_json = ?, updated_at = ? WHERE skill_id = ?",
                    (json.dumps(skill_json, ensure_ascii=False, sort_keys=True), review["reviewed_at"], pattern_id),
                )
        store.build_hnsw_index(args.output_index, ef_search=128)
        remaining = [
            neighbor.id
            for _edge, neighbor, _direction in store.neighbors(
                pattern_id, relations=(RelationType.CONTAINS,), direction="out"
            )
        ]
        print(json.dumps({
            "output_db": str(args.output_db),
            "output_index": str(args.output_index),
            "pattern_id": pattern_id,
            "contains_workflows": sorted(remaining),
            "removed_workflows": sorted(current - set(supported)),
        }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
