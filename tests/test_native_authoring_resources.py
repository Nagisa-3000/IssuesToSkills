import importlib.util
from pathlib import Path

import pytest

from arex_skill_graph.pattern_contracts import native_authoring_protocol_path


def test_native_authoring_snapshot_requires_its_protocol_resource(tmp_path):
    with pytest.raises(FileNotFoundError, match="execution snapshot"):
        native_authoring_protocol_path(tmp_path)
    expected = (
        tmp_path
        / "data/skill-extraction/packages/universal-resolution-distiller/references/action-contract-v4.md"
    )
    expected.parent.mkdir(parents=True)
    expected.write_text("Closed fixture protocol")
    assert native_authoring_protocol_path(tmp_path).read_text() == "Closed fixture protocol"


def test_missing_protocol_fails_before_census_loading_or_model_calls(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "native_history_authoring_cli",
        Path(__file__).resolve().parents[1] / "experiments/extract_verified_history_skills.py",
    )
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    monkeypatch.setattr(
        cli, "native_authoring_protocol_path", lambda: native_authoring_protocol_path(tmp_path)
    )

    def forbidden(*args, **kwargs):
        pytest.fail("missing snapshot resource must stop before model transport creation")

    monkeypatch.setattr(cli, "OpenAICompatibleTransport", forbidden)
    with pytest.raises(FileNotFoundError, match="execution snapshot"):
        cli.main(
            [
                "--census",
                str(tmp_path / "missing-census"),
                "--verifications",
                str(tmp_path / "missing-inventory"),
                "--output-dir",
                str(tmp_path / "output"),
                "--audit-dir",
                str(tmp_path / "audit"),
                "--model",
                "fixture-model",
                "--base-url",
                "https://example.invalid/v1",
            ]
        )
