#!/usr/bin/env python3
"""Validate and summarize a parallel Issue -> Episode -> Atomic -> Workflow run."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def cases_from_manifest(path: Path) -> list[dict[str, Any]]:
    value = load_json(path)
    if isinstance(value, dict):
        value = value.get("cases")
    if not isinstance(value, list):
        raise TypeError(f"{path} must contain a cases array")
    return [dict(item) for item in value if isinstance(item, dict)]


def parse_usage(path: Path) -> dict[str, int]:
    result: dict[str, int] = {}
    if not path.is_file():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if value.get("type") != "turn.completed" or not isinstance(value.get("usage"), dict):
            continue
        result = {
            key: int(value["usage"].get(key, 0))
            for key in (
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "reasoning_output_tokens",
            )
        }
    return result


def category_from_filename(path: Path) -> str:
    return re.sub(r"^\d\d-", "", path.stem)


def case_directory(category_dir: Path, case: dict[str, Any]) -> Path:
    repository = str(case["repository"]).replace("/", "__")
    return category_dir / f"{repository}__{case['issue']}"


def canonical_episode_key(episode: dict[str, Any]) -> tuple[str, int]:
    metadata = episode.get("metadata") if isinstance(episode.get("metadata"), dict) else {}
    return str(episode.get("repository") or metadata.get("repository") or ""), int(
        metadata.get("issue") or 0
    )


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def summarize(
    run_root: Path,
    manifest_root: Path,
    schema_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    category_manifests = sorted(manifest_root.glob("[0-9][0-9]-*.json"))
    holdout_cases = cases_from_manifest(manifest_root / "holdouts.json")
    holdout_by_category = {str(item["category"]): item for item in holdout_cases}
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    all_episodes: list[dict[str, Any]] = []
    category_summaries: list[dict[str, Any]] = []

    for manifest_path in category_manifests:
        category = category_from_filename(manifest_path)
        category_dir = run_root / manifest_path.stem
        cases = cases_from_manifest(manifest_path)
        summary_path = category_dir / "extraction-summary.json"
        episodes_path = category_dir / "episodes.json"
        if not summary_path.is_file() or not episodes_path.is_file():
            errors.append(f"{category}: missing extraction summary or episodes.json")
            continue
        run_summary = load_json(summary_path)
        episodes = load_json(episodes_path)
        if not isinstance(episodes, list):
            errors.append(f"{category}: episodes.json is not an array")
            continue
        all_episodes.extend(dict(item) for item in episodes if isinstance(item, dict))
        episodes_by_key = {
            canonical_episode_key(item): item for item in episodes if isinstance(item, dict)
        }
        category_atomic_count = 0
        category_workflow_count = 0
        exact = 0
        substitutes = 0

        holdout = holdout_by_category.get(category)
        holdout_url = str(holdout.get("issue_url") or "") if holdout else ""
        if holdout_url:
            for path in category_dir.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix not in {".json", ".md", ".txt", ".log"}:
                    continue
                if holdout_url in path.read_text(encoding="utf-8", errors="ignore"):
                    errors.append(f"{category}: holdout URL leaked into {path}")

        for case in cases:
            repository = str(case["repository"])
            issue = int(case["issue"])
            case_dir = case_directory(category_dir, case)
            response_path = case_dir / "codex-response.json"
            validation_path = case_dir / "validation.json"
            if not response_path.is_file() or not validation_path.is_file():
                errors.append(f"{category}: missing response/validation for {repository}#{issue}")
                continue
            response = load_json(response_path)
            schema_errors = sorted(error.message for error in validator.iter_errors(response))
            validation = load_json(validation_path)
            manual_valid = validation == {"valid": True, "errors": []}
            episode = episodes_by_key.get((repository, issue))
            if episode is None:
                errors.append(f"{category}: no canonical episode for {repository}#{issue}")
            if schema_errors:
                errors.append(
                    f"{category}: schema failure for {repository}#{issue}: {schema_errors[0]}"
                )
            if not manual_valid:
                errors.append(f"{category}: manual validation failure for {repository}#{issue}")

            atomics = _list(response.get("candidate_atomics"))
            workflows = _list(response.get("candidate_workflows"))
            category_atomic_count += len(atomics)
            category_workflow_count += len(workflows)
            sample_kind = str(case.get("sample_kind") or "")
            exact += sample_kind == "exact_table_row"
            substitutes += sample_kind == "verified_substitute"
            usage = parse_usage(case_dir / "codex-stdout.log")
            command = load_json(case_dir / "codex-command.json")
            first_workflow = workflows[0] if workflows else {}
            graph = (
                first_workflow.get("workflow_graph")
                if isinstance(first_workflow.get("workflow_graph"), dict)
                else {}
            )
            records.append(
                {
                    "category": category,
                    "case_id": case.get("case_id") or case.get("id"),
                    "repository": repository,
                    "artifact_number": issue,
                    "artifact_url": case.get("resolution_url")
                    or case.get("issue_url")
                    or case.get("seed_issue_url"),
                    "sample_kind": sample_kind,
                    "seed_issue": case.get("seed_issue"),
                    "seed_issue_url": case.get("seed_issue_url"),
                    "seed_relation": case.get("seed_relation"),
                    "ref": case.get("ref") or case.get("extraction_ref"),
                    "episode_id": (episode or {}).get("episode_id"),
                    "episode_title": response.get("episode", {}).get("title"),
                    "evidence_count": len(_list(response.get("evidence_units"))),
                    "atomic_count": len(atomics),
                    "atomic_names": [item.get("name") for item in atomics],
                    "atomic_titles": [item.get("title") for item in atomics],
                    "workflow_count": len(workflows),
                    "workflow_names": [item.get("name") for item in workflows],
                    "workflow_titles": [item.get("title") for item in workflows],
                    "when_to_use": _list(graph.get("when_to_use")),
                    "anti_goals": _list(graph.get("anti_goals")),
                    "validation_ladder": _list(graph.get("validation_ladder")),
                    "stop_conditions": _list(graph.get("stop_conditions")),
                    "unresolved_count": len(_list(response.get("unresolved_questions"))),
                    "manual_validation_valid": manual_valid,
                    "jsonschema_valid": not schema_errors,
                    "model": command.get("model"),
                    "profile": command.get("profile"),
                    "sandbox": command.get("sandbox"),
                    "bypass_sandbox": command.get("bypass_sandbox"),
                    "usage": usage,
                    "relative_output": str(case_dir),
                }
            )

        category_summaries.append(
            {
                "category": category,
                "admitted_episodes": len(episodes),
                "exact_table_rows": exact,
                "verified_substitutes": substitutes,
                "atomic_count": category_atomic_count,
                "workflow_count": category_workflow_count,
                "runner_total_cases": run_summary.get("total_cases"),
                "runner_admitted_episodes": run_summary.get("admitted_episodes"),
                "runner_insufficient_or_failed": run_summary.get("insufficient_or_failed"),
                "holdout": holdout,
            }
        )

    usage_totals = Counter()
    for record in records:
        usage_totals.update(record["usage"])
    counts = {
        "categories": len(category_summaries),
        "training_cases": len(records),
        "admitted_episodes": len(all_episodes),
        "manual_validation_pass": sum(record["manual_validation_valid"] for record in records),
        "jsonschema_validation_pass": sum(record["jsonschema_valid"] for record in records),
        "exact_table_rows": sum(item["exact_table_rows"] for item in category_summaries),
        "verified_substitutes": sum(item["verified_substitutes"] for item in category_summaries),
        "candidate_atomics": sum(record["atomic_count"] for record in records),
        "candidate_workflows": sum(record["workflow_count"] for record in records),
        "holdouts": len(holdout_cases),
        "holdout_leaks": sum("holdout URL leaked" in error for error in errors),
    }
    inventory = {
        "schema_version": "agent-core-seven-category-extraction-inventory-v2-contract",
        "scope": "ChangeEpisode plus candidate Atomic and actionable Workflow extraction only",
        "run": {
            "path": str(run_root),
            "response_schema": str(schema_path),
            "model": sorted({str(record["model"]) for record in records}),
            "profile": sorted({str(record["profile"]) for record in records}),
            "sandbox": sorted({str(record["sandbox"]) for record in records}),
            "api_key_persisted": False,
        },
        "counts": counts,
        "token_usage": dict(usage_totals),
        "category_summaries": category_summaries,
        "records": records,
        "validation_errors": errors,
    }
    return inventory, all_episodes, errors


def render_markdown(inventory: dict[str, Any]) -> str:
    counts = inventory["counts"]
    lines = [
        "# Agent-core seven-category extraction: actionable Workflow contract",
        "",
        "## Summary",
        "",
        f"- Training cases: {counts['training_cases']}",
        f"- Admitted ChangeEpisodes: {counts['admitted_episodes']}",
        f"- Candidate Atomics: {counts['candidate_atomics']}",
        f"- Candidate Workflows: {counts['candidate_workflows']}",
        f"- Schema-valid responses: {counts['jsonschema_validation_pass']}",
        f"- Holdout leaks: {counts['holdout_leaks']}",
        "",
        "| Category | Episodes | Atomic | Workflow | Exact | Substitute | Holdout |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in inventory["category_summaries"]:
        holdout = item.get("holdout") or {}
        holdout_text = f"{holdout.get('repository', '')} #{holdout.get('issue', '')}".strip()
        lines.append(
            f"| {item['category']} | {item['admitted_episodes']} | "
            f"{item['atomic_count']} | {item['workflow_count']} | "
            f"{item['exact_table_rows']} | {item['verified_substitutes']} | "
            f"{holdout_text} |"
        )
    lines.extend(["", "## Cases", ""])
    for record in inventory["records"]:
        lines.extend(
            [
                f"### {record['repository']} #{record['artifact_number']}",
                "",
                f"- Category: `{record['category']}`",
                f"- Episode: {record['episode_title']}",
                "- Atomics: " + "; ".join(str(value) for value in record["atomic_titles"]),
                "- Workflows: " + "; ".join(str(value) for value in record["workflow_titles"]),
                "- When to use: " + "; ".join(str(value) for value in record["when_to_use"]),
                "- Anti-goals: " + "; ".join(str(value) for value in record["anti_goals"]),
                "",
            ]
        )
    if inventory["validation_errors"]:
        lines.extend(["## Validation errors", ""])
        lines.extend(f"- {error}" for error in inventory["validation_errors"])
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--manifest-root", type=Path, required=True)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()
    inventory, episodes, errors = summarize(args.run_root, args.manifest_root, args.schema)
    (args.run_root / "episodes-all.json").write_text(
        json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.run_root / "extraction-inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.run_root / "extraction-inventory.md").write_text(
        render_markdown(inventory), encoding="utf-8"
    )
    print(json.dumps({"counts": inventory["counts"], "errors": errors}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
