"""Native revisions preserve authored bytes and cannot bypass publication gates."""

import json

import pytest
from adaptive_fixture import CUTOFF, authored_bundle

from arex_skill_graph.action_contracts import TemporalPolicy, read_contract
from arex_skill_graph.native_authoring_revision import (
    NativeAuthoringDraft,
    apply_native_revision,
    diagnose_pattern_roles,
)
from arex_skill_graph.pattern_contracts import publish_v4_bundle


def replace_contract(content, marker, changes):
    contract = read_contract(content, marker)
    contract.update(changes)
    start = content.index("\u0060\u0060\u0060" + marker + "\n") + len(marker) + 4
    end = content.index("\n\u0060\u0060\u0060", start)
    return content[:start] + json.dumps(contract, ensure_ascii=False, indent=2) + content[end:]


def revision(draft, replacements, *, digest=None, name=None):
    return (
        "AREX-SKILL-REVISION 1\nBase-Draft-SHA256: "
        + (digest or draft.sha256)
        + "\n"
        + "".join(
            f"<<<FILE {name or draft.name}/{path}>>>\n{content}<<<END FILE>>>\n"
            for path, content in replacements.items()
        )
        + "AREX-SKILL-REVISION-END\n"
    )


def damaged_draft():
    response, sources = authored_bundle()
    draft = NativeAuthoringDraft.from_bundle(response)
    files = draft.files()
    path = "references/actions/detect-a.md"
    files[path] = replace_contract(
        files[path], "arex-contract-v4", {"semantic_role": "different-label"}
    )
    return NativeAuthoringDraft(draft.name, tuple(sorted(files.items()))), draft, sources, path


def test_diagnostic_names_every_declared_role_mismatch_without_semantic_approval():
    damaged, original, _sources, path = damaged_draft()
    result = diagnose_pattern_roles(damaged)
    assert result["status"] == "FAIL"
    (error,) = result["failures"]
    assert error["role_id"] == "detect_context"
    assert error["action_id"] == "detect:a"
    assert error["resource"] == path
    assert error["actual_semantic_role"] == "different-label"
    assert result["affected_resources"] == ["SKILL.md", path]
    valid = diagnose_pattern_roles(original)
    assert valid["status"] == "PASS"
    assert not valid["semantic_applicability_established"]
    assert not valid["full_package_validation_executed"]
    assert not valid["functional_evals_executed"]


def test_role_effect_omission_is_reported_independently():
    response, _sources = authored_bundle()
    draft = NativeAuthoringDraft.from_bundle(response)
    files = draft.files()
    path = "references/actions/detect-a.md"
    files[path] = replace_contract(files[path], "arex-contract-v4", {"effects": []})
    result = diagnose_pattern_roles(NativeAuthoringDraft(draft.name, tuple(sorted(files.items()))))
    assert result["status"] == "FAIL"
    assert result["failures"][0]["code"] == "role-effects-missing"
    assert result["failures"][0]["missing_effects"][0]["key"] == "context_known"


def test_model_revision_retains_all_other_authored_bytes_then_passes_normal_publisher(tmp_path):
    damaged, original, sources, path = damaged_draft()
    response = revision(damaged, {path: original.files()[path]})
    revised, audit = apply_native_revision(damaged, response, allowed_resources=[path])
    assert revised.resources == original.resources
    assert audit["changed_resources"] == [path]
    for resource, content in damaged.resources:
        if resource != path:
            assert revised.files()[resource] == content
            assert audit["unchanged_resource_sha256"][resource] == damaged.resource_hashes[resource]
    assert not audit["host_semantic_resources_authored"]
    assert not audit["functional_evals_executed"]
    assert not audit["formal_KB_admitted"]
    with pytest.raises(ValueError, match="role disagrees"):
        publish_v4_bundle(
            damaged.as_bundle(), sources, TemporalPolicy(CUTOFF), tmp_path / "rejected"
        )
    with pytest.raises(ValueError, match="complete direct Skill"):
        publish_v4_bundle(response, sources, TemporalPolicy(CUTOFF), tmp_path / "revision-only")
    (package,) = publish_v4_bundle(
        revised.as_bundle(),
        sources,
        TemporalPolicy(CUTOFF),
        tmp_path / "accepted",
        require_coherent_workflows=True,
    )
    assert package.pattern.id == "pattern:type-context"
    assert not list((tmp_path / "rejected").glob("*/SKILL.md"))
    assert not list((tmp_path / "revision-only").glob("*/SKILL.md"))


@pytest.mark.parametrize(
    "problem", ["base", "namespace", "scope", "unknown", "traversal", "incomplete", "noop"]
)
def test_invalid_revision_never_changes_base_draft(problem):
    damaged, original, _sources, path = damaged_draft()
    initial = damaged.resources
    replacements = {path: original.files()[path]}
    kwargs = {}
    apply_kwargs = {}
    if problem == "base":
        kwargs["digest"] = "0" * 64
    elif problem == "namespace":
        kwargs["name"] = "different-package"
    elif problem == "scope":
        apply_kwargs["allowed_resources"] = ["SKILL.md"]
    elif problem == "unknown":
        replacements = {"references/actions/unprovided.md": original.files()[path]}
    elif problem == "traversal":
        replacements = {"../escape.md": original.files()[path]}
    elif problem == "noop":
        replacements = {path: damaged.files()[path]}
    response = revision(damaged, replacements, **kwargs)
    if problem == "incomplete":
        response = response.replace("AREX-SKILL-REVISION-END\n", "")
    with pytest.raises(ValueError):
        apply_native_revision(damaged, response, **apply_kwargs)
    assert damaged.resources == initial


@pytest.mark.parametrize(
    "resource", ["references/provenance.json", "references/episode.md", "first-evidence-card"]
)
def test_authority_and_source_resources_are_immutable_even_with_explicit_scope(resource):
    response, _sources = authored_bundle()
    draft = NativeAuthoringDraft.from_bundle(response)
    if resource == "first-evidence-card":
        resource = next(path for path in draft.files() if path.startswith("references/evidence/"))
    assert resource in draft.files()
    replacement = draft.files()[resource] + "changed\n"
    with pytest.raises(ValueError, match="immutable|unsupported mutable"):
        apply_native_revision(
            draft, revision(draft, {resource: replacement}), allowed_resources=[resource]
        )
    assert draft.files()[resource] != replacement


def test_revisions_preserve_whitespace_in_untouched_semantic_files():
    damaged, original, _sources, path = damaged_draft()
    files = damaged.files()
    untouched = "references/actions/guard-a.md"
    files[untouched] += "\nAdditional authored prose with spaces.   \n\n"
    damaged = NativeAuthoringDraft(damaged.name, tuple(sorted(files.items())))
    revised, _audit = apply_native_revision(
        damaged, revision(damaged, {path: original.files()[path]})
    )
    assert revised.files()[untouched] == files[untouched]
    reparsed = NativeAuthoringDraft.from_bundle(revised.as_bundle())
    assert reparsed.files()[untouched] == files[untouched]


@pytest.mark.parametrize(
    "missing", ["SKILL.md", "evals/functional-cases.json", "references/episode.md"]
)
def test_incomplete_authored_resources_cannot_become_revision_base(missing):
    response, _sources = authored_bundle()
    draft = NativeAuthoringDraft.from_bundle(response)
    with pytest.raises(ValueError, match="complete authored resources"):
        NativeAuthoringDraft(draft.name, tuple((p, c) for p, c in draft.resources if p != missing))


def test_deferred_or_multiple_packages_cannot_become_revision_base():
    with pytest.raises(ValueError, match="never a deferral"):
        NativeAuthoringDraft.from_bundle(
            "AREX-SKILL-DEFERRED 1\nEvidence unavailable.\nAREX-SKILL-DEFERRED-END\n"
        )
    response, _sources = authored_bundle()
    with pytest.raises(ValueError, match="one authored draft"):
        NativeAuthoringDraft.from_bundle(
            response.replace("AREX-SKILL-BUNDLE-END\n", "")
            + response.replace("AREX-SKILL-BUNDLE 1\n", "", 1).replace(
                "type-context-pattern/", "different-package/"
            )
        )


@pytest.mark.parametrize(
    "problem", ["missing_checks", "missing_setup", "coverage", "duplicate", "executed", "boundary"]
)
def test_eval_diagnostics_name_declared_failures_without_interpreting_checks(problem):
    from arex_skill_graph.native_authoring_revision import diagnose_native_eval_definitions

    response, _sources = authored_bundle()
    draft = NativeAuthoringDraft.from_bundle(response)
    baseline = diagnose_native_eval_definitions(draft)
    assert baseline["status"] == "PASS"
    assert not baseline["checks_executed"]
    assert not baseline["checks_semantically_verified"]
    files = draft.files()
    path = "evals/activation-cases.json" if problem == "boundary" else "evals/functional-cases.json"
    suite = json.loads(files[path])
    if problem in {"missing_checks", "missing_setup"}:
        key = problem.removeprefix("missing_")
        suite["cases"][0].pop(key)
    elif problem == "coverage":
        suite["cases"][0]["action_id"] = "unknown-action"
    elif problem == "duplicate":
        suite["cases"].append(suite["cases"][0])
    elif problem == "executed":
        suite["status"] = "passed"
    else:
        suite["cases"][0]["expected"] = "unsupported"
    files[path] = json.dumps(suite) + "\n"
    changed = NativeAuthoringDraft(draft.name, tuple(sorted(files.items())))
    report = diagnose_native_eval_definitions(changed)
    assert report["status"] == "FAIL"
    assert report["affected_resources"] == [path]
    if problem.startswith("missing_"):
        failure = report["failures"][0]
        assert failure["case_id"] == suite["cases"][0]["id"]
        assert failure["missing_fields"] == [problem.removeprefix("missing_")]
    assert not report["functional_evals_executed"]
    assert draft.files()[path] != changed.files()[path]
