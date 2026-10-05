import importlib.util
from pathlib import Path

import pytest


def authoring_cli():
    spec = importlib.util.spec_from_file_location(
        "native_history_scope_cli",
        Path(__file__).resolve().parents[1] / "experiments/extract_verified_history_skills.py",
    )
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def test_rust_source_authoring_does_not_claim_changed_test_files_qualification():
    limits = authoring_cli().qualification_scope_limits(
        {
            "schema": "historical-rust-test-causal-verification-v1",
            "qualification_scope": "exact-rust-libtest-with-original-base-control-v1",
        }
    )
    assert "one exact named Rust library test" in limits
    assert "original expected snapshot" in limits
    assert "Changed test files only" not in limits
    assert "whole-project regression" in limits and "cross-project transfer" in limits


def test_python_source_keeps_its_existing_qualification_limits():
    limits = authoring_cli().qualification_scope_limits(
        {
            "schema": "historical-causal-verification-v1",
            "qualification_scope": "changed-test-files-with-original-base-control",
        }
    )
    assert (
        limits
        == "Changed test files only; whole-project regression and cross-project transfer are untested."
    )


@pytest.mark.parametrize(
    "report",
    [
        {
            "schema": "historical-rust-test-causal-verification-v1",
            "qualification_scope": "changed-test-files-with-original-base-control",
        },
        {
            "schema": "unknown",
            "qualification_scope": "exact-rust-libtest-with-original-base-control-v1",
        },
    ],
)
def test_unknown_or_mismatched_source_scope_cannot_reach_authoring(report):
    with pytest.raises(ValueError, match="unsupported native authoring qualification scope"):
        authoring_cli().qualification_scope_limits(report)


def test_actual_rust_author_packet_keeps_the_native_scope_boundary(tmp_path, monkeypatch):
    cli = authoring_cli()
    captured = {}

    class PacketCaptured(Exception):
        pass

    def capture(sources, packet, policy):
        captured.update(packet)
        raise PacketCaptured

    monkeypatch.setattr(cli, "validate_historical_qualification", lambda *args: None)
    monkeypatch.setattr(cli, "native_extraction_prompt", capture)
    verification = {
        "schema": "historical-rust-test-causal-verification-v1",
        "qualification_scope": "exact-rust-libtest-with-original-base-control-v1",
        "verified_resolution": True,
        "observations": [],
        "observations_sha256": cli.fingerprint([]),
        "identity": {
            "issue_id": "astral-sh/ruff:5124",
            "fix_id": "astral-sh/ruff:pr:5125",
            "repair_available_at": "2023-06-15T19:00:20Z",
            "merge_commit": "107a295af4f51dce1e78dcbfd234b2a3ad99a00f",
        },
        "checked_at": "2026-10-05T07:00:00Z",
        "runtime_sha256": "a" * 64,
        "fail_to_pass": ["exact-named-test"],
        "pass_to_pass": ["exact-named-test"],
    }
    record = {
        "issue_id": "astral-sh/ruff:5124",
        "evidence": [],
        "identity": {
            "repository": "astral-sh/ruff",
            "created_at": "2023-06-15T18:00:00Z",
            "url": "https://github.com/astral-sh/ruff/issues/5124",
        },
    }
    with pytest.raises(PacketCaptured):
        cli.author_case(
            record,
            verification,
            {"production_diff": "implementation", "regression_diff": "fixture"},
            cli.TemporalPolicy("2024-01-01T00:00:00Z"),
            tmp_path / "output",
            tmp_path / "audit",
            None,
        )
    attestation = captured["qualification_attestation"]
    assert attestation["scope"] == verification["qualification_scope"]
    assert "one exact named Rust library test" in attestation["scope_limits"]
    assert "Changed test files only" not in attestation["scope_limits"]
