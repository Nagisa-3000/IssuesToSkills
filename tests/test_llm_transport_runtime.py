import importlib.util
import io
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from urllib.error import URLError

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import ActionContract
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport

SENTINEL = "synthetic-process-only-credential-fixture"


def transport(**kwargs):
    return OpenAICompatibleTransport(
        OpenAICompatibleConfig(SENTINEL, "https://example.invalid/v1", "fixture-model", **kwargs)
    )


def envelope(content="{}", finish="stop"):
    return {
        "id": "fixture-response",
        "choices": [{"finish_reason": finish, "message": {"content": content}}],
        "usage": {"prompt_tokens": 12, "completion_tokens": 3},
    }


def test_windows_pipe_keeps_credentials_out_of_argv_and_audits_unicode_response(monkeypatch):
    def fake_run(argv, **kwargs):
        assert SENTINEL not in " ".join(argv)
        supplied = json.loads(kwargs["input"])
        assert supplied["credential"] == SENTINEL
        assert supplied["body"]["messages"][1]["content"] == "公开验证"
        assert kwargs["stderr"] == subprocess.DEVNULL
        return SimpleNamespace(
            returncode=0,
            stdout="\ufeff"
            + json.dumps({"status": 200, "body": json.dumps(envelope("完成"), ensure_ascii=False)}),
        )

    monkeypatch.setattr("arex_skill_graph.llm_http.subprocess.run", fake_run)
    model = transport(http_backend="windows_pipe", retries=0)
    assert model.complete_text(system="Read public evidence", user="公开验证") == "完成"
    assert model.calls[0]["successful"] is True
    assert SENTINEL not in json.dumps(model.calls + model.transcripts)
    assert SENTINEL not in repr(model.config)


def test_pipe_timeout_and_malformed_wrapper_suppress_native_values(monkeypatch):
    def timeout(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, 1, output=SENTINEL, stderr=SENTINEL)

    monkeypatch.setattr("arex_skill_graph.llm_http.subprocess.run", timeout)
    model = transport(http_backend="windows_pipe", retries=0)
    with pytest.raises(RuntimeError) as failure:
        model.complete_text(system="Public", user="Public")
    assert SENTINEL not in str(failure.value)
    assert model.calls[0]["successful"] is False
    assert model.calls[0]["usage"] is None  # Unreported failure usage is unknown, not zero.
    monkeypatch.setattr(
        "arex_skill_graph.llm_http.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=json.dumps([SENTINEL])),
    )
    with pytest.raises(URLError) as failure:
        model._windows_request("https://example.invalid/v1/chat/completions", {})
    assert SENTINEL not in str(failure.value)


def test_incomplete_json_attempt_retains_reported_usage_before_retry(monkeypatch):
    responses = [envelope('{"unfinished":', "length"), envelope('{"ok":true}')]

    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()

    monkeypatch.setattr(
        "arex_skill_graph.llm_http.urlopen",
        lambda *args, **kwargs: Response(json.dumps(responses.pop(0)).encode()),
    )
    monkeypatch.setattr("arex_skill_graph.llm_http.time.sleep", lambda _: None)
    model = transport(retries=1)
    assert model.complete(system="Public", user="Public", response_schema={}) == {"ok": True}
    assert [call["successful"] for call in model.calls] == [False, True]
    assert all(call["usage"]["prompt_tokens"] == 12 for call in model.calls)
    assert len(model.transcripts) == 1
    assert SENTINEL not in json.dumps(model.calls + model.transcripts)


def test_credential_in_service_response_is_rejected_without_persistence(monkeypatch):
    monkeypatch.setattr(
        OpenAICompatibleTransport,
        "_windows_request",
        lambda *args, **kwargs: json.dumps(envelope(SENTINEL)),
    )
    model = transport(http_backend="windows_pipe", retries=0)
    with pytest.raises(RuntimeError):
        model.complete_text(system="Public", user="Public")
    assert not model.transcripts
    assert SENTINEL not in json.dumps(model.calls)
    for base in (
        "https://user:fixture@example.invalid/v1",
        "https://example.invalid/v1?key=fixture",
    ):
        with pytest.raises(ValueError, match="credential-free"):
            OpenAICompatibleTransport(OpenAICompatibleConfig(SENTINEL, base, "fixture-model"))


def test_runtime_credential_wrapper_cleans_environment_even_when_experiment_raises(
    monkeypatch, capsys
):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "runtime_wrapper", root / "experiments/with_runtime_credential.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(
        "sys.stdin",
        io.TextIOWrapper(io.BytesIO((json.dumps({"api_key": SENTINEL}) + "\n").encode())),
    )
    monkeypatch.setattr(
        "sys.argv",
        ["with_runtime_credential.py", str(root / "experiments/review_temporal_history.py")],
    )
    monkeypatch.delenv("AREX_LLM_API_KEY", raising=False)

    def experiment(*args, **kwargs):
        import os

        assert os.environ["AREX_LLM_API_KEY"] == SENTINEL
        raise RuntimeError("synthetic experiment failure")

    monkeypatch.setattr(module.runpy, "run_path", experiment)
    with pytest.raises(RuntimeError, match="synthetic experiment failure"):
        module.main()
    import os

    assert "AREX_LLM_API_KEY" not in os.environ
    output = capsys.readouterr()
    assert SENTINEL not in output.out + output.err


@pytest.mark.parametrize(
    "field",
    [
        "inputs",
        "outputs",
        "preconditions",
        "effects",
        "preserves",
        "oracle",
        "source_ids",
        "evidence_refs",
    ],
)
def test_action_contract_requires_explicit_array_fields(tmp_path, field):
    package, _, _ = make_fixture(tmp_path)
    contract = asdict(package.actions[0])
    del contract[field]
    with pytest.raises(ValueError, match="required array field"):
        ActionContract.from_dict(contract)
    contract[field] = {"a": "single object"}
    with pytest.raises(ValueError, match="must be an array"):
        ActionContract.from_dict(contract)
