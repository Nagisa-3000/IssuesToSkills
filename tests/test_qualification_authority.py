"""Report evidence cannot be substituted by a summary, a hash, or an alias."""

import copy
import json
from dataclasses import replace

import pytest
from adaptive_fixture import CUTOFF, authored_bundle
from test_native_authority import bundle_from_files
from test_pattern_authoring_authority import Transport

from arex_skill_graph.action_contracts import SourceRecord, TemporalPolicy
from arex_skill_graph.direct_skill_extraction import parse_bundle
from arex_skill_graph.generation_context import generation_context_for_packages
from arex_skill_graph.history_census import fingerprint
from arex_skill_graph.pattern_contracts import extract_native_pattern, publish_v4_bundle
from arex_skill_graph.qualification_authority import (
    HistoricalQualification,
    load_source_qualifications,
    validate_historical_qualification,
)

POLICY = TemporalPolicy(CUTOFF)


def source():
    return SourceRecord(
        "example/repo:1:repair:" + "a" * 12,
        "example/repo",
        "example/repo:1",
        "example/repo:pr:2",
        "a" * 40,
        "2020-01-01T00:00:00Z",
        ("example/repo:1:regression",),
        aliases=("example/repo:1",),
        verified_resolution=True,
    )


def report_for(record):
    observations = {
        "original_base": {"existing": "passed"},
        "base_with_regression": {"existing": "passed", "regression": "failed"},
        "historical_fixed": {"existing": "passed", "regression": "passed"},
    }
    return {
        "schema": "historical-causal-verification-v1",
        "identity": {
            "issue_id": record.bug_cluster_id,
            "fix_id": record.fix_id,
            "base_commit": "0" * 40,
            "merge_commit": record.revision,
            "repair_available_at": record.available_at,
            "cutoff_exclusive": CUTOFF,
            "resolution_relationship": "direct_closure",
            "resolution_relationship_evidence_refs": [record.bug_cluster_id + ":closure"],
        },
        "checked_at": "2026-10-04T00:00:00Z",
        "verified_resolution": True,
        "historical_artifact_verified": True,
        "issue_relationship_verified": True,
        "qualification_scope": "changed-test-files-with-original-base-control",
        "runtime_sha256": "1" * 64,
        "observations": observations,
        "observations_sha256": fingerprint(observations),
        "fail_to_pass": ["regression"],
        "pass_to_pass": ["existing"],
        "runs": {
            phase: {
                "exit_code": exit_code,
                "timed_out": False,
                "runtime_sha256": "1" * 64,
                "isolation": "synthetic-isolation",
                "output": "Synthetic fixture, not a real solver result.",
            }
            for phase, exit_code in zip(observations, [0, 1, 0])
        },
        "formal_SWE_run": False,
        "verification_does_not_backdate_new_information": True,
    }


def write_inventory(tmp_path, record, report, *, aliases=()):
    report_path = tmp_path / "verification.json"
    report_path.write_text(json.dumps(report))
    row = {
        "issue_id": record.bug_cluster_id,
        "fix_id": report["identity"]["fix_id"],
        "verification_path": str(report_path),
        "verified_resolution": True,
        "fail_to_pass_count": len(report["fail_to_pass"]),
        "pass_to_pass_count": len(report["pass_to_pass"]),
        "request_aliases": list(aliases),
    }
    inventory = {
        "schema": "historical-development-verification-inventory-v1",
        "canonical_requested_count": 1,
        "results": [row],
    }
    path = tmp_path / "inventory.json"
    path.write_text(json.dumps(inventory))
    return path


@pytest.mark.parametrize(
    "field,value",
    [
        ("issue_id", "example/repo:99"),
        ("merge_commit", "b" * 40),
        ("fix_id", "example/repo:pr:99"),
        ("cutoff_exclusive", "2025-01-01T00:00:00Z"),
        ("repair_available_at", "2024-01-01T00:00:00Z"),
    ],
)
def test_source_identity_and_time_are_not_inferred_from_a_passed_flag(field, value):
    report = report_for(source())
    report["identity"][field] = value
    with pytest.raises(ValueError, match="identity/time"):
        validate_historical_qualification(report, source(), POLICY)


@pytest.mark.parametrize(
    "mutation",
    ["observation_hash", "fabricated_f2p", "original_failure", "runtime", "timeout", "closure"],
)
def test_actual_controls_must_recompute_even_with_a_passed_summary(mutation):
    report = report_for(source())
    if mutation == "observation_hash":
        report["observations"]["historical_fixed"]["regression"] = "failed"
    elif mutation == "fabricated_f2p":
        report["observations"]["base_with_regression"]["regression"] = "passed"
        report["observations_sha256"] = fingerprint(report["observations"])
    elif mutation == "original_failure":
        report["observations"]["original_base"]["existing"] = "failed"
        report["observations_sha256"] = fingerprint(report["observations"])
    elif mutation == "runtime":
        report["runs"]["original_base"]["runtime_sha256"] = "2" * 64
    elif mutation == "timeout":
        report["runs"]["historical_fixed"]["timed_out"] = True
    else:
        report["identity"]["resolution_relationship"] = "mention_only_not_verified_resolution"
    with pytest.raises(ValueError):
        validate_historical_qualification(report, source(), POLICY)


def test_completed_inventory_attaches_complete_immutable_record(tmp_path):
    report = report_for(source())
    path = write_inventory(tmp_path, source(), report)
    (record,) = load_source_qualifications(path, [source()], POLICY)
    assert record.report == report
    assert record.verification_sha256 == fingerprint(report)
    assert record.to_dict()["report"]["checked_at"] > CUTOFF
    record.report["runs"]["historical_fixed"]["exit_code"] = 1
    with pytest.raises(ValueError, match="binding/hash"):
        record.validate(source(), POLICY)


@pytest.mark.parametrize("bad_alias", [False, True])
def test_commit_alias_requires_same_issue_repository_and_full_revision(tmp_path, bad_alias):
    canonical = source()
    report = report_for(canonical)
    alias_source = replace(canonical, fix_id="example/repo:commit:" + canonical.revision)
    aliases = [
        {
            "fix_id": alias_source.fix_id,
            "locator": {
                "repository": canonical.repository,
                "commit": ("b" * 40 if bad_alias else canonical.revision),
            },
        }
    ]
    path = write_inventory(tmp_path, canonical, report, aliases=aliases)
    if bad_alias:
        with pytest.raises(ValueError, match="missing"):
            load_source_qualifications(path, [alias_source], POLICY)
    else:
        (record,) = load_source_qualifications(path, [alias_source], POLICY)
        record.validate(alias_source, POLICY)


@pytest.mark.parametrize("mutation", ["incomplete", "row_count", "duplicate"])
def test_inventory_cannot_hide_population_or_disagree_with_report(tmp_path, mutation):
    path = write_inventory(tmp_path, source(), report_for(source()))
    inventory = json.loads(path.read_text())
    if mutation == "incomplete":
        inventory["canonical_requested_count"] = 2
    elif mutation == "row_count":
        inventory["results"][0]["fail_to_pass_count"] = 7
    else:
        inventory["results"] *= 2
        inventory["canonical_requested_count"] = 2
    path.write_text(json.dumps(inventory))
    with pytest.raises(ValueError):
        load_source_qualifications(path, [source()], POLICY)


def pattern_input(tmp_path):
    response, old_sources = authored_bundle()
    sources = []
    for old in old_sources:
        new = replace(old, bug_cluster_id=old.repository + ":1", fix_id=old.repository + ":pr:2")
        response = response.replace(json.dumps(old.bug_cluster_id), json.dumps(new.bug_cluster_id))
        response = response.replace(json.dumps(old.fix_id), json.dumps(new.fix_id))
        sources.append(new)
    (package,) = publish_v4_bundle(response, sources, POLICY, tmp_path / "source")
    files_by_name, _ = parse_bundle(response)
    name, files = next(iter(files_by_name.items()))
    records = tuple(
        HistoricalQualification(s.id, fingerprint(report_for(s)), "3" * 64, report_for(s))
        for s in sources
    )
    provenance = json.loads(files["references/provenance.json"])
    provenance["source_package_hashes"] = {
        package.reference["skill_id"]: package.reference["package_sha256"]
    }
    provenance["generation_context"] = generation_context_for_packages([package]).to_dict()
    provenance["qualification_report_hashes"] = {
        r.source_id: r.verification_sha256 for r in records
    }
    files["references/provenance.json"] = json.dumps(provenance)
    return package, name, files, records


def test_author_receives_complete_report_separately_from_historical_evidence(tmp_path):
    package, name, files, records = pattern_input(tmp_path)
    transport = Transport([bundle_from_files(name, files)])
    (derived,) = extract_native_pattern(
        transport,
        [package],
        POLICY,
        tmp_path / "output",
        qualification_records=records,
        audit_dir=tmp_path / "audit",
    )
    payload, _ = json.JSONDecoder().raw_decode(transport.calls[0]["user"])
    assert payload["independent_qualification_records"] == [
        r.to_dict() for r in sorted(records, key=lambda r: r.source_id)
    ]
    assert "validation provenance only" in payload["qualification_instruction"]
    assert (
        json.loads((tmp_path / "audit/qualification-input.json").read_text())
        == payload["independent_qualification_records"]
    )
    assert [s.available_at for s in derived.sources] == [s.available_at for s in package.sources]
    assert not list((tmp_path / "output").rglob("qualification-input.json"))


@pytest.mark.parametrize("mutation", ["missing_source", "tampered_record", "authored_hash"])
def test_unqualified_or_changed_report_never_publishes(tmp_path, mutation):
    package, name, files, records = pattern_input(tmp_path)
    records = copy.deepcopy(records)
    if mutation == "missing_source":
        records = records[:1]
    elif mutation == "tampered_record":
        records[0].report["identity"]["merge_commit"] = "f" * 40
    else:
        provenance = json.loads(files["references/provenance.json"])
        provenance["qualification_report_hashes"] = {}
        files["references/provenance.json"] = json.dumps(provenance)
    transport = Transport([bundle_from_files(name, files)])
    with pytest.raises(ValueError):
        extract_native_pattern(
            transport, [package], POLICY, tmp_path / "output", qualification_records=records
        )
    assert not list((tmp_path / "output").rglob("SKILL.md"))
    if mutation != "authored_hash":
        assert not transport.calls
