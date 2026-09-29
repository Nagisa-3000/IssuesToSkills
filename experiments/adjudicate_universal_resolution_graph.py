#!/usr/bin/env python3
"""Adjudicate semantic Action peers and Pattern candidates with an LLM.

The structural graph builder is intentionally deterministic and conservative.
This command is the optional semantic boundary described by the meta-skill:
the model reads bounded evidence-backed cards, returns JSON decisions, and
never gets permission to rewrite historical episodes.  With no API key it
records ``deferred`` decisions, preserving a truthful offline artifact.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
import os
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport


ACTION_SCHEMA = {
    "type": "object",
    "required": ["decision", "confidence", "rationale", "evidence_ids"],
    "properties": {
        "decision": {"enum": ["equivalent", "distinct", "unknown"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "rationale": {"type": "string"},
        "evidence_ids": {"type": "array", "items": {"type": "string"}},
    },
}

PATTERN_SCHEMA = {
    "type": "object",
    "required": ["decision", "confidence", "rationale", "evidence_ids", "missing_probes"],
    "properties": {
        "decision": {"enum": ["promote_candidate", "defer", "reject"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "rationale": {"type": "string"},
        "evidence_ids": {"type": "array", "items": {"type": "string"}},
        "missing_probes": {"type": "array", "items": {"type": "string"}},
    },
}


def bounded_call(transport: OpenAICompatibleTransport | None, *, system: str, payload: dict[str, Any], schema: dict[str, Any]) -> tuple[str, dict[str, Any] | None, str | None]:
    if transport is None:
        return "deferred_no_api_key", None, None
    try:
        result = dict(transport.complete(system=system, user=json.dumps(payload, ensure_ascii=False), response_schema=schema))
        return "llm", result, None
    except Exception as exc:  # preserve the decision artifact for later retry
        return "deferred_llm_error", None, f"{type(exc).__name__}: {exc}"


def action_pairs(actions: list[dict[str, Any]], max_pairs: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for action in actions:
        key = (str(action.get("category", "")), str(action.get("operation", "")))
        grouped.setdefault(key, []).append(action)
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for group in grouped.values():
        pairs.extend(combinations(group, 2))
        if len(pairs) >= max_pairs:
            break
    return pairs[:max_pairs]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--max-action-pairs", type=int, default=80)
    args = parser.parse_args()
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    transport = None
    if args.api_key:
        transport = OpenAICompatibleTransport(OpenAICompatibleConfig(
            api_key=args.api_key, base_url=args.base_url, model=args.model,
            timeout_seconds=180, max_output_tokens=1800, retries=2,
        ))
    action_rows = [dict(item) for item in graph.get("actions", []) if isinstance(item, dict)]
    workflow_by_id = {str(item.get("id")): item for item in graph.get("workflows", []) if isinstance(item, dict)}
    action_judgments: list[dict[str, Any]] = []
    for left, right in action_pairs(action_rows, max(0, args.max_action_pairs)):
        status, result, error = bounded_call(
            transport,
            system=(
                "You are the semantic Action adjudicator for an evidence-grounded graph. "
                "Compare intent, module role, operation, pre/post state, validation, "
                "parameters, and evidence. Titles, paths, and similarity are not proof. "
                "Return equivalent only when the same reusable operation and postcondition "
                "are supported; otherwise use distinct or unknown. JSON only."
            ),
            payload={"left": left, "right": right, "rule": "same-level semantic equivalence only"},
            schema=ACTION_SCHEMA,
        )
        action_judgments.append({"left_id": left.get("id"), "right_id": right.get("id"), "status": status, "result": result, "error": error})

    pattern_judgments: list[dict[str, Any]] = []
    for pattern in graph.get("patterns", []):
        if not isinstance(pattern, dict):
            continue
        workflows = [workflow_by_id[item] for item in pattern.get("supporting_workflows", []) if item in workflow_by_id]
        status, result, error = bounded_call(
            transport,
            system=(
                "You are the independent Pattern adjudicator. Decide whether the candidate "
                "is a project-independent abstraction supported by the supplied training "
                "Workflows. Require multiple repositories, mandatory actions with evidence, "
                "explicit exclusions/uncertainty, and a holdout probe before promotion. "
                "Do not invent missing evidence. JSON only."
            ),
            payload={"pattern": pattern, "supporting_workflows": workflows, "holdout_gate": "not yet run"},
            schema=PATTERN_SCHEMA,
        )
        decision = dict(pattern)
        decision["judge_status"] = status
        decision["judge_result"] = result
        decision["judge_error"] = error
        pattern_judgments.append(decision)

    payload = {
        "schema_version": "universal-resolution-graph-adjudication-v1",
        "source_graph": str(args.graph),
        "model": args.model if transport is not None else None,
        "llm_available": transport is not None,
        "action_judgments": action_judgments,
        "pattern_judgments": pattern_judgments,
        "calls": transport.calls if transport is not None else [],
        "transcripts": transport.transcripts if transport is not None else [],
        "promotion_policy": {
            "equivalent_action_is_a_proposal_until_evidence_review": True,
            "pattern_promotion_requires_holdout": True,
            "no_historical_episode_mutation": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"actions": len(action_judgments), "patterns": len(pattern_judgments), "llm_available": payload["llm_available"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
