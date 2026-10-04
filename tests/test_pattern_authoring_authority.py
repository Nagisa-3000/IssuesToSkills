"""Pattern authoring cannot change reviewed support or publish rejected drafts."""

import json
from dataclasses import replace

import pytest
from adaptive_fixture import CUTOFF, MECHANISM, authored_bundle
from test_native_authority import bundle_from_files

from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.direct_skill_extraction import parse_bundle
from arex_skill_graph.pattern_contracts import extract_native_pattern, publish_v4_bundle


class Transport:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def complete_text(self, **kwargs):
        self.calls.append({"user": kwargs["user"]})
        return next(self.responses)


def source_and_response(tmp_path, *, local=False):
    response, sources = authored_bundle()
    if local:
        response = response.replace('"synthetic/a"', '"synthetic/one"').replace(
            '"synthetic/b"', '"synthetic/one"'
        )
        response = response.replace('"cross_project": true', '"cross_project": false')
        response = response.replace('"package_kind": "pattern"', '"package_kind": "local_template"')
        response = response.replace('"level": "pattern"', '"level": "local_template"')
        sources = [replace(source, repository="synthetic/one") for source in sources]
    (package,) = publish_v4_bundle(response, sources, TemporalPolicy(CUTOFF), tmp_path / "source")
    packages, _ = parse_bundle(response)
    name, files = next(iter(packages.items()))
    provenance = json.loads(files["references/provenance.json"])
    provenance["source_package_hashes"] = {
        package.reference["skill_id"]: package.reference["package_sha256"]
    }
    files["references/provenance.json"] = json.dumps(provenance)
    return package, name, files


@pytest.mark.parametrize("drift", ["kind", "mechanism", "cross_project", "lineage"])
def test_pattern_drift_is_rejected_before_publication(tmp_path, drift):
    package, name, files = source_and_response(tmp_path, local=True)
    if drift in {"kind", "lineage"}:
        provenance = json.loads(files["references/provenance.json"])
        if drift == "kind":
            provenance["package_kind"] = "pattern"
        else:
            provenance["source_package_hashes"] = {}
        files["references/provenance.json"] = json.dumps(provenance)
    elif drift == "mechanism":
        files["SKILL.md"] = files["SKILL.md"].replace(MECHANISM, "Unreviewed mechanism")
    else:
        files["SKILL.md"] = files["SKILL.md"].replace(
            '"cross_project": false', '"cross_project": true'
        )
    transport = Transport([bundle_from_files(name, files)])
    with pytest.raises(ValueError):
        extract_native_pattern(
            transport,
            [package],
            TemporalPolicy(CUTOFF),
            tmp_path / "output",
            reviewed_mechanism=MECHANISM,
            expected_kind="local_template",
        )
    assert not (tmp_path / "output").exists()


def test_repair_or_defer_preserves_rejection_and_call_audit(tmp_path):
    package, name, files = source_and_response(tmp_path)
    files["SKILL.md"] = files["SKILL.md"].replace(MECHANISM, "Unreviewed mechanism")
    transport = Transport(
        [
            bundle_from_files(name, files),
            "AREX-SKILL-DEFERRED 1\nInsufficient reviewed support.\nAREX-SKILL-DEFERRED-END\n",
        ]
    )
    assert (
        extract_native_pattern(
            transport,
            [package],
            TemporalPolicy(CUTOFF),
            tmp_path / "output",
            reviewed_mechanism=MECHANISM,
            audit_dir=tmp_path / "audit",
            max_attempts=2,
        )
        == ()
    )
    audit = json.loads((tmp_path / "audit/authoring-audit.json").read_text())
    assert len(audit["failures"]) == 1 and len(audit["calls"]) == 2
    assert "rejected" in transport.calls[1]["user"]
    assert not list((tmp_path / "output").rglob("SKILL.md"))


def test_valid_reviewed_abstraction_is_still_publishable(tmp_path):
    package, name, files = source_and_response(tmp_path)
    (derived,) = extract_native_pattern(
        Transport([bundle_from_files(name, files)]),
        [package],
        TemporalPolicy(CUTOFF),
        tmp_path / "output",
        reviewed_mechanism=MECHANISM,
        expected_kind="pattern",
    )
    assert derived.pattern.mechanism == MECHANISM and derived.kind == "pattern"
