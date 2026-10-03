#!/usr/bin/env python3
"""Validate evidence gates before universal graph admission.

The validator is intentionally stricter than the JSON schema.  Schema validity
means that an extractor returned well-formed JSON; this command checks that the
episode is actually tied to a training candidate, a closed/merged or locally
pinned implementation, and implementation/test evidence.  It does not promote
the episode and does not modify the episode file.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


QUALIFYING_KINDS = {
    "implementation", "implementation_change", "diff", "commit", "call-site",
    "call_site", "test", "validation", "benchmark", "code_review",
}


def manifest_cases(path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise TypeError("manifest must contain cases")
    return {(str(item["repository"]), int(item["issue"])): dict(item) for item in cases}


def issue_for_episode(episode: dict[str, Any]) -> int:
    metadata = episode.get("metadata") or {}
    return int(metadata.get("issue", 0)) if isinstance(metadata, dict) else 0


def evidence_units(episode: dict[str, Any]) -> list[dict[str, Any]]:
    metadata = episode.get("metadata") or {}
    response = metadata.get("codex_response") if isinstance(metadata, dict) else None
    if isinstance(response, dict) and isinstance(response.get("evidence_units"), list):
        return [dict(item) for item in response["evidence_units"] if isinstance(item, dict)]
    return []


def resolution_gate(episode: dict[str, Any]) -> tuple[bool, str]:
    metadata = episode.get("metadata") or {}
    bundle = metadata.get("github_bundle") if isinstance(metadata, dict) else None
    if not isinstance(bundle, dict):
        return False, "missing github_bundle"
    if bundle.get("source") == "local_git_pinned_ref" and bundle.get("resolved_commit"):
        return True, "locally pinned implementation commit"
    issue = bundle.get("issue") or {}
    if issue.get("state") != "closed":
        return False, "issue is not verified closed"
    prs = bundle.get("linked_pull_requests") or []
    merged = [
        item for item in prs
        if isinstance(item, dict)
        and isinstance(item.get("pull_request"), dict)
        and item["pull_request"].get("merged") is True
    ]
    if not merged:
        return False, "no merged linked pull request"
    return True, "closed issue with merged linked pull request"


def validate(episodes: list[dict[str, Any]], cases: dict[tuple[str, int], dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for episode in episodes:
        repository = str(episode.get("repository", ""))
        issue = issue_for_episode(episode)
        key = (repository, issue)
        errors: list[str] = []
        case = cases.get(key)
        if case is None:
            errors.append("episode is absent from universal manifest")
        elif (str(case.get("role") or case.get("split")) != "train_candidate"
              or case.get("extraction_forbidden") or "holdout" in str(case.get("split"))):
            errors.append("holdout/non-training episode cannot enter graph admission")
        if key in seen:
            errors.append("duplicate repository/issue episode")
        seen.add(key)
        resolved, resolution_reason = resolution_gate(episode)
        if not resolved:
            errors.append(resolution_reason)
        units = evidence_units(episode)
        evidence_kinds = {
            str(item.get("kind", "")).strip().lower().replace(" ", "_")
            for item in units
        }
        if not evidence_kinds & {kind.replace("-", "_") for kind in QUALIFYING_KINDS}:
            errors.append("no qualifying implementation/call-site/test evidence")
        metadata = episode.get("metadata") or {}
        if metadata.get("source") == "direct_skill_package_extraction":
            from arex_skill_graph.direct_skill_extraction import project_episode_packages

            try:
                projection = project_episode_packages(episode)
                units = projection["evidence"]
                evidence_kinds = {item["kind"] for item in units}
                atomics, workflows = projection["actions"], projection["workflows"]
                errors = [error for error in errors if error != "no qualifying implementation/call-site/test evidence"]
            except (ValueError, OSError, KeyError):
                atomics, workflows = [], []
                errors.append("direct Skill package validation failed")
            rows.append({"episode_id": episode.get("episode_id"), "repository": repository,
                         "issue": issue, "category": str((case or {}).get("category") or ""),
                         "resolution_verified": resolved, "resolution_reason": resolution_reason,
                         "evidence_kinds": sorted(evidence_kinds), "atomics": len(atomics),
                         "workflows": len(workflows), "semantic_missing": 0,
                         "workflow_graph_missing": 0, "accepted_for_graph": not errors, "errors": errors})
            continue
        atomics = metadata.get("candidate_atomics", []) if isinstance(metadata, dict) else []
        workflows = metadata.get("candidate_workflows", []) if isinstance(metadata, dict) else []
        if not isinstance(atomics, list):
            atomics = []
            errors.append("candidate_atomics is not an array")
        if not isinstance(workflows, list):
            workflows = []
            errors.append("candidate_workflows is not an array")
        if not atomics:
            errors.append("no candidate Change Action was extracted")
        if not workflows:
            errors.append("no candidate Workflow was extracted")
        semantic_missing = 0
        workflow_missing = 0
        for item in atomics:
            semantic = item.get("semantic_action") if isinstance(item, dict) else None
            required = ("intent", "module_role", "operation", "pre_state", "post_state", "validation")
            if not isinstance(semantic, dict) or any(not str(semantic.get(field, "")).strip() for field in required):
                semantic_missing += 1
        for item in workflows:
            graph = item.get("workflow_graph") if isinstance(item, dict) else None
            if not isinstance(graph, dict) or not isinstance(graph.get("steps"), list):
                workflow_missing += 1
        if atomics and semantic_missing:
            errors.append(f"{semantic_missing} atomic candidate(s) lack semantic_action contract")
        if workflows and workflow_missing:
            errors.append(f"{workflow_missing} workflow candidate(s) lack workflow_graph")
        category = str((case or {}).get("category") or "")
        rows.append({
            "episode_id": episode.get("episode_id"),
            "repository": repository,
            "issue": issue,
            "category": category,
            "resolution_verified": resolved,
            "resolution_reason": resolution_reason,
            "evidence_kinds": sorted(evidence_kinds),
            "atomics": len(atomics),
            "workflows": len(workflows),
            "semantic_missing": semantic_missing,
            "workflow_graph_missing": workflow_missing,
            "accepted_for_graph": not errors,
            "errors": errors,
        })
    accepted = [row for row in rows if row["accepted_for_graph"]]
    return {
        "schema_version": "universal-episode-admission-report-v1",
        "episodes": len(episodes),
        "accepted_for_graph": len(accepted),
        "rejected": len(rows) - len(accepted),
        "accepted_by_repository": dict(Counter(row["repository"] for row in accepted)),
        "accepted_by_category": dict(Counter(row["category"] for row in accepted)),
        "rows": rows,
        "policy": {
            "closed_without_implementation_is_rejected": True,
            "holdout_is_rejected": True,
            "semantic_action_and_workflow_graph_required_when_candidates_exist": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--accepted-output", type=Path, help="optional JSON array containing only episodes accepted for graph admission")
    args = parser.parse_args()
    raw = json.loads(args.episodes.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError("episodes must be an array")
    report = validate(raw, manifest_cases(args.manifest))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.accepted_output:
        accepted_ids = {str(row.get("episode_id")) for row in report["rows"] if row.get("accepted_for_graph")}
        accepted = [episode for episode in raw if str(episode.get("episode_id")) in accepted_ids]
        args.accepted_output.parent.mkdir(parents=True, exist_ok=True)
        args.accepted_output.write_text(json.dumps(accepted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("episodes", "accepted_for_graph", "rejected")}, ensure_ascii=False))
    return 0 if report["rejected"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
