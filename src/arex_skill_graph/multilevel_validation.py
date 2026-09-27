from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Iterable


ORDERING_RELATIONS = frozenset({"requires", "enables", "precedes", "validates"})
QUALITY_DIMENSIONS = (
    "evidence_coverage",
    "semantic_coherence",
    "boundary_clarity",
    "validation_strength",
    "cross_repository_support",
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    path: str
    message: str


@dataclass(slots=True)
class ValidationReport:
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def add_error(self, code: str, path: str, message: str) -> None:
        self.errors.append(ValidationIssue(code, path, message))

    def add_warning(self, code: str, path: str, message: str) -> None:
        self.warnings.append(ValidationIssue(code, path, message))


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_json_schema(
    bundle: dict[str, Any], schema: dict[str, Any]
) -> ValidationReport:
    """Validate Draft 2020-12 shape without making jsonschema a runtime dependency."""
    report = ValidationReport()
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError:
        report.add_warning(
            "jsonschema_unavailable",
            "$",
            "Install the dev dependency jsonschema to run structural validation.",
        )
        return report

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(bundle), key=lambda item: list(item.absolute_path)):
        path = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        report.add_error("json_schema", path, error.message)
    return report


def validate_semantics(bundle: dict[str, Any]) -> ValidationReport:
    """Legacy offline audit for v1 bundles.

    This is not part of runtime Skill admission. New semantic decisions
    (equivalence, applicability, promotion, failure cause) must be made by the
    LLM Governance Skill. Runtime code should use schema/reference checks and
    ``BottomUpSkillAdmission``; this function remains only for migration tests
    and historical artifact audits.
    """
    report = ValidationReport()
    evidence_ids = _ids(bundle.get("evidence_units", []))
    validation_ids = _ids(bundle.get("validations", []))
    episode_ids = _ids(bundle.get("candidate_episodes", []))
    atomic_ids = _ids(bundle.get("atomic_skills", []))
    workflow_ids = _ids(bundle.get("workflows", []))
    pattern_ids = _ids(bundle.get("patterns", []))
    binding_ids = _ids(bundle.get("bindings", []))
    claim_ids = {
        value["id"]
        for _, value in _walk(bundle)
        if isinstance(value, dict) and str(value.get("id", "")).startswith("claim:")
    }

    workflow_step_ids = {
        step["id"]
        for workflow in bundle.get("workflows", [])
        for step in workflow.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("id"), str)
    }
    pattern_step_ids = {
        step["id"]
        for pattern in bundle.get("patterns", [])
        for step in pattern.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("id"), str)
    }
    task_family_id = bundle.get("task_family", {}).get("id")
    semantic_node_ids = (
        atomic_ids
        | workflow_ids
        | workflow_step_ids
        | pattern_ids
        | pattern_step_ids
        | validation_ids
        | binding_ids
    )

    _check_duplicate_ids(bundle, report)
    _check_claim_evidence(bundle, evidence_ids, report)
    _check_named_references(bundle, evidence_ids, validation_ids, episode_ids, report)
    _check_atomic_skills(bundle, episode_ids, evidence_ids, report)
    _check_workflows(bundle, atomic_ids, validation_ids, evidence_ids, report)
    _check_patterns(
        bundle,
        workflow_ids,
        workflow_step_ids,
        atomic_ids,
        validation_ids,
        evidence_ids,
        task_family_id,
        report,
    )
    _check_bindings(bundle, semantic_node_ids, evidence_ids, report)
    _check_relations(
        bundle,
        atomic_ids,
        workflow_ids,
        workflow_step_ids,
        pattern_ids,
        pattern_step_ids,
        validation_ids,
        binding_ids,
        evidence_ids,
        claim_ids,
        report,
    )
    _check_views(bundle, claim_ids, workflow_step_ids | pattern_step_ids, validation_ids, evidence_ids, report)
    _check_quality(bundle, report)
    _check_lifecycle(bundle, report)
    _check_report_statistics(bundle, report)
    return report


def validate_bundle(
    bundle: dict[str, Any], schema: dict[str, Any] | None = None
) -> ValidationReport:
    report = ValidationReport()
    if schema is not None:
        shape = validate_json_schema(bundle, schema)
        report.errors.extend(shape.errors)
        report.warnings.extend(shape.warnings)
    semantic = validate_semantics(bundle)
    report.errors.extend(semantic.errors)
    report.warnings.extend(semantic.warnings)
    return report


def _ids(items: Iterable[dict[str, Any]]) -> set[str]:
    return {
        item["id"]
        for item in items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _check_duplicate_ids(bundle: dict[str, Any], report: ValidationReport) -> None:
    seen: dict[str, tuple[str, str]] = {}
    for path, value in _walk(bundle):
        if not isinstance(value, dict) or not isinstance(value.get("id"), str):
            continue
        identifier = value["id"]
        canonical = _canonical(value)
        previous = seen.get(identifier)
        if previous is None:
            seen[identifier] = (path, canonical)
            continue
        previous_path, previous_canonical = previous
        if identifier.startswith("claim:") and canonical == previous_canonical:
            continue
        report.add_error(
            "duplicate_id",
            path,
            f"{identifier!r} already occurs at {previous_path}; repeated claims must be byte-equivalent.",
        )


def _check_claim_evidence(
    bundle: dict[str, Any], evidence_ids: set[str], report: ValidationReport
) -> None:
    for path, value in _walk(bundle):
        if not isinstance(value, dict) or not str(value.get("id", "")).startswith("claim:"):
            continue
        refs = value.get("evidence_ids", [])
        for ref in refs:
            if ref not in evidence_ids:
                report.add_error("dangling_claim_evidence", path, f"Unknown evidence ID {ref!r}.")
        if value.get("epistemic_status") == "observed" and not refs:
            report.add_error("ungrounded_observation", path, "Observed claims require evidence.")


def _check_named_references(
    bundle: dict[str, Any],
    evidence_ids: set[str],
    validation_ids: set[str],
    episode_ids: set[str],
    report: ValidationReport,
) -> None:
    evidence_keys = {
        "evidence_ids",
        "result_evidence_ids",
        "probe_evidence_ids",
        "positive_example_evidence_ids",
        "negative_example_evidence_ids",
    }
    validation_keys = {
        "validation_ids",
        "validation_contract_ids",
        "acceptance_validation_ids",
        "validation_ladder_ids",
        "validation_template_ids",
    }
    for path, value in _walk(bundle):
        if not isinstance(value, dict):
            continue
        for key in evidence_keys:
            for ref in value.get(key, []) if isinstance(value.get(key), list) else []:
                if ref not in evidence_ids:
                    report.add_error("dangling_evidence", f"{path}.{key}", f"Unknown evidence ID {ref!r}.")
        for key in validation_keys:
            for ref in value.get(key, []) if isinstance(value.get(key), list) else []:
                if ref not in validation_ids:
                    report.add_error("dangling_validation", f"{path}.{key}", f"Unknown validation ID {ref!r}.")
        for ref in value.get("source_episode_ids", []) if isinstance(value.get("source_episode_ids"), list) else []:
            if ref not in episode_ids:
                report.add_error("dangling_episode", f"{path}.source_episode_ids", f"Unknown episode ID {ref!r}.")



def _check_atomic_skills(
    bundle: dict[str, Any],
    episode_ids: set[str],
    evidence_ids: set[str],
    report: ValidationReport,
) -> None:
    episodes = {item.get("id"): item for item in bundle.get("candidate_episodes", [])}
    evidence = {item.get("id"): item for item in bundle.get("evidence_units", [])}
    for index, skill in enumerate(bundle.get("atomic_skills", [])):
        path = f"$.atomic_skills[{index}]"
        repository = skill.get("repository")
        for ref in skill.get("source_episode_ids", []):
            if ref not in episode_ids:
                continue
            source_repository = episodes[ref].get("anchor", {}).get("repository")
            if source_repository != repository:
                report.add_error(
                    "atomic_episode_repository_mismatch", path,
                    f"Episode {ref!r} belongs to {source_repository!r}, not {repository!r}.",
                )
        for ref in skill.get("evidence_ids", []):
            if ref not in evidence_ids:
                continue
            source_repository = evidence[ref].get("repository")
            if source_repository != repository:
                report.add_error(
                    "atomic_evidence_repository_mismatch", path,
                    f"Evidence {ref!r} belongs to {source_repository!r}, not {repository!r}.",
                )


def _check_workflows(
    bundle: dict[str, Any],
    atomic_ids: set[str],
    validation_ids: set[str],
    evidence_ids: set[str],
    report: ValidationReport,
) -> None:
    atomics = {item.get("id"): item for item in bundle.get("atomic_skills", [])}
    for index, workflow in enumerate(bundle.get("workflows", [])):
        path = f"$.workflows[{index}]"
        steps = {step.get("id"): step for step in workflow.get("steps", [])}
        repository = workflow.get("repository")
        if repository != workflow.get("anchor", {}).get("repository"):
            report.add_error("workflow_repository_mismatch", path, "Workflow and anchor repositories differ.")
        for step_index, step in enumerate(workflow.get("steps", [])):
            step_path = f"{path}.steps[{step_index}]"
            for ref in step.get("atomic_skill_ids", []):
                if ref not in atomic_ids:
                    report.add_error("dangling_atomic_skill", step_path, f"Unknown atomic Skill ID {ref!r}.")
                elif atomics[ref].get("repository") != repository:
                    report.add_error(
                        "workflow_atomic_repository_mismatch", step_path,
                        f"Atomic Skill {ref!r} belongs to another repository.",
                    )
            for ref in step.get("validation_ids", []):
                if ref not in validation_ids:
                    report.add_error("dangling_validation", step_path, f"Unknown validation ID {ref!r}.")
            for ref in step.get("evidence_ids", []):
                if ref not in evidence_ids:
                    report.add_error("dangling_evidence", step_path, f"Unknown evidence ID {ref!r}.")
        ordering_edges: list[tuple[str, str]] = []
        for edge_index, edge in enumerate(workflow.get("edges", [])):
            edge_path = f"{path}.edges[{edge_index}]"
            source, target = edge.get("source_step_id"), edge.get("target_step_id")
            if source not in steps:
                report.add_error("dangling_workflow_step", edge_path, f"Unknown source step {source!r}.")
            if target not in steps:
                report.add_error("dangling_workflow_step", edge_path, f"Unknown target step {target!r}.")
            if edge.get("relation") in ORDERING_RELATIONS and source in steps and target in steps:
                ordering_edges.append((source, target))
        for decision_index, decision in enumerate(workflow.get("decision_points", [])):
            for branch in decision.get("branches", []):
                for ref in branch.get("step_ids", []):
                    if ref not in steps:
                        report.add_error(
                            "dangling_decision_step", f"{path}.decision_points[{decision_index}]",
                            f"Unknown decision branch step {ref!r}.",
                        )
        for loop_index, loop in enumerate(workflow.get("repair_loops", [])):
            for key in ("failed_step_id", "repair_step_id"):
                if loop.get(key) not in steps:
                    report.add_error(
                        "dangling_repair_step", f"{path}.repair_loops[{loop_index}]",
                        f"Unknown repair-loop step {loop.get(key)!r}.",
                    )
        _check_acyclic(set(steps), ordering_edges, path, report)


def _check_patterns(
    bundle: dict[str, Any],
    workflow_ids: set[str],
    workflow_step_ids: set[str],
    atomic_ids: set[str],
    validation_ids: set[str],
    evidence_ids: set[str],
    task_family_id: str | None,
    report: ValidationReport,
) -> None:
    workflows = {item.get("id"): item for item in bundle.get("workflows", [])}
    step_owner: dict[str, str] = {}
    step_actions: dict[str, set[str]] = {}
    for workflow_id, workflow in workflows.items():
        for step in workflow.get("steps", []):
            step_id = step.get("id")
            step_owner[step_id] = workflow_id
            step_actions[step_id] = set(step.get("atomic_skill_ids", []))

    for index, pattern in enumerate(bundle.get("patterns", [])):
        path = f"$.patterns[{index}]"
        support = pattern.get("supporting_workflow_ids", [])
        if len(set(support)) < 2:
            report.add_error("insufficient_pattern_support", path, "A Pattern requires two distinct Workflows.")
        for ref in support:
            if ref not in workflow_ids:
                report.add_error("dangling_workflow", path, f"Unknown supporting Workflow {ref!r}.")
        if pattern.get("task_family_id") != task_family_id:
            report.add_error("task_family_mismatch", path, "Pattern does not reference this bundle's task family.")
        support_repositories = {
            workflows[ref].get("repository") for ref in support if ref in workflows
        }
        diversity = pattern.get("evidence_diversity", {})
        declared_repositories = set(diversity.get("repositories", []))
        if support_repositories != declared_repositories:
            report.add_error(
                "diversity_mismatch", f"{path}.evidence_diversity.repositories",
                f"Declared repositories {sorted(declared_repositories)} do not match support {sorted(support_repositories)}.",
            )
        if set(diversity.get("workflow_ids", [])) != set(support):
            report.add_error(
                "diversity_workflow_mismatch", f"{path}.evidence_diversity.workflow_ids",
                "Evidence-diversity Workflow IDs must equal supporting_workflow_ids.",
            )
        if pattern.get("cross_repository_claim") and len(support_repositories) < 2:
            report.add_error("false_cross_repository_claim", path, "Cross-repository Pattern needs two repositories.")

        step_ids = {step.get("id") for step in pattern.get("steps", [])}
        ordering_edges: list[tuple[str, str]] = []
        for edge_index, edge in enumerate(pattern.get("edges", [])):
            edge_path = f"{path}.edges[{edge_index}]"
            source, target = edge.get("source_step_id"), edge.get("target_step_id")
            if source not in step_ids or target not in step_ids:
                report.add_error("dangling_pattern_step", edge_path, "Pattern edge references an unknown step.")
            if edge.get("relation") in ORDERING_RELATIONS and source in step_ids and target in step_ids:
                ordering_edges.append((source, target))
        _check_acyclic(step_ids, ordering_edges, path, report)

        for decision_index, decision in enumerate(pattern.get("decision_points", [])):
            for branch in decision.get("branches", []):
                for ref in branch.get("step_ids", []):
                    if ref not in step_ids:
                        report.add_error(
                            "dangling_decision_step", f"{path}.decision_points[{decision_index}]",
                            f"Unknown Pattern decision step {ref!r}.",
                        )

        for step_index, step in enumerate(pattern.get("steps", [])):
            step_path = f"{path}.steps[{step_index}]"
            realized_by: set[str] = set()
            for realization in step.get("realizations", []):
                workflow_id = realization.get("workflow_id")
                realized_by.add(workflow_id)
                if workflow_id not in support:
                    report.add_error("realization_outside_support", step_path, f"Realization uses unsupported Workflow {workflow_id!r}.")
                selected_actions: set[str] = set()
                for ref in realization.get("workflow_step_ids", []):
                    if ref not in workflow_step_ids:
                        report.add_error("dangling_workflow_step", step_path, f"Unknown WorkflowStep {ref!r}.")
                    elif step_owner.get(ref) != workflow_id:
                        report.add_error(
                            "realization_workflow_mismatch", step_path,
                            f"WorkflowStep {ref!r} does not belong to {workflow_id!r}.",
                        )
                    selected_actions.update(step_actions.get(ref, set()))
                for ref in realization.get("atomic_skill_ids", []):
                    if ref not in atomic_ids:
                        report.add_error("dangling_atomic_skill", step_path, f"Unknown Atomic Skill {ref!r}.")
                    elif ref not in selected_actions:
                        report.add_error(
                            "realization_action_mismatch", step_path,
                            f"Atomic Skill {ref!r} is not executed by the realized WorkflowSteps.",
                        )
            if len(realized_by) < 2:
                report.add_error("insufficient_step_realization", step_path, "Each PatternStep needs two distinct Workflow realizations.")
            for ref in step.get("validation_template_ids", []):
                if ref not in validation_ids:
                    report.add_error("dangling_validation", step_path, f"Unknown validation ID {ref!r}.")

        if pattern.get("lifecycle") == "validated":
            qualifying = [
                result for result in pattern.get("held_out_results", [])
                if result.get("split") in {"held_out", "time_split", "cross_repository_held_out"}
                and result.get("target_solution_access") in {"prohibited", "not_provided"}
                and result.get("success") is True
            ]
            if not qualifying:
                report.add_error("invalid_validated_pattern", path, "Validated Pattern needs a successful leakage-isolated held-out result.")
            for result in pattern.get("held_out_results", []):
                for ref in result.get("evidence_ids", []):
                    if ref not in evidence_ids:
                        report.add_error("dangling_evidence", path, f"Unknown held-out evidence ID {ref!r}.")


def _check_bindings(
    bundle: dict[str, Any], semantic_node_ids: set[str], evidence_ids: set[str], report: ValidationReport
) -> None:
    for index, binding in enumerate(bundle.get("bindings", [])):
        path = f"$.bindings[{index}]"
        for ref in binding.get("target_ids", []):
            if ref not in semantic_node_ids:
                report.add_error("dangling_binding_target", path, f"Unknown binding target {ref!r}.")
        for ref in binding.get("probe_evidence_ids", []):
            if ref not in evidence_ids:
                report.add_error("dangling_evidence", path, f"Unknown probe evidence {ref!r}.")


def _check_relations(
    bundle: dict[str, Any],
    atomic_ids: set[str], workflow_ids: set[str], workflow_step_ids: set[str],
    pattern_ids: set[str], pattern_step_ids: set[str], validation_ids: set[str],
    binding_ids: set[str], evidence_ids: set[str], claim_ids: set[str],
    report: ValidationReport,
) -> None:
    types: dict[str, str] = {}
    for ids, kind in ((atomic_ids, "atomic"), (workflow_ids, "workflow"),
                      (workflow_step_ids, "workflow_step"), (pattern_ids, "pattern"),
                      (pattern_step_ids, "pattern_step"), (validation_ids, "validation"),
                      (binding_ids, "binding"), (evidence_ids, "evidence"),
                      (claim_ids, "predicate")):
        types.update({identifier: kind for identifier in ids})
    allowed: dict[str, tuple[set[str], set[str]]] = {
        "declares_step": ({"pattern"}, {"pattern_step"}),
        "instantiates": ({"workflow"}, {"pattern"}),
        "has_step": ({"workflow"}, {"workflow_step"}),
        "realizes": ({"workflow_step"}, {"pattern_step"}),
        "executed_by": ({"workflow_step"}, {"atomic"}),
        "conforms_to": ({"atomic"}, {"pattern_step"}),
        "evidenced_by": ({"atomic", "workflow_step", "pattern_step"}, {"evidence"}),
        "supported_by": ({"pattern"}, {"workflow"}),
        "applicable_when": ({"atomic", "workflow_step", "pattern_step", "pattern"}, {"predicate"}),
        "verifies": ({"validation"}, {"atomic", "workflow", "pattern"}),
        "grounds": ({"binding"}, {"atomic", "pattern_step"}),
        "requires": ({"atomic"}, {"atomic"}),
        "enables": ({"atomic"}, {"atomic"}),
        "precedes": ({"atomic"}, {"atomic"}),
        "validates": ({"atomic"}, {"atomic"}),
        "repairs": ({"atomic"}, {"atomic"}),
        "alternative_to": ({"atomic", "pattern"}, {"atomic", "pattern"}),
        "specializes": ({"pattern"}, {"pattern"}),
        "composes_with": ({"pattern"}, {"pattern"}),
        "requires_pattern": ({"pattern"}, {"pattern"}),
    }
    for index, relation in enumerate(bundle.get("relations", [])):
        path = f"$.relations[{index}]"
        source = relation.get("source_id")
        target = relation.get("target_id")
        kind = relation.get("relation")
        if source not in types:
            report.add_error("dangling_relation_source", path, f"Unknown relation source {source!r}.")
        if target not in types:
            report.add_error("dangling_relation_target", path, f"Unknown relation target {target!r}.")
        endpoints = allowed.get(kind)
        if endpoints and source in types and target in types:
            source_types, target_types = endpoints
            if types[source] not in source_types or types[target] not in target_types:
                report.add_error(
                    "invalid_relation_endpoints", path,
                    f"{kind} cannot connect {types[source]} to {types[target]}.",
                )
            if kind == "alternative_to" and types[source] != types[target]:
                report.add_error(
                    "invalid_symmetric_relation", path,
                    "alternative_to must connect nodes of the same type.",
                )


def _check_views(
    bundle: dict[str, Any], claim_ids: set[str], step_ids: set[str],
    validation_ids: set[str], evidence_ids: set[str], report: ValidationReport,
) -> None:
    for path, value in _walk(bundle):
        if not isinstance(value, dict) or set(value) != {"routing", "execution", "audit"}:
            continue
        execution = value.get("execution", {})
        audit = value.get("audit", {})
        for ref in execution.get("step_ids", []):
            if ref not in step_ids:
                report.add_error("dangling_view_step", f"{path}.execution.step_ids", f"Unknown step ID {ref!r}.")
        for ref in execution.get("validation_ids", []):
            if ref not in validation_ids:
                report.add_error("dangling_view_validation", f"{path}.execution.validation_ids", f"Unknown validation ID {ref!r}.")
        for ref in audit.get("claim_ids", []):
            if ref not in claim_ids:
                report.add_error("dangling_view_claim", f"{path}.audit.claim_ids", f"Unknown Claim ID {ref!r}.")
        for ref in audit.get("evidence_ids", []):
            if ref not in evidence_ids:
                report.add_error("dangling_view_evidence", f"{path}.audit.evidence_ids", f"Unknown Evidence ID {ref!r}.")


def _check_quality(bundle: dict[str, Any], report: ValidationReport) -> None:
    for path, value in _walk(bundle):
        if not isinstance(value, dict) or not all(key in value for key in ("overall", "aggregation_method")):
            continue
        if not any(key in value for key in QUALITY_DIMENSIONS):
            continue
        dimensions = [value.get(key) for key in QUALITY_DIMENSIONS if value.get(key) is not None]
        if not dimensions:
            report.add_error("empty_quality", path, "At least one quality dimension must apply.")
            continue
        ceiling = min(dimensions)
        overall = value.get("overall")
        if not isinstance(overall, (int, float)):
            continue
        if overall > ceiling + 1e-9:
            report.add_error("inflated_confidence", path, f"overall={overall} exceeds weakest dimension={ceiling}.")
        if value.get("aggregation_method") == "min_dimensions" and abs(overall - ceiling) > 1e-9:
            report.add_error("incorrect_confidence_aggregation", path, "min_dimensions requires overall to equal the weakest applicable dimension.")


def _check_lifecycle(bundle: dict[str, Any], report: ValidationReport) -> None:
    review_status = bundle.get("extraction", {}).get("human_review", {}).get("status")
    for collection in ("atomic_skills", "workflows", "patterns"):
        for index, item in enumerate(bundle.get(collection, [])):
            lifecycle = item.get("lifecycle")
            path = f"$.{collection}[{index}]"
            if lifecycle in {"reviewed", "validated"} and review_status != "approved":
                report.add_error("unapproved_promotion", path, f"{lifecycle} requires approved human review.")
            if lifecycle == "deprecated" and item.get("deprecation") is None:
                report.add_error("missing_deprecation", path, "Deprecated nodes require deprecation metadata.")
            if lifecycle != "deprecated" and item.get("deprecation") is not None:
                report.add_error("premature_deprecation", path, "Non-deprecated nodes cannot carry deprecation metadata.")


def _check_report_statistics(bundle: dict[str, Any], report: ValidationReport) -> None:
    statistics = bundle.get("quality_report", {}).get("statistics", {})
    expected = {
        "evidence_count": len(bundle.get("evidence_units", [])),
        "atomic_skill_count": len(bundle.get("atomic_skills", [])),
        "workflow_count": len(bundle.get("workflows", [])),
        "pattern_count": len(bundle.get("patterns", [])),
        "binding_count": len(bundle.get("bindings", [])),
        "claim_count": sum(
            1 for _, value in _walk(bundle)
            if isinstance(value, dict) and str(value.get("id", "")).startswith("claim:")
        ),
    }
    for key, actual in expected.items():
        if statistics.get(key) != actual:
            report.add_error("statistics_mismatch", f"$.quality_report.statistics.{key}", f"Expected {actual}, found {statistics.get(key)!r}.")


def _check_acyclic(
    nodes: set[str], edges: list[tuple[str, str]], path: str, report: ValidationReport
) -> None:
    adjacency = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}
    for source, target in edges:
        adjacency[source].append(target)
        indegree[target] += 1
    queue = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in adjacency[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(nodes):
        report.add_error("ordering_cycle", path, "Primary ordering relations must form a DAG.")
