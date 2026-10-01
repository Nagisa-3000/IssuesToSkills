#!/usr/bin/env python3
"""Compose a traceable training/holdout manifest from several source manifests."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def cases_from(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        payload = payload.get("cases", [])
    if not isinstance(payload, list):
        raise ValueError("each manifest must be an object with cases or a JSON array")
    return [dict(item) for item in payload if isinstance(item, dict)]


def key(case: dict[str, Any]) -> tuple[str, int]:
    return str(case.get("repository") or ""), int(case["issue"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, action="append", required=True,
                        help="source manifest; repeat to compose several manifests")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    merged: dict[tuple[str, int], dict[str, Any]] = {}
    conflicts: list[dict[str, Any]] = []
    source_paths: list[str] = []
    for path in args.source:
        source_paths.append(str(path))
        for case in cases_from(json.loads(path.read_text(encoding="utf-8"))):
            item = dict(case)
            item.setdefault("manifest_origin", str(path))
            item.setdefault("exact_table_row", "user_supplied_agent_core_issue_table" in str(item.get("source") or ""))
            item.setdefault("role", item.get("split") or "train_candidate")
            item.setdefault("split", item.get("role"))
            item_key = key(item)
            if item_key in merged:
                previous = merged[item_key]
                if previous.get("category") != item.get("category") or previous.get("role") != item.get("role"):
                    conflicts.append({
                        "key": list(item_key),
                        "kept": previous.get("manifest_origin"),
                        "ignored": item.get("manifest_origin"),
                        "kept_category": previous.get("category"),
                        "ignored_category": item.get("category"),
                    })
                continue
            merged[item_key] = item

    cases = sorted(merged.values(), key=lambda item: (str(item.get("category")), str(item.get("repository")), int(item["issue"])))
    categories = sorted({str(item.get("category")) for item in cases if item.get("category")})
    repositories = sorted({str(item.get("repository")) for item in cases if item.get("repository")})
    payload = {
        "schema_version": "agent-core-composed-training-manifest-v1",
        "source_manifests": source_paths,
        "composition_policy": {
            "training_catalog_only": True,
            "holdout_cases_retained_for_gate_but_refused_by_catalog_builder": True,
            "duplicate_key_policy": "first source wins; category/role conflicts are recorded",
            "exact_rows_and_substitutes_remain_distinguishable": True,
        },
        "categories": categories,
        "repositories": repositories,
        "cases": cases,
        "composition_conflicts": conflicts,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "cases": len(cases), "categories": len(categories), "repositories": len(repositories), "conflicts": len(conflicts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
