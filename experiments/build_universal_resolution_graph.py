#!/usr/bin/env python3
"""Build an evidence-preserving ChangeAction -> Workflow -> Pattern graph.

This is the deterministic structural stage of the corrected meta-skill.  It
does not pretend to solve semantic equivalence with keywords.  When an
extractor supplies a ``semantic_action`` object, its fields form the primary
fingerprint; otherwise the record remains a low-confidence candidate and is
kept separate by episode.  An LLM may adjudicate the small peer sets later.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from collections.abc import Iterable
from itertools import pairwise
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "experiments" / "manifests" / "universal-issue-manifest-v1.json"

OPERATIONS = (
    "normalize",
    "adapt",
    "reconcile",
    "guard",
    "route",
    "map",
    "propagate",
    "validate",
    "serialize",
    "restore",
    "preserve",
    "bound",
    "cancel",
    "retry",
    "isolate",
    "authorize",
    "register",
    "discover",
    "load",
    "reload",
    "coordinate",
    "instrument",
    "classify",
    "deduplicate",
    "aggregate",
    "repair",
)


def _stable(prefix: str, *values: object) -> str:
    raw = "\x1f".join(str(value) for value in values)
    return f"{prefix}:{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]}"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _normal(value: Any) -> str:
    text = _text(value).lower()
    text = re.sub(r"`[^`]+`", "<code>", text)
    text = re.sub(r"https?://\S+", "<url>", text)
    text = re.sub(r"\b[0-9a-f]{7,40}\b", "<sha>", text)
    text = re.sub(r"(?:issue|pr|pull request)\s*#?\d+", "<ref>", text)
    text = re.sub(r"\b\d+(?:\.\d+)+\b", "<version>", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _infer_operation(text: str) -> str:
    lowered = _normal(text)
    for operation in OPERATIONS:
        if re.search(rf"\b{re.escape(operation)}(?:s|ed|ing)?\b", lowered):
            return operation
    return "change"


def _manifest_cases(manifest: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    cases = manifest.get("cases", manifest if isinstance(manifest, list) else [])
    return {(str(item["repository"]), int(item["issue"])): dict(item) for item in cases}


def _episode_issue(episode: dict[str, Any]) -> int:
    metadata = episode.get("metadata") or {}
    if isinstance(metadata, dict) and metadata.get("issue") is not None:
        return int(metadata["issue"])
    match = re.search(r"#(\d+)", _text(episode.get("episode_id")))
    return int(match.group(1)) if match else 0


def _candidate_items(episode: dict[str, Any], key: str) -> list[dict[str, Any]]:
    metadata = episode.get("metadata") or {}
    if not isinstance(metadata, dict):
        return []
    value = metadata.get(key)
    if value is None and isinstance(metadata.get("codex_response"), dict):
        value = metadata["codex_response"].get(key)
    return (
        [dict(item) for item in value if isinstance(item, dict)] if isinstance(value, list) else []
    )


def _semantic_action(
    item: dict[str, Any], category: str, episode: dict[str, Any]
) -> tuple[dict[str, Any], bool]:
    semantic = item.get("semantic_action") or item.get("semantic") or {}
    if not isinstance(semantic, dict):
        semantic = {}
    description = _text(item.get("description") or item.get("summary") or item.get("name"))
    intent = _text(semantic.get("intent")) or description
    module_role = _text(semantic.get("module_role")) or f"unresolved-owner:{category}"
    operation = _text(semantic.get("operation")) or _infer_operation(description)
    pre_state = _text(semantic.get("pre_state")) or "unknown"
    post_state = _text(semantic.get("post_state")) or "unknown"
    validation = _text(semantic.get("validation")) or "unknown"
    parameters = semantic.get("parameters") if isinstance(semantic.get("parameters"), list) else []
    evidence_ids = (
        semantic.get("evidence_ids")
        if isinstance(semantic.get("evidence_ids"), list)
        else item.get("evidence_ids", [])
    )
    grounded = bool(semantic) and all(
        value not in {"", "unknown"}
        for value in (intent, module_role, operation, pre_state, post_state, validation)
    )
    action = {
        "intent": intent,
        "module_role": module_role,
        "operation": operation,
        "pre_state": pre_state,
        "post_state": post_state,
        "validation": validation,
        "parameters": [_text(value) for value in parameters],
        "evidence_ids": [_text(value) for value in evidence_ids if _text(value)],
        "source_name": _text(item.get("name") or item.get("title")),
        "description": description,
        "grounded_semantics": grounded,
    }
    return action, grounded


def _action_fingerprint(action: dict[str, Any], category: str, episode_id: str) -> tuple[str, bool]:
    # Unknown semantic fields must not collapse unrelated episode-local actions.
    grounded = bool(action.get("grounded_semantics"))
    if not grounded:
        return (
            _stable(
                "episode-action", episode_id, action.get("source_name"), action.get("description")
            ),
            False,
        )
    key = (
        category,
        _normal(action.get("module_role")),
        _normal(action.get("operation")),
        _normal(action.get("post_state")),
        _normal(action.get("validation")),
    )
    return (_stable("semantic-action", *key), True)


def _workflow_steps(
    item: dict[str, Any], atomic_by_name: dict[str, str], action_ids: list[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    graph = item.get("workflow_graph") or {}
    steps: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    if isinstance(graph, dict) and isinstance(graph.get("steps"), list):
        for index, raw in enumerate(graph["steps"]):
            if not isinstance(raw, dict):
                continue
            name = _text(raw.get("action_name") or raw.get("action") or raw.get("name"))
            action_id = atomic_by_name.get(name)
            if action_id is None and name:
                raise ValueError(f"explicit Workflow step references unknown Action: {name}")
            if action_id is None and not name and index < len(action_ids):
                action_id = action_ids[index]
            if action_id:
                required = raw.get("required")
                if not isinstance(required, bool):
                    required = not bool(raw.get("optional", False))
                depends_on = (
                    raw.get("depends_on") if isinstance(raw.get("depends_on"), list) else []
                )
                steps.append(
                    {
                        "step_id": f"step-{index + 1}",
                        "action_id": action_id,
                        "action_name": name,
                        "role": _text(raw.get("role")) or "implement",
                        "required": required,
                        "optional": not required,
                        "depends_on": [_text(value) for value in depends_on if _text(value)],
                        "condition": _text(raw.get("condition")),
                        "validation": _text(raw.get("validation")),
                    }
                )
        raw_edges = graph.get("edges") if isinstance(graph.get("edges"), list) else []
        by_step = {step["step_id"]: step for step in steps}
        by_name = {
            (_text(raw.get("action_name")) if isinstance(raw, dict) else ""): step["step_id"]
            for raw, step in zip(graph.get("steps", []), steps)
        }
        for raw in raw_edges:
            if not isinstance(raw, dict):
                continue
            source = _text(raw.get("from"))
            target = _text(raw.get("to"))
            source = (
                by_step.get(source, {}).get("step_id", by_name.get(source, source))
                if isinstance(by_step.get(source), dict)
                else by_name.get(source, source)
            )
            target = (
                by_step.get(target, {}).get("step_id", by_name.get(target, target))
                if isinstance(by_step.get(target), dict)
                else by_name.get(target, target)
            )
            if source in by_step and target in by_step:
                edges.append(
                    {"from": source, "to": target, "type": _text(raw.get("type")) or "requires"}
                )
    if not steps:
        for index, action_id in enumerate(action_ids):
            steps.append(
                {
                    "step_id": f"step-{index + 1}",
                    "action_id": action_id,
                    "action_name": "",
                    "role": "implement",
                    "required": True,
                    "optional": False,
                    "depends_on": [],
                    "condition": "",
                    "validation": "",
                }
            )
    if not edges:
        edges = [
            {"from": left["step_id"], "to": right["step_id"], "type": "requires"}
            for left, right in pairwise(steps)
        ]
    return steps, edges


def build(
    episodes: Iterable[dict[str, Any]], manifest: dict[str, Any], *, min_pattern_support: int = 2
) -> dict[str, Any]:
    cases = _manifest_cases(manifest)
    actions: dict[str, dict[str, Any]] = {}
    workflows: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_episode_keys: set[tuple[str, int]] = set()
    for episode in episodes:
        repository = _text(episode.get("repository"))
        issue = _episode_issue(episode)
        key = (repository, issue)
        case = cases.get(key)
        if case is None:
            rejected.append(
                {
                    "episode_id": episode.get("episode_id"),
                    "reason": "episode is absent from universal manifest",
                    "key": key,
                }
            )
            continue
        case_role = str(case.get("role") or case.get("split") or "")
        if case_role != "train_candidate":
            rejected.append(
                {
                    "episode_id": episode.get("episode_id"),
                    "reason": "holdout or non-training episode refused by default",
                    "key": key,
                }
            )
            continue
        if key in seen_episode_keys:
            rejected.append(
                {"episode_id": episode.get("episode_id"), "reason": "duplicate episode key"}
            )
            continue
        seen_episode_keys.add(key)
        category = _text(case.get("category"))
        episode_id = _text(episode.get("episode_id")) or f"episode:{repository}#{issue}"
        atomics = _candidate_items(episode, "candidate_atomics")
        by_name: dict[str, str] = {}
        local_action_ids: list[str] = []
        local_action_map: dict[str, str] = {}
        for index, item in enumerate(atomics):
            action, grounded = _semantic_action(item, category, episode)
            key_id, _semantic_key = _action_fingerprint(action, category, episode_id)
            if key_id not in actions:
                actions[key_id] = {
                    "id": key_id,
                    "node_type": "change_action",
                    "category": category,
                    **action,
                    "supporting_episodes": [],
                    "supporting_repositories": [],
                    "aliases": [],
                    "status": "candidate" if grounded else "episode_local_candidate",
                }
            record = actions[key_id]
            record["supporting_episodes"] = sorted(
                set(record["supporting_episodes"]) | {episode_id}
            )
            record["supporting_repositories"] = sorted(
                set(record["supporting_repositories"]) | {repository}
            )
            if action.get("source_name") and action["source_name"] != record.get("source_name"):
                record["aliases"] = sorted(set(record.get("aliases", [])) | {action["source_name"]})
            local_action_ids.append(key_id)
            name = _text(item.get("name") or item.get("title"))
            if name:
                by_name[name] = key_id
                local_action_map[name] = key_id
            edges.append({"from": key_id, "to": f"evidence:{episode_id}", "type": "evidenced_by"})
        workflow_items = _candidate_items(episode, "candidate_workflows")
        if not workflow_items:
            workflow_items = [
                {
                    "name": f"workflow-{episode_id}",
                    "description": _text(episode.get("after")),
                    "atomic_names": list(by_name),
                }
            ]
        for index, item in enumerate(workflow_items):
            names = [_text(value) for value in item.get("atomic_names", []) if _text(value)]
            action_ids = [by_name[name] for name in names if name in by_name] or list(
                dict.fromkeys(local_action_ids)
            )
            steps, workflow_edges = _workflow_steps(item, by_name, action_ids)
            workflow_id = _stable("workflow", episode_id, index, item.get("name"))
            workflow = {
                "id": workflow_id,
                "node_type": "issue_workflow",
                "category": category,
                "repository": repository,
                "issue": issue,
                "episode_id": episode_id,
                "name": _text(item.get("name")) or workflow_id,
                "title": _text(item.get("title") or item.get("name")) or workflow_id,
                "description": _text(item.get("description")),
                "goal": _text((item.get("workflow_graph") or {}).get("goal"))
                if isinstance(item.get("workflow_graph"), dict)
                else _text(episode.get("after")),
                "when_to_use": list((item.get("workflow_graph") or {}).get("when_to_use", []))
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "anti_goals": list((item.get("workflow_graph") or {}).get("anti_goals", []))
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "not_applicable_when": list(
                    (item.get("workflow_graph") or {}).get("not_applicable_when", [])
                )
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "inputs": list((item.get("workflow_graph") or {}).get("inputs", []))
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "entry_state": _text((item.get("workflow_graph") or {}).get("entry_state"))
                if isinstance(item.get("workflow_graph"), dict)
                else _text(episode.get("before")),
                "exit_state": _text((item.get("workflow_graph") or {}).get("exit_state"))
                if isinstance(item.get("workflow_graph"), dict)
                else _text(episode.get("after")),
                "steps": steps,
                "edges": workflow_edges,
                "validation_ladder": list(
                    (item.get("workflow_graph") or {}).get("validation_ladder", [])
                )
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "stop_conditions": list(
                    (item.get("workflow_graph") or {}).get("stop_conditions", [])
                )
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "unresolved_or_deferred": list(
                    (item.get("workflow_graph") or {}).get("unresolved_or_deferred", [])
                )
                if isinstance(item.get("workflow_graph"), dict)
                else [],
                "evidence_ids": [
                    _text(value)
                    for value in item.get("evidence_ids", episode.get("evidence_ids", []))
                    if _text(value)
                ],
                "supporting_repositories": [repository],
                "source_case": f"{repository}#{issue}",
                "skill_contract": dict(item.get("skill_contract") or {}),
            }
            package = (episode.get("metadata", {}).get("skill_packages") or {}).get(workflow_id)
            workflow["extraction_status"] = "admitted_candidate" if package else "structured_only"
            if package:
                workflow["skill_package"] = dict(package)
            workflows.append(workflow)
            for edge in workflow_edges:
                step_by_id = {step["step_id"]: step for step in steps}
                source = step_by_id.get(edge["from"])
                target = step_by_id.get(edge["to"])
                if source and target:
                    edges.append(
                        {
                            "from": source["action_id"],
                            "to": target["action_id"],
                            "type": edge["type"],
                            "workflow_id": workflow_id,
                            "workflow_step_from": edge["from"],
                            "workflow_step_to": edge["to"],
                        }
                    )

    workflows_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for workflow in workflows:
        workflows_by_category[workflow["category"]].append(workflow)
    patterns: list[dict[str, Any]] = []
    for category, group in sorted(workflows_by_category.items()):
        support_by_action: dict[str, set[str]] = defaultdict(set)
        for workflow in group:
            for step in workflow["steps"]:
                support_by_action[step["action_id"]].add(workflow["id"])
        mandatory = sorted(
            action_id
            for action_id, support in support_by_action.items()
            if len(support) >= min_pattern_support
            and len(
                {
                    next((w["repository"] for w in group if w["id"] == workflow_id), "")
                    for workflow_id in support
                }
            )
            >= 2
        )
        optional = sorted(
            action_id
            for action_id, support in support_by_action.items()
            if action_id not in mandatory and len(support) >= min_pattern_support
        )
        repositories = sorted({workflow["repository"] for workflow in group})
        patterns.append(
            {
                "id": _stable("pattern", category),
                "node_type": "resolution_pattern",
                "category": category,
                "intent": f"Resolve {category.replace('-', ' ')} through a contract-first, evidence-validated change chain.",
                "mandatory_actions": mandatory,
                "optional_actions": optional,
                "workflow_template": [],
                "ordering_constraints": [],
                "decision_points": [],
                "invariants": [],
                "validation_ladder": [],
                "known_failure_modes": [],
                "supporting_workflows": sorted(workflow["id"] for workflow in group),
                "supporting_repositories": repositories,
                "counterexamples": [],
                "confidence": 0.0,
                "promotion_status": "candidate"
                if len(repositories) >= 2 and len(mandatory) >= 1
                else "insufficient-structural-support",
                "held_out_results": [],
                "extraction_method": "structural-action-fingerprint-v1; semantic judge required before promotion",
            }
        )
        for action_id in mandatory:
            edges.append(
                {"from": _stable("pattern", category), "to": action_id, "type": "declares_step"}
            )
        for workflow in group:
            edges.append(
                {"from": _stable("pattern", category), "to": workflow["id"], "type": "supported_by"}
            )
    return {
        "schema_version": "universal-resolution-graph-v1",
        "extraction_policy": {
            "training_only": True,
            "holdout_refused": True,
            "unknown_semantics_are_not_deduplicated": True,
            "pattern_promotion_requires_llm_judge_and_holdout": True,
        },
        "actions": sorted(actions.values(), key=lambda item: item["id"]),
        "workflows": sorted(workflows, key=lambda item: item["id"]),
        "patterns": sorted(patterns, key=lambda item: item["id"]),
        "edges": edges,
        "rejected": rejected,
        "summary": {
            "episodes_input": len(list(episodes))
            if not isinstance(episodes, list)
            else len(episodes),
            "episodes_used": len(seen_episode_keys),
            "actions": len(actions),
            "grounded_actions": sum(
                1 for action in actions.values() if action["grounded_semantics"]
            ),
            "workflows": len(workflows),
            "patterns": len(patterns),
            "patterns_with_cross_repository_support": sum(
                1 for pattern in patterns if len(pattern["supporting_repositories"]) >= 2
            ),
            "rejected": len(rejected),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-pattern-support", type=int, default=2)
    args = parser.parse_args()
    episodes = json.loads(args.episodes.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(episodes, list):
        raise TypeError("episodes must be a JSON array")
    result = build(episodes, manifest, min_pattern_support=max(2, args.min_pattern_support))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(args.output), **result["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
