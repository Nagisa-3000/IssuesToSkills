import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


def authoring_cli():
    spec = importlib.util.spec_from_file_location(
        "native_history_checkpoint_cli",
        Path(__file__).resolve().parents[1] / "experiments/extract_verified_history_skills.py",
    )
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def author_inputs(cli):
    record = {
        "issue_id": "owner/repo:42",
        "identity": {
            "repository": "owner/repo",
            "created_at": "2020-01-01T00:00:00Z",
            "url": "https://example.invalid/owner/repo/issues/42",
        },
        "evidence": [
            {
                "id": "owner/repo:42:body",
                "kind": "issue_body_as_of_cutoff",
                "available_at": "2020-01-01T00:00:00Z",
                "text": "Public fixture report",
            }
        ],
    }
    verification = {
        "schema": "historical-causal-verification-v1",
        "qualification_scope": "changed-test-files-with-original-base-control",
        "verified_resolution": True,
        "identity": {
            "issue_id": "owner/repo:42",
            "fix_id": "owner/repo:pr:43",
            "repair_available_at": "2020-01-02T00:00:00Z",
            "merge_commit": "a" * 40,
        },
        "observations": [],
        "observations_sha256": cli.fingerprint([]),
        "checked_at": "2026-10-05T00:00:00Z",
        "runtime_sha256": "b" * 64,
        "fail_to_pass": ["test_fixture"],
        "pass_to_pass": ["test_fixture"],
    }
    config = SimpleNamespace(
        model="fixture-model", base_url="https://example.invalid/v1", max_output_tokens=24000
    )
    return (
        record,
        verification,
        {"production_diff": "implementation", "regression_diff": "tests"},
        config,
    )


def prepare_checkpoint(tmp_path, monkeypatch):
    cli = authoring_cli()
    # Qualification and bundle behavior have separate tests. Exercise the real
    # author identity construction, serialization and checkpoint boundary here.
    monkeypatch.setattr(cli, "validate_historical_qualification", lambda *args: None)
    monkeypatch.setattr(cli, "native_extraction_prompt", lambda *args: "Stable fixture protocol")
    created = []

    class OfflineFailure:
        def __init__(self, config):
            created.append(config)
            self.calls = []

        def complete_text(self, **kwargs):
            raise RuntimeError("Offline fixture: no network request executed")

    monkeypatch.setattr(cli, "OpenAICompatibleTransport", OfflineFailure)
    inputs = author_inputs(cli)
    first = cli.author_case(
        *inputs[:3],
        cli.TemporalPolicy("2024-01-01T00:00:00Z"),
        tmp_path / "output",
        tmp_path / "audit",
        inputs[3],
    )
    assert first["deferred"] and len(created) == 1
    result_path = tmp_path / "audit/extraction-result.json"
    cached = json.loads(result_path.read_text())
    assert isinstance(first["input_identity"]["source"]["evidence_refs"], tuple)
    assert isinstance(cached["input_identity"]["source"]["evidence_refs"], list)
    before = {path: path.read_bytes() for path in (tmp_path / "audit").iterdir()}

    def forbidden(*args, **kwargs):
        pytest.fail("checkpoint reuse/rejection must happen before model transport creation")

    monkeypatch.setattr(cli, "OpenAICompatibleTransport", forbidden)
    return cli, inputs, result_path, cached, before


def test_author_checkpoint_json_roundtrip_reuses_without_model_calls(tmp_path, monkeypatch):
    cli, inputs, _path, cached, before = prepare_checkpoint(tmp_path, monkeypatch)
    reused = cli.author_case(
        *inputs[:3],
        cli.TemporalPolicy("2024-01-01T00:00:00Z"),
        tmp_path / "output",
        tmp_path / "audit",
        inputs[3],
    )
    assert reused == cached
    assert {path: path.read_bytes() for path in (tmp_path / "audit").iterdir()} == before
    assert not (tmp_path / "output").exists()


@pytest.mark.parametrize(
    "mutation", ["protocol", "source_revision", "source_alias", "model", "evidence"]
)
def test_author_checkpoint_rejects_actual_identity_changes(tmp_path, monkeypatch, mutation):
    cli, inputs, result_path, cached, _before = prepare_checkpoint(tmp_path, monkeypatch)
    identity = cached["input_identity"]
    if mutation == "protocol":
        identity["authoring_protocol_version"] = "different-protocol"
    elif mutation == "source_revision":
        identity["source"]["revision"] = "c" * 40
    elif mutation == "source_alias":
        identity["source"]["aliases"].append("owner/repo:unrelated")
    elif mutation == "model":
        identity["model"] = "different-model"
    else:
        identity["evidence_sha256"] = "d" * 64
    result_path.write_text(json.dumps(cached))
    before = {path: path.read_bytes() for path in (tmp_path / "audit").iterdir()}
    with pytest.raises(ValueError, match="checkpoint identity changed"):
        cli.author_case(
            *inputs[:3],
            cli.TemporalPolicy("2024-01-01T00:00:00Z"),
            tmp_path / "output",
            tmp_path / "audit",
            inputs[3],
        )
    assert {path: path.read_bytes() for path in (tmp_path / "audit").iterdir()} == before
