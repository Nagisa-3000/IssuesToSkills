#!/usr/bin/env python3
"""Induce and validate a human-readable cross-project Resolution Pattern.

The deterministic graph builder deliberately does not infer that different
repository Actions are interchangeable.  This stage asks an LLM to induce a
role-level decision policy over multiple admitted Workflows, then validates
every role binding against the actual Action ids in those Workflows.  Holdout
records are not inputs to this command and promotion remains pending until a
separate held-out end-task experiment passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport

DEFAULT_SCHEMA = ROOT / "schemas" / "resolution-pattern-induction-v1.schema.json"
DECISION_TO_STATUS = {
    "candidate_pending_holdout": "candidate_pending_holdout",
    "defer": "deferred_by_semantic_judge",
    "reject": "rejected_by_semantic_judge",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _rows(value: Any) -> list[dict[str, Any]]:
    return [dict(item) for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _strings(value: Any) -> list[str]:
    return [str(item) for item in value if str(item)] if isinstance(value, list) else []


def select_pattern(graph: Mapping[str, Any], pattern_id: str | None) -> dict[str, Any]:
    patterns = _rows(graph.get("patterns"))
    if pattern_id is not None:
        matches = [item for item in patterns if str(item.get("id")) == pattern_id]
    else:
        matches = patterns
    if len(matches) != 1:
        raise ValueError(f"expected exactly one Pattern candidate, found {len(matches)}")
    return matches[0]


def bounded_training_payload(
    graph: Mapping[str, Any], pattern: Mapping[str, Any], audit: Mapping[str, Any] | None
) -> dict[str, Any]:
    workflow_ids = set(_strings(pattern.get("supporting_workflows")))
    workflows = [
        item for item in _rows(graph.get("workflows")) if str(item.get("id")) in workflow_ids
    ]
    action_ids = {
        str(step.get("action_id"))
        for workflow in workflows
        for step in _rows(workflow.get("steps"))
        if step.get("action_id")
    }
    actions = [item for item in _rows(graph.get("actions")) if str(item.get("id")) in action_ids]
    return {
        "pattern_candidate": dict(pattern),
        "workflows": workflows,
        "actions": actions,
        "factorization_audit": dict(audit or {}),
        "boundary": {
            "training_only": True,
            "holdout_loaded": False,
            "action_similarity_is_not_equivalence": True,
            "role_templates_must_bind_to_real_action_ids": True,
        },
    }


def system_prompt() -> str:
    return (
        "You are the independent Pattern inducer for an evidence-grounded resolution graph. "
        "Use only the supplied training Workflows and Actions. A Pattern is a plain-language "
        "cross-project decision policy, not a category label, repository recipe, or claim that "
        "different Actions are interchangeable. Preserve distinct Action contracts. Express the "
        "reusable structure as role-level action_template entries and bind each supporting "
        "Workflow to the exact Action ids that realize those roles. State when to use the Pattern, "
        "anti-goals, exclusions, decision branches, ordering, and validation. Use "
        "candidate_pending_holdout only when at least two repositories support every required "
        "role; it still requires a separate untouched holdout repair. Never invent holdout facts, "
        "solution refs, tests, evidence ids, Action ids, or Workflow ids. Return JSON only."
    )


def user_payload(
    training: Mapping[str, Any], previous_errors: list[str] | None = None
) -> dict[str, Any]:
    return {
        "operation": "induce_human_resolution_pattern",
        "instructions": [
            "Give the Pattern a short title a software engineer can understand without knowing AREX.",
            "Describe observable applicability signals, not product names or issue numbers.",
            "Do not merge Actions. Use workflow_realizations to map generic roles to existing ids.",
            "A required role must be independently realized in at least two repositories.",
            "Keep repository-specific branches conditional rather than universally mandatory.",
            "The validation ladder must distinguish focused contract checks, integration checks, and regressions.",
            "If the evidence supports only fragments rather than one coherent policy, return defer.",
        ],
        "training_graph": dict(training),
        "previous_validation_errors": list(previous_errors or []),
    }


def _workflow_index(graph: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in _rows(graph.get("workflows"))}


def _action_index(graph: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("id")): item for item in _rows(graph.get("actions"))}


def _available_evidence(graph: Mapping[str, Any]) -> set[str]:
    evidence: set[str] = set()
    for item in [*_rows(graph.get("actions")), *_rows(graph.get("workflows"))]:
        evidence.update(_strings(item.get("evidence_ids")))
    return evidence


def semantic_validation_errors(
    contract: Mapping[str, Any], graph: Mapping[str, Any], pattern: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    expected_pattern_id = str(pattern.get("id"))
    expected_category = str(pattern.get("category"))
    if str(contract.get("pattern_id")) != expected_pattern_id:
        errors.append("pattern_id does not match the structural candidate")
    if str(contract.get("category")) != expected_category:
        errors.append("category does not match the structural candidate")

    title = str(contract.get("title") or "").strip()
    normalized_title = " ".join(title.lower().replace("-", " ").split())
    normalized_category = " ".join(expected_category.lower().replace("-", " ").split())
    if normalized_title == normalized_category:
        errors.append("title is only the machine category")
    if normalized_title.startswith("resolve ") and " evidence validated change chain" in normalized_title:
        errors.append("title repeats the generic structural placeholder")
    if re.search(r"(?:pattern|workflow|semantic-action):|(?:issue|pr)\s*#?\d+", title, re.IGNORECASE):
        errors.append("title leaks a machine id or issue/PR identity")

    workflow_by_id = _workflow_index(graph)
    action_by_id = _action_index(graph)
    allowed_workflow_ids = set(_strings(pattern.get("supporting_workflows")))
    supporting_ids = _strings(contract.get("supporting_workflow_ids"))
    supporting_set = set(supporting_ids)
    if len(supporting_set) != len(supporting_ids):
        errors.append("supporting_workflow_ids contains duplicates")
    unknown_workflows = supporting_set - allowed_workflow_ids
    if unknown_workflows:
        errors.append(f"unknown supporting workflows: {sorted(unknown_workflows)}")
    repositories = {
        str(workflow_by_id[item].get("repository"))
        for item in supporting_set
        if item in workflow_by_id
    }
    if len(repositories) < 2:
        errors.append("Pattern support does not span at least two repositories")

    template = _rows(contract.get("action_template"))
    role_ids = [str(item.get("role_id")) for item in template]
    role_set = set(role_ids)
    if len(role_set) != len(role_ids):
        errors.append("action_template role_id values are not unique")
    required_roles = {str(item.get("role_id")) for item in template if item.get("required") is True}

    realization_rows = _rows(contract.get("workflow_realizations"))
    realization_ids = [str(item.get("workflow_id")) for item in realization_rows]
    if set(realization_ids) != supporting_set or len(realization_ids) != len(set(realization_ids)):
        errors.append("workflow_realizations must cover each supporting Workflow exactly once")

    role_repository_support: dict[str, set[str]] = {role_id: set() for role_id in role_set}
    for realization in realization_rows:
        workflow_id = str(realization.get("workflow_id"))
        workflow = workflow_by_id.get(workflow_id)
        if workflow is None:
            continue
        repository = str(workflow.get("repository"))
        if str(realization.get("repository")) != repository:
            errors.append(f"{workflow_id}: realization repository does not match graph")
        workflow_action_ids = {
            str(step.get("action_id"))
            for step in _rows(workflow.get("steps"))
            if step.get("action_id")
        }
        workflow_evidence = set(_strings(workflow.get("evidence_ids")))
        for action_id in workflow_action_ids:
            action = action_by_id.get(action_id)
            if action is not None:
                workflow_evidence.update(_strings(action.get("evidence_ids")))
        realization_evidence = set(_strings(realization.get("evidence_ids")))
        unrelated_evidence = realization_evidence - workflow_evidence
        if unrelated_evidence:
            errors.append(
                f"{workflow_id}: realization cites evidence outside its Workflow: "
                f"{sorted(unrelated_evidence)}"
            )
        seen_roles: set[str] = set()
        for binding in _rows(realization.get("role_bindings")):
            role_id = str(binding.get("role_id"))
            if role_id not in role_set:
                errors.append(f"{workflow_id}: unknown role binding {role_id}")
                continue
            if role_id in seen_roles:
                errors.append(f"{workflow_id}: duplicate role binding {role_id}")
            seen_roles.add(role_id)
            bound_action_ids = set(_strings(binding.get("action_ids")))
            unknown_actions = bound_action_ids - workflow_action_ids
            if unknown_actions:
                errors.append(
                    f"{workflow_id}/{role_id}: actions are not Workflow steps: "
                    f"{sorted(unknown_actions)}"
                )
            missing_actions = bound_action_ids - set(action_by_id)
            if missing_actions:
                errors.append(
                    f"{workflow_id}/{role_id}: actions are absent from graph: "
                    f"{sorted(missing_actions)}"
                )
            if bound_action_ids and not unknown_actions and not missing_actions:
                role_repository_support.setdefault(role_id, set()).add(repository)

    if contract.get("decision") == "candidate_pending_holdout":
        for role_id in sorted(required_roles):
            support = role_repository_support.get(role_id, set())
            if len(support) < 2:
                errors.append(
                    f"required role {role_id} is supported by fewer than two repositories"
                )
        missing_probes = " ".join(_strings(contract.get("missing_probes"))).lower()
        if "holdout" not in missing_probes and "held-out" not in missing_probes:
            errors.append("candidate_pending_holdout must name the missing holdout probe")

    for row in _rows(contract.get("ordering_constraints")):
        for key in ("before_role_id", "after_role_id"):
            if str(row.get(key)) not in role_set:
                errors.append(f"ordering constraint references unknown role: {row.get(key)}")
    for point in _rows(contract.get("decision_points")):
        for branch in _rows(point.get("branches")):
            unknown_roles = set(_strings(branch.get("action_role_ids"))) - role_set
            if unknown_roles:
                errors.append(f"decision branch references unknown roles: {sorted(unknown_roles)}")

    available_evidence = _available_evidence(graph)
    cited_evidence = set(_strings(contract.get("evidence_ids")))
    for realization in realization_rows:
        cited_evidence.update(_strings(realization.get("evidence_ids")))
    unknown_evidence = cited_evidence - available_evidence
    if unknown_evidence:
        errors.append(f"Pattern cites unknown evidence ids: {sorted(unknown_evidence)}")
    if contract.get("decision") == "candidate_pending_holdout" and not cited_evidence:
        errors.append("candidate_pending_holdout has no evidence ids")
    return errors


def validate_contract(
    contract: Mapping[str, Any],
    graph: Mapping[str, Any],
    pattern: Mapping[str, Any],
    schema: Mapping[str, Any],
) -> list[str]:
    schema_errors = sorted(error.message for error in Draft202012Validator(schema).iter_errors(contract))
    return [f"schema: {item}" for item in schema_errors] + semantic_validation_errors(
        contract, graph, pattern
    )


def apply_contract(
    graph: Mapping[str, Any], pattern_id: str, contract: Mapping[str, Any]
) -> dict[str, Any]:
    result = deepcopy(dict(graph))
    workflow_by_id = _workflow_index(result)
    patterns = _rows(result.get("patterns"))
    updated = False
    for pattern in patterns:
        if str(pattern.get("id")) != pattern_id:
            continue
        pattern["structural_intent"] = pattern.get("intent")
        for key in (
            "title",
            "summary",
            "when_to_use",
            "anti_goals",
            "not_applicable_when",
            "invariants",
            "action_template",
            "decision_points",
            "ordering_constraints",
            "validation_ladder",
            "known_failure_modes",
            "exclusions",
            "workflow_realizations",
            "rationale",
            "evidence_ids",
            "missing_probes",
        ):
            pattern[key] = deepcopy(contract.get(key))
        pattern["intent"] = str(contract.get("summary"))
        pattern["supporting_workflows"] = list(contract.get("supporting_workflow_ids", []))
        pattern["supporting_repositories"] = sorted(
            {
                str(workflow_by_id[workflow_id].get("repository"))
                for workflow_id in pattern["supporting_workflows"]
                if workflow_id in workflow_by_id
            }
        )
        pattern["confidence"] = float(contract.get("confidence") or 0.0)
        pattern["promotion_status"] = DECISION_TO_STATUS[str(contract.get("decision"))]
        pattern["semantic_induction"] = {
            "schema_version": contract.get("schema_version"),
            "decision": contract.get("decision"),
            "holdout_used": False,
            "contract_sha256": canonical_json_sha256(contract),
        }
        updated = True
        break
    if not updated:
        raise KeyError(f"Pattern not found: {pattern_id}")
    result["patterns"] = sorted(patterns, key=lambda row: str(row.get("id")))
    result["summary"] = {
        **dict(result.get("summary") or {}),
        "patterns": len(result["patterns"]),
        "patterns_pending_holdout": sum(
            item.get("promotion_status") == "candidate_pending_holdout"
            for item in result["patterns"]
        ),
    }
    result["semantic_pattern_induction"] = {
        "holdout_loaded": False,
        "pattern_id": pattern_id,
        "contract_sha256": canonical_json_sha256(contract),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--pattern-id")
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    parser.add_argument("--max-output-tokens", type=int, default=7000)
    parser.add_argument("--semantic-attempts", type=int, default=3)
    args = parser.parse_args()
    if not args.api_key:
        raise ValueError("OPENAI_API_KEY or --api-key is required")

    graph = load_json(args.graph)
    if not isinstance(graph, dict):
        raise TypeError("graph must be an object")
    audit = load_json(args.audit) if args.audit else None
    if audit is not None and not isinstance(audit, dict):
        raise TypeError("audit must be an object")
    schema = load_json(args.schema)
    if not isinstance(schema, dict):
        raise TypeError("schema must be an object")
    pattern = select_pattern(graph, args.pattern_id)
    training = bounded_training_payload(graph, pattern, audit)

    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_record = {
        "system": system_prompt(),
        "user": user_payload(training),
        "schema": schema,
        "holdout_loaded": False,
    }
    (output_dir / "prompt.json").write_text(
        json.dumps(prompt_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    transport = OpenAICompatibleTransport(
        OpenAICompatibleConfig(
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
            timeout_seconds=max(1.0, args.timeout_seconds),
            max_output_tokens=max(1000, args.max_output_tokens),
            retries=2,
        )
    )
    attempts: list[dict[str, Any]] = []
    contract: dict[str, Any] | None = None
    errors: list[str] = []
    for attempt in range(1, max(1, args.semantic_attempts) + 1):
        response = dict(
            transport.complete(
                system=system_prompt(),
                user=json.dumps(
                    user_payload(training, errors if attempt > 1 else None),
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                response_schema=schema,
            )
        )
        errors = validate_contract(response, graph, pattern, schema)
        attempts.append(
            {
                "attempt": attempt,
                "valid": not errors,
                "errors": errors,
                "response": response,
            }
        )
        if not errors:
            contract = response
            break

    validation = {
        "valid": contract is not None,
        "attempts": len(attempts),
        "errors": [] if contract is not None else errors,
    }
    (output_dir / "attempts.json").write_text(
        json.dumps(attempts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if contract is None:
        (output_dir / "run-record.json").write_text(
            json.dumps(
                {
                    "model": args.model,
                    "source_graph": str(args.graph),
                    "source_graph_sha256": file_sha256(args.graph),
                    "holdout_loaded": False,
                    "calls": transport.calls,
                    "transcripts": transport.transcripts,
                    "validation": validation,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(json.dumps(validation, ensure_ascii=False))
        return 1

    semantic_graph = apply_contract(graph, str(pattern.get("id")), contract)
    (output_dir / "pattern-contract.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "semantic-graph.json").write_text(
        json.dumps(semantic_graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    run_record = {
        "schema_version": "resolution-pattern-induction-run-v1",
        "model": args.model,
        "base_url": args.base_url,
        "source_graph": str(args.graph),
        "source_graph_sha256": file_sha256(args.graph),
        "source_audit": str(args.audit) if args.audit else None,
        "source_audit_sha256": file_sha256(args.audit) if args.audit else None,
        "prompt_sha256": canonical_json_sha256(prompt_record),
        "contract_sha256": canonical_json_sha256(contract),
        "holdout_loaded": False,
        "api_key_persisted": False,
        "calls": transport.calls,
        "transcripts": transport.transcripts,
        "validation": validation,
    }
    (output_dir / "run-record.json").write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output_dir),
                "pattern_id": contract["pattern_id"],
                "title": contract["title"],
                "decision": contract["decision"],
                "supporting_workflows": len(contract["supporting_workflow_ids"]),
                "attempts": len(attempts),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
