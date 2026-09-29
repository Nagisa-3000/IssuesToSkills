#!/usr/bin/env python3
"""Apply reviewed semantic action merges without mutating source episodes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def remap(value: str, aliases: dict[str, str]) -> str:
    seen: set[str] = set()
    while value in aliases and value not in seen:
        seen.add(value)
        value = aliases[value]
    return value


def merge_action_records(canonical: dict[str, Any], member: dict[str, Any], merge: dict[str, Any]) -> None:
    canonical["supporting_episodes"] = sorted(set(canonical.get("supporting_episodes", [])) | set(member.get("supporting_episodes", [])))
    canonical["supporting_repositories"] = sorted(set(canonical.get("supporting_repositories", [])) | set(member.get("supporting_repositories", [])))
    canonical["aliases"] = sorted(set(canonical.get("aliases", [])) | set(member.get("aliases", [])) | {str(member.get("source_name") or "")})
    canonical["adjudicated_equivalents"] = sorted(set(canonical.get("adjudicated_equivalents", [])) | {str(member.get("id"))})
    canonical["adjudication_rationales"] = sorted(set(canonical.get("adjudication_rationales", [])) | {str(merge.get("rationale"))})


def is_unambiguously_equivalent(merge: dict[str, Any]) -> bool:
    """Reject a contradictory LLM row instead of treating its enum as proof.

    The judge schema intentionally keeps a small enum, so the rationale is an
    independent consistency check.  A model can accidentally emit
    ``equivalent`` while explaining that postconditions/oracles differ.  Such
    rows are unresolved and must not collapse graph identities.
    """
    if merge.get("decision") != "equivalent":
        return False
    rationale = " ".join(str(merge.get("rationale") or "").lower().split())
    contradiction_markers = (
        "overlap is insufficient",
        "insufficient for an equivalent",
        "not an equivalent",
        "not equivalent",
        "different semantic targets",
        "different postconditions and oracles",
        "different validation oracles",
        "different control-state contracts",
        "not equivalence",
    )
    return not any(marker in rationale for marker in contradiction_markers)


def apply(graph: dict[str, Any], adjudication: dict[str, Any]) -> dict[str, Any]:
    aliases: dict[str, str] = {}
    accepted_merges: list[dict[str, Any]] = []
    rejected_merges: list[dict[str, Any]] = []
    action_rows = [dict(row) for row in graph.get("actions", []) if isinstance(row, dict)]
    action_by_id = {str(row.get("id")): row for row in action_rows}
    for merge in adjudication.get("action_merges", []):
        if not isinstance(merge, dict) or merge.get("decision") != "equivalent":
            continue
        if not is_unambiguously_equivalent(merge):
            rejected_merges.append({**merge, "rejected_by_consistency_guard": True})
            continue
        member_ids = [str(value) for value in merge.get("member_action_ids", []) if str(value)]
        canonical_id = str(merge.get("canonical_action_id") or "")
        if len(member_ids) < 2 or canonical_id not in member_ids or any(value not in action_by_id for value in member_ids):
            continue
        for member_id in member_ids:
            if member_id != canonical_id:
                aliases[member_id] = canonical_id
        canonical = action_by_id[canonical_id]
        for member_id in member_ids:
            if member_id != canonical_id:
                merge_action_records(canonical, action_by_id[member_id], merge)
        accepted_merges.append(merge)

    def mapped(value: Any) -> str:
        return remap(str(value), aliases)

    actions = [row for row in action_rows if str(row.get("id")) not in aliases]
    for row in actions:
        row["id"] = mapped(row.get("id"))

    workflows: list[dict[str, Any]] = []
    for raw in graph.get("workflows", []):
        if not isinstance(raw, dict):
            continue
        workflow = dict(raw)
        steps: list[dict[str, Any]] = []
        for raw_step in workflow.get("steps", []):
            if not isinstance(raw_step, dict):
                continue
            step = dict(raw_step)
            step["action_id"] = mapped(step.get("action_id"))
            steps.append(step)
        workflow["steps"] = steps
        new_edges: list[dict[str, Any]] = []
        for raw_edge in workflow.get("edges", []):
            if not isinstance(raw_edge, dict):
                continue
            edge = dict(raw_edge)
            source = mapped(edge.get("from"))
            target = mapped(edge.get("to"))
            if source == target and source.startswith("semantic-action:"):
                continue
            edge["from"] = source
            edge["to"] = target
            new_edges.append(edge)
        workflow["edges"] = new_edges
        workflows.append(workflow)

    patterns: list[dict[str, Any]] = []
    pattern_judgments = {
        str(item.get("pattern_id")): item
        for item in adjudication.get("pattern_judgments", [])
        if isinstance(item, dict) and item.get("pattern_id")
    }
    for raw in graph.get("patterns", []):
        if not isinstance(raw, dict):
            continue
        pattern = dict(raw)
        pattern["mandatory_actions"] = list(dict.fromkeys(mapped(value) for value in pattern.get("mandatory_actions", [])))
        pattern["optional_actions"] = list(dict.fromkeys(mapped(value) for value in pattern.get("optional_actions", [])))
        judgment = pattern_judgments.get(str(pattern.get("id")))
        if judgment:
            pattern["judge_decision"] = judgment.get("decision")
            pattern["judge_confidence"] = judgment.get("confidence")
            pattern["judge_rationale"] = judgment.get("rationale")
            pattern["missing_probes"] = list(judgment.get("missing_probes", []))
            if judgment.get("decision") != "promote_candidate":
                pattern["promotion_status"] = "deferred_by_semantic_judge"
        patterns.append(pattern)

    edges: list[dict[str, Any]] = []
    for raw_edge in graph.get("edges", []):
        if not isinstance(raw_edge, dict):
            continue
        edge = dict(raw_edge)
        edge["from"] = mapped(edge.get("from"))
        edge["to"] = mapped(edge.get("to"))
        if edge["from"] == edge["to"]:
            continue
        if edge not in edges:
            edges.append(edge)

    result = dict(graph)
    result["actions"] = sorted(actions, key=lambda row: str(row.get("id")))
    result["workflows"] = sorted(workflows, key=lambda row: str(row.get("id")))
    result["patterns"] = sorted(patterns, key=lambda row: str(row.get("id")))
    result["edges"] = edges
    result["semantic_adjudication"] = {
        "source": "codex-graph-adjudication",
        "accepted_action_merges": accepted_merges,
        "rejected_action_merges": rejected_merges,
        "action_aliases": aliases,
        "pattern_judgments": list(pattern_judgments.values()),
        "holdout_used": False,
        "promotion_gate": "no pattern is final before untouched holdout end-task validation",
    }
    result["summary"] = {
        **dict(graph.get("summary") or {}),
        "actions": len(result["actions"]),
        "grounded_actions": sum(1 for row in result["actions"] if row.get("grounded_semantics")),
        "action_merges_applied": len(accepted_merges),
        "workflows": len(result["workflows"]),
        "patterns": len(result["patterns"]),
        "patterns_promotable": sum(1 for row in result["patterns"] if row.get("promotion_status") == "candidate"),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--adjudication", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    adjudication = json.loads(args.adjudication.read_text(encoding="utf-8"))
    result = apply(graph, adjudication)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"actions": len(result["actions"]), "workflows": len(result["workflows"]), "patterns": len(result["patterns"]), "merges": result["summary"].get("action_merges_applied")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
