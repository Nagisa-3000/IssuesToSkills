#!/usr/bin/env python3
"""Deterministically validate a compiled Resolution Agent Skill package."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_FILES = (
    "SKILL.md",
    "references/workflow.md",
    "references/action-contracts.md",
    "references/validation.md",
    "references/feedback.md",
    "references/provenance.yaml",
    "evals/prompts.jsonl",
    "evals/rubric.schema.json",
    "evals/expected.jsonl",
)
REQUIRED_SECTION_GROUPS = (
    ("## use this skill when",),
    ("## do not use this skill when", "## anti-goals"),
    ("## required inputs",),
    ("## workflow", "## action sequence"),
    ("## validation",),
    ("## stop, ask, or defer", "## stopping conditions"),
    ("## supporting references", "## resources"),
)
REQUIRED_PROMPT_CLASSES = {
    "direct",
    "indirect",
    "contextual",
    "incomplete",
    "negative",
    "edge",
}
FORBIDDEN_PROVENANCE_KEYS = {
    "base_ref",
    "solution_ref",
    "hidden_solution",
    "hidden_solution_patch",
}


def _read_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name} is not valid JSON: {exc}")
        return None


def _read_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"could not read {path.name}: {exc}")
        return rows
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{number} is not valid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.name}:{number} must be a JSON object")
            continue
        rows.append(value)
    return rows


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_walk_keys(nested))
    return keys


def _frontmatter(text: str, errors: list[str]) -> str | None:
    if not text.startswith("---\n") or text.count("---") < 2:
        errors.append("SKILL.md must start with YAML frontmatter")
        return None
    value = text.split("---", 2)[1]
    name_match = re.search(r"^name:\s*([^\n]+)", value, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+)", value, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else None
    description = description_match.group(1).strip() if description_match else None
    if not name or not NAME_RE.fullmatch(name):
        errors.append("frontmatter name must be lowercase hyphenated")
    if name and len(name) > 63:
        errors.append("frontmatter name must be shorter than 64 characters")
    if not description or len(description) < 20:
        errors.append("frontmatter description is missing or too short")
    return name


def _validate_links(root: Path, text: str, errors: list[str]) -> None:
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        local = target.split("#", 1)[0]
        if local and not (root / local).is_file():
            errors.append(f"SKILL.md links to missing file: {target}")


def _validate_provenance(root: Path, name: str | None, errors: list[str]) -> None:
    path = root / "references" / "provenance.yaml"
    if not path.is_file():
        return
    provenance = _read_json(path, errors)
    if not isinstance(provenance, Mapping):
        return
    if provenance.get("schema_version") != "resolution-skill-provenance-v1":
        errors.append("unsupported provenance schema_version")
    package = provenance.get("package")
    if not isinstance(package, Mapping):
        errors.append("provenance package must be an object")
    else:
        if name and package.get("name") != name:
            errors.append("provenance package name does not match SKILL.md")
        if package.get("status") not in {"candidate", "deferred", "promoted"}:
            errors.append("provenance package status is invalid")
        if package.get("status") == "promoted":
            holdout = provenance.get("holdout")
            if not isinstance(holdout, Mapping) or holdout.get("agent_pair_status") != "pass":
                errors.append("a promoted package requires a passing paired agent holdout")
    forbidden = sorted(FORBIDDEN_PROVENANCE_KEYS.intersection(_walk_keys(provenance)))
    if forbidden:
        errors.append(f"provenance leaks hidden holdout fields: {forbidden}")

    workflow_text = (root / "references" / "workflow.md").read_text(encoding="utf-8")
    action_text = (root / "references" / "action-contracts.md").read_text(encoding="utf-8")
    role_bindings = provenance.get("role_bindings")
    if not isinstance(role_bindings, list) or not role_bindings:
        errors.append("provenance must include role_bindings")
        return
    for role in role_bindings:
        if not isinstance(role, Mapping) or not role.get("role_id"):
            errors.append("every provenance role binding needs a role_id")
            continue
        role_id = str(role["role_id"])
        if role_id not in workflow_text:
            errors.append(f"role {role_id} is absent from workflow.md")
        bindings = role.get("workflow_bindings")
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"role {role_id} has no concrete Workflow bindings")
            continue
        for binding in bindings:
            if not isinstance(binding, Mapping):
                errors.append(f"role {role_id} has a malformed Workflow binding")
                continue
            action_ids = binding.get("action_ids")
            if not isinstance(action_ids, list) or not action_ids:
                errors.append(f"role {role_id} has a binding without Action ids")
                continue
            for action_id in action_ids:
                if str(action_id) not in action_text:
                    errors.append(f"bound Action {action_id} is absent from action-contracts.md")


def _validate_evals(root: Path, errors: list[str]) -> None:
    prompts_path = root / "evals" / "prompts.jsonl"
    expected_path = root / "evals" / "expected.jsonl"
    prompts = _read_jsonl(prompts_path, errors) if prompts_path.is_file() else []
    expected = _read_jsonl(expected_path, errors) if expected_path.is_file() else []
    prompt_ids = {str(row.get("id")) for row in prompts if row.get("id")}
    expected_ids = {str(row.get("id")) for row in expected if row.get("id")}
    if prompt_ids != expected_ids:
        errors.append("prompt and expected eval ids do not match")
    classes = {str(row.get("class")) for row in prompts if row.get("class")}
    missing = sorted(REQUIRED_PROMPT_CLASSES.difference(classes))
    if missing:
        errors.append(f"activation evals are missing classes: {missing}")
    for row in expected:
        if row.get("decision") not in {"activate", "clarify", "do_not_activate"}:
            errors.append(f"eval {row.get('id')} has an invalid decision")

    rubric_path = root / "evals" / "rubric.schema.json"
    rubric = _read_json(rubric_path, errors) if rubric_path.is_file() else None
    if isinstance(rubric, Mapping):
        required = rubric.get("required")
        expected_fields = {
            "activation_decision",
            "action_role_coverage",
            "anti_goal_violations",
            "validation_quality",
            "leakage_detected",
        }
        if rubric.get("type") != "object" or not isinstance(required, list):
            errors.append("rubric schema must describe an object with required fields")
        elif not expected_fields.issubset(set(required)):
            errors.append("rubric schema is missing required evaluation dimensions")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    source = root / "SKILL.md"
    if not source.is_file():
        return errors
    try:
        text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append("SKILL.md must be UTF-8 text")
        return errors
    name = _frontmatter(text, errors)
    lowered = text.lower()
    for choices in REQUIRED_SECTION_GROUPS:
        if not any(choice in lowered for choice in choices):
            errors.append(f"missing required guidance section: {' or '.join(choices)}")
    if re.search(r"TODO|FIXME|<FILL_ME>|<INSERT_HERE>", text, re.IGNORECASE):
        errors.append("unfinished placeholder detected")
    _validate_links(root, text, errors)
    _validate_provenance(root, name, errors)
    _validate_evals(root, errors)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"package file must be UTF-8 text: {path.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    errors = validate(args.skill_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.skill_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
