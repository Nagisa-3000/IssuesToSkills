#!/usr/bin/env python3
"""Merge validated per-category Resolution Pattern contracts into one semantic graph."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from induce_human_resolution_pattern import (
    DEFAULT_SCHEMA,
    apply_contract,
    canonical_json_sha256,
    file_sha256,
    select_pattern,
    validate_contract,
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_contracts(
    graph: Mapping[str, Any],
    contracts: Sequence[Mapping[str, Any]],
    schema: Mapping[str, Any],
    *,
    require_complete: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result = dict(graph)
    source_pattern_ids = {
        str(item.get("id"))
        for item in graph.get("patterns", [])
        if isinstance(item, Mapping) and item.get("id")
    }
    merged_ids: set[str] = set()
    rows: list[dict[str, Any]] = []
    for raw_contract in contracts:
        contract = dict(raw_contract)
        pattern_id = str(contract.get("pattern_id") or "")
        if not pattern_id:
            raise ValueError("every contract must contain pattern_id")
        if pattern_id in merged_ids:
            raise ValueError(f"duplicate Pattern contract: {pattern_id}")
        pattern = select_pattern(result, pattern_id)
        errors = validate_contract(contract, result, pattern, schema)
        if errors:
            raise ValueError(
                f"Pattern contract {pattern_id} failed validation:\n- " + "\n- ".join(errors)
            )
        result = apply_contract(result, pattern_id, contract)
        merged_ids.add(pattern_id)
        rows.append(
            {
                "pattern_id": pattern_id,
                "category": contract.get("category"),
                "title": contract.get("title"),
                "decision": contract.get("decision"),
                "contract_sha256": canonical_json_sha256(contract),
            }
        )

    missing = sorted(source_pattern_ids - merged_ids)
    if require_complete and missing:
        raise ValueError(f"missing Pattern contracts: {missing}")
    result["semantic_pattern_induction"] = {
        "holdout_loaded": False,
        "merged_pattern_ids": sorted(merged_ids),
        "missing_pattern_ids": missing,
        "contracts": rows,
    }
    report = {
        "schema_version": "resolution-pattern-contract-merge-v1",
        "source_patterns": len(source_pattern_ids),
        "merged_patterns": len(merged_ids),
        "missing_pattern_ids": missing,
        "decision_counts": {
            decision: sum(row["decision"] == decision for row in rows)
            for decision in ("candidate_pending_holdout", "defer", "reject")
        },
        "contracts": rows,
    }
    return result, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--contract", type=Path, action="append", required=True)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    graph = _read_json(args.graph)
    schema = _read_json(args.schema)
    contracts = [_read_json(path) for path in args.contract]
    if not isinstance(graph, Mapping):
        raise TypeError("graph must be an object")
    if not isinstance(schema, Mapping):
        raise TypeError("schema must be an object")
    if not all(isinstance(contract, Mapping) for contract in contracts):
        raise TypeError("contracts must be objects")

    result, report = merge_contracts(
        graph,
        contracts,
        schema,
        require_complete=args.require_complete,
    )
    report.update(
        {
            "source_graph": str(args.graph),
            "source_graph_sha256": file_sha256(args.graph),
            "contract_paths": [str(path) for path in args.contract],
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = args.report or args.output.with_name("semantic-pattern-merge-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "report": str(report_path),
                "merged_patterns": report["merged_patterns"],
                "decision_counts": report["decision_counts"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
