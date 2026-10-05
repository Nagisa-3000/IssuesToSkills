import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest


def discovery_module():
    path = Path(__file__).resolve().parents[1] / "experiments/discover_native_history_patterns.py"
    spec = importlib.util.spec_from_file_location("test_native_discovery_entry", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup_discovery(tmp_path, monkeypatch):
    module = discovery_module()
    packages = []
    for index in range(2):
        root = tmp_path / f"source-{index}"
        evidence = root / "references/evidence"
        evidence.mkdir(parents=True)
        (evidence / "source.md").write_text("Independent current-state historical evidence")
        source = SimpleNamespace(
            id=f"source:{index}",
            bug_cluster_id=f"cluster:{index}",
            fix_id=f"fix:{index}",
            revision=f"revision:{index}",
            repository=f"repo:{index}",
        )
        packages.append(
            SimpleNamespace(
                reference={"skill_id": f"package:{index}", "package_sha256": str(index) * 64},
                sources=(source,),
                workflows=(SimpleNamespace(to_dict=lambda: {"mechanism": "fixture"}),),
                evidence_ids=(f"evidence:{index}",),
                root=str(root),
            )
        )
    response = {
        "groups": [
            {
                "mechanism": "Synthetic shared mechanism",
                "reason": "Two independent source fixes",
                "package_ids": ["package:0", "package:1"],
                "evidence_refs": ["evidence:0", "evidence:1"],
            }
        ]
    }

    @dataclass
    class Config:
        max_output_tokens: int = 10
        timeout_seconds: float = 1
        stream_responses: bool = False

    class Transport:
        def __init__(self):
            self.config = Config()
            self.calls = []

        def complete(self, **kwargs):
            self.calls.append({"system": kwargs["system"], "corpus": json.loads(kwargs["user"])})
            return response

    transport = Transport()
    monkeypatch.setattr(module, "read_references", lambda path: packages)
    monkeypatch.setattr(module, "load_native_package", lambda package, policy: package)
    monkeypatch.setattr(
        module,
        "load_source_qualifications",
        lambda *args: [
            SimpleNamespace(source_id=f"source:{i}", verification_sha256=str(i) * 64)
            for i in range(2)
        ],
    )
    monkeypatch.setattr(
        module,
        "generation_context_for_packages",
        lambda *args, **kwargs: SimpleNamespace(to_dict=lambda: {"fixture": True}),
    )
    monkeypatch.setattr(module, "transport_from_args", lambda args: transport)
    verifications = tmp_path / "verifications.json"
    verifications.write_text("{}")
    arguments = [
        "--references",
        str(tmp_path / "references.json"),
        "--verifications",
        str(verifications),
        "--output-dir",
        str(tmp_path / "output"),
        "--audit-dir",
        str(tmp_path / "audit"),
        "--model",
        "synthetic",
        "--base-url",
        "https://example.invalid/v1",
    ]
    return module, transport, arguments


def test_discover_stage_covers_all_packages_without_authoring(tmp_path, monkeypatch):
    module, transport, args = setup_discovery(tmp_path, monkeypatch)

    def forbidden(*args, **kwargs):
        raise AssertionError("Discover-only must never author packages")

    monkeypatch.setattr(module, "extract_native_pattern", forbidden)
    assert module.main([*args, "--stage", "discover"]) == 0
    assert len(transport.calls) == 1
    assert len(transport.calls[0]["corpus"]) == 2
    inventory = json.loads((tmp_path / "output/discovery-inventory.json").read_text())
    assert inventory["stage"] == "discover"
    assert inventory["references"] == []
    assert not inventory["groups_semantically_accepted"]
    assert inventory["results"][0]["status"] == "discovered-unreviewed"
    assert inventory["results"][0]["expected_kind"] == "pattern"
    assert (tmp_path / "audit/calls.json").exists()


def test_discovery_reuse_requires_identical_complete_source_corpus(tmp_path, monkeypatch):
    module, transport, args = setup_discovery(tmp_path, monkeypatch)
    monkeypatch.setattr(module, "extract_native_pattern", lambda *args, **kwargs: [])
    assert module.main([*args, "--stage", "discover"]) == 0
    previous = tmp_path / "audit"
    changed = list(args)
    changed[changed.index("--output-dir") + 1] = str(tmp_path / "authored")
    changed[changed.index("--audit-dir") + 1] = str(tmp_path / "author-audit")
    assert module.main([*changed, "--discovery-audit", str(previous)]) == 0
    assert len(transport.calls) == 1
    input_path = previous / "discovery-input.json"
    input_path.write_text("[]")
    changed[changed.index("--output-dir") + 1] = str(tmp_path / "mismatch-output")
    changed[changed.index("--audit-dir") + 1] = str(tmp_path / "mismatch-audit")
    with pytest.raises(ValueError, match="exact full source corpus"):
        module.main([*changed, "--discovery-audit", str(previous)])
    assert len(transport.calls) == 1


def reviewed_authoring_inputs(tmp_path, monkeypatch):
    module, transport, args = setup_discovery(tmp_path, monkeypatch)
    original_complete = transport.complete

    def complete(**kwargs):
        response = original_complete(**kwargs)
        second = {**response["groups"][0], "mechanism": "Distinct fixture mechanism"}
        response["groups"].append(second)
        return response

    monkeypatch.setattr(transport, "complete", complete)
    assert module.main([*args, "--stage", "discover"]) == 0
    previous = tmp_path / "audit"
    corpus = json.loads((previous / "discovery-input.json").read_text())
    inventory = json.loads((tmp_path / "output/discovery-inventory.json").read_text())
    rows = []
    for index, item in enumerate(inventory["results"]):
        group = item["group"]
        rows.append(
            {
                "group_id": item["canonical_package_id"],
                "status": "ACCEPT" if index == 0 else "DEFER",
                "reviewed_mechanism": "Reviewed narrower fixture mechanism",
                "supported_package_ids": group["package_ids"],
                "unsupported_package_ids": [],
                "limitations": [
                    "Only the supplied owner boundary is supported; transfer untested."
                ],
                "rationale": "Independent fixture review narrows the discovery claim.",
                "evidence_refs": group["evidence_refs"],
            }
        )
    review = {"schema": "complete-native-mechanism-group-review-v1", "reviews": rows}
    original = inventory["results"][0]
    approved = {
        "discovery_group_id": rows[0]["group_id"],
        "package_ids": original["group"]["package_ids"],
        "evidence_refs": original["group"]["evidence_refs"],
        "expected_kind": original["expected_kind"],
        "mechanism": rows[0]["reviewed_mechanism"],
        "reason": rows[0]["rationale"],
        "limitations": rows[0]["limitations"],
        "formal_KB_admitted": False,
        "native_package_authoring_status": "pending",
    }
    manifest = {
        "schema": "independently-reviewed-native-authoring-groups-v1",
        "adjudicated_review_sha256": module.fingerprint(review),
        "source_corpus_sha256": module.fingerprint(corpus),
        "full_original_discovery_population": len(corpus),
        "generation_context": {"fixture": True},
        "groups": [approved],
    }
    review_path = tmp_path / "independent-review.json"
    manifest_path = tmp_path / "accepted.json"
    review_path.write_text(json.dumps(review))
    manifest_path.write_text(json.dumps(manifest))
    args = list(args)
    args[args.index("--output-dir") + 1] = str(tmp_path / "authored")
    args[args.index("--audit-dir") + 1] = str(tmp_path / "author-audit")
    args += [
        "--discovery-audit",
        str(previous),
        "--reviewed-groups",
        str(manifest_path),
        "--mechanism-review",
        str(review_path),
    ]
    return module, transport, args, manifest, review, manifest_path, review_path


def test_reviewed_authoring_keeps_narrowed_limits_and_does_not_author_deferred_group(
    tmp_path, monkeypatch
):
    module, transport, args, manifest, _review, _manifest_path, _review_path = (
        reviewed_authoring_inputs(tmp_path, monkeypatch)
    )
    author_calls = []

    def author(*positional, **kwargs):
        author_calls.append(kwargs)
        return []

    monkeypatch.setattr(module, "extract_native_pattern", author)
    assert module.main(args) == 0
    assert len(transport.calls) == 1 and len(author_calls) == 1
    assert author_calls[0]["reviewed_mechanism"] == manifest["groups"][0]["mechanism"]
    packet = author_calls[0]["mechanism_review"]
    assert packet["limitations"] == manifest["groups"][0]["limitations"]
    assert packet["authoring_manifest_sha256"] == module.fingerprint(manifest)
    inventory = json.loads((tmp_path / "authored/extraction-inventory-v4.json").read_text())
    assert inventory["source_package_count"] == 2
    assert inventory["independently_accepted_authoring_groups"] == 1
    assert inventory["reviewed_authoring_only"] and not inventory["formal_KB_admitted"]
    assert inventory["results"][1]["status"] == "deferred-by-independent-review"


@pytest.mark.parametrize(
    "drift",
    [
        "review_hash",
        "future_context",
        "corpus",
        "population",
        "omitted_review",
        "duplicate_review",
        "invented_group",
        "lost_limits",
        "changed_support",
        "overclaimed_kind",
    ],
)
def test_review_drift_is_rejected_before_author_calls(tmp_path, monkeypatch, drift):
    module, transport, args, manifest, review, manifest_path, review_path = (
        reviewed_authoring_inputs(tmp_path, monkeypatch)
    )
    if drift == "review_hash":
        manifest["adjudicated_review_sha256"] = "0" * 64
    elif drift == "future_context":
        manifest["generation_context"] = {"fixture": True, "future_source": "2025-01-01"}
    elif drift == "corpus":
        manifest["source_corpus_sha256"] = "0" * 64
    elif drift == "population":
        manifest["full_original_discovery_population"] = 1
    elif drift in {"omitted_review", "duplicate_review"}:
        if drift == "omitted_review":
            review["reviews"].pop()
        else:
            review["reviews"].append(review["reviews"][0])
        manifest["adjudicated_review_sha256"] = module.fingerprint(review)
    elif drift == "invented_group":
        manifest["groups"][0]["discovery_group_id"] = "pattern:unobserved"
    elif drift == "lost_limits":
        manifest["groups"][0]["limitations"] = []
    elif drift == "changed_support":
        manifest["groups"][0]["package_ids"] = ["package:0"]
    else:
        manifest["groups"][0]["expected_kind"] = "local_template"
    manifest_path.write_text(json.dumps(manifest))
    review_path.write_text(json.dumps(review))
    monkeypatch.setattr(
        module,
        "extract_native_pattern",
        lambda *args, **kwargs: pytest.fail("Invalid review must never reach authoring"),
    )
    with pytest.raises(ValueError, match="mechanism|accepted"):
        module.main(args)
    assert len(transport.calls) == 1


def test_complete_discovery_is_validated_before_first_author_call(tmp_path, monkeypatch):
    module, transport, args, _manifest, _review, _manifest_path, _review_path = (
        reviewed_authoring_inputs(tmp_path, monkeypatch)
    )
    previous = tmp_path / "audit/discovery-response.json"
    discovery = json.loads(previous.read_text())
    discovery["groups"][1]["evidence_refs"] = ["evidence:invented"]
    previous.write_text(json.dumps(discovery))
    monkeypatch.setattr(
        module,
        "extract_native_pattern",
        lambda *args, **kwargs: pytest.fail("Late invalid group must prevent all author calls"),
    )
    with pytest.raises(ValueError, match="every contributing package"):
        module.main(args)
    assert len(transport.calls) == 1
