#!/usr/bin/env python3
"""Compile a validated Resolution Pattern into a candidate Agent Skill package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

PACKAGE_SCHEMA = "resolution-skill-package-v1"
PROVENANCE_SCHEMA = "resolution-skill-provenance-v1"
DEFAULT_SKILL_NAME = "adapt-provider-interface-boundaries"
DEFAULT_DESCRIPTION = (
    "Diagnose and repair compatible-provider routing or request-shape failures by "
    "establishing provider identity and precedence before changing only the owning boundary."
)
REQUIRED_PATTERN_LISTS = (
    "when_to_use",
    "anti_goals",
    "not_applicable_when",
    "action_template",
    "validation_ladder",
    "workflow_realizations",
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, value: Any) -> None:
    _write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    _write_text(
        path,
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows),
    )


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _code(value: object) -> str:
    return f"`{value}`"


def _bullets(items: Sequence[object], *, empty: str = "None recorded.") -> str:
    values = [f"- {str(item).strip()}" for item in items if str(item).strip()]
    return "\n".join(values) if values else f"- {empty}"


def _numbered(items: Sequence[object], *, empty: str = "None recorded.") -> str:
    values = [
        f"{index}. {str(item).strip()}"
        for index, item in enumerate(items, start=1)
        if str(item).strip()
    ]
    return "\n".join(values) if values else f"1. {empty}"


def _index(items: object, label: str) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        raise TypeError(f"graph {label} records must be a list")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, Mapping) or not isinstance(item.get("id"), str):
            raise TypeError(f"every {label} record must have a string id")
        item_id = str(item["id"])
        if item_id in result:
            raise ValueError(f"duplicate {label} id: {item_id}")
        result[item_id] = dict(item)
    return result


def _holdout_summary(
    cases_path: Path | None,
    qualification_path: Path | None,
    training_repositories: set[str],
) -> dict[str, Any]:
    cases: list[Mapping[str, Any]] = []
    if cases_path is not None:
        raw = _read_json(cases_path)
        if not isinstance(raw, list):
            raise TypeError("holdout case manifest must be a JSON array")
        cases = [item for item in raw if isinstance(item, Mapping)]

    qualification_rows: list[Mapping[str, Any]] = []
    if qualification_path is not None:
        raw = _read_json(qualification_path)
        rows = raw.get("rows") if isinstance(raw, Mapping) else None
        if not isinstance(rows, list):
            raise TypeError("qualification report must contain a rows array")
        qualification_rows = [item for item in rows if isinstance(item, Mapping)]

    repositories = sorted(
        {str(item["repository"]) for item in cases if isinstance(item.get("repository"), str)}
    )
    overlap = sorted(training_repositories.intersection(repositories))
    return {
        "case_ids": sorted(
            str(item.get("id") or item.get("case_id"))
            for item in cases
            if item.get("id") or item.get("case_id")
        ),
        "repositories": repositories,
        "repository_disjoint": not overlap,
        "training_repository_overlap": overlap,
        "oracle_qualified": bool(qualification_rows)
        and all(bool(item.get("oracle_qualified")) for item in qualification_rows),
        "qualified": bool(qualification_rows)
        and all(bool(item.get("qualified")) for item in qualification_rows),
        "agent_pair_status": "pending",
    }


def _retrieval_summary(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"status": "unavailable", "arms": {}}
    raw = _read_json(path)
    aggregate = raw.get("aggregate") if isinstance(raw, Mapping) else None
    if not isinstance(aggregate, Mapping):
        raise TypeError("retrieval evaluation must contain an aggregate object")
    arms: dict[str, dict[str, Any]] = {}
    for name, metrics in sorted(aggregate.items()):
        if not isinstance(metrics, Mapping):
            continue
        arms[str(name)] = {
            key: metrics.get(key)
            for key in (
                "cases",
                "recall_at_k",
                "mrr",
                "mean_first_relevant_rank",
                "mean_latency_ms",
                "mean_seed_count",
                "mean_expanded_count",
            )
        }
    return {
        "status": "recorded",
        "hnsw_available": bool(raw.get("hnsw_available")),
        "arms": arms,
    }


def _agent_evaluation_summary(
    evaluation_path: Path | None,
    aggregate_path: Path | None,
) -> dict[str, Any]:
    if evaluation_path is None:
        return {
            "status": "pending",
            "lifecycle_decision": "retain_candidate",
            "promotion_supported": False,
            "promotion_blockers": ["paired_agent_evaluation_pending"],
        }
    document = _read_json(evaluation_path)
    evaluations = document.get("evaluations") if isinstance(document, Mapping) else None
    if not isinstance(evaluations, list) or not evaluations:
        raise TypeError("weighted agent evaluation must contain evaluations")
    evaluation = evaluations[0]
    if not isinstance(evaluation, Mapping):
        raise TypeError("weighted agent evaluation row must be an object")
    arms = evaluation.get("arms") if isinstance(evaluation.get("arms"), Mapping) else {}
    arm_summary: dict[str, Any] = {}
    concerns: dict[str, list[str]] = {}
    for arm in ("no_skill", "guided"):
        value = arms.get(arm) if isinstance(arms, Mapping) else None
        if not isinstance(value, Mapping):
            continue
        arm_summary[arm] = {
            key: value.get(key)
            for key in (
                "task_solved",
                "correctness",
                "code_quality",
                "overall_score",
                "usage_tokens",
                "wall_seconds",
            )
        }
        judge = value.get("judge")
        if isinstance(judge, Mapping):
            concerns[arm] = _strings(judge.get("concerns"))

    aggregate: Mapping[str, Any] = {}
    if aggregate_path is not None:
        raw = _read_json(aggregate_path)
        if not isinstance(raw, Mapping):
            raise TypeError("weighted evaluation aggregate must be an object")
        aggregate = raw
    promotion_supported = bool(aggregate.get("pattern_promotion_supported"))
    eligible = bool(evaluation.get("eligible_for_causal_comparison"))
    both_solved = all(
        bool(arm_summary.get(arm, {}).get("task_solved")) for arm in ("no_skill", "guided")
    )
    status = "pass_directional" if eligible and both_solved else "failed_or_descriptive"
    return {
        "status": status,
        "lifecycle_decision": "promote" if promotion_supported else "retain_candidate",
        "promotion_supported": promotion_supported,
        "promotion_blockers": _strings(aggregate.get("promotion_blockers"))
        or (["independent_holdout_aggregate_unavailable"] if not promotion_supported else []),
        "independent_cases": aggregate.get("independent_cases"),
        "replicates": aggregate.get("replicates"),
        "outcome": evaluation.get("outcome"),
        "eligible_for_causal_comparison": eligible,
        "guided_minus_no_skill": dict(evaluation.get("guided_minus_no_skill", {})),
        "arms": arm_summary,
        "concerns": concerns,
    }


def _stop_conditions(pattern: Mapping[str, Any]) -> list[str]:
    explicit = _strings(pattern.get("stop_conditions"))
    if explicit:
        return explicit
    derived: list[str] = []
    for item in pattern.get("known_failure_modes", []):
        if not isinstance(item, Mapping):
            continue
        failure = str(item.get("failure") or "").strip()
        detection = str(item.get("detection") or "").strip()
        if failure:
            detail = f" Detection signal: {detection}" if detection else ""
            derived.append(f"Stop and reassess if {failure[0].lower() + failure[1:]}{detail}")
    return derived or [
        (
            "Stop when provider identity, precedence, boundary ownership, or a validation oracle "
            "cannot be established from current evidence."
        )
    ]


def _validate_source(
    pattern: Mapping[str, Any],
    workflows: Mapping[str, Mapping[str, Any]],
    actions: Mapping[str, Mapping[str, Any]],
    holdout: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_PATTERN_LISTS:
        value = pattern.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"pattern field {field} must be a non-empty list")

    templates = {
        str(item.get("role_id")): item
        for item in pattern.get("action_template", [])
        if isinstance(item, Mapping) and item.get("role_id")
    }
    if len(templates) != len(pattern.get("action_template", [])):
        errors.append("every Action template must have a unique role_id")

    supporting = set(_strings(pattern.get("supporting_workflows")))
    unknown = sorted(supporting.difference(workflows))
    if unknown:
        errors.append(f"unknown supporting Workflows: {unknown}")

    realized: set[str] = set()
    role_repositories: dict[str, set[str]] = defaultdict(set)
    for realization in pattern.get("workflow_realizations", []):
        if not isinstance(realization, Mapping):
            errors.append("Workflow realizations must be objects")
            continue
        workflow_id = str(realization.get("workflow_id") or "")
        workflow = workflows.get(workflow_id)
        if workflow is None:
            errors.append(f"realization references unknown Workflow: {workflow_id}")
            continue
        realized.add(workflow_id)
        repository = str(realization.get("repository") or workflow.get("repository") or "")
        if repository != str(workflow.get("repository") or ""):
            errors.append(f"realization repository disagrees with Workflow {workflow_id}")
        workflow_actions = {
            str(step.get("action_id"))
            for step in workflow.get("steps", [])
            if isinstance(step, Mapping) and step.get("action_id")
        }
        for binding in realization.get("role_bindings", []):
            if not isinstance(binding, Mapping):
                errors.append(f"Workflow {workflow_id} has a malformed role binding")
                continue
            role_id = str(binding.get("role_id") or "")
            if role_id not in templates:
                errors.append(f"Workflow {workflow_id} binds unknown role {role_id}")
            action_ids = _strings(binding.get("action_ids"))
            if not action_ids:
                errors.append(f"Workflow {workflow_id} role {role_id} has no Action ids")
            for action_id in action_ids:
                if action_id not in actions:
                    errors.append(f"Workflow {workflow_id} binds unknown Action {action_id}")
                if action_id not in workflow_actions:
                    errors.append(f"Action {action_id} is not a step of Workflow {workflow_id}")
            if repository:
                role_repositories[role_id].add(repository)

    if supporting != realized:
        errors.append("supporting_workflows must exactly match Workflow realizations")
    for role_id, template in templates.items():
        if bool(template.get("required")) and len(role_repositories[role_id]) < 2:
            errors.append(f"required role {role_id} is realized by fewer than two repositories")
    if not bool(holdout.get("repository_disjoint", True)):
        errors.append(
            "holdout repositories overlap training repositories: "
            f"{holdout.get('training_repository_overlap')}"
        )
    return errors


def _role_bindings(
    pattern: Mapping[str, Any],
    workflows: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    concrete: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for realization in pattern.get("workflow_realizations", []):
        if not isinstance(realization, Mapping):
            continue
        workflow_id = str(realization["workflow_id"])
        repository = str(
            realization.get("repository") or workflows[workflow_id].get("repository") or ""
        )
        for binding in realization.get("role_bindings", []):
            if not isinstance(binding, Mapping):
                continue
            concrete[str(binding["role_id"])].append(
                {
                    "workflow_id": workflow_id,
                    "repository": repository,
                    "action_ids": sorted(_strings(binding.get("action_ids"))),
                }
            )

    result: list[dict[str, Any]] = []
    for template in pattern.get("action_template", []):
        if not isinstance(template, Mapping):
            continue
        role_id = str(template["role_id"])
        result.append(
            {
                "role_id": role_id,
                "title": str(template.get("title") or role_id),
                "required": bool(template.get("required")),
                "workflow_bindings": sorted(
                    concrete.get(role_id, []),
                    key=lambda item: (item["repository"], item["workflow_id"]),
                ),
            }
        )
    return result


def _render_skill(
    skill_name: str,
    description: str,
    pattern: Mapping[str, Any],
    package_status: str,
    promotion_status: str,
) -> str:
    role_sections: list[str] = []
    for index, role in enumerate(pattern["action_template"], start=1):
        status = "required" if role.get("required") else "conditional"
        role_sections.append(
            "\n".join(
                (
                    f"### {index}. {role.get('title')}",
                    "",
                    f"- Role id: {_code(role.get('role_id'))}",
                    f"- Status: {status}",
                    f"- Use when: {role.get('condition')}",
                    f"- Action: {role.get('purpose')}",
                    f"- Check: {role.get('validation')}",
                )
            )
        )
    roles = "\n\n".join(role_sections)
    lifecycle = (
        "This package is a candidate. Retrieval and the holdout oracle are recorded, but paired "
        "agent validation is still pending; do not install it as a validated global Skill yet."
        if package_status == "candidate"
        else "This package is deferred and must not be installed until its blockers clear."
    )
    return f"""---
name: {skill_name}
description: {description}
metadata:
  short-description: Establish a provider contract, then repair only its owning boundary
  status: {package_status}
---

# {pattern.get("title")}

{pattern.get("summary")}

**Lifecycle:** {_code(promotion_status)}. {lifecycle}

## Use this skill when

{_bullets(pattern.get("when_to_use", []))}

## Do not use this skill when

### Anti-goals

{_bullets(pattern.get("anti_goals", []))}

### Not applicable

{_bullets(pattern.get("not_applicable_when", []))}

## Required inputs

- Runtime task context: repository slug, absolute checkout, optional base ref, and target scope.
- The observed provider symptom and the narrowest reproducible request, resume, or construction path.
- Observable interface signals such as explicit provider mode, canonical endpoint identity, or an
  authoritative persisted route.
- Competing configuration sources and their evidenced precedence.
- A focused oracle plus regression commands for unaffected provider paths.

Do not create a persistent project-binding layer. Locate semantic roles in the supplied checkout
and keep that mapping only in the run record.

## Workflow

{roles}

Establish all required roles before a conditional role. Role ids express portable intent; they do
not authorize copying a training-repository implementation. Read
[the Workflow reference](references/workflow.md) for ordering and decision points, and
[the Action contracts](references/action-contracts.md) for real graph bindings.

## Validation

{_numbered(pattern.get("validation_ladder", []))}

Static inspection is not runtime validation. Run the focused oracle, the affected integration path,
and regressions for unchanged providers in the current checkout.

## Stop, ask, or defer

{_bullets(_stop_conditions(pattern))}

Also stop when no evidence-backed provider identity or precedence rule is available. Ask for the
missing contract instead of guessing from a model name or a broad hostname substring.

## Supporting references

- [Workflow roles, ordering, and concrete realizations](references/workflow.md)
- [Bound Action contracts](references/action-contracts.md)
- [Validation ladder and failure modes](references/validation.md)
- [Observed holdout feedback and lifecycle decision](references/feedback.md)
- [Provenance and promotion status](references/provenance.yaml)
"""


def _render_workflow(
    pattern: Mapping[str, Any],
    workflows: Mapping[str, Mapping[str, Any]],
) -> str:
    lines = [
        f"# Workflow for {pattern.get('title')}",
        "",
        (
            "Portable roles are bound to real graph Actions in each training realization. The "
            "ids are evidence, not repository-independent patch recipes."
        ),
        "",
        "## Portable roles",
        "",
    ]
    for index, role in enumerate(pattern.get("action_template", []), start=1):
        lines.extend(
            (
                f"### {index}. {role.get('title')}",
                "",
                f"- role_id: {_code(role.get('role_id'))}",
                f"- required: {_code(str(bool(role.get('required'))).lower())}",
                f"- condition: {role.get('condition')}",
                f"- purpose: {role.get('purpose')}",
                f"- validation: {role.get('validation')}",
                "",
            )
        )
    lines.extend(("## Ordering constraints", ""))
    for item in pattern.get("ordering_constraints", []):
        if isinstance(item, Mapping):
            lines.append(
                f"- {_code(item.get('before_role_id'))} before "
                f"{_code(item.get('after_role_id'))}: {item.get('condition')}"
            )
    lines.extend(("", "## Decision points", ""))
    for item in pattern.get("decision_points", []):
        if not isinstance(item, Mapping):
            continue
        lines.extend((f"### {item.get('question')}", ""))
        for branch in item.get("branches", []):
            if not isinstance(branch, Mapping):
                continue
            roles = ", ".join(_code(value) for value in _strings(branch.get("action_role_ids")))
            lines.append(f"- {branch.get('condition')} -> {roles or 'no additional role'}")
        lines.append("")
    lines.extend(("## Concrete graph realizations", ""))
    for realization in pattern.get("workflow_realizations", []):
        if not isinstance(realization, Mapping):
            continue
        workflow_id = str(realization["workflow_id"])
        workflow = workflows[workflow_id]
        lines.extend(
            (
                f"### {realization.get('repository')} — {workflow.get('title')}",
                "",
                f"- workflow_id: {_code(workflow_id)}",
            )
        )
        for binding in realization.get("role_bindings", []):
            if isinstance(binding, Mapping):
                action_ids = ", ".join(
                    _code(value) for value in _strings(binding.get("action_ids"))
                )
                lines.append(f"- {_code(binding.get('role_id'))} -> {action_ids}")
        lines.append("")
    return "\n".join(lines)


def _render_actions(
    pattern: Mapping[str, Any],
    workflows: Mapping[str, Mapping[str, Any]],
    actions: Mapping[str, Mapping[str, Any]],
) -> str:
    action_roles: dict[str, set[str]] = defaultdict(set)
    action_workflows: dict[str, set[str]] = defaultdict(set)
    for realization in pattern.get("workflow_realizations", []):
        if not isinstance(realization, Mapping):
            continue
        workflow_id = str(realization["workflow_id"])
        for binding in realization.get("role_bindings", []):
            if not isinstance(binding, Mapping):
                continue
            for action_id in _strings(binding.get("action_ids")):
                action_roles[action_id].add(str(binding.get("role_id")))
                action_workflows[action_id].add(workflow_id)

    lines = [
        "# Bound Action contracts",
        "",
        (
            "Locate each Action's semantic owner in the target checkout. Do not search for these "
            "ids or copy repository symbols into an unrelated project."
        ),
        "",
    ]
    for action_id in sorted(action_roles):
        action = actions[action_id]
        workflow_ids = sorted(action_workflows[action_id])
        repositories = sorted(
            {
                str(workflows[workflow_id].get("repository"))
                for workflow_id in workflow_ids
                if workflows[workflow_id].get("repository")
            }
        )
        lines.extend(
            (
                f"## {action.get('source_name') or action_id}",
                "",
                f"- action_id: {_code(action_id)}",
                "- role_ids: "
                + ", ".join(_code(value) for value in sorted(action_roles[action_id])),
                "- workflow_ids: " + ", ".join(_code(value) for value in workflow_ids),
                "- supporting repositories: " + ", ".join(repositories),
                f"- module role: {action.get('module_role')}",
                f"- operation: {_code(action.get('operation'))}",
                "",
                f"**Pre-state:** {action.get('pre_state')}",
                "",
                f"**Post-state:** {action.get('post_state')}",
                "",
                f"**Validation oracle:** {action.get('validation')}",
                "",
                "**Parameters:**",
                "",
                _bullets(action.get("parameters", [])),
                "",
                "**Evidence ids:** "
                + ", ".join(_code(value) for value in _strings(action.get("evidence_ids"))),
                "",
            )
        )
    return "\n".join(lines)


def _render_validation(
    pattern: Mapping[str, Any],
    holdout: Mapping[str, Any],
    retrieval: Mapping[str, Any],
    package_status: str,
    promotion_status: str,
) -> str:
    lines = [
        "# Validation and promotion gates",
        "",
        "## Validation ladder",
        "",
        _numbered(pattern.get("validation_ladder", [])),
        "",
        "## Known failure modes",
        "",
    ]
    for item in pattern.get("known_failure_modes", []):
        if not isinstance(item, Mapping):
            continue
        lines.extend(
            (
                f"### {item.get('failure')}",
                "",
                f"- Detection: {item.get('detection')}",
                f"- Mitigation: {item.get('mitigation')}",
                "",
            )
        )
    lines.extend(
        (
            "## Exclusions",
            "",
            _bullets(pattern.get("exclusions", [])),
            "",
            "## Current package gate",
            "",
            f"- package status: {_code(package_status)}",
            f"- promotion status: {_code(promotion_status)}",
            f"- repository-disjoint holdout: {_code(holdout.get('repository_disjoint'))}",
            f"- oracle qualified: {_code(holdout.get('oracle_qualified'))}",
            f"- paired agent evaluation: {_code(holdout.get('agent_pair_status'))}",
            f"- retrieval evaluation: {_code(retrieval.get('status'))}",
            "",
            (
                "Retrieval success and a discriminating oracle do not promote this Skill. "
                "Promotion requires a leakage-audited paired agent run and independent weighted "
                "evaluation."
            ),
        )
    )
    return "\n".join(lines)


def _render_feedback(evaluation: Mapping[str, Any]) -> str:
    lines = [
        "# Holdout feedback and lifecycle decision",
        "",
        f"- evaluation status: {_code(evaluation.get('status'))}",
        f"- lifecycle decision: {_code(evaluation.get('lifecycle_decision'))}",
        f"- outcome: {_code(evaluation.get('outcome'))}",
        f"- independent cases: {_code(evaluation.get('independent_cases'))}",
        f"- replicates: {_code(evaluation.get('replicates'))}",
        f"- promotion supported: {_code(evaluation.get('promotion_supported'))}",
        "",
        "## Paired result",
        "",
    ]
    arms = evaluation.get("arms")
    if isinstance(arms, Mapping) and arms:
        for arm in ("no_skill", "guided"):
            value = arms.get(arm)
            if not isinstance(value, Mapping):
                continue
            lines.extend(
                (
                    f"### {arm}",
                    "",
                    f"- task solved: {_code(value.get('task_solved'))}",
                    f"- correctness: {_code(value.get('correctness'))}",
                    f"- code quality: {_code(value.get('code_quality'))}",
                    f"- overall score: {_code(value.get('overall_score'))}",
                    f"- usage tokens: {_code(value.get('usage_tokens'))}",
                    f"- wall seconds: {_code(value.get('wall_seconds'))}",
                    "",
                )
            )
    else:
        lines.extend(("The paired agent run has not been completed.", ""))
    delta = evaluation.get("guided_minus_no_skill")
    if isinstance(delta, Mapping):
        lines.extend(
            (
                "## Guided minus no-skill",
                "",
                f"- overall score: {_code(delta.get('overall_score'))}",
                f"- usage tokens: {_code(delta.get('usage_tokens'))}",
                f"- wall seconds: {_code(delta.get('wall_seconds'))}",
                "",
            )
        )
    lines.extend(("## Evaluator observations", ""))
    concerns = evaluation.get("concerns")
    added = False
    if isinstance(concerns, Mapping):
        for arm in ("guided", "no_skill"):
            values = _strings(concerns.get(arm))
            if not values:
                continue
            added = True
            lines.extend((f"### {arm}", "", _bullets(values), ""))
    if not added:
        lines.extend(("- No evaluator observations are recorded yet.", ""))
    lines.extend(
        (
            "## Candidate update",
            "",
            (
                "- Add a focused case where a canonical or aliased provider prefix competes with "
                "a provider-agnostic raw id."
            ),
            (
                "- Add slash-containing model ids with fuzzy matches and thinking-level suffixes "
                "so fallback compatibility is observed rather than assumed."
            ),
            (
                "- Run the broader resolver regression suite in addition to the "
                "evaluator-authored holdout test."
            ),
            "",
            (
                "Treat these observations as holdout evidence, not universal rules. The current "
                "update retains the candidate and strengthens edge-case validation; it does not "
                "merge, retire, or globally promote the Pattern."
            ),
            "",
            "## Promotion blockers",
            "",
            _bullets(evaluation.get("promotion_blockers", [])),
        )
    )
    return "\n".join(lines)


def _activation_evals(
    pattern: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    prompts = [
        {
            "id": "direct-provider-precedence",
            "class": "direct",
            "prompt": (
                "An explicit provider/model pair resolves to a different provider because a "
                "fallback catalog entry with the same raw model id is examined first. Repair "
                "selection without changing unrelated providers."
            ),
        },
        {
            "id": "indirect-resume-route",
            "class": "indirect",
            "prompt": (
                "A resumed session reaches a stale endpoint even though its latest persisted "
                "runtime snapshot records a newer provider route. Align the inconsistent consumer."
            ),
        },
        {
            "id": "contextual-strict-endpoint",
            "class": "contextual",
            "prompt": (
                "A compatible endpoint accepts ordinary turns but rejects replay after a structured "
                "assistant response because one synthesized field is outside its request contract."
            ),
        },
        {
            "id": "incomplete-custom-provider",
            "class": "incomplete",
            "prompt": "The custom provider is broken after switching models. Please fix it.",
        },
        {
            "id": "negative-credential-acquisition",
            "class": "negative",
            "prompt": (
                "OAuth succeeds but the CLI keeps loading an expired API key. Redesign credential "
                "acquisition and key precedence."
            ),
        },
        {
            "id": "edge-incompatible-protocol",
            "class": "edge",
            "prompt": (
                "Add a provider whose streaming request and response protocol is incompatible with "
                "the existing client and needs a new transport."
            ),
        },
    ]
    decisions = {
        "direct": "activate",
        "indirect": "activate",
        "contextual": "activate",
        "incomplete": "clarify",
        "negative": "do_not_activate",
        "edge": "do_not_activate",
    }
    required_roles = [
        str(item["role_id"])
        for item in pattern.get("action_template", [])
        if isinstance(item, Mapping) and item.get("required")
    ]
    optional_roles = [
        str(item["role_id"])
        for item in pattern.get("action_template", [])
        if isinstance(item, Mapping) and not item.get("required")
    ]
    expected = []
    for prompt in prompts:
        decision = decisions[str(prompt["class"])]
        expected.append(
            {
                "id": prompt["id"],
                "decision": decision,
                "required_role_ids": required_roles if decision == "activate" else [],
                "optional_role_ids": optional_roles if decision == "activate" else [],
                "forbidden_behaviors": _strings(pattern.get("anti_goals"))[:3],
                "must_request_missing_contract": decision == "clarify",
            }
        )
    return prompts, expected


def _rubric_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Resolution Skill activation and use rubric",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "activation_decision",
            "interface_contract_quality",
            "action_role_coverage",
            "anti_goal_violations",
            "validation_quality",
            "unrelated_changes",
            "leakage_detected",
            "rationale",
        ],
        "properties": {
            "activation_decision": {
                "type": "string",
                "enum": ["activate", "clarify", "do_not_activate"],
            },
            "interface_contract_quality": {"type": "number", "minimum": 0, "maximum": 100},
            "action_role_coverage": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": True,
            },
            "anti_goal_violations": {"type": "array", "items": {"type": "string"}},
            "validation_quality": {"type": "number", "minimum": 0, "maximum": 100},
            "unrelated_changes": {"type": "array", "items": {"type": "string"}},
            "leakage_detected": {"type": "boolean"},
            "rationale": {"type": "string", "minLength": 1},
        },
    }


def _prepare_output(output_dir: Path, *, force: bool) -> Path:
    root = Path(__file__).resolve().parents[1]
    output = output_dir.expanduser().resolve()
    forbidden = {Path.cwd().resolve(), root, root.parent, Path(output.anchor)}
    if output in forbidden or len(output.parts) < 4:
        raise ValueError(f"refusing unsafe output directory: {output}")
    if output.exists() and any(output.iterdir()):
        if not force:
            raise ValueError(f"output directory is not empty: {output}")
        if output.is_symlink() or not output.is_dir():
            raise ValueError(f"refusing to replace non-directory output: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    return output


def compile_package(
    graph_path: Path,
    pattern_id: str,
    output_dir: Path,
    *,
    skill_name: str = DEFAULT_SKILL_NAME,
    description: str = DEFAULT_DESCRIPTION,
    holdout_cases_path: Path | None = None,
    qualification_path: Path | None = None,
    retrieval_path: Path | None = None,
    agent_evaluation_path: Path | None = None,
    evaluation_aggregate_path: Path | None = None,
    force: bool = False,
) -> dict[str, Any]:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name):
        raise ValueError("skill name must be lowercase hyphenated")
    if len(skill_name) > 63:
        raise ValueError("skill name must be shorter than 64 characters")
    graph = _read_json(graph_path)
    if not isinstance(graph, Mapping):
        raise TypeError("semantic graph must be a JSON object")
    patterns = _index(graph.get("patterns"), "Pattern")
    workflows = _index(graph.get("workflows"), "Workflow")
    actions = _index(graph.get("actions"), "Action")
    if pattern_id not in patterns:
        raise ValueError(f"Pattern not found: {pattern_id}")
    pattern = patterns[pattern_id]
    training_repositories = set(_strings(pattern.get("supporting_repositories")))
    holdout = _holdout_summary(
        holdout_cases_path,
        qualification_path,
        training_repositories,
    )
    retrieval = _retrieval_summary(retrieval_path)
    evaluation = _agent_evaluation_summary(
        agent_evaluation_path,
        evaluation_aggregate_path,
    )
    holdout["agent_pair_status"] = evaluation["status"]
    errors = _validate_source(pattern, workflows, actions, holdout)
    if errors:
        raise ValueError("source graph failed package gates:\n- " + "\n- ".join(errors))

    if evaluation["promotion_supported"]:
        package_status = "promoted"
        promotion_status = "promoted_holdout_supported"
    elif holdout["qualified"] and holdout["repository_disjoint"]:
        package_status = "candidate"
        promotion_status = (
            "candidate_pending_independent_holdouts"
            if evaluation["status"] == "pass_directional"
            else "candidate_pending_agent_holdout"
        )
    elif qualification_path is not None:
        package_status = "deferred"
        promotion_status = "deferred_holdout_oracle"
    else:
        package_status = "candidate"
        promotion_status = "candidate_pending_holdout_oracle"

    output = _prepare_output(output_dir, force=force)
    role_bindings = _role_bindings(pattern, workflows)
    provenance = {
        "schema_version": PROVENANCE_SCHEMA,
        "package": {
            "name": skill_name,
            "version": 1,
            "status": package_status,
            "promotion_status": promotion_status,
        },
        "source": {
            "pattern_id": pattern_id,
            "category": pattern.get("category"),
            "graph_schema_version": graph.get("schema_version"),
            "graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
            "pattern_confidence": pattern.get("confidence"),
            "pattern_source_status": pattern.get("promotion_status"),
        },
        "support": {
            "workflow_ids": sorted(_strings(pattern.get("supporting_workflows"))),
            "repositories": sorted(training_repositories),
            "evidence_ids": sorted(set(_strings(pattern.get("evidence_ids")))),
        },
        "role_bindings": role_bindings,
        "holdout": holdout,
        "retrieval": retrieval,
        "agent_evaluation": evaluation,
        "promotion_reasons": [
            (
                "The package preserves plain-language activation, anti-goals, exclusions, real "
                "Action bindings, and validation."
            ),
            (
                "The repository-disjoint holdout oracle is qualified."
                if holdout["qualified"]
                else "The repository-disjoint holdout oracle is not yet qualified."
            ),
            (
                "The paired agent result is directional and the package remains a candidate."
                if evaluation["status"] == "pass_directional"
                else "Paired no-skill versus guided agent evaluation is still pending."
            ),
        ],
    }

    _write_text(
        output / "SKILL.md",
        _render_skill(skill_name, description, pattern, package_status, promotion_status),
    )
    _write_text(output / "references" / "workflow.md", _render_workflow(pattern, workflows))
    _write_text(
        output / "references" / "action-contracts.md",
        _render_actions(pattern, workflows, actions),
    )
    _write_text(
        output / "references" / "validation.md",
        _render_validation(pattern, holdout, retrieval, package_status, promotion_status),
    )
    _write_text(output / "references" / "feedback.md", _render_feedback(evaluation))
    # JSON is valid YAML 1.2 and keeps the provenance sidecar dependency-free.
    _write_json(output / "references" / "provenance.yaml", provenance)
    prompts, expected = _activation_evals(pattern)
    _write_jsonl(output / "evals" / "prompts.jsonl", prompts)
    _write_json(output / "evals" / "rubric.schema.json", _rubric_schema())
    _write_jsonl(output / "evals" / "expected.jsonl", expected)

    return {
        "schema_version": PACKAGE_SCHEMA,
        "output_dir": str(output),
        "skill_name": skill_name,
        "status": package_status,
        "promotion_status": promotion_status,
        "pattern_id": pattern_id,
        "workflow_count": len(pattern.get("supporting_workflows", [])),
        "bound_action_count": len(
            {
                action_id
                for role in role_bindings
                for binding in role["workflow_bindings"]
                for action_id in binding["action_ids"]
            }
        ),
        "activation_eval_count": len(prompts),
        "holdout_oracle_qualified": holdout["oracle_qualified"],
        "holdout_repository_disjoint": holdout["repository_disjoint"],
        "agent_pair_status": evaluation["status"],
        "promotion_supported": evaluation["promotion_supported"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--pattern-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skill-name", default=DEFAULT_SKILL_NAME)
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION)
    parser.add_argument("--holdout-cases", type=Path)
    parser.add_argument("--qualification", type=Path)
    parser.add_argument("--retrieval-evaluation", type=Path)
    parser.add_argument("--agent-evaluation", type=Path)
    parser.add_argument("--evaluation-aggregate", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = compile_package(
        args.graph,
        args.pattern_id,
        args.output,
        skill_name=args.skill_name,
        description=args.description,
        holdout_cases_path=args.holdout_cases,
        qualification_path=args.qualification,
        retrieval_path=args.retrieval_evaluation,
        agent_evaluation_path=args.agent_evaluation,
        evaluation_aggregate_path=args.evaluation_aggregate,
        force=args.force,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
