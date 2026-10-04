"""Selection support is insufficient to reconstruct a Pattern's earlier-time knowledge."""

import json
from dataclasses import replace
from datetime import timedelta

import pytest
from test_native_authority import bundle_from_files
from test_pattern_authoring_authority import Transport, source_and_response

from arex_skill_graph.action_contracts import TemporalPolicy, utc
from arex_skill_graph.generation_context import generation_context_for_packages
from arex_skill_graph.pattern_contracts import extract_native_pattern, load_native_package


def authored_with_context(tmp_path):
    package, name, files = source_and_response(tmp_path)
    context = generation_context_for_packages([package])
    latest = max(utc(source.available_at) for source in context.sources)
    query_time = (latest + timedelta(days=1)).isoformat()
    outside = replace(
        context.sources[0],
        id="source:uncited-discovery-input",
        bug_cluster_id="cluster:uncited-query",
        fix_id="fix:uncited-query",
        aliases=("query:uncited",),
        copied_from=(),
        available_at=(latest + timedelta(days=2)).isoformat(),
    )
    context = replace(context, sources=(*context.sources, outside))
    provenance = json.loads(files["references/provenance.json"])
    provenance["generation_context"] = context.to_dict()
    files["references/provenance.json"] = json.dumps(provenance)
    return package, name, files, context, query_time


def test_uncited_future_discovery_input_excludes_earlier_query(tmp_path):
    package, name, files, context, query_time = authored_with_context(tmp_path)
    (derived,) = extract_native_pattern(
        Transport([bundle_from_files(name, files)]),
        [package],
        TemporalPolicy(package.cutoff),
        tmp_path / "derived",
        generation_context=context,
    )
    assert all(utc(s.available_at) < utc(query_time) for s in derived.sources)
    with pytest.raises(ValueError, match="before cutoff"):
        load_native_package(derived.reference, TemporalPolicy(query_time))
    later = TemporalPolicy((utc(context.sources[-1].available_at) + timedelta(days=1)).isoformat())
    assert load_native_package(derived.reference, later).reference == derived.reference


@pytest.mark.parametrize("exclusion", ["identity", "cluster", "fix"])
def test_uncited_own_query_and_aliases_cannot_leak_through_discovery(tmp_path, exclusion):
    package, name, files, context, _ = authored_with_context(tmp_path)
    (derived,) = extract_native_pattern(
        Transport([bundle_from_files(name, files)]),
        [package],
        TemporalPolicy(package.cutoff),
        tmp_path / "derived",
        generation_context=context,
    )
    kwargs = {
        "identity": {"excluded_ids": ("query:uncited",)},
        "cluster": {"excluded_clusters": ("cluster:uncited-query",)},
        "fix": {"excluded_fixes": ("fix:uncited-query",)},
    }[exclusion]
    with pytest.raises(ValueError, match="excluded identity/bug cluster/fix"):
        load_native_package(derived.reference, TemporalPolicy(package.cutoff, **kwargs))


@pytest.mark.parametrize("drift", ["omit_source", "change_hash", "omit_context"])
def test_author_cannot_shrink_or_replace_complete_generation_context(tmp_path, drift):
    package, name, files, context, _ = authored_with_context(tmp_path)
    provenance = json.loads(files["references/provenance.json"])
    if drift == "omit_source":
        provenance["generation_context"]["sources"].pop()
    elif drift == "change_hash":
        provenance["generation_context"]["source_corpus_sha256"] = "f" * 64
    else:
        del provenance["generation_context"]
    files["references/provenance.json"] = json.dumps(provenance)
    with pytest.raises(ValueError, match="complete generation context"):
        extract_native_pattern(
            Transport([bundle_from_files(name, files)]),
            [package],
            TemporalPolicy(package.cutoff),
            tmp_path / "derived",
            generation_context=context,
        )
    assert not list((tmp_path / "derived").rglob("SKILL.md"))


def test_context_remains_transitive_when_abstractions_are_reabstracted(tmp_path):
    package, name, files, context, _ = authored_with_context(tmp_path)
    parent_id = package.reference["skill_id"]
    for resource, content in files.items():
        if resource != "references/provenance.json":
            files[resource] = content.replace(json.dumps(parent_id), json.dumps("pattern:derived"))
    provenance = json.loads(files["references/provenance.json"])
    provenance["package"]["skill_id"] = "pattern:derived"
    files["references/provenance.json"] = json.dumps(provenance)
    (derived,) = extract_native_pattern(
        Transport([bundle_from_files(name, files)]),
        [package],
        TemporalPolicy(package.cutoff),
        tmp_path / "derived",
        generation_context=context,
    )
    inherited = generation_context_for_packages([derived])
    assert set(inherited.sources) == set(context.sources)
    assert (
        inherited.source_package_hashes[package.reference["skill_id"]]
        == package.reference["package_sha256"]
    )
    assert (
        inherited.source_package_hashes[derived.reference["skill_id"]]
        == derived.reference["package_sha256"]
    )
