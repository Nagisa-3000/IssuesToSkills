#!/usr/bin/env python3
"""Audit Action reuse, Workflow fragments, and Action granularity.

The graph builder intentionally uses a conservative fingerprint.  This report
explains *why* two semantically nearby Actions were not merged and separates
real Action reuse from reusable Workflow-role skeletons.  It is an analysis
tool, not an automatic merge tool: a matching text or operation never proves
that two Actions share a state contract or validation oracle.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re
from typing import Any, Iterable


CONTRACT_FIELDS = ("pre_state", "post_state", "validation")
OPERATION_WORDS = (
    "normalize", "adapt", "reconcile", "guard", "route", "map", "propagate",
    "validate", "serialize", "restore", "preserve", "bound", "cancel", "retry",
    "isolate", "authorize", "register", "discover", "load", "reload", "coordinate",
    "instrument", "classify", "deduplicate", "aggregate", "repair", "compose",
)
ROLE_VALUES = {
    "diagnose", "establish-contract", "implement", "reconcile", "validate", "repair",
}


def text(value: Any) -> str:
    return str(value or "").strip()


def normal(value: Any) -> str:
    value = text(value).lower()
    value = re.sub(r"`[^`]+`", "<code>", value)
    value = re.sub(r"https?://\S+", "<url>", value)
    value = re.sub(r"\b[0-9a-f]{7,40}\b", "<sha>", value)
    value = re.sub(r"(?:issue|pr|pull request)\s*#?\d+", "<ref>", value)
    value = re.sub(r"\b\d+(?:\.\d+)+\b", "<version>", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def operation_tokens(value: Any) -> set[str]:
    lowered = normal(value)
    return {
        word for word in OPERATION_WORDS
        if re.search(rf"\b{re.escape(word)}(?:s|ed|ing|ation|al|ions)?\b", lowered)
    }


def action_key(action: dict[str, Any]) -> tuple[str, str]:
    return (normal(action.get("module_role")), normal(action.get("operation")))


def contract_value(action: dict[str, Any], field: str) -> str:
    return normal(action.get(field))


def source_repositories(action: dict[str, Any], workflows_by_action: dict[str, list[dict[str, Any]]]) -> list[str]:
    repositories = action.get("supporting_repositories")
    if isinstance(repositories, list) and repositories:
        return sorted({text(item) for item in repositories if text(item)})
    return sorted({text(item.get("repository")) for item in workflows_by_action.get(text(action.get("id")), []) if text(item.get("repository"))})


def action_grain(action: dict[str, Any]) -> dict[str, Any]:
    description = text(action.get("description"))
    # State predicates often contain words such as "restore", "preserve", or
    # "route" even when the Action is one resolver operation.  Use the
    # human-facing operation description for the split signal and retain the
    # broader semantic tokens only as context.
    description_tokens = operation_tokens(description)
    semantic_text = " ".join(text(action.get(field)) for field in ("intent", "description", "pre_state", "post_state"))
    semantic_tokens = operation_tokens(semantic_text)
    declared = normal(action.get("operation"))
    secondary = sorted(token for token in description_tokens if token != declared)
    clauses = len(re.findall(r"\b(?:and|then|while|without|only when)\b|;", description.lower()))
    grounded = bool(action.get("grounded_semantics"))
    # This is deliberately a review signal.  A validation action may mention
    # several paths but still have one oracle, so it is never split solely by
    # this heuristic.
    # A validation Action normally covers several test paths with one oracle;
    # mentioning those paths is not evidence that the validation Action should
    # be split into implementation Actions.
    split_signal = declared != "validate" and len(secondary) >= 2 and clauses >= 1
    if not grounded:
        verdict = "unresolved"
        reason = "semantic contract is not grounded"
    elif split_signal:
        verdict = "split-review"
        reason = "description contains multiple finite-operation signals; inspect independent postconditions/oracles"
    else:
        verdict = "atomic-review"
        reason = "one declared operation with one explicit semantic contract; no independent split is proven"
    return {
        "id": text(action.get("id")),
        "verdict": verdict,
        "reason": reason,
        "declared_operation": declared,
        "operation_signals": sorted(semantic_tokens),
        "description_operation_signals": sorted(description_tokens),
        "secondary_operation_signals": secondary,
        "clause_signal_count": clauses,
    }


def compare_actions(left: dict[str, Any], right: dict[str, Any], workflows_by_action: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    left_key = action_key(left)
    right_key = action_key(right)
    same_module = left_key[0] == right_key[0]
    same_operation = left_key[1] == right_key[1]
    same_contract = {field: contract_value(left, field) == contract_value(right, field) for field in CONTRACT_FIELDS}
    reasons: list[str] = []
    if not same_module:
        reasons.append("semantic-owner-differs")
    if not same_operation:
        reasons.append("finite-operation-differs")
    for field, same in same_contract.items():
        if not same:
            reasons.append({"pre_state": "precondition-differs", "post_state": "postcondition-differs", "validation": "oracle-differs"}[field])
    if same_module and same_operation and all(same_contract.values()):
        decision = "safe-reuse-candidate"
    elif same_module and same_operation:
        decision = "same-owner-operation-but-contract-diverges"
    elif same_operation:
        decision = "same-operation-different-owner"
    else:
        decision = "not-a-peer"
    return {
        "left": text(left.get("id")),
        "right": text(right.get("id")),
        "left_repositories": source_repositories(left, workflows_by_action),
        "right_repositories": source_repositories(right, workflows_by_action),
        "decision": decision,
        "reasons": reasons,
        "same_contract_fields": same_contract,
    }


def action_pairs(actions: Iterable[dict[str, Any]], workflows_by_action: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    items = list(actions)
    for left, right in combinations(items, 2):
        left_repos = set(source_repositories(left, workflows_by_action))
        right_repos = set(source_repositories(right, workflows_by_action))
        if not left_repos or not right_repos or left_repos.isdisjoint(right_repos):
            rows.append(compare_actions(left, right, workflows_by_action))
    return rows


def workflow_role_segments(workflows: list[dict[str, Any]], minimum_length: int = 2) -> list[dict[str, Any]]:
    by_signature: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for workflow in workflows:
        steps = workflow.get("steps") if isinstance(workflow.get("steps"), list) else []
        roles = [text(step.get("role")) for step in steps if text(step.get("role")) in ROLE_VALUES]
        for length in range(minimum_length, len(roles) + 1):
            for start in range(0, len(roles) - length + 1):
                signature = tuple(roles[start:start + length])
                by_signature[signature].append({
                    "workflow_id": text(workflow.get("id")),
                    "repository": text(workflow.get("repository")),
                    "issue": workflow.get("issue"),
                    "category": text(workflow.get("category")),
                    "action_ids": [text(step.get("action_id")) for step in steps[start:start + length]],
                })
    rows: list[dict[str, Any]] = []
    for signature, occurrences in sorted(by_signature.items(), key=lambda item: (len(item[0]), item[0])):
        repositories = sorted({text(item.get("repository")) for item in occurrences if text(item.get("repository"))})
        workflows_seen = sorted({text(item.get("workflow_id")) for item in occurrences if text(item.get("workflow_id"))})
        categories = sorted({text(item.get("category")) for item in occurrences if text(item.get("category"))})
        category_repository_support: dict[str, list[str]] = {}
        for category in categories:
            category_repository_support[category] = sorted({
                text(item.get("repository"))
                for item in occurrences
                if text(item.get("category")) == category and text(item.get("repository"))
            })
        same_category_support = {
            category: repos
            for category, repos in category_repository_support.items()
            if len(repos) >= 2
        }
        if len(repositories) < 2:
            continue
        rows.append({
            "segment_roles": list(signature),
            "kind": "workflow-role-skeleton",
            "supporting_repositories": repositories,
            "supporting_categories": categories,
            "category_repository_support": category_repository_support,
            "same_category_cross_repository_support": same_category_support,
            "reuse_scope": (
                "same-category-cross-repository"
                if same_category_support else
                "cross-category-skeleton"
            ),
            "supporting_workflows": workflows_seen,
            "occurrences": occurrences,
            "action_reuse": False,
            "interpretation": (
                "Reusable control-flow skeleton only; each step still needs a repository-specific Action contract."
                if not same_category_support else
                "The role sequence recurs within at least one category across repositories, but each step still needs a repository-specific Action contract."
            ),
        })
    # A longer segment subsumes its contiguous shorter fragments.  Keep the
    # longest occurrence for a readable report while retaining support counts.
    rows.sort(key=lambda row: (-len(row["segment_roles"]), row["segment_roles"]))
    kept: list[dict[str, Any]] = []
    for row in rows:
        if not any(tuple(row["segment_roles"]) == tuple(other["segment_roles"]) for other in kept):
            kept.append(row)
    return kept


def audit(graph: dict[str, Any]) -> dict[str, Any]:
    actions = [dict(item) for item in graph.get("actions", []) if isinstance(item, dict)]
    workflows = [dict(item) for item in graph.get("workflows", []) if isinstance(item, dict)]
    workflows_by_action: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for workflow in workflows:
        for step in workflow.get("steps", []) if isinstance(workflow.get("steps"), list) else []:
            action_id = text(step.get("action_id"))
            if action_id:
                workflows_by_action[action_id].append(workflow)

    pairs = action_pairs(actions, workflows_by_action)
    pair_counts = Counter(row["decision"] for row in pairs)
    coarse_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for action in actions:
        coarse_groups[action_key(action)].append(action)
    shared_actions = []
    for action in actions:
        action_id = text(action.get("id"))
        support = workflows_by_action.get(action_id, [])
        repositories = sorted({text(item.get("repository")) for item in support if text(item.get("repository"))})
        if len(repositories) >= 2:
            shared_actions.append({
                "action_id": action_id,
                "supporting_repositories": repositories,
                "supporting_workflows": sorted({text(item.get("id")) for item in support}),
                "decision": "already-reused-action",
            })

    grain = [action_grain(action) for action in actions]
    split_count = sum(item["verdict"] == "split-review" for item in grain)
    same_owner_contract_divergence = pair_counts["same-owner-operation-but-contract-diverges"]
    same_operation_different_owner = pair_counts["same-operation-different-owner"]
    safe_reuse = pair_counts["safe-reuse-candidate"]
    role_segments = workflow_role_segments(workflows)
    same_category_role_segments = sum(
        bool(item.get("same_category_cross_repository_support"))
        for item in role_segments
    )
    cross_category_role_segments = sum(
        len(item.get("supporting_categories", [])) >= 2
        for item in role_segments
    )
    if split_count > max(1, len(actions) // 3):
        hypothesis = "action-grain-too-coarse-is-plausible"
        hypothesis_reason = "many Actions contain multiple finite-operation signals; inspect their independent postconditions and oracles before factoring"
    elif same_owner_contract_divergence > 0 and safe_reuse == 0:
        hypothesis = "semantic-contract-divergence-is-the-primary-blocker"
        hypothesis_reason = "nearby operations share an owner/verb but differ in pre-state, post-state, or validation oracle; splitting would not create a shared Action"
    elif same_operation_different_owner > 0 and role_segments:
        hypothesis = "workflow-skeleton-reuses-but-action-contracts-do-not"
        hypothesis_reason = "the same lifecycle roles recur across repositories, while equal finite verbs belong to different semantic owners; this supports reusable Workflow templates, not Action merging"
    elif safe_reuse > 0:
        hypothesis = "some-action-reuse-is-supported"
        hypothesis_reason = "at least one cross-repository pair has the same owner, finite operation, state contract, and validation oracle"
    else:
        hypothesis = "insufficient-cross-repository-action-coverage"
        hypothesis_reason = "no cross-repository semantic peers were found; collect more episodes before deciding whether granularity is the cause"

    return {
        "schema_version": "action-factorization-audit-v1",
        "policy": {
            "merge_requires": ["same semantic owner", "same finite operation", "same pre-state", "same post-state", "same validation oracle"],
            "role_skeleton_is_not_action_reuse": True,
            "split_is_review_signal_only": True,
        },
        "summary": {
            "actions": len(actions),
            "workflows": len(workflows),
            "cross_repository_action_pairs": len(pairs),
            "safe_reuse_candidates": safe_reuse,
            "same_owner_operation_contract_divergences": same_owner_contract_divergence,
            "same_operation_different_owner_pairs": same_operation_different_owner,
            "already_reused_actions": len(shared_actions),
            "split_review_signals": split_count,
            "workflow_role_segments": len(role_segments),
            "same_category_workflow_role_segments": same_category_role_segments,
            "cross_category_workflow_role_segments": cross_category_role_segments,
            "hypothesis": hypothesis,
            "hypothesis_reason": hypothesis_reason,
        },
        "pair_decision_counts": dict(sorted(pair_counts.items())),
        "action_grain": grain,
        "coarse_action_groups": [
            {
                "module_role": key[0],
                "operation": key[1],
                "action_ids": [text(item.get("id")) for item in group],
                "repositories": sorted({repo for item in group for repo in source_repositories(item, workflows_by_action)}),
            }
            for key, group in sorted(coarse_groups.items())
        ],
        "cross_repository_pair_analysis": pairs,
        "already_reused_actions": shared_actions,
        "workflow_role_segments": workflow_role_segments(workflows),
        "interpretation": {
            "action_reuse": "An Action is reusable only when its semantic owner, finite operation, state transition, and validation oracle all survive substitution into the other repository.",
            "workflow_reuse": "A repeated role sequence such as establish-contract -> reconcile -> validate is a reusable Workflow fragment, but it is a template over new Actions rather than evidence that the Actions themselves are interchangeable.",
            "granularity": "A split is justified only when a candidate contains independently testable finite operations with separate postconditions or validation oracles. Different paths, providers, or filenames alone are not a reason to split.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    report = audit(graph)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), **report["summary"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
