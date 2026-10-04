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


def canonical_response(package, name, files):
    response = bundle_from_files(name, files)
    pid = package.reference["skill_id"]
    for action in package.actions:
        response = response.replace(json.dumps(action.id), json.dumps(pid + ":" + action.id))
    for workflow in package.workflows:
        response = response.replace(json.dumps(workflow.id), json.dumps(pid + ":" + workflow.id))
    return response


@pytest.mark.parametrize("local", [False, True])
def test_canonical_abstraction_namespaces_actions_and_realizations(tmp_path, local):
    package, name, files = source_and_response(tmp_path, local=local)
    pid = package.reference["skill_id"]
    (derived,) = extract_native_pattern(
        Transport([canonical_response(package, name, files)]),
        [package],
        TemporalPolicy(CUTOFF),
        tmp_path / "output",
        canonical_package_id=pid,
        reviewed_mechanism=MECHANISM,
    )
    assert all(w.id.startswith(pid + ":") for w in derived.workflows)
    assert all(a.id.startswith(pid + ":") for a in derived.actions)


@pytest.mark.parametrize(
    "resource", ["references/workflow.md", "references/realizations/workflow-b.md"]
)
def test_realization_namespace_drift_never_publishes(tmp_path, resource):
    package, name, files = source_and_response(tmp_path)
    response = canonical_response(package, name, files)
    authored, _ = parse_bundle(response)
    files = authored[name]
    files[resource] = files[resource].replace(
        json.dumps(
            package.reference["skill_id"]
            + ":workflow:"
            + ("a" if resource.endswith("/workflow.md") else "b")
        ),
        json.dumps("workflow:outside-namespace"),
    )
    with pytest.raises(ValueError, match="authoritative package namespace"):
        extract_native_pattern(
            Transport([bundle_from_files(name, files)]),
            [package],
            TemporalPolicy(CUTOFF),
            tmp_path / "output",
            canonical_package_id=package.reference["skill_id"],
        )
    assert not list((tmp_path / "output").rglob("SKILL.md"))


@pytest.mark.parametrize("malformation", ["index_only", "duplicate_block"])
def test_primary_workflow_must_have_exactly_one_realization_contract(tmp_path, malformation):
    package, name, files = source_and_response(tmp_path)
    if malformation == "index_only":
        files["references/workflow.md"] = (
            "# Index" + chr(10) * 2 + "See realizations for historical Workflows." + chr(10)
        )
    else:
        files["references/workflow.md"] *= 2
    with pytest.raises(ValueError, match=r"references/workflow\.md: .*exactly one"):
        publish_v4_bundle(
            bundle_from_files(name, files),
            package.sources,
            TemporalPolicy(CUTOFF),
            tmp_path / "output",
        )
    assert not list((tmp_path / "output").rglob("SKILL.md"))
