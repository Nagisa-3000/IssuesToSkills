#!/usr/bin/env python3
"""Validate a cross-project Issue/PR extraction inventory and its artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REQUIRED_ARTIFACTS = (
    "prompt.txt",
    "issue-bundle.json",
    "codex-response.json",
    "validation.json",
)
REQUIRED_GRAPH_LISTS = (
    "when_to_use",
    "anti_goals",
    "not_applicable_when",
    "validation_ladder",
    "stop_conditions",
)


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return value


def find_repository_root(path: Path) -> Path:
    for candidate in (path.parent, *path.parents):
        if (candidate / ".git").exists():
            return candidate.resolve()
    return Path.cwd().resolve()


def validate_inventory(
    inventory_path: Path,
    *,
    repository_root: Path | None = None,
    expected_categories: int | None = None,
    expected_training_per_category: int | None = None,
    expected_model: str | None = None,
    require_packages: bool = False,
) -> dict[str, Any]:
    """Audit historical IR by default; the CLI requires packages for completion."""
    inventory_path = inventory_path.resolve()
    root = (repository_root or find_repository_root(inventory_path)).resolve()
    inventory = load_object(inventory_path)
    errors: list[str] = []

    records = inventory.get("records")
    summaries = inventory.get("category_summaries")
    if not isinstance(records, list):
        return {"valid": False, "errors": ["inventory.records must be an array"]}
    if not isinstance(summaries, list):
        return {"valid": False, "errors": ["inventory.category_summaries must be an array"]}

    summary_by_category: dict[str, dict[str, Any]] = {}
    for summary in summaries:
        if not isinstance(summary, dict) or not isinstance(summary.get("category"), str):
            errors.append("each category summary must be an object with a category")
            continue
        category = summary["category"]
        if category in summary_by_category:
            errors.append(f"duplicate category summary: {category}")
        summary_by_category[category] = summary

    records_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    case_ids: list[str] = []
    models: Counter[str] = Counter()
    sample_kinds: Counter[str] = Counter()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index} must be an object")
            continue
        category = record.get("category")
        case_id = record.get("case_id")
        if not isinstance(category, str):
            errors.append(f"record {index} has no category")
            continue
        records_by_category[category].append(record)
        if isinstance(case_id, str):
            case_ids.append(case_id)
        else:
            errors.append(f"record {index} has no case_id")
        if isinstance(record.get("model"), str):
            models[record["model"]] += 1
        if isinstance(record.get("sample_kind"), str):
            sample_kinds[record["sample_kind"]] += 1

    if len(case_ids) != len(set(case_ids)):
        errors.append("training case ids must be unique")
    if set(records_by_category) != set(summary_by_category):
        errors.append("record categories do not match category summaries")
    if expected_categories is not None and len(summary_by_category) != expected_categories:
        errors.append(
            f"expected {expected_categories} categories, found {len(summary_by_category)}"
        )
    if expected_model is not None and set(models) != {expected_model}:
        errors.append(f"expected only model {expected_model}, found {sorted(models)}")

    holdout_leaks = 0
    admitted_atomics = 0
    admitted_workflows = 0
    for category, summary in summary_by_category.items():
        category_records = records_by_category.get(category, [])
        repositories = {
            record.get("repository")
            for record in category_records
            if isinstance(record.get("repository"), str)
        }
        if len(repositories) != len(category_records):
            errors.append(f"{category}: training records must use distinct repositories")
        if expected_training_per_category is not None:
            if len(category_records) != expected_training_per_category:
                errors.append(
                    f"{category}: expected {expected_training_per_category} training records, "
                    f"found {len(category_records)}"
                )
            if len(repositories) != expected_training_per_category:
                errors.append(
                    f"{category}: training records must come from "
                    f"{expected_training_per_category} distinct repositories"
                )

        holdout = summary.get("holdout")
        if not isinstance(holdout, dict):
            errors.append(f"{category}: missing holdout object")
            continue
        if holdout.get("repository") in repositories:
            errors.append(f"{category}: holdout repository appears in training records")
        if holdout.get("case_id") in case_ids:
            errors.append(f"{category}: holdout case appears in training records")
        if holdout.get("role") != "holdout_candidate":
            errors.append(f"{category}: holdout must set role=holdout_candidate")
        if holdout.get("split") != "holdout_candidate":
            errors.append(f"{category}: holdout must set split=holdout_candidate")
        if holdout.get("extraction_forbidden") is not True:
            errors.append(f"{category}: holdout must set extraction_forbidden=true")
        if holdout.get("evidence_status") != "intentionally_not_extracted":
            errors.append(f"{category}: holdout is not marked intentionally_not_extracted")

        holdout_needles = [
            value
            for value in (holdout.get("case_id"), holdout.get("issue_url"))
            if isinstance(value, str) and value
        ]
        for record in category_records:
            case_id = str(record.get("case_id", "<unknown>"))
            if record.get("manual_validation_valid") is not True:
                errors.append(f"{case_id}: manual validation did not pass")
            direct = record.get("output_contract") == "direct-skill-files-v1"
            if not direct and record.get("jsonschema_valid") is not True:
                errors.append(f"{case_id}: JSON Schema validation did not pass")
            relative_output = record.get("relative_output")
            if not isinstance(relative_output, str):
                errors.append(f"{case_id}: missing relative_output")
                continue
            output = (root / relative_output).resolve()
            if not output.is_relative_to(root):
                errors.append(f"{case_id}: relative_output escapes repository root")
                continue

            artifact_texts: dict[str, str] = {}
            required_artifacts = tuple("codex-response.skill.md" if direct and name == "codex-response.json" else name for name in REQUIRED_ARTIFACTS)
            for artifact_name in required_artifacts:
                artifact = output / artifact_name
                if not artifact.is_file():
                    errors.append(f"{case_id}: missing {artifact_name}")
                    continue
                artifact_texts[artifact_name] = artifact.read_text(encoding="utf-8")
            if len(artifact_texts) != len(required_artifacts):
                continue

            for artifact_name, artifact_text in artifact_texts.items():
                for needle in holdout_needles:
                    if needle in artifact_text:
                        holdout_leaks += 1
                        errors.append(f"{case_id}: holdout leaked into {artifact_name}")

            if direct:
                sys.path.insert(0, str(root / "src"))
                from arex_skill_graph.direct_skill_extraction import (
                    inspect_direct_package,
                    parse_bundle,
                )
                from arex_skill_graph.skill_packages import hydrate_package

                try:
                    authored, deferred = parse_bundle(artifact_texts["codex-response.skill.md"])
                    if deferred or not authored:
                        raise ValueError("no directly authored Skill packages")
                    if json.loads(artifact_texts["validation.json"]) != {"valid": True, "errors": []}:
                        raise ValueError("validation.json does not record a clean pass")
                    refs = record.get("skill_packages") or []
                    if len(refs) != len(authored) or len(refs) != record.get("workflow_count"):
                        raise ValueError("direct package count disagrees with inventory")
                    direct_actions = set()
                    for reference in refs:
                        hydrated = hydrate_package({"id": reference["skill_id"], "skill_package": reference}, repository_root=root)
                        package = Path(hydrated["package_path"])
                        for relative, content in authored[package.name].items():
                            if (package / relative).read_bytes() != content.encode("utf-8"):
                                raise ValueError("published files differ from model-authored response")
                        projection = inspect_direct_package(package)
                        if projection["episode"]["episode_id"] != record.get("episode_id"):
                            raise ValueError("direct Episode identity disagrees with inventory")
                        direct_actions.update(row["id"] for row in projection["actions"])
                    if len(direct_actions) != record.get("atomic_count"):
                        raise ValueError("direct Action count disagrees with inventory")
                    admitted_atomics += len(direct_actions)
                    admitted_workflows += len(refs)
                except (ValueError, OSError, KeyError, TypeError):
                    errors.append(f"{case_id}: direct Skill artifact validation failed")
                continue

            try:
                response = json.loads(artifact_texts["codex-response.json"])
                validation = json.loads(artifact_texts["validation.json"])
            except json.JSONDecodeError as exc:
                errors.append(f"{case_id}: invalid artifact JSON: {exc}")
                continue
            if validation != {"valid": True, "errors": []}:
                errors.append(f"{case_id}: validation.json does not record a clean pass")
            if not isinstance(response, dict):
                errors.append(f"{case_id}: codex-response.json must be an object")
                continue

            episode = response.get("episode")
            if not isinstance(episode, dict) or episode.get("episode_id") != record.get("episode_id"):
                errors.append(f"{case_id}: episode id does not match inventory")

            evidence = response.get("evidence_units")
            atomics = response.get("candidate_atomics")
            workflows = response.get("candidate_workflows")
            if not isinstance(evidence, list) or not evidence:
                errors.append(f"{case_id}: response has no evidence units")
                continue
            if not isinstance(atomics, list) or not atomics:
                errors.append(f"{case_id}: response has no candidate Actions")
                continue
            if not isinstance(workflows, list) or not workflows:
                errors.append(f"{case_id}: response has no candidate Workflows")
                continue

            admitted_atomics += len(atomics)
            admitted_workflows += len(workflows)
            evidence_ids = {
                unit.get("id") for unit in evidence if isinstance(unit, dict) and unit.get("id")
            }
            atomic_names = {
                atomic.get("name")
                for atomic in atomics
                if isinstance(atomic, dict) and atomic.get("name")
            }
            if len(evidence_ids) != len(evidence):
                errors.append(f"{case_id}: evidence ids must be present and unique")
            if len(atomic_names) != len(atomics):
                errors.append(f"{case_id}: Action names must be present and unique")

            for atomic in atomics:
                if not isinstance(atomic, dict):
                    errors.append(f"{case_id}: candidate Action must be an object")
                    continue
                if not set(atomic.get("evidence_ids", [])) <= evidence_ids:
                    errors.append(f"{case_id}: Action references unknown evidence")
                semantic_action = atomic.get("semantic_action")
                if not isinstance(semantic_action, dict):
                    errors.append(f"{case_id}: Action has no semantic_action contract")
                    continue
                for field in ("pre_state", "post_state", "validation"):
                    if not semantic_action.get(field):
                        errors.append(f"{case_id}: Action is missing {field}")
                if not set(semantic_action.get("evidence_ids", [])) <= evidence_ids:
                    errors.append(f"{case_id}: semantic Action references unknown evidence")

            for workflow in workflows:
                if not isinstance(workflow, dict):
                    errors.append(f"{case_id}: candidate Workflow must be an object")
                    continue
                if not set(workflow.get("atomic_names", [])) <= atomic_names:
                    errors.append(f"{case_id}: Workflow references unknown Actions")
                if not set(workflow.get("evidence_ids", [])) <= evidence_ids:
                    errors.append(f"{case_id}: Workflow references unknown evidence")
                graph = workflow.get("workflow_graph")
                if not isinstance(graph, dict):
                    errors.append(f"{case_id}: Workflow has no workflow_graph")
                    continue
                for field in REQUIRED_GRAPH_LISTS:
                    if not isinstance(graph.get(field), list) or not graph[field]:
                        errors.append(f"{case_id}: Workflow is missing non-empty {field}")
                steps = graph.get("steps")
                if not isinstance(steps, list) or not steps:
                    errors.append(f"{case_id}: Workflow has no steps")
                    continue
                step_refs = {
                    step.get("action_name")
                    for step in steps
                    if isinstance(step, dict) and step.get("action_name")
                }
                if not step_refs <= atomic_names:
                    errors.append(f"{case_id}: Workflow step references unknown Actions")
                for step in steps:
                    if not isinstance(step, dict):
                        continue
                    if not set(step.get("depends_on", [])) <= atomic_names:
                        errors.append(f"{case_id}: Workflow dependency references unknown Actions")
                for edge in graph.get("edges", []):
                    if not isinstance(edge, dict):
                        errors.append(f"{case_id}: Workflow edge must be an object")
                        continue
                    if edge.get("from") not in atomic_names or edge.get("to") not in atomic_names:
                        errors.append(f"{case_id}: Workflow edge references unknown Actions")

    counts = inventory.get("counts")
    if isinstance(counts, dict):
        actual_counts = {
            "categories": len(summary_by_category),
            "training_cases": len(records),
            "admitted_episodes": len(records),
            "manual_validation_pass": sum(
                record.get("manual_validation_valid") is True
                for record in records
                if isinstance(record, dict)
            ),
            "jsonschema_validation_pass": sum(
                record.get("jsonschema_valid") is True
                for record in records
                if isinstance(record, dict)
            ),
            "candidate_atomics": admitted_atomics,
            "candidate_workflows": admitted_workflows,
            "holdouts": len(summary_by_category),
            "holdout_leaks": holdout_leaks,
        }
        for key, actual in actual_counts.items():
            if key in counts and counts[key] != actual:
                errors.append(f"inventory count {key}={counts[key]} does not match {actual}")

    declared_sample_kinds = inventory.get("sample_kind_counts")
    if isinstance(declared_sample_kinds, dict) and dict(sample_kinds) != declared_sample_kinds:
        errors.append("sample_kind_counts does not match records")

    if inventory_path.is_relative_to(root):
        inventory_reference = inventory_path.relative_to(root).as_posix()
        repository_reference = "."
    else:
        inventory_reference = str(inventory_path)
        repository_reference = str(root)

    report = {
        "schema_version": "extraction-inventory-validation-v1",
        "inventory": inventory_reference,
        "repository_root": repository_reference,
        "valid": not errors,
        "counts": {
            "categories": len(summary_by_category),
            "training_cases": len(records),
            "holdouts": len(summary_by_category),
            "candidate_atomics": admitted_atomics,
            "candidate_workflows": admitted_workflows,
            "holdout_leaks": holdout_leaks,
        },
        "models": dict(models),
        "sample_kinds": dict(sample_kinds),
        "errors": errors,
    }
    if require_packages:
        sys.path.insert(0, str(root / "src"))
        from arex_skill_graph.skill_packages import hydrate_package

        package_errors = []
        package_count = 0
        for record in records:
            refs = record.get("skill_packages") or []
            if len(refs) != record.get("workflow_count", 0) or not refs:
                package_errors.append(f"{record.get('case_id')}: Workflow IR has no complete package mapping")
                continue
            for reference in refs:
                try:
                    hydrate_package({"id": reference["skill_id"], "skill_package": reference},
                                    repository_root=root)
                    package_count += 1
                except (ValueError, KeyError):
                    package_errors.append(f"{record.get('case_id')}: invalid Skill package reference")
        report["ir_validation_valid"] = report["valid"]
        report["artifact_validation_valid"] = report["valid"]
        report["materialized_skill_packages"] = package_count
        report["extraction_success"] = report["valid"] and not package_errors and package_count > 0
        report["status"] = "admitted_candidate" if report["extraction_success"] else "materialization_pending"
        report["valid"] = report["extraction_success"]
        report["errors"] = errors + package_errors
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--expected-categories", type=int)
    parser.add_argument("--expected-training-per-category", type=int)
    parser.add_argument("--expected-model")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--structured-ir-only", action="store_true",
                        help="audit frozen JSON IR without claiming complete Skill extraction")
    args = parser.parse_args()

    report = validate_inventory(
        args.inventory,
        repository_root=args.repository_root,
        expected_categories=args.expected_categories,
        expected_training_per_category=args.expected_training_per_category,
        expected_model=args.expected_model,
        require_packages=not args.structured_ir_only,
    )
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
