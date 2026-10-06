"""Source authority and full publication stay mandatory during native revisions."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from adaptive_fixture import CUTOFF, MECHANISM
from test_native_authoring_revision import replace_contract, revision
from test_pattern_authoring_authority import (
    canonical_response,
    mechanism_review_packet,
    source_and_response,
)

from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.generation_context import GenerationContext, generation_context_for_packages
from arex_skill_graph.native_authoring_revision import NativeAuthoringDraft
from arex_skill_graph.native_pattern_revision import (
    prepare_native_pattern_revision,
    recover_native_pattern,
)
from arex_skill_graph.native_provenance_authority import generation_context_reference
from arex_skill_graph.pattern_contracts import (
    native_pattern_authoring_request,
    prepare_native_pattern_authoring,
)


def fixture(tmp_path, *, sealed=True):
    package, name, files = source_and_response(tmp_path)
    review = mechanism_review_packet(package)
    context = generation_context_for_packages([package])
    provenance = json.loads(files["references/provenance.json"])
    provenance["mechanism_review"] = review
    if sealed:
        provenance["generation_context"] = generation_context_reference(context)
    files["references/provenance.json"] = json.dumps(provenance) + "\n"
    original = NativeAuthoringDraft.from_bundle(canonical_response(package, name, files))
    mutable = original.files()
    resource = "references/actions/detect-a.md"
    mutable[resource] = replace_contract(
        mutable[resource], "arex-contract-v4", {"semantic_role": "inconsistent-role"}
    )
    damaged = NativeAuthoringDraft(original.name, tuple(sorted(mutable.items())))
    kwargs = {
        "canonical_package_id": package.reference["skill_id"],
        "reviewed_mechanism": MECHANISM,
        "mechanism_review": review,
        "expected_kind": "pattern",
        "generation_context": context,
        "seal_generation_context": sealed,
    }
    payload, _evidence, _sources = prepare_native_pattern_authoring(
        [package], TemporalPolicy(CUTOFF), **kwargs
    )
    request = native_pattern_authoring_request(payload)
    return package, original, damaged, resource, request, kwargs


def prepare(data, **overrides):
    package, _original, damaged, _resource, request, kwargs = data
    return prepare_native_pattern_revision(
        damaged, request, [package], TemporalPolicy(CUTOFF), **{**kwargs, **overrides}
    )


@pytest.mark.parametrize("sealed", [False, True])
def test_source_bound_revision_uses_full_original_publisher(tmp_path, sealed):
    data = fixture(tmp_path, sealed=sealed)
    _package, original, damaged, resource, request, _kwargs = data
    session = prepare(data)
    proof = session.proof()
    assert proof["actual_model_calls"] == 0
    assert proof["original_request_rebuilt_exactly"]
    assert proof["declared_role_diagnostics"]["status"] == "FAIL"
    assert "role disagrees" in proof["initial_full_publisher_rejection"]
    transport = ReplayTransport([revision(damaged, {resource: original.files()[resource]})])
    (published,) = recover_native_pattern(
        session, transport, tmp_path / "recovered", tmp_path / "audit"
    )
    assert published.pattern.mechanism == MECHANISM
    assert (Path(published.root) / resource).read_text() == original.files()[resource]
    saved = json.loads((tmp_path / "audit/original-authoring-request.json").read_text())
    assert saved == request
    outgoing = json.loads((tmp_path / "audit/revision-request-attempt-1.json").read_text())
    packet = json.loads(outgoing["user"].split("\nRevision input:\n", 1)[1])
    assert packet["original_authoring_request"] == request
    audit = json.loads((tmp_path / "audit/revision-audit.json").read_text())
    assert audit["attempts"][0]["full_package_validation_executed"]
    assert not audit["functional_evals_executed"]
    assert not audit["formal_KB_admitted"]


@pytest.mark.parametrize("drift", ["request", "review", "parent_bytes", "later_context"])
def test_zero_call_preflight_rejects_source_review_or_complete_context_drift(tmp_path, drift):
    data = list(fixture(tmp_path))
    package, _original, _damaged, _resource, request, kwargs = data
    if drift == "request":
        data[4] = {**request, "user": request["user"] + "\nUnrecorded instruction."}
    elif drift == "review":
        data[5] = {
            **kwargs,
            "mechanism_review": {**kwargs["mechanism_review"], "limitations": []},
        }
    elif drift == "parent_bytes":
        path = Path(package.root) / "SKILL.md"
        path.write_text(path.read_text() + "\nChanged after original authoring.\n")
    else:
        original_context = kwargs["generation_context"]
        late = replace(original_context.sources[0], available_at="2025-01-01T00:00:00Z")
        data[5] = {
            **kwargs,
            "generation_context": GenerationContext(
                original_context.source_corpus_sha256,
                original_context.source_package_hashes,
                (late, *original_context.sources[1:]),
            ),
        }
    with pytest.raises(ValueError):
        prepare(data)
    assert not (tmp_path / "recovered").exists()


@pytest.mark.parametrize("drift", ["identity", "cutoff", "review", "lineage", "context", "source"])
def test_immutable_authority_failures_are_never_sent_for_model_revision(tmp_path, drift):
    data = list(fixture(tmp_path))
    draft = data[2]
    files = draft.files()
    provenance = json.loads(files["references/provenance.json"])
    if drift == "identity":
        provenance["package"]["skill_id"] = "pattern:unreviewed"
    elif drift == "cutoff":
        provenance["cutoff"] = "2025-01-01T00:00:00Z"
    elif drift == "review":
        provenance.pop("mechanism_review")
    elif drift == "lineage":
        provenance["source_package_hashes"] = {}
    elif drift == "context":
        provenance["generation_context"]["sha256"] = "0" * 64
    else:
        provenance["sources"][0]["revision"] = "f" * 40
    files["references/provenance.json"] = json.dumps(provenance) + "\n"
    data[2] = NativeAuthoringDraft(draft.name, tuple(sorted(files.items())))
    with pytest.raises(ValueError):
        prepare(data)


def test_already_publishable_draft_needs_no_revision_call(tmp_path):
    data = list(fixture(tmp_path))
    data[2] = data[1]
    with pytest.raises(ValueError, match="already passes"):
        prepare(data)


def test_rejected_assembled_draft_is_preserved_as_exact_next_base(tmp_path):
    data = fixture(tmp_path)
    _package, original, damaged, resource, _request, _kwargs = data
    session = prepare(data)
    first = revision(
        damaged,
        {
            resource: original.files()[resource],
            "SKILL.md": original.files()["SKILL.md"].replace(MECHANISM, "Unsupported mechanism"),
        },
    )
    revised, _ = session.assemble(first)
    second = revision(revised, {"SKILL.md": original.files()["SKILL.md"]})
    transport = ReplayTransport([first, second])
    (published,) = recover_native_pattern(
        session, transport, tmp_path / "recovered", tmp_path / "audit"
    )
    assert published.pattern.mechanism == MECHANISM
    audit = json.loads((tmp_path / "audit/revision-audit.json").read_text())
    assert audit["attempts"][0]["status"] == "rejected"
    assert "reviewed causal mechanism" in audit["attempts"][0]["reason"]
    assert audit["attempts"][1]["base_draft_sha256"] == revised.sha256
    assert (tmp_path / "audit/base-draft-attempt-2.txt").read_text() == revised.as_bundle()
    assert (tmp_path / "audit/original-authored-draft.txt").read_text() == damaged.as_bundle()


def test_author_deferral_is_retained_without_becoming_applicability_negative(tmp_path):
    session = prepare(fixture(tmp_path))
    response = "AREX-SKILL-DEFERRED 1\nUnable to justify this revision.\nAREX-SKILL-DEFERRED-END\n"
    assert (
        recover_native_pattern(
            session, ReplayTransport([response]), tmp_path / "recovered", tmp_path / "audit"
        )
        == ()
    )
    audit = json.loads((tmp_path / "audit/revision-audit.json").read_text())
    assert audit["attempts"][0]["status"] == "deferred-by-native-revision-author"
    assert audit["attempts"][0]["applicability_negative"] is False
    assert not (tmp_path / "recovered").exists()


def test_invalid_revision_cannot_publish_and_terminal_failure_is_retained(tmp_path):
    data = fixture(tmp_path)
    _package, original, damaged, resource, _request, _kwargs = data
    session = prepare(data)
    wrong_base = revision(damaged, {resource: original.files()[resource]}, digest="0" * 64)
    with pytest.raises(ValueError, match="exact base"):
        recover_native_pattern(
            session,
            ReplayTransport([wrong_base]),
            tmp_path / "recovered",
            tmp_path / "audit",
            max_attempts=1,
        )
    assert not (tmp_path / "recovered").exists()
    audit = json.loads((tmp_path / "audit/revision-audit.json").read_text())
    assert audit["attempts"][0]["status"] == "rejected"


@pytest.mark.parametrize("drift", ["id", "source_id", "available_at", "kind"])
def test_immutable_evidence_drift_is_rejected_before_revision_preflight(tmp_path, drift):
    data = list(fixture(tmp_path))
    draft = data[2]
    files = draft.files()
    resource = next(path for path in files if path.startswith("references/evidence/"))
    changed = {
        "id": "evidence:outside-original-authority",
        "source_id": "source:outside-original-authority",
        "available_at": "2023-01-01T00:00:00Z",
        "kind": "unsupported-evidence-kind",
    }
    files[resource] = replace_contract(files[resource], "arex-evidence-v4", {drift: changed[drift]})
    data[2] = NativeAuthoringDraft(draft.name, tuple(sorted(files.items())))
    with pytest.raises(ValueError, match="authored evidence"):
        prepare(data)
    assert not (tmp_path / "recovered").exists()
    assert not (tmp_path / "audit").exists()
