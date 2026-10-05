"""Revise model-authored native files without filling or rewriting semantics.

Revision envelopes are drafts, never admitted Skills. Final publication uses the
unchanged v4 authority, support, coherence and resource-completeness checks.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass

from .action_contracts import ActionContract, read_contract
from .direct_skill_extraction import parse_bundle
from .pattern_contracts import PatternContract
from .skill_packages import REQUIRED_FILES

REVISION_START = "AREX-SKILL-REVISION 1\n"
REVISION_END = "AREX-SKILL-REVISION-END"


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _bundle(name, resources):
    return (
        "AREX-SKILL-BUNDLE 1\n"
        + "".join(
            f"<<<FILE {name}/{path}>>>\n{content}<<<END FILE>>>\n" for path, content in resources
        )
        + "AREX-SKILL-BUNDLE-END\n"
    )


@dataclass(frozen=True, slots=True)
class NativeAuthoringDraft:
    name: str
    resources: tuple[tuple[str, str], ...]

    def __post_init__(self):
        if not isinstance(self.resources, tuple) or any(
            not isinstance(pair, tuple)
            or len(pair) != 2
            or not all(isinstance(value, str) for value in pair)
            or not pair[1].endswith("\n")
            for pair in self.resources
        ):
            raise TypeError("native draft resources must be immutable newline-ended file contents")
        parsed, deferred = parse_bundle(self.as_bundle())
        if deferred is not None or set(parsed) != {self.name}:
            raise ValueError("native revision needs one complete authored draft")
        files = parsed[self.name]
        required = REQUIRED_FILES | {"references/episode.md"}
        if (
            not required.issubset(files)
            or not any(path.startswith("references/actions/") for path in files)
            or not any(path.startswith("references/evidence/") for path in files)
            or "manifest.json" in files
            or "scripts/verify_package.py" in files
        ):
            raise ValueError(
                "native revision requires complete authored resources and no host artifacts"
            )
        if files != dict(self.resources):
            raise ValueError("native draft contains ambiguous resource identities")

    @classmethod
    def from_bundle(cls, response: str):
        packages, deferred = parse_bundle(response)
        if deferred is not None or len(packages) != 1:
            raise ValueError("native revision needs one authored draft, never a deferral")
        name, files = next(iter(packages.items()))
        return cls(name, tuple(sorted(files.items())))

    def as_bundle(self):
        return _bundle(self.name, self.resources)

    def files(self):
        return dict(self.resources)

    @property
    def resource_hashes(self):
        return {path: _sha(content) for path, content in self.resources}

    @property
    def sha256(self):
        identity = {"name": self.name, "resources": self.resource_hashes}
        return _sha(json.dumps(identity, ensure_ascii=False, sort_keys=True))

    @property
    def mutable_resources(self):
        return tuple(
            path
            for path, _content in self.resources
            if path == "SKILL.md"
            or path == "references/workflow.md"
            or path.startswith(("references/actions/", "references/realizations/", "evals/"))
        )


def apply_native_revision(draft, response, *, allowed_resources=None):
    """Merge only explicit model replacements; retain every other authored byte."""
    if not isinstance(draft, NativeAuthoringDraft):
        raise TypeError("native revision requires a NativeAuthoringDraft")
    terminal = REVISION_END + "\n" if response.endswith(REVISION_END + "\n") else REVISION_END
    if not response.startswith(REVISION_START) or not response.endswith(terminal):
        raise ValueError("expected a complete native revision envelope")
    header_end = response.find("\n", len(REVISION_START))
    header = response[len(REVISION_START) : header_end]
    match = re.fullmatch(r"Base-Draft-SHA256: ([0-9a-f]{64})", header)
    if header_end < 0 or not match or match[1] != draft.sha256:
        raise ValueError("native revision does not bind the exact base draft")
    body = response[header_end + 1 : -len(terminal)]
    packages, deferred = parse_bundle("AREX-SKILL-BUNDLE 1\n" + body + "AREX-SKILL-BUNDLE-END\n")
    if deferred is not None or set(packages) != {draft.name}:
        raise ValueError("native revision changed its package namespace")
    replacements = packages[draft.name]
    permitted = set(draft.mutable_resources)
    if allowed_resources is not None:
        allowed = set(allowed_resources)
        if not allowed.issubset(permitted):
            raise ValueError("native revision requested an unsupported mutable resource scope")
        permitted = allowed
    if not set(replacements).issubset(permitted):
        raise ValueError("native revision changes immutable, unknown or unapproved resources")
    original = draft.files()
    changed = sorted(path for path, value in replacements.items() if value != original[path])
    if not changed:
        raise ValueError("native revision must explicitly change at least one resource")
    revised = NativeAuthoringDraft(draft.name, tuple(sorted({**original, **replacements}.items())))
    untouched = {path: _sha(content) for path, content in draft.resources if path not in changed}
    if any(revised.resource_hashes[path] != sha for path, sha in untouched.items()):
        raise ValueError("native revision changed an untouched authored resource")
    audit = {
        "schema": "native-model-file-revision-v1",
        "base_draft_sha256": draft.sha256,
        "revised_draft_sha256": revised.sha256,
        "revision_response_sha256": _sha(response),
        "changed_resources": changed,
        "unchanged_resource_sha256": untouched,
        "resources_added_or_removed": False,
        "host_semantic_resources_authored": False,
        "full_package_validation_executed": False,
        "functional_evals_executed": False,
        "formal_KB_admitted": False,
    }
    return revised, audit


def diagnose_pattern_roles(draft):
    """Report declared role/effect inconsistencies, without inferring applicability."""
    if not isinstance(draft, NativeAuthoringDraft):
        raise TypeError("role diagnostics require a NativeAuthoringDraft")
    files = draft.files()
    failures, affected = [], set()
    pattern = PatternContract.from_dict(read_contract(files["SKILL.md"], "arex-pattern-v4"))
    actions = {}
    for path, content in draft.resources:
        if not path.startswith("references/actions/") or not path.endswith(".md"):
            continue
        action = ActionContract.from_dict(read_contract(content))
        if action.id in actions:
            failures.append(
                {"code": "duplicate-action-id", "action_id": action.id, "resource": path}
            )
            affected.update((path, actions[action.id][1]))
        actions[action.id] = (action, path)
    for role in pattern.roles:
        for aid in role.alternatives:
            if aid not in actions:
                failures.append(
                    {"code": "missing-role-alternative", "role_id": role.id, "action_id": aid}
                )
                affected.add("SKILL.md")
                continue
            action, path = actions[aid]
            if action.semantic_role != role.id:
                failures.append(
                    {
                        "code": "role-label-mismatch",
                        "role_id": role.id,
                        "action_id": aid,
                        "resource": path,
                        "actual_semantic_role": action.semantic_role,
                        "required_condition": "PatternRole.id == ActionContract.semantic_role",
                    }
                )
                affected.update(("SKILL.md", path))
            missing = set(role.effects) - set(action.effects)
            if missing:
                failures.append(
                    {
                        "code": "role-effects-missing",
                        "role_id": role.id,
                        "action_id": aid,
                        "resource": path,
                        "missing_effects": [
                            asdict(p)
                            for p in sorted(
                                missing, key=lambda p: (p.key, str(p.value), p.evaluator)
                            )
                        ],
                    }
                )
                affected.update(("SKILL.md", path))
    return {
        "schema": "native-declared-pattern-role-diagnostics-v1",
        "draft_sha256": draft.sha256,
        "pattern_id": pattern.id,
        "scope": "declared-role-identities-and-effects-only",
        "status": "FAIL" if failures else "PASS",
        "failures": failures,
        "affected_resources": sorted(affected),
        "semantic_applicability_established": False,
        "full_package_validation_executed": False,
        "functional_evals_executed": False,
    }


def diagnose_native_eval_definitions(draft):
    """Enumerate declared eval-field failures; never interpret or execute checks."""
    if not isinstance(draft, NativeAuthoringDraft):
        raise TypeError("eval diagnostics require a NativeAuthoringDraft")
    files = draft.files()
    action_ids = {
        ActionContract.from_dict(read_contract(content)).id
        for path, content in draft.resources
        if path.startswith("references/actions/") and path.endswith(".md")
    }
    failures, affected = [], set()
    for filename, outcomes in (
        ("activation-cases.json", {"activate", "clarify", "do_not_activate"}),
        ("applicability-cases.json", {"applicable", "insufficient", "not_applicable"}),
        ("functional-cases.json", None),
    ):
        path = "evals/" + filename
        suite = json.loads(files[path])
        cases = suite.get("cases")
        if suite.get("status") != "not_executed" or not isinstance(cases, list) or not cases:
            failures.append({"code": "unexecuted-nonempty-suite-required", "resource": path})
            affected.add(path)
            continue
        if any(not isinstance(case, dict) or not case.get("id") for case in cases):
            failures.append({"code": "case-identity-required", "resource": path})
            affected.add(path)
            continue
        ids = [case["id"] for case in cases]
        if len(set(ids)) != len(ids):
            failures.append({"code": "duplicate-eval-case", "resource": path})
            affected.add(path)
        if outcomes is not None:
            actual = {case.get("expected") for case in cases}
            if actual != outcomes:
                failures.append(
                    {
                        "code": "boundary-outcomes-mismatch",
                        "resource": path,
                        "missing_outcomes": sorted(outcomes - actual),
                        "unexpected_outcomes": sorted(str(value) for value in actual - outcomes),
                    }
                )
                affected.add(path)
            continue
        covered = {case.get("action_id") for case in cases}
        if covered != action_ids:
            failures.append(
                {
                    "code": "functional-action-coverage-mismatch",
                    "resource": path,
                    "uncovered_actions": sorted(action_ids - covered),
                    "unknown_actions": sorted(str(value) for value in covered - action_ids),
                }
            )
            affected.add(path)
        for index, case in enumerate(cases):
            missing = [key for key in ("setup", "checks") if not case.get(key)]
            if missing:
                failures.append(
                    {
                        "code": "functional-observable-definition-fields-missing",
                        "resource": path,
                        "case_index": index,
                        "case_id": case["id"],
                        "action_id": case.get("action_id"),
                        "missing_fields": missing,
                        "present_fields": sorted(case),
                    }
                )
                affected.add(path)
    return {
        "schema": "native-declared-eval-definition-diagnostics-v1",
        "draft_sha256": draft.sha256,
        "scope": "declared-native-evaluation-definition-fields-only",
        "status": "FAIL" if failures else "PASS",
        "failures": failures,
        "affected_resources": sorted(affected),
        "checks_semantically_verified": False,
        "checks_executed": False,
        "full_package_validation_executed": False,
        "functional_evals_executed": False,
    }
