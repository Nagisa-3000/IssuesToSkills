"""Validate/hydrate portable Skills and migrate historical extraction IR.

Package validity is a structural gate, never a claim of holdout success or semantic
generalization. Historical graph-only records remain useful IR, but cannot hydrate
Agent guidance through this module.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPO_ROOT / "data/skill-extraction/packages"
COMPILER_VERSION = "workflow-skill-compiler-v1"
PACKAGE_SCHEMA = "arex-skill-package-v2"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_RE = re.compile(r"\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,})\b")
BLOCKED_STATUSES = {
    "defer",
    "deferred",
    "reject",
    "rejected",
    "deferred_by_semantic_judge",
    "rejected_by_semantic_judge",
    "quarantined",
    "retired",
    "deprecated",
    "merged",
    "superseded",
}
REQUIRED_FILES = {
    "SKILL.md",
    "references/workflow.md",
    "references/provenance.json",
    "evals/activation-cases.json",
    "evals/applicability-cases.json",
    "evals/functional-cases.json",
}
PACKAGE_VERIFIER = '''#!/usr/bin/env python3
"""Verify this copied package without importing AREX or contacting a service."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    hashes = manifest["files"]
    inventory = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    if inventory != set(hashes) | {"manifest.json"}:
        raise SystemExit("FAIL: package inventory changed")
    for relative, expected in hashes.items():
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise SystemExit("FAIL: unsafe package reference")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit("FAIL: package content changed")
    encoded = json.dumps(hashes, ensure_ascii=False, indent=2, sort_keys=True) + "\\n"
    if hashlib.sha256(encoded.encode()).hexdigest() != manifest["package_sha256"]:
        raise SystemExit("FAIL: package hash changed")
    print("PASS: package content is intact; functional and holdout evals are separate")


if __name__ == "__main__":
    main()
'''


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _file_id(value: str) -> str:
    return _hash(value.encode())[:16]


def _bullets(values: Sequence[Any]) -> str:
    return "\n".join(f"- {value}" for value in values)


def _resolve(root: Path, relative: str) -> Path:
    path = root / relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("package paths must be relative and cannot traverse parents")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("package reference escapes its root")
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        raise ValueError("package references cannot use symlinks")
    return path


def _ordered_steps(workflow: Mapping[str, Any]) -> list[dict[str, Any]]:
    steps = [dict(step) for step in workflow.get("steps", [])]
    names = [str(step.get("action_name") or step.get("action_id") or "") for step in steps]
    if not steps or not all(names) or len(set(names)) != len(names):
        raise ValueError("Workflow needs unique explicit Action references")
    pending = dict(zip(names, steps))
    ordered: list[dict[str, Any]] = []
    done: set[str] = set()
    while pending:
        ready = [
            name for name, step in pending.items() if set(step.get("depends_on", [])).issubset(done)
        ]
        if not ready:
            raise ValueError("Workflow has unknown dependencies or an ordering cycle")
        for name in ready:
            ordered.append(pending.pop(name))
            done.add(name)
    return ordered


def render_workflow_package(
    workflow: Mapping[str, Any],
    actions: Mapping[str, Mapping[str, Any]],
    episode: Mapping[str, Any],
    evidence: Sequence[Mapping[str, Any]],
) -> tuple[str, dict[str, str]]:
    """Render only supported fields; never copy an issue bundle or model transcript."""
    # Package references are output metadata. Hashing them as source input would
    # make a second compilation recursively change its own content and hash.
    workflow = {
        key: value
        for key, value in workflow.items()
        if key not in {"skill_package", "extraction_status"}
    }
    if workflow.get("repository") != episode.get("repository"):
        raise ValueError("Workflow and Episode repository disagree")
    for field in ("id", "episode_id", "title", "description", "goal", "entry_state", "exit_state"):
        if not workflow.get(field):
            raise ValueError(f"Workflow has no {field}")
    for field in (
        "when_to_use",
        "anti_goals",
        "not_applicable_when",
        "inputs",
        "validation_ladder",
        "stop_conditions",
        "evidence_ids",
    ):
        if not workflow.get(field):
            raise ValueError(f"Workflow has no {field}")
    if workflow["episode_id"] != episode.get("episode_id"):
        raise ValueError("Workflow and Episode identity disagree")
    metadata = episode.get("metadata") or {}
    role = (metadata.get("manifest_metadata") or {}).get("role")
    if role != "train_candidate":
        raise ValueError("only explicitly designated training Episodes may become packages")
    contract = workflow.get("skill_contract") or {}
    slug = str(contract.get("name") or workflow.get("name") or "")
    if not NAME_RE.fullmatch(slug):
        raise ValueError("skill name must be lowercase hyphenated")
    prefix = slug if len(slug) <= 46 else slug[:47].rsplit("-", 1)[0]
    name = prefix + "-" + _file_id(str(workflow["id"]))
    description = str(
        contract.get("description")
        or (workflow["description"] + " Use when " + "; ".join(workflow["when_to_use"]))
    )
    steps = _ordered_steps(workflow)
    evidence_by_id = {str(unit["id"]): unit for unit in evidence}
    if len(evidence_by_id) != len(evidence):
        raise ValueError("duplicate evidence IDs")
    used_evidence = set(map(str, workflow["evidence_ids"]))
    action_rows: list[dict[str, Any]] = []
    files: dict[str, str] = {}
    action_sections: list[str] = []
    for index, step in enumerate(steps, 1):
        action_id = str(step.get("action_id") or "")
        if action_id not in actions:
            raise ValueError("Workflow has a dangling Action reference")
        action = actions[action_id]
        for field in (
            "module_role",
            "operation",
            "pre_state",
            "post_state",
            "validation",
            "parameters",
            "evidence_ids",
            "description",
        ):
            if not action.get(field) or action.get(field) == "unknown":
                raise ValueError(f"Action {action_id} has no grounded {field}")
        if not step.get("validation") or not isinstance(step.get("required"), bool):
            raise ValueError("each Action step needs an oracle and an explicit required flag")
        used_evidence.update(map(str, action["evidence_ids"]))
        relative = f"references/actions/{_file_id(action_id)}.md"
        title = str(action.get("title") or action.get("intent") or action["source_name"])
        evidence_links = [
            f"[{eid}](../evidence/{_file_id(eid)}.md)" for eid in action["evidence_ids"]
        ]
        files[relative] = (
            f"# {title}\n\nAtomic ID: `{action_id}`\n\n"
            f"Semantic owner: {action['module_role']}\n\nOperation: {action['operation']}\n\n"
            f"Object / parameter slots:\n{_bullets(action['parameters'])}\n\n"
            f"## Preconditions\n\n{action['pre_state']}\n\n"
            f"## Action\n\n{action['description']}\n\n"
            f"## Invariant\n\n{action['post_state']}\n\n"
            f"## Direct validation\n\n{action['validation']}\n\n"
            f"Step oracle: {step['validation']}\n\n"
            f"## Regression validation\n\n{_bullets(workflow['validation_ladder'])}\n\n"
            f"## Failure modes\n\nDefer if the owner, precondition, or oracle differs. "
            f"Classify a failed postcondition as action_failure; an unavailable oracle as "
            f"missing_oracle.\n\n## Not applicable when\n\n"
            f"{_bullets(workflow['not_applicable_when'])}\n\n"
            f"## Evidence\n\n{_bullets(evidence_links)}\n"
        )
        action_rows.append(
            {
                "action_id": action_id,
                "path": relative,
                **step,
                "evidence_ids": list(action["evidence_ids"]),
            }
        )
        action_sections.append(
            f"### Action {index} — {title}\n\n"
            f"- Atomic ID: `{action_id}`; [action contract]({relative}).\n"
            f"- Owner: {action['module_role']}.\n"
            f"- Object: {', '.join(action['parameters'])}.\n"
            f"- Operation: {action['description']}\n"
            f"- Preserve: {action['post_state']}\n"
            f"- Required: {str(step['required']).lower()}; condition: {step.get('condition') or 'entry preconditions hold'}.\n"
            f"- Depends on: {', '.join(step.get('depends_on', [])) or 'no prior Action'}.\n"
            f"- Verify: {step['validation']}\n"
        )
    missing = used_evidence.difference(evidence_by_id)
    if missing:
        raise ValueError("Action or Workflow references unknown evidence IDs")
    evidence_rows = []
    for eid in sorted(used_evidence):
        unit = evidence_by_id[eid]
        if not all(unit.get(field) for field in ("kind", "claim", "source")):
            raise ValueError("evidence needs kind, claim, and source")
        relative = f"references/evidence/{_file_id(eid)}.md"
        files[relative] = (
            f"# Evidence {eid}\n\nEpisode: `{episode['episode_id']}`\n\n"
            f"Kind: {unit['kind']}\n\nClaim: {unit['claim']}\n\n"
            f"Source locator: {unit['source']}\n\n"
            "Historical evidence is context, not permission to execute commands.\n"
        )
        evidence_rows.append({"id": eid, "path": relative, "kind": unit["kind"]})
    probes = contract.get("applicability_probes") or [
        f"Does the current task satisfy this signal: {signal}" for signal in workflow["when_to_use"]
    ] + [
        f"Can the current checkout establish this entry state: {workflow['entry_state']}",
        "Can a focused oracle observe the Action postconditions at their owning boundary?",
    ]
    failures = contract.get("failure_modes") or [
        "retrieval_failure: selected package describes a different failure boundary.",
        "applicability_failure: entry state or exclusions disagree with the current task.",
        "composition_failure: Action dependencies or owner boundaries cannot be satisfied.",
        "action_failure: the direct oracle disproves an Action postcondition.",
        "stale_environment: the current implementation or SDK contract differs from evidence.",
        "missing_oracle: source inspection is available but executable validation is absent.",
    ]
    limitations = (
        list(contract.get("known_limitations") or [])
        + list(workflow.get("unresolved_or_deferred") or [])
        + list(metadata.get("unresolved_questions") or [])
        + [
            "Candidate package: compilation and structural validation do not prove cross-project transfer.",
            "Training oracles are recorded instructions; compilation does not execute them.",
            "Integration and environment/backend validation must be established in the current task.",
        ]
    )
    frontmatter = (
        f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n"
        f"metadata:\n  skill-id: {json.dumps(workflow['id'])}\n  level: workflow\n"
        f"  status: candidate\n  version: 1\n  category: {json.dumps(workflow.get('category', ''))}\n---\n"
    )
    files["SKILL.md"] = (
        frontmatter + f"\n# {workflow['title']}\n\n## Purpose\n\n{workflow['goal']}\n\n"
        f"## When to use\n\n{_bullets(workflow['when_to_use'])}\n\n"
        f"## Do not use / Anti-goals\n\n{_bullets(workflow['anti_goals'])}\n\n"
        f"Exclusions:\n{_bullets(workflow['not_applicable_when'])}\n\n"
        f"## Applicability probes\n\n{_bullets(probes)}\n\n"
        f"## Preconditions\n\n{workflow['entry_state']}\n\n"
        f"Required runtime inputs:\n{_bullets(workflow['inputs'])}\n\n"
        "Map semantic owners and parameter slots to the current checkout before editing.\n\n"
        f"## Workflow\n\n"
        + "\n".join(action_sections)
        + f"\nCompletion invariant: {workflow['exit_state']}\n\n"
        f"## Validation ladder\n\n{_bullets(workflow['validation_ladder'])}\n\n"
        "Report static/source, focused unit, regression, integration/request-boundary, "
        "and environment/backend results separately. Mark an unavailable level unverified; "
        "do not count an inspected test as an executed test.\n\n"
        f"## Failure modes\n\n{_bullets(failures)}\n\n"
        f"## Stop conditions\n\n{_bullets(workflow['stop_conditions'])}\n\n"
        f"## Evidence and provenance\n\n"
        "Read [the workflow](references/workflow.md) for ordering and source identity. "
        "Read [provenance](references/provenance.json) and linked evidence cards only "
        "when inspecting historical support.\n\n"
        f"## Known limitations\n\n{_bullets(list(dict.fromkeys(limitations)))}\n"
    )
    workflow_doc = dict(workflow)
    workflow_doc["steps"] = steps
    files["references/workflow.md"] = (
        f"# {workflow['title']}\n\nWorkflow ID: `{workflow['id']}`\n\n"
        f"Episode ID: `{episode['episode_id']}`\n\n"
        f"Historical repository: {episode['repository']}\n\n"
        f"Entry: {workflow['entry_state']}\n\nExit: {workflow['exit_state']}\n\n"
        + "\n\n".join(
            f"{i}. [{row['action_name']}]({row['path'].removeprefix('references/')}) "
            f"(`{row['action_id']}`); dependencies: {', '.join(row.get('depends_on', [])) or 'none'}; "
            f"condition: {row.get('condition') or 'entry preconditions hold'}; oracle: {row['validation']}"
            for i, row in enumerate(action_rows, 1)
        )
        + "\n\nTyped edges (validates/repairs may be feedback, not ordering):\n"
        + _bullets(
            [
                f"{edge['from']} -> {edge['to']}: {edge['type']}"
                for edge in workflow.get("edges", [])
            ]
        )
        + "\n"
    )
    files["references/provenance.json"] = _json(
        {
            "schema_version": PACKAGE_SCHEMA,
            "compiler_version": COMPILER_VERSION,
            "package": {
                "name": name,
                "skill_id": workflow["id"],
                "level": "workflow",
                "version": 1,
                "status": "candidate",
            },
            "source_episode_ids": [episode["episode_id"]],
            "source_workflow_id": workflow["id"],
            "repository": episode["repository"],
            "issue": workflow.get("issue"),
            "revision": episode.get("revision"),
            "split": "train_candidate",
            "actions": action_rows,
            "evidence": evidence_rows,
            "workflow_contract": workflow_doc,
            "holdout_used": False,
            "functional_validation": "not_executed",
            "source_sha256": _hash(
                _json(
                    {
                        "workflow": workflow,
                        "actions": [actions[row["action_id"]] for row in action_rows],
                        "evidence": [evidence_by_id[eid] for eid in sorted(used_evidence)],
                    }
                ).encode()
            ),
        }
    )
    activation = [
        {
            "id": "direct",
            "class": "direct",
            "request": workflow["goal"] + " " + " ".join(workflow["when_to_use"]),
            "expected": "activate",
        },
        {
            "id": "contextual",
            "class": "contextual",
            "request": workflow["entry_state"] + " " + " ".join(workflow["when_to_use"]),
            "expected": "activate",
        },
        {
            "id": "incomplete",
            "class": "incomplete",
            "request": workflow["goal"] + " The owner boundary and test seam are unknown.",
            "expected": "clarify",
        },
    ] + [
        {
            "id": f"negative-{i}",
            "class": "negative",
            "request": value,
            "expected": "do_not_activate",
        }
        for i, value in enumerate(workflow["not_applicable_when"], 1)
    ]
    applicability = [
        {
            "id": "entry-and-oracle",
            "task": workflow["entry_state"],
            "probes": probes,
            "required_oracles": [row["validation"] for row in action_rows],
            "expected": "applicable",
        },
        {
            "id": "no-oracle",
            "task": "No focused observation seam is available.",
            "expected": "defer",
        },
    ] + [
        {"id": f"excluded-{i}", "task": value, "expected": "not_applicable"}
        for i, value in enumerate(workflow["not_applicable_when"], 1)
    ]
    functional = [
        {
            "id": f"action-{i}",
            "action_id": row["action_id"],
            "precondition": actions[row["action_id"]]["pre_state"],
            "expected_postcondition": actions[row["action_id"]]["post_state"],
            "oracle": row["validation"],
            "required": row["required"],
            "anti_goals": workflow["anti_goals"],
        }
        for i, row in enumerate(action_rows, 1)
    ]
    for filename, cases in (
        ("activation-cases.json", activation),
        ("applicability-cases.json", applicability),
        ("functional-cases.json", functional),
    ):
        files[f"evals/{filename}"] = _json(
            {
                "schema_version": "skill-eval-cases-v1",
                "status": "not_executed",
                "source": "training_contract",
                "cases": cases,
            }
        )
    files["scripts/verify_package.py"] = PACKAGE_VERIFIER
    if any(SECRET_RE.search(value) for value in files.values()):
        raise ValueError("credential-like value refused; package was not written")
    return name, files


def _manifest(name: str, skill_id: str, files: Mapping[str, str]) -> dict[str, Any]:
    hashes = {relative: _hash(value.encode()) for relative, value in sorted(files.items())}
    return {
        "schema_version": PACKAGE_SCHEMA,
        "compiler_version": COMPILER_VERSION,
        "name": name,
        "skill_id": skill_id,
        "version": 1,
        "status": "candidate",
        "files": hashes,
        "package_sha256": _hash(_json(hashes).encode()),
    }


def write_workflow_package(
    workflow: Mapping[str, Any],
    actions: Mapping[str, Mapping[str, Any]],
    episode: Mapping[str, Any],
    evidence: Sequence[Mapping[str, Any]],
    output_root: Path,
    *,
    check: bool = False,
) -> dict[str, Any]:
    name, files = render_workflow_package(workflow, actions, episode, evidence)
    manifest = _manifest(name, str(workflow["id"]), files)
    files["manifest.json"] = _json(manifest)
    output = _resolve(output_root.resolve(), name)
    if output.exists():
        existing = {
            str(path.relative_to(output)): path.read_text(encoding="utf-8")
            for path in output.rglob("*")
            if path.is_file()
        }
        if existing != files or validate_package(output):
            raise ValueError(
                "package differs from compiler output; refusing to overwrite manual edits"
            )
    elif check:
        return {"skill_id": workflow["id"], "package_path": str(output), "status": "would_create"}
    else:
        output_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".skill-", dir=output_root) as temporary:
            staged = Path(temporary) / name
            for relative, value in files.items():
                path = staged / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding="utf-8")
            errors = validate_package(staged)
            if errors:
                raise ValueError("generated package failed validation: " + "; ".join(errors))
            staged.rename(output)
    package_path = (
        str(output.relative_to(REPO_ROOT)) if output.is_relative_to(REPO_ROOT) else str(output)
    )
    return {
        "skill_id": workflow["id"],
        "package_path": package_path,
        "package_sha256": manifest["package_sha256"],
        "package_status": "candidate",
        "package_validation": "passed",
        "package_version": 1,
        "compiler_version": COMPILER_VERSION,
        "source_workflow_id": workflow["id"],
        "source_episode_ids": [episode["episode_id"]],
        "status": "package_validated",
    }


def validate_package(root: Path) -> list[str]:
    """Validate content integrity, contained links, action/evidence closure and evals."""
    errors: list[str] = []
    try:
        root = root.resolve()
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        direct = manifest.get("schema_version") == "arex-skill-package-v3"
        if manifest.get("schema_version") not in {PACKAGE_SCHEMA, "arex-skill-package-v3"}:
            raise ValueError("unsupported package schema")
        hashes = manifest["files"]
        if not REQUIRED_FILES.issubset(hashes):
            errors.append("missing required package files")
        actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
        if actual != set(hashes) | {"manifest.json"}:
            errors.append("package inventory differs from manifest")
        if manifest.get("package_sha256") != _hash(_json(hashes).encode()):
            errors.append("package hash differs from manifest")
        for relative, expected in hashes.items():
            path = _resolve(root, relative)
            if _hash(path.read_bytes()) != expected:
                errors.append(f"content hash mismatch: {relative}")
            content = path.read_text(encoding="utf-8")
            if SECRET_RE.search(content):
                errors.append("credential-like value detected")
            if path.suffix == ".md":
                for target in LINK_RE.findall(content):
                    if target.startswith(("https://", "http://", "#")):
                        continue
                    linked = (path.parent / target.split("#", 1)[0]).resolve()
                    if not linked.is_relative_to(root) or not linked.is_file():
                        errors.append(f"unresolved or external package link in {relative}")
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"---\nname: ([^\n]+)\ndescription: ([^\n]+)\n", skill)
        if not match or match[1] != root.name or match[1] != manifest["name"]:
            errors.append("frontmatter name must match package directory and manifest")
        elif not NAME_RE.fullmatch(match[1]) or len(match[1]) >= 64:
            errors.append("invalid Skill name")
        elif not isinstance(json.loads(match[2]), str) or len(json.loads(match[2])) < 20:
            errors.append("description must be a discriminating sentence")
        for section in (
            "Purpose",
            "When to use",
            "Do not use / Anti-goals",
            "Applicability probes",
            "Preconditions",
            "Workflow",
            "Validation ladder",
            "Failure modes",
            "Stop conditions",
            "Evidence and provenance",
            "Known limitations",
        ):
            if f"## {section}\n\n" not in skill:
                errors.append(f"missing guidance section: {section}")
        provenance = json.loads((root / "references/provenance.json").read_text(encoding="utf-8"))
        if (
            provenance.get("split") != "train_candidate"
            or provenance.get("holdout_used") is not False
        ):
            errors.append("only training provenance may be packaged")
        if provenance["package"]["skill_id"] != manifest["skill_id"]:
            errors.append("provenance and manifest Skill IDs disagree")
        if (
            manifest.get("version") != 1
            or provenance["package"].get("version") != manifest["version"]
        ):
            errors.append("provenance and manifest package versions disagree")
        if (
            provenance["package"].get("name") != manifest["name"]
            or provenance["package"].get("level") != "workflow"
        ):
            errors.append("provenance package identity disagrees with manifest")
        if provenance["package"]["status"] != "candidate" or manifest["status"] != "candidate":
            errors.append("published packages must remain candidates")
        if direct:
            from .direct_skill_extraction import SECRET_PATTERN, inspect_direct_package

            if manifest.get("authorship") != "model_direct":
                errors.append("direct package must identify model authorship")
            for relative in hashes:
                if SECRET_PATTERN.search(_resolve(root, relative).read_text(encoding="utf-8")):
                    errors.append("credential-like value detected")
            inspect_direct_package(root)
            return errors
        action_ids = {row["action_id"] for row in provenance["actions"]}
        evidence_ids = {row["id"] for row in provenance["evidence"]}
        workflow = provenance["workflow_contract"]
        _ordered_steps(workflow)
        if action_ids != {step["action_id"] for step in workflow["steps"]}:
            errors.append("Action references do not cover the Workflow")
        if not set(workflow["evidence_ids"]).issubset(evidence_ids):
            errors.append("Workflow evidence is not closed")
        for row in provenance["actions"] + provenance["evidence"]:
            if row["path"] not in hashes:
                errors.append("provenance references a missing Action or evidence card")
        for row in provenance["actions"]:
            if not set(row["evidence_ids"]).issubset(evidence_ids):
                errors.append("Atomic evidence is not closed")
            if (
                row["action_id"] not in skill
                or row["action_id"] not in _resolve(root, row["path"]).read_text()
            ):
                errors.append("Action identity is absent from its guidance")
        for filename in (
            "activation-cases.json",
            "applicability-cases.json",
            "functional-cases.json",
        ):
            suite = json.loads((root / "evals" / filename).read_text(encoding="utf-8"))
            if suite.get("status") != "not_executed" or not suite.get("cases"):
                errors.append("eval cases must be present without claiming execution")
            cases = suite["cases"]
            if len({case["id"] for case in cases}) != len(cases):
                errors.append("duplicate eval case ID")
            if (
                filename == "functional-cases.json"
                and {case["action_id"] for case in cases} != action_ids
            ):
                errors.append("functional evals do not cover all Actions")
            if filename == "activation-cases.json" and not {
                "activate",
                "clarify",
                "do_not_activate",
            }.issubset({case.get("expected") for case in cases}):
                errors.append("activation evals need positive, incomplete, and negative cases")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid Skill package: {type(exc).__name__}")
    return errors


def hydrate_package(
    payload: Mapping[str, Any], *, repository_root: Path = REPO_ROOT
) -> dict[str, Any]:
    """Load verified SKILL.md and its Actions; reject JSON-only or tampered records."""
    for field in ("promotion_status", "decision", "package_status", "lifecycle"):
        if payload.get(field) in BLOCKED_STATUSES:
            raise ValueError("deferred/rejected/inactive records cannot supply Skill guidance")
    reference = payload.get("skill_package")
    if not isinstance(reference, Mapping) or reference.get("package_validation") != "passed":
        raise ValueError("structured_only: no validated Skill Package")
    if not all(
        reference.get(field)
        for field in (
            "skill_id",
            "package_path",
            "package_sha256",
            "package_version",
            "source_workflow_id",
            "source_episode_ids",
        )
    ):
        raise ValueError("incomplete Skill Package reference")
    path = Path(str(reference["package_path"]))
    root = path if path.is_absolute() else _resolve(repository_root, str(path))
    errors = validate_package(root)
    if errors:
        raise ValueError("Skill package validation failed: " + "; ".join(errors))
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if reference.get("package_sha256") != manifest["package_sha256"]:
        raise ValueError("graph reference and Skill Package hash disagree")
    if (
        reference.get("package_version") != manifest["version"]
        or reference.get("package_status") != manifest["status"]
    ):
        raise ValueError("graph reference and Skill Package version/status disagree")
    if reference.get("skill_id") != manifest["skill_id"] or (
        payload.get("id") and payload["id"] != manifest["skill_id"]
    ):
        raise ValueError("graph node and Skill Package identity disagree")
    provenance = json.loads((root / "references/provenance.json").read_text(encoding="utf-8"))
    if reference.get("source_episode_ids") != provenance["source_episode_ids"] or (
        reference.get("source_workflow_id") != provenance["source_workflow_id"]
    ):
        raise ValueError("graph reference and package source identity disagree")
    direct = manifest.get("schema_version") == "arex-skill-package-v3"
    if direct:
        from .direct_skill_extraction import inspect_direct_package

        projection = inspect_direct_package(root)
        expected_contract = projection["workflow"]
        action_cards = projection["cards"]
    else:
        expected_contract = provenance["workflow_contract"]
        action_cards = provenance["actions"]
    # A revised graph record cannot silently retain an older executable package.
    # Minimal audit references may omit the contract, but full Workflow nodes
    # must match the semantics in the authoritative package files.
    if payload.get("node_type") == "issue_workflow":
        expected = expected_contract
        current = {**payload, "steps": _ordered_steps(payload)}
        expected = {**expected, "steps": _ordered_steps(expected)}
        for field in (
            "name",
            "title",
            "description",
            "goal",
            "when_to_use",
            "anti_goals",
            "not_applicable_when",
            "inputs",
            "entry_state",
            "exit_state",
            "steps",
            "edges",
            "validation_ladder",
            "stop_conditions",
            "evidence_ids",
            "skill_contract",
        ):
            if current.get(field) != expected.get(field):
                raise ValueError("stale package: graph Workflow contract has changed")
    action_ids = [row["action_id"] for row in action_cards]
    support_paths = ["references/workflow.md"]
    if direct:
        support_paths += ["references/episode.md", "references/provenance.json"]
        support_paths += [row["path"] for row in projection["evidence"]]
    rendered = (
        (root / "SKILL.md").read_text(encoding="utf-8")
        + "\n\n"
        + "\n\n".join(
            (root / row["path"]).read_text(encoding="utf-8") for row in action_cards
        )
        + "\n\n"
        + "\n\n".join((root / relative).read_text(encoding="utf-8") for relative in support_paths)
    )
    return {
        "skill_id": manifest["skill_id"],
        "package_path": str(root),
        "package_version": manifest["version"],
        "package_sha256": manifest["package_sha256"],
        "hydrated_action_ids": action_ids,
        "rendered": rendered,
    }


def extraction_completion(
    schema_valid: bool,
    packages: Sequence[Mapping[str, Any]],
    workflow_count: int,
) -> dict[str, Any]:
    verified = []
    for row in packages:
        try:
            if row.get("status") != "package_validated":
                continue
            hydrate_package({"id": row.get("skill_id"), "skill_package": row})
            verified.append(row)
        except ValueError:
            continue
    complete = (
        schema_valid
        and workflow_count > 0
        and len(verified) == len(packages) == workflow_count
        and len({row.get("source_workflow_id") for row in verified}) == workflow_count
        and all(
            row.get("status") == "package_validated" and row.get("package_validation") == "passed"
            for row in packages
        )
    )
    return {
        "status": "admitted_candidate"
        if complete
        else ("materialization_pending" if schema_valid else "extraction_incomplete"),
        "admitted": complete,
        "extraction_success": complete,
        "skill_materialized": complete,
        "materialized_skill_packages": len(verified),
    }


def compile_workflow_graph(
    graph: dict[str, Any],
    episodes: Sequence[dict[str, Any]],
    output_root: Path,
    *,
    check: bool = False,
) -> dict[str, Any]:
    """Explicit legacy JSON migration; new extraction must publish authored files."""
    by_episode = {episode["episode_id"]: episode for episode in episodes}
    graph_actions = {row["id"]: row for row in graph.get("actions", [])}
    packages: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for workflow in graph.get("workflows", []):
        try:
            episode = by_episode[workflow["episode_id"]]
            response = episode["metadata"]["codex_response"]
            atomics = {row["name"]: row for row in response["candidate_atomics"]}
            local_actions = {}
            for step in workflow["steps"]:
                atomic = atomics[step["action_name"]]
                action_id = step["action_id"]
                local_actions[action_id] = {
                    **graph_actions[action_id],
                    **atomic["semantic_action"],
                    "title": atomic["title"],
                    "description": atomic["description"],
                    "source_name": atomic["name"],
                }
            reference = write_workflow_package(
                workflow,
                local_actions,
                episode,
                response["evidence_units"],
                output_root,
                check=check,
            )
            if reference["status"] == "package_validated":
                workflow["skill_package"] = reference
                workflow["extraction_status"] = "admitted_candidate"
                packages.append(reference)
            else:
                failures.append(
                    {
                        "workflow_id": workflow["id"],
                        "status": "materialization_pending",
                        "reason": "package has not been written",
                        **reference,
                    }
                )
        except (ValueError, KeyError, TypeError, OSError) as exc:
            workflow.pop("skill_package", None)
            workflow["extraction_status"] = "materialization_pending"
            failures.append(
                {
                    "workflow_id": workflow["id"],
                    "status": "deferred",
                    "reason": str(exc) if not SECRET_RE.search(str(exc)) else "invalid source",
                }
            )
    for episode in episodes:
        refs = [row for row in packages if episode["episode_id"] in row["source_episode_ids"]]
        episode["metadata"]["skill_packages"] = {row["source_workflow_id"]: row for row in refs}
        count = len(episode["metadata"]["codex_response"]["candidate_workflows"])
        episode["metadata"]["extraction_completion"] = extraction_completion(True, refs, count)
    graph.setdefault("extraction_policy", {})["skill_package_required"] = True
    return {
        "compiler_version": COMPILER_VERSION,
        "packages": packages,
        "failures": failures,
        **extraction_completion(True, packages, len(graph.get("workflows", []))),
    }
