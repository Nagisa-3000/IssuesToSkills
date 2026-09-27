"""Structural validation for generalized Skill Family Bundle v2.

Only shape, references, tree closure, and report consistency are checked here.
Semantic equivalence, usefulness, applicability, duplicate/merge decisions,
and transfer judgments remain LLM-governed and are represented as evidence or
explicit governance proposals rather than inferred by this module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(slots=True)
class V2ValidationReport:
    errors: list[dict[str, str]] = field(default_factory=list)
    warnings: list[dict[str, str]] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def error(self, code: str, path: str, message: str) -> None:
        self.errors.append({"code": code, "path": path, "message": message})

    def warning(self, code: str, path: str, message: str) -> None:
        self.warnings.append({"code": code, "path": path, "message": message})


def validate_v2_bundle(bundle: Mapping[str, Any], schema: Mapping[str, Any] | None = None) -> V2ValidationReport:
    report = V2ValidationReport()
    if not isinstance(bundle, Mapping):
        report.error("root_type", "$", "bundle must be a JSON object")
        return report
    if schema is not None:
        _validate_json_schema(bundle, schema, report)
    if bundle.get("schema_version") != "2.0.0":
        report.error("schema_version", "$.schema_version", "expected 2.0.0")
    collections = _collections(bundle)
    all_ids: dict[str, str] = {}
    for name, items in collections.items():
        for index, item in enumerate(items):
            path = f"$.{name}[{index}]"
            if not isinstance(item, Mapping):
                report.error("item_type", path, "collection item must be an object")
                continue
            identifier = item.get("id")
            if not isinstance(identifier, str) or not identifier:
                report.error("missing_id", path, "collection item requires a non-empty id")
                continue
            if identifier in all_ids:
                report.error("duplicate_id", path, f"{identifier!r} already occurs at {all_ids[identifier]}")
            else:
                all_ids[identifier] = path

    evidence_ids = _ids(collections["evidence_units"])
    action_ids = _ids(collections["case_actions"])
    case_workflow_ids = _ids(collections["case_workflows"])
    atomic_ids = _ids(collections["atomic_skills"])
    workflow_ids = _ids(collections["workflow_skills"])
    pattern_ids = _ids(collections["patterns"])
    node_ids = atomic_ids | workflow_ids | pattern_ids
    realization_ids = _nested_ids(collections["atomic_skills"] + collections["workflow_skills"] + collections["patterns"], "realizations")
    transfer_ids = _ids(collections["transfer_records"])

    for name, items in collections.items():
        for index, item in enumerate(items):
            if isinstance(item, Mapping):
                _check_evidence_refs(item, evidence_ids, f"$.{name}[{index}]", report)

    for index, workflow in enumerate(collections["case_workflows"]):
        if not isinstance(workflow, Mapping):
            continue
        path = f"$.case_workflows[{index}]"
        _check_refs(workflow.get("case_action_ids", []), action_ids, f"{path}.case_action_ids", report)
        _check_refs(workflow.get("failed_or_reverted_action_ids", []), action_ids, f"{path}.failed_or_reverted_action_ids", report)
        _check_refs(workflow.get("acceptance_evidence_ids", []), evidence_ids, f"{path}.acceptance_evidence_ids", report)
        local_actions = set(workflow.get("case_action_ids", []))
        for edge_index, edge in enumerate(workflow.get("edges", [])):
            if isinstance(edge, Mapping) and (edge.get("source_id") not in local_actions or edge.get("target_id") not in local_actions):
                report.error("dangling_case_edge", f"{path}.edges[{edge_index}]", "edge endpoint is not a case action in this workflow")

    for index, skill in enumerate(collections["atomic_skills"]):
        if isinstance(skill, Mapping):
            _check_skill(skill, atomic_ids, workflow_ids, pattern_ids, transfer_ids, realization_ids, evidence_ids, f"$.atomic_skills[{index}]", report)
    for index, skill in enumerate(collections["workflow_skills"]):
        if not isinstance(skill, Mapping):
            continue
        path = f"$.workflow_skills[{index}]"
        _check_skill(skill, atomic_ids, workflow_ids, pattern_ids, transfer_ids, realization_ids, evidence_ids, path, report)
        local_step_ids = {s.get("id") for s in skill.get("steps", []) if isinstance(s, Mapping)}
        for step_index, step in enumerate(skill.get("steps", [])):
            if isinstance(step, Mapping):
                _check_refs(step.get("uses_atomic_skill_ids", []), atomic_ids, f"{path}.steps[{step_index}].uses_atomic_skill_ids", report)
        for edge_index, edge in enumerate(skill.get("edges", [])):
            if isinstance(edge, Mapping) and (edge.get("source_id") not in local_step_ids or edge.get("target_id") not in local_step_ids):
                report.error("dangling_workflow_edge", f"{path}.edges[{edge_index}]", "edge endpoint is not a workflow step")
    for index, pattern in enumerate(collections["patterns"]):
        if not isinstance(pattern, Mapping):
            continue
        path = f"$.patterns[{index}]"
        _check_skill(pattern, atomic_ids, workflow_ids, pattern_ids, transfer_ids, realization_ids, evidence_ids, path, report)
        _check_refs(pattern.get("supporting_case_workflow_ids", []), case_workflow_ids, f"{path}.supporting_case_workflow_ids", report)
        for variant_index, variant in enumerate(pattern.get("workflow_variants", [])):
            if isinstance(variant, Mapping) and variant.get("workflow_skill_id") not in workflow_ids:
                report.error("dangling_pattern_workflow", f"{path}.workflow_variants[{variant_index}]", "workflow variant does not reference a workflow skill")

    for index, transfer in enumerate(collections["transfer_records"]):
        if not isinstance(transfer, Mapping):
            continue
        path = f"$.transfer_records[{index}]"
        if transfer.get("knowledge_node_id") not in node_ids:
            report.error("dangling_transfer_node", path, "knowledge_node_id does not reference a skill node")
        _check_refs(transfer.get("evidence_ids", []), evidence_ids, f"{path}.evidence_ids", report)
        if transfer.get("result") == "not_run":
            report.warning("transfer_not_run", path, "transfer is not evidence of validation")

    for index, binding in enumerate(collections["bindings"]):
        if not isinstance(binding, Mapping):
            continue
        path = f"$.bindings[{index}]"
        if binding.get("knowledge_node_id") not in node_ids:
            report.error("dangling_binding_node", path, "knowledge_node_id does not reference a skill node")
        _check_refs(binding.get("probe_evidence_ids", []), evidence_ids, f"{path}.probe_evidence_ids", report)

    for index, relation in enumerate(collections["relations"]):
        if not isinstance(relation, Mapping):
            continue
        path = f"$.relations[{index}]"
        source, target = relation.get("source_id"), relation.get("target_id")
        if source not in all_ids or target not in all_ids:
            report.error("dangling_relation", path, "relation endpoint does not reference a bundle item")
        if relation.get("relation") == "part_of":
            # Tree edges point from child to parent: Atomic -> Workflow -> Pattern.
            if source in workflow_ids and target not in pattern_ids:
                report.error("invalid_workflow_parent", path, "workflow part_of edges must target patterns")
            if source in atomic_ids and target not in workflow_ids:
                report.error("invalid_atomic_parent", path, "atomic part_of edges must target workflows")

    _check_packages(collections["agent_skill_packages"], node_ids, report)
    _check_quality(bundle, collections, report)
    _check_promotion(collections, report)
    return report


def _collections(bundle: Mapping[str, Any]) -> dict[str, list[Any]]:
    names = ("evidence_units", "case_actions", "case_workflows", "atomic_skills", "workflow_skills", "patterns", "transfer_records", "bindings", "relations", "rejected_alignments", "agent_skill_packages")
    return {name: list(bundle.get(name, [])) if isinstance(bundle.get(name, []), list) else [] for name in names}


def _ids(items: Iterable[Any]) -> set[str]:
    return {str(item["id"]) for item in items if isinstance(item, Mapping) and isinstance(item.get("id"), str)}


def _nested_ids(items: Iterable[Any], key: str) -> set[str]:
    result: set[str] = set()
    for item in items:
        if isinstance(item, Mapping) and isinstance(item.get(key), list):
            result |= _ids(item[key])
    return result


def _check_refs(values: Any, known: set[str], path: str, report: V2ValidationReport) -> None:
    if isinstance(values, list):
        for index, value in enumerate(values):
            if value not in known:
                report.error("dangling_reference", f"{path}[{index}]", f"unknown id {value!r}")


def _check_evidence_refs(item: Mapping[str, Any], evidence_ids: set[str], path: str, report: V2ValidationReport) -> None:
    for key in ("evidence_ids", "acceptance_evidence_ids", "probe_evidence_ids"):
        if key in item:
            _check_refs(item.get(key), evidence_ids, f"{path}.{key}", report)


def _check_skill(skill: Mapping[str, Any], atomic_ids: set[str], workflow_ids: set[str], pattern_ids: set[str], transfer_ids: set[str], realization_ids: set[str], evidence_ids: set[str], path: str, report: V2ValidationReport) -> None:
    _check_refs(skill.get("transfer_record_ids", []), transfer_ids, f"{path}.transfer_record_ids", report)
    for realization_index, realization in enumerate(skill.get("realizations", [])):
        if not isinstance(realization, Mapping):
            continue
        if realization.get("id") not in realization_ids:
            report.error("dangling_realization", f"{path}.realizations[{realization_index}]", "unknown realization id")
        _check_refs(realization.get("evidence_ids", []), evidence_ids, f"{path}.realizations[{realization_index}].evidence_ids", report)
    assessment = skill.get("abstraction_assessment")
    if isinstance(assessment, Mapping):
        for key, check in assessment.items():
            if isinstance(check, Mapping):
                _check_refs(check.get("supporting_realization_ids", []), realization_ids, f"{path}.abstraction_assessment.{key}.supporting_realization_ids", report)
    if skill.get("lifecycle") == "validated" and isinstance(skill.get("quality"), Mapping) and skill["quality"].get("validation_strength", 0) <= 0:
        report.error("validated_without_validation_strength", path, "validated node must have non-zero validation strength")


def _check_packages(packages: list[Any], node_ids: set[str], report: V2ValidationReport) -> None:
    for index, package in enumerate(packages):
        if not isinstance(package, Mapping):
            continue
        path = f"$.agent_skill_packages[{index}]"
        if package.get("primary_node_id") not in node_ids:
            report.error("dangling_package_node", path, "primary_node_id does not reference a skill node")


def _check_quality(bundle: Mapping[str, Any], collections: Mapping[str, list[Any]], report: V2ValidationReport) -> None:
    value = bundle.get("quality_report")
    if not isinstance(value, Mapping):
        return
    expected = {"evidence_units": len(collections["evidence_units"]), "case_actions": len(collections["case_actions"]), "case_workflows": len(collections["case_workflows"]), "atomic_skills": len(collections["atomic_skills"]), "workflow_skills": len(collections["workflow_skills"]), "patterns": len(collections["patterns"]), "package_count": len(collections["agent_skill_packages"])}
    observed = dict(value.get("instance_counts", {})) | dict(value.get("knowledge_counts", {}))
    observed["package_count"] = value.get("package_count")
    for key, expected_value in expected.items():
        if observed.get(key) != expected_value:
            report.error("quality_count_mismatch", f"$.quality_report.{key}", f"expected {expected_value}, got {observed.get(key)!r}")


def _check_promotion(collections: Mapping[str, list[Any]], report: V2ValidationReport) -> None:
    for collection_name in ("atomic_skills", "workflow_skills", "patterns"):
        for index, skill in enumerate(collections[collection_name]):
            if not isinstance(skill, Mapping):
                continue
            if skill.get("lifecycle") != "validated":
                continue
            transfers = [item for item in collections["transfer_records"] if isinstance(item, Mapping) and item.get("knowledge_node_id") == skill.get("id")]
            if not any(item.get("result") == "pass" for item in transfers):
                report.error("validated_without_transfer", f"$.{collection_name}[{index}]", "validated node requires a passing transfer record")


def _validate_json_schema(bundle: Mapping[str, Any], schema: Mapping[str, Any], report: V2ValidationReport) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        report.warning("jsonschema_unavailable", "$", "jsonschema is unavailable; structural validation only")
        return
    for error in sorted(Draft202012Validator(schema).iter_errors(bundle), key=lambda item: list(item.path)):
        location = "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.path)
        report.error("schema", location, error.message)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

