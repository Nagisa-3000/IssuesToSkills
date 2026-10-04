"""Authority sealing never reconstructs or repairs authored Skill semantics."""

import json
from dataclasses import asdict

import pytest
from adaptive_fixture import CUTOFF, MECHANISM
from test_native_authority import bundle_from_files
from test_pattern_authoring_authority import Transport, source_and_response

from arex_skill_graph.action_contracts import SourceRecord, TemporalPolicy, digest
from arex_skill_graph.direct_skill_extraction import parse_bundle
from arex_skill_graph.generation_context import GenerationContext, generation_context_for_packages
from arex_skill_graph.native_provenance_authority import (
    MATERIALIZATION_FIELD,
    generation_context_reference,
    materialize_generation_context,
)
from arex_skill_graph.pattern_contracts import extract_native_pattern


def authority_input(tmp_path, *, future=False):
    package, name, files = source_and_response(tmp_path)
    context = generation_context_for_packages([package])
    if future:
        late = SourceRecord(
            "synthetic/later:9",
            "synthetic/later",
            "late-cluster",
            "late-fix",
            "f" * 40,
            "2023-01-01T00:00:00Z",
            ("late-evidence",),
            verified_resolution=True,
        )
        sources = (*context.sources, late)
        context = GenerationContext(
            digest([asdict(s) for s in sources]), context.source_package_hashes, sources
        )
    provenance = json.loads(files["references/provenance.json"])
    provenance["generation_context"] = generation_context_reference(context)
    files["references/provenance.json"] = json.dumps(provenance)
    return package, name, files, context


def test_expansion_preserves_every_authored_semantic_resource_byte(tmp_path):
    _package, name, files, context = authority_input(tmp_path)
    response = bundle_from_files(name, files)
    complete, audit = materialize_generation_context(response, context)
    before, _ = parse_bundle(response)
    after, _ = parse_bundle(complete)
    for path, content in before[name].items():
        if path != "references/provenance.json":
            assert after[name][path] == content
    original = json.loads(before[name]["references/provenance.json"])
    provenance = json.loads(after[name]["references/provenance.json"])
    assert provenance["generation_context"] == context.to_dict()
    assert provenance[MATERIALIZATION_FIELD]["semantic_resources_modified"] is False
    for key, value in original.items():
        if key != "generation_context":
            assert provenance[key] == value
    assert audit["author_bundle_sha256"] != audit["materialized_bundle_sha256"]
    assert audit["semantic_resources_modified"] is False


@pytest.mark.parametrize("mutation", ["digest", "schema", "extra", "missing", "shortened"])
def test_missing_forged_or_shortened_context_is_never_repaired(tmp_path, mutation):
    _package, name, files, context = authority_input(tmp_path)
    provenance = json.loads(files["references/provenance.json"])
    if mutation == "digest":
        provenance["generation_context"]["sha256"] = "0" * 64
    elif mutation == "schema":
        provenance["generation_context"]["schema"] = "unreviewed-context"
    elif mutation == "extra":
        provenance["generation_context"]["drop_source"] = True
    elif mutation == "missing":
        provenance.pop("generation_context")
    else:
        provenance["generation_context"] = {**context.to_dict(), "sources": []}
    files["references/provenance.json"] = json.dumps(provenance)
    with pytest.raises(ValueError, match="exact caller authority"):
        materialize_generation_context(bundle_from_files(name, files), context)


def test_model_cannot_forge_publisher_attestation(tmp_path):
    _package, name, files, context = authority_input(tmp_path)
    provenance = json.loads(files["references/provenance.json"])
    provenance[MATERIALIZATION_FIELD] = {"semantic_resources_modified": False}
    files["references/provenance.json"] = json.dumps(provenance)
    with pytest.raises(ValueError, match="reserved materialization"):
        materialize_generation_context(bundle_from_files(name, files), context)


def test_complete_legacy_context_remains_byte_identical(tmp_path):
    _package, name, files = source_and_response(tmp_path)
    # The context must be the package already named by the source lineage.
    context = generation_context_for_packages([_package])
    response = bundle_from_files(name, files)
    materialized, audit = materialize_generation_context(response, context)
    assert materialized == response
    assert audit["author_bundle_sha256"] == audit["materialized_bundle_sha256"]


def test_reference_mode_is_explicit_and_default_author_still_rejects_it(tmp_path):
    package, name, files, _context = authority_input(tmp_path)
    with pytest.raises(ValueError, match="complete generation context"):
        extract_native_pattern(
            Transport([bundle_from_files(name, files)]),
            [package],
            TemporalPolicy(CUTOFF),
            tmp_path / "out",
        )
    assert not (tmp_path / "out").exists()


def test_opt_in_publishes_full_self_contained_context_and_raw_draft_audit(tmp_path):
    package, name, files, context = authority_input(tmp_path, future=True)
    transport = Transport([bundle_from_files(name, files)])
    (published,) = extract_native_pattern(
        transport,
        [package],
        TemporalPolicy(CUTOFF),
        tmp_path / "out",
        generation_context=context,
        seal_generation_context=True,
        audit_dir=tmp_path / "audit",
    )
    assert published.generation_context == context
    payload, _ = json.JSONDecoder().raw_decode(transport.calls[0]["user"])
    assert payload["authoritative_generation_context_reference"] == generation_context_reference(
        context
    )
    draft = (tmp_path / "audit/authored-attempt-1.txt").read_text()
    final = (tmp_path / "audit/materialized-attempt-1.txt").read_text()
    assert draft != final
    audit = json.loads(
        (tmp_path / "audit/generation-context-materialization-attempt-1.json").read_text()
    )
    assert audit["packages"][name]["source_count"] == len(context.sources)
    assert audit["semantic_resources_modified"] is False
    # Uncited learning inputs still block earlier-query reuse after sealing.
    with pytest.raises(ValueError, match="not available before cutoff"):
        published.admit(TemporalPolicy("2021-01-01T00:00:00Z"))


def test_valid_metadata_reference_never_repairs_a_changed_mechanism(tmp_path):
    package, name, files, context = authority_input(tmp_path)
    files["SKILL.md"] = files["SKILL.md"].replace(MECHANISM, "Unreviewed mechanism")
    with pytest.raises(ValueError, match="reviewed causal mechanism"):
        extract_native_pattern(
            Transport([bundle_from_files(name, files)]),
            [package],
            TemporalPolicy(CUTOFF),
            tmp_path / "out",
            generation_context=context,
            reviewed_mechanism=MECHANISM,
            seal_generation_context=True,
        )
    assert not (tmp_path / "out").exists()


def test_defer_is_preserved_without_materializing_a_package(tmp_path):
    _package, _name, _files, context = authority_input(tmp_path)
    response = "AREX-SKILL-DEFERRED 1\nUnsupported reviewed mechanism.\nAREX-SKILL-DEFERRED-END\n"
    materialized, audit = materialize_generation_context(response, context)
    assert materialized == response
    assert audit["packages"] == {}
    assert audit["deferred"] is True
