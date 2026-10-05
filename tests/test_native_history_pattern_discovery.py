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
