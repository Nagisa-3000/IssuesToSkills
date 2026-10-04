"""Sealed response replay must preserve the exact original semantic review context."""

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_action_grounding import observed

from arex_skill_graph.action_grounding import review_action_observation
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger

PATH = Path(__file__).resolve().parents[1] / "experiments/prepare_native_overload_edit_cases.py"
SPEC = importlib.util.spec_from_file_location("native_edit_preparation", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def captured_review(tmp_path):
    _package, task, action, record, observations, response = observed(tmp_path)

    class CapturedFixture:
        calls = []
        config = SimpleNamespace(model="synthetic-fixture", max_output_tokens=5000, retries=0)
        request = None

        def complete(self, **request):
            self.request = request
            return response

    transport = CapturedFixture()
    _current, audit = review_action_observation(
        task,
        action,
        record,
        observations,
        transport,
        BudgetLedger(BudgetCaps(history_tokens=200000, model_tokens=1000000)),
    )
    transcript = {**transport.request, "response": response}
    return task, action, record, observations, transcript, json.loads(json.dumps(audit))


def test_exact_accepted_review_reapplication_is_not_a_new_model_review(tmp_path):
    args = captured_review(tmp_path)
    current, audit = MODULE.exact_reapplication(*args)
    current.verify()
    assert current.port_values
    assert audit["new_actual_model_calls"] == 0
    assert audit["new_independent_review"] is False
    assert audit["repair_success_established"] is False


@pytest.mark.parametrize(
    "mutation", ["system", "current_source", "schema", "response", "accepted_record"]
)
def test_reapplication_rejects_changed_prompt_response_or_verdict(tmp_path, mutation):
    task, action, record, observations, transcript, accepted = captured_review(tmp_path)
    if mutation == "system":
        transcript["system"] += " Altered instruction."
    elif mutation == "current_source":
        payload = json.loads(transcript["user"])
        payload["current_evidence"][0]["observation"] = "Invented context"
        transcript["user"] = json.dumps(payload)
    elif mutation == "schema":
        transcript["response_schema"] = {"type": "string"}
    elif mutation == "response":
        transcript["response"]["checks"][0]["rationale"] = "Altered semantic review"
    else:
        accepted["workspace_execution_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="reapplication"):
        MODULE.exact_reapplication(task, action, record, observations, transcript, accepted)


def test_native_cli_preserves_rejected_grounding_and_does_not_run_solver(tmp_path, monkeypatch):
    from dataclasses import dataclass
    from adaptive_fixture import make_fixture

    cli_path = PATH.with_name("eval_native_action_observation.py")
    spec = importlib.util.spec_from_file_location("native_action_cli_fixture", cli_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    package, task, _policy = make_fixture(tmp_path, pattern=False)
    refs = tmp_path / "references.json"
    refs.write_text(json.dumps({"references": [package.reference]}))
    task_path = tmp_path / "task.json"
    task_path.write_text(json.dumps(task.to_dict()))
    output = tmp_path / "attempt"

    @dataclass(frozen=True)
    class Config:
        model: str = "synthetic-fixture"
        api_key: str = "synthetic-private-value"
        max_output_tokens: int = 4000
        timeout_seconds: int = 180
        stream_responses: bool = True
        retries: int = 0

    class RejectedGrounding:
        config = Config()
        calls = []
        transcripts = []

        def complete(self, **request):
            self.calls.append({"successful": True, "response_id": "fixture-response"})
            self.transcripts.append({"response_id": "fixture-response", "response": {"checks": []}})
            raise ValueError("Invalid fixture response synthetic-private-value")

    monkeypatch.setattr(cli, "transport_from_args", lambda _args: RejectedGrounding())
    monkeypatch.setattr(
        cli,
        "new_ledger",
        lambda **_kwargs: BudgetLedger(BudgetCaps(history_tokens=200000, model_tokens=1000000)),
    )
    monkeypatch.setattr(
        cli,
        "AdaptiveSolver",
        lambda *_args, **_kwargs: pytest.fail("Rejected grounding must not start a solver"),
    )
    code = cli.main(
        [
            "--references",
            str(refs),
            "--task-context",
            str(task_path),
            "--output-dir",
            str(output),
            "--action-id",
            package.actions[0].id,
            "--cutoff",
            "2024-01-01T00:00:00Z",
            "--dependency-root",
            str(tmp_path),
            "--model",
            "synthetic-fixture",
            "--base-url",
            "https://example.invalid/v1",
            "--ground-current-action",
        ]
    )
    assert code == 1
    failure = json.loads((output / "exercise-failure.json").read_text())
    assert failure["model_calls"] == 1
    assert failure["actual_action_records"] == 0
    assert "synthetic-private-value" not in failure["failure_reason"]
    assert json.loads((output / "grounding-transcript.json").read_text())
    assert not (output / "trajectory.json").exists()
