"""Synthetic structural regressions; no real model, repair or utility labels."""

from dataclasses import replace

import pytest
from adaptive_fixture import CUTOFF, authored_bundle

from arex_skill_graph.action_contracts import Predicate, SourceRecord, TemporalPolicy
from arex_skill_graph.pattern_contracts import publish_v4_bundle
from arex_skill_graph.source_support import independent_source_components


def source(identifier, **changes):
    index = {"a": "1", "b": "2", "c": "3", "d": "4"}[identifier]
    record = SourceRecord(
        id=f"synthetic-unit:source:{identifier}",
        repository=f"synthetic-unit/repo-{identifier}",
        bug_cluster_id=f"synthetic-unit:cluster:{identifier}",
        fix_id=f"synthetic-unit:fix:{identifier}",
        revision=index * 40,
        available_at="2020-01-01T00:00:00Z",
        evidence_refs=(f"synthetic-unit:evidence:{identifier}",),
        verified_resolution=True,
    )
    return replace(record, **changes)


def ids(components):
    return tuple(tuple(record.id for record in group) for group in components)


def native_pattern(tmp_path):
    response, sources = authored_bundle()
    (package,) = publish_v4_bundle(response, sources, TemporalPolicy(CUTOFF), tmp_path / "native")
    return (
        package.pattern,
        package.workflows,
        {s.id: s for s in package.sources},
        package.evidence_ids,
    )


def test_redundant_repairs_preserve_two_genuine_source_components():
    first, second = source("a"), source("b")
    extra = source("c", bug_cluster_id=first.bug_cluster_id, aliases=(first.id,))
    groups = independent_source_components((first, extra, second))
    assert ids(groups) == ((first.id, extra.id), (second.id,))


def test_copies_link_transitively_across_different_cluster_and_fix_labels():
    first = source("a", aliases=("synthetic-unit:shared-left",))
    middle = source(
        "b", copied_from=("synthetic-unit:shared-left",), aliases=("synthetic-unit:shared-right",)
    )
    last = source("c", copied_from=("synthetic-unit:shared-right",))
    assert len(independent_source_components((first, middle, last))) == 1


def test_shared_fix_and_revision_chain_cannot_claim_two_independent_repairs():
    first = source("a")
    middle = source("b", fix_id=first.fix_id)
    last = source("c", revision=middle.revision)
    assert len({first.fix_id, middle.fix_id, last.fix_id}) == 2
    assert len({first.revision, middle.revision, last.revision}) == 2
    assert len(independent_source_components((first, middle, last))) == 1


def test_alias_to_issue_identity_links_a_source_without_alias_metadata():
    first = source("a")
    copied = source("b", copied_from=(first.bug_cluster_id,))
    assert len(independent_source_components((first, copied))) == 1


def test_order_and_repeated_identical_records_do_not_change_support():
    first, second = source("a"), source("b")
    extra = source("c", aliases=(first.id,))
    assert ids(independent_source_components((extra, second, first, first))) == ids(
        independent_source_components((first, second, extra))
    )


def test_conflicting_same_id_is_rejected_instead_of_overwritten():
    first = source("a")
    with pytest.raises(ValueError, match="conflicting source identity"):
        independent_source_components((first, replace(first, revision="5" * 40)))


def test_pattern_keeps_redundant_source_when_another_independent_fix_exists(tmp_path):
    pattern, workflows, records, evidence = native_pattern(tmp_path)
    first, second = tuple(records.values())
    redundant = replace(
        first,
        id=first.id + ":second-repair",
        fix_id=first.fix_id + ":second",
        revision="3" * 40,
        aliases=(first.id,),
    )
    records[redundant.id] = redundant
    updated = tuple(
        replace(workflow, source_ids=(*workflow.source_ids, redundant.id))
        if first.id in workflow.source_ids
        else workflow
        for workflow in workflows
    )
    pattern.validate_support(updated, records, set(evidence))
    assert len(independent_source_components(records.values())) == 2
    assert second.bug_cluster_id != first.bug_cluster_id


def test_pattern_rejects_transitively_shared_repair_despite_two_unique_counts(tmp_path):
    pattern, workflows, records, evidence = native_pattern(tmp_path)
    first, second = tuple(records.values())
    second = replace(second, fix_id=first.fix_id)
    third = replace(
        first,
        id=first.id + ":third",
        bug_cluster_id=first.bug_cluster_id + ":third",
        fix_id=first.fix_id + ":third",
        revision=second.revision,
    )
    records = {s.id: s for s in (first, second, third)}
    updated = tuple(
        replace(workflow, source_ids=(*workflow.source_ids, third.id))
        if first.id in workflow.source_ids
        else workflow
        for workflow in workflows
    )
    with pytest.raises(ValueError, match="not independent Pattern support"):
        pattern.validate_support(updated, records, set(evidence))


def test_redundant_support_does_not_waive_mechanism_alignment(tmp_path):
    pattern, workflows, records, evidence = native_pattern(tmp_path)
    first = next(iter(records.values()))
    redundant = replace(first, id=first.id + ":duplicate", aliases=(first.id,))
    records[redundant.id] = redundant
    updated = tuple(
        replace(
            workflow,
            source_ids=(*workflow.source_ids, redundant.id),
            mechanism="unsupported other mechanism",
        )
        if first.id in workflow.source_ids
        else workflow
        for workflow in workflows
    )
    with pytest.raises(ValueError, match="different reviewed mechanisms"):
        pattern.validate_support(updated, records, set(evidence))


def test_redundant_support_does_not_waive_necessary_effect_coverage(tmp_path):
    pattern, workflows, records, evidence = native_pattern(tmp_path)
    first = next(iter(records.values()))
    redundant = replace(first, id=first.id + ":duplicate", aliases=(first.id,))
    records[redundant.id] = redundant
    updated = tuple(
        replace(workflow, source_ids=(*workflow.source_ids, redundant.id))
        if first.id in workflow.source_ids
        else workflow
        for workflow in workflows
    )
    incomplete = replace(
        pattern,
        required_effects=(*pattern.required_effects, Predicate("synthetic-unit:unprovided", True)),
    )
    with pytest.raises(ValueError, match="does not independently cover"):
        incomplete.validate_support(updated, records, set(evidence))
