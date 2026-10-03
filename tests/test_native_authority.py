"""Reject authored provenance drift before any native package is published."""

import json
from dataclasses import replace

import pytest
from adaptive_fixture import CUTOFF, DATE, authored_bundle

from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.direct_skill_extraction import parse_bundle
from arex_skill_graph.pattern_contracts import publish_v4_bundle


def bundle_from_files(name, files):
    return (
        "AREX-SKILL-BUNDLE 1\n"
        + "".join(
            f"<<<FILE {name}/{path}>>>\n{content.rstrip()}\n<<<END FILE>>>\n"
            for path, content in files.items()
        )
        + "AREX-SKILL-BUNDLE-END\n"
    )


def authority_bundle():
    response, sources = authored_bundle(pattern=False)
    for action in ("detect:a", "guard:a", "validate:a"):
        response = response.replace(action, "workflow:a:" + action)
    packages, _ = parse_bundle(response)
    name, files = next(iter(packages.items()))
    evidence = {"evidence:a": {"available_at": DATE, "kind": "resolution"}}
    return name, files, sources, evidence


def test_authority_accepts_exact_repair_id(tmp_path):
    name, files, sources, evidence = authority_bundle()
    repaired = replace(sources[0], id="source:a:repair:aaaaaaaaaaaa", aliases=("source:a",))
    response = bundle_from_files(name, files).replace('"source:a"', '"' + repaired.id + '"')
    # The SourceRecord itself must retain the original issue alias exactly.
    packages, _ = parse_bundle(response)
    files = packages[name]
    provenance = json.loads(files["references/provenance.json"])
    provenance["sources"][0]["aliases"] = ["source:a"]
    files["references/provenance.json"] = json.dumps(provenance)
    (package,) = publish_v4_bundle(
        bundle_from_files(name, files),
        (repaired,),
        TemporalPolicy(CUTOFF),
        tmp_path,
        authoritative_evidence=evidence,
        authoritative_package_id="workflow:a",
    )
    assert package.reference["source_episode_ids"] == [repaired.id]


def test_native_coherence_refuses_invalidation_of_preserved_behavior(tmp_path):
    name, files, sources, evidence = authority_bundle()
    path = "references/actions/guard-a.md"
    files[path] = files[path].replace('"invalidates": []', '"invalidates": ["runtime-diagnostic"]')
    # Edit the contract rather than relying on the fixture's formatting.
    from arex_skill_graph.action_contracts import read_contract

    action = dict(read_contract(files[path]))
    action["invalidates"] = [action["preserves"][0]["key"]]
    start = files[path].index("```arex-contract-v4\n") + len("```arex-contract-v4\n")
    end = files[path].index("\n```", start)
    files[path] = files[path][:start] + json.dumps(action) + files[path][end:]
    with pytest.raises(ValueError, match="invalidates preserved behavior"):
        publish_v4_bundle(
            bundle_from_files(name, files),
            sources,
            TemporalPolicy(CUTOFF),
            tmp_path,
            authoritative_evidence=evidence,
            authoritative_package_id="workflow:a",
            require_coherent_workflows=True,
        )
    assert not list(tmp_path.glob("*/SKILL.md"))


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("episode_alias", "source_episode_ids"),
        ("source_alias", "contradicts authoritative"),
        ("evidence_date", "date/kind"),
        ("evidence_kind", "date/kind"),
        ("evidence_id", "outside authoritative source"),
        ("package_id", "authoritative package identity"),
        ("action_namespace", "authoritative package namespace"),
    ],
)
def test_authority_rejects_drift_without_publication(tmp_path, mutation, message):
    name, files, sources, evidence = authority_bundle()
    provenance = json.loads(files["references/provenance.json"])
    if mutation == "episode_alias":
        provenance["source_episode_ids"] = ["issue:alias"]
    elif mutation == "source_alias":
        provenance["sources"][0]["aliases"] = ["invented:alias"]
    elif mutation == "package_id":
        provenance["package"]["skill_id"] = "workflow:invented"
    elif mutation.startswith("evidence_"):
        _field, old, new = {
            "evidence_date": ("available_at", DATE, "2019-01-01T00:00:00Z"),
            "evidence_kind": ("kind", "resolution", "invented-execution"),
            "evidence_id": ("id", "evidence:a", "evidence:invented"),
        }[mutation]
        path = "references/evidence/source-a.md"
        files[path] = files[path].replace(json.dumps(old), json.dumps(new))
    elif mutation == "action_namespace":
        path = "references/actions/detect-a.md"
        files[path] = files[path].replace("workflow:a:detect:a", "detect:outside")
    files["references/provenance.json"] = json.dumps(provenance)
    with pytest.raises(ValueError, match=message):
        publish_v4_bundle(
            bundle_from_files(name, files),
            sources,
            TemporalPolicy(CUTOFF),
            tmp_path,
            authoritative_evidence=evidence,
            authoritative_package_id="workflow:a",
        )
    assert not list(tmp_path.glob("*/SKILL.md"))
