"""Original-input acceptance cannot reuse a native-parent or weakened oracle."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from arex_skill_graph.historical_replay_controls import (
    freeze_replay_cohort,
    project_replay_production_diff,
    verify_replay_controls,
)
from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.original_query_evaluator import (
    load_original_replay_authority,
    original_query_evaluator,
)
from arex_skill_graph.task_context import TaskContext

MODULE = "arex_skill_graph.original_query_evaluator"


@pytest.fixture
def authority(tmp_path, monkeypatch):
    monkeypatch.setattr(TaskContext, "verify", lambda self: None)
    task = TaskContext.from_dict(
        {
            "task_id": "example/project:1",
            "repository": "example/project",
            "base_commit": "a" * 40,
            "root": str(tmp_path / "public"),
            "input_available_at": "2020-01-01T00:00:00Z",
            "public_problem": "an async overload is rejected",
            "anchors": [
                {
                    "id": "current:issue",
                    "kind": "public_issue",
                    "base_commit": "a" * 40,
                    "available_at": "2020-01-01T00:00:00Z",
                    "observation": "an async overload is rejected",
                    "path": "",
                    "sha256": "",
                    "exit_code": None,
                }
            ],
        }
    )
    native = {
        "schema": "historical-causal-verification-v1",
        "verified_resolution": True,
        "identity": {"issue_id": task.task_id, "base_commit": "b" * 40},
        "command": ["python3", "-m", "pytest", "tests/test_bug.py", "-q"],
        "fail_to_pass": ["bug"],
        "pass_to_pass": ["good"],
    }
    runtime = "c" * 64
    original, before, after = (
        {"good": "passed"},
        {"good": "passed", "bug": "failed"},
        {"good": "passed", "bug": "passed"},
    )
    phases = {
        name: {
            "setup_complete": True,
            "runtime_sha256": runtime,
            "focused_test_run": {"exit_code": rc, "timed_out": False},
            "observations": obs,
        }
        for name, obs, rc in (
            ("original_base", original, 0),
            ("base_with_regression", before, 1),
            ("known_repair", after, 0),
        )
    }
    cohort = freeze_replay_cohort(task, native, original, before)
    root = tmp_path / "private-controls"
    verification = tmp_path / "native" / "verification.json"
    diff = {
        "production_diff": "production",
        "regression_diff": "oracle",
        "paths": ["tests/test_bug.py"],
    }
    write_json(verification, native)
    write_json(verification.parent / "historical-diff.json", diff)
    for name, phase in phases.items():
        write_json(root / (name + ".json"), phase)
    completion = verify_replay_controls(
        cohort, phases, source_files_unchanged=True, task_input_unchanged=True
    )
    production, projection = project_replay_production_diff(diff["production_diff"])
    completion.update(
        native_verification_file_sha256=hashlib.sha256(verification.read_bytes()).hexdigest(),
        historical_diff_file_sha256=hashlib.sha256(
            (verification.parent / "historical-diff.json").read_bytes()
        ).hexdigest(),
        raw_known_repair_file_sha256=hashlib.sha256(diff["production_diff"].encode()).hexdigest(),
        controlled_known_repair_file_sha256=hashlib.sha256(production.encode()).hexdigest(),
        known_repair_adapted=False,
        production_projection=projection,
        historical_regression_assertions_unchanged=True,
    )
    write_json(root / "cohort.json", cohort)
    write_json(root / "completion.json", completion)
    review_input = {
        "task_identity": cohort["task_identity"],
        "public_problem": task.public_problem,
        "frozen_current_cohort": cohort,
        "mechanical_controls": completion,
        "native_regression_diff": diff["regression_diff"],
        "evaluator_known_production_diff": diff["production_diff"],
        "phase_receipts": phases,
    }
    write_json(root / "input.json", review_input)
    write_json(
        root / "calls.json",
        [
            {
                "successful": True,
                "model": "synthetic-unit-reviewer",
                "purpose": "unit fixture only; not a model call",
            }
        ],
    )
    review = {
        "review_input_sha256": fingerprint(review_input),
        "reviewer_model": "synthetic-unit-reviewer",
        "schema": "original-query-replay-independent-review-v1",
        "task_identity": cohort["task_identity"],
        "control_completion_sha256": fingerprint(completion),
        "cohort_sha256": cohort["cohort_sha256"],
        "accepted_limited_replay": True,
        "mechanism_alignment": "PASS",
        "oracle_fidelity": "PASS",
        "regression_coverage": "PASS",
        "rationale": "Synthetic unit fixture only.",
        "evidence_refs": ["native_regression_diff"],
        "limitations": ["Synthetic unit fixture; no actual repair result."],
        "actual_model_calls": 1,
        "formal_SWE_run": False,
    }
    write_json(root / "review.json", review)
    return task, verification, root, runtime


def load(authority):
    task, verification, root, _ = authority
    return load_original_replay_authority(task, verification, root, root / "review.json")


def test_different_native_parent_does_not_replace_original_input(authority):
    result = load(authority)
    assert result.cohort["native_identity"]["base_commit"] != authority[0].base_commit
    assert result.cohort["task_identity"]["base_commit"] == authority[0].base_commit
    assert result.independently_reviewed
    assert result.completion["complete_replay_acceptance"] is False


@pytest.mark.parametrize("name", ["cohort", "completion", "known_repair", "verification", "diff"])
def test_tampered_authority_cannot_enter_submission_acceptance(authority, name):
    _, verification, root, _ = authority
    path = {
        "cohort": root / "cohort.json",
        "completion": root / "completion.json",
        "known_repair": root / "known_repair.json",
        "verification": verification,
        "diff": verification.parent / "historical-diff.json",
    }[name]
    value = json.loads(path.read_text())
    if name == "cohort":
        value["current_pass_to_pass"] = []
    elif name == "completion":
        value["mechanical_controls_passed"] = False
    elif name == "known_repair":
        value["observations"]["good"] = "skipped"
    elif name == "verification":
        value["identity"]["base_commit"] = "d" * 40
    else:
        value["regression_diff"] = "weakened oracle"
    write_json(path, value)
    with pytest.raises(ValueError):
        load(authority)


@pytest.mark.parametrize(
    "field,value",
    [
        ("control_completion_sha256", "0" * 64),
        ("cohort_sha256", "0" * 64),
        ("oracle_fidelity", "UNKNOWN"),
        ("actual_model_calls", 0),
        ("evidence_refs", []),
        ("limitations", []),
    ],
)
def test_missing_or_mismatched_review_never_authorizes_utility(authority, field, value):
    root = authority[2]
    review = json.loads((root / "review.json").read_text())
    review[field] = value
    write_json(root / "review.json", review)
    with pytest.raises(ValueError, match="review"):
        load(authority)


def install_runtime(authority, monkeypatch, *, outcomes=None, runtime=None, rc=0, timed_out=False):
    _, _, _, expected_runtime = authority
    state = {"tools_created": 0, "oracle_before_restore": None, "closed": False}
    observed = {"bug": "passed", "good": "passed"} if outcomes is None else outcomes

    def snapshot(task, work):
        work.mkdir()
        (work / "tests").mkdir()
        (work / "tests/test_bug.py").write_text("original assertion")
        (work / "module.py").write_text("original implementation")

    class Tools:
        runtime_sha256 = runtime or expected_runtime
        isolation = "synthetic-unit-runtime"

        def __init__(self, work):
            self.work = work
            state["tools_created"] += 1

        def preflight(self):
            return None

        def close(self):
            state["closed"] = True

        def run(self, argv, **kwargs):
            if argv[:2] == ["git", "apply"]:
                if kwargs["stdin"] == b"submission":
                    (self.work / "module.py").write_text("new implementation")
                    (self.work / "tests/test_bug.py").write_text("weakened assertion")
                if kwargs["stdin"] == b"oracle":
                    state["oracle_before_restore"] = (self.work / "tests/test_bug.py").read_text()
                    assert (self.work / "module.py").read_text() == "new implementation"
                return {"exit_code": 0}
            return {"exit_code": rc, "execution_available": True, "timed_out": timed_out}

    monkeypatch.setattr(MODULE + ".snapshot_base", snapshot)
    monkeypatch.setattr(MODULE + ".make_namespace_tools", lambda work, *a, **k: Tools(work))
    monkeypatch.setattr(MODULE + ".junit_observations", lambda path: deepcopy(observed))
    return state


def evaluate(authority, *, reviewed=True):
    task, verification, root, _ = authority
    return original_query_evaluator(
        verification,
        Path("runtime"),
        root,
        independent_review_path=root / "review.json" if reviewed else None,
    )(task, "submission")


def test_solver_cannot_weaken_independent_assertions(authority, monkeypatch):
    state = install_runtime(authority, monkeypatch)
    result = evaluate(authority)
    assert state["oracle_before_restore"] == "original assertion"
    assert state["closed"]
    assert result["validated_resolved"]
    assert result["evaluation_completed"]
    assert result["whole_project_regression_checked"] is False
    assert result["formal_SWE_run"] is False


def test_missing_review_keeps_pass_only_as_mechanical_observation(authority, monkeypatch):
    install_runtime(authority, monkeypatch)
    result = evaluate(authority, reviewed=False)
    assert result["mechanically_resolved"]
    assert not result["validated_resolved"]
    assert not result["evaluation_completed"]
    assert not result["causal_controls_passed"]


@pytest.mark.parametrize(
    "outcomes,rc,timed_out",
    [
        ({"good": "passed"}, 0, False),
        ({"bug": "passed", "good": "skipped"}, 0, False),
        ({"bug": "passed", "good": "passed", "extra": "passed"}, 0, False),
        ({"bug": "passed", "good": "passed"}, 2, False),
        ({"bug": "passed", "good": "passed"}, 0, True),
    ],
)
def test_collection_or_execution_gap_is_excluded_not_a_candidate_loss(
    authority, monkeypatch, outcomes, rc, timed_out
):
    install_runtime(authority, monkeypatch, outcomes=outcomes, rc=rc, timed_out=timed_out)
    result = evaluate(authority)
    assert not result["evaluation_completed"]
    assert not result["validated_resolved"]
    assert result["supervision_exclusion_reason"]


def test_actual_functional_failure_can_be_a_qualified_outcome(authority, monkeypatch):
    install_runtime(authority, monkeypatch, outcomes={"bug": "failed", "good": "passed"}, rc=1)
    result = evaluate(authority)
    assert result["evaluation_completed"]
    assert result["causal_controls_passed"]
    assert not result["validated_resolved"]
    assert result["fail_to_pass_outcomes"] == ["failed"]


def test_runtime_mismatch_excludes_even_passing_tests(authority, monkeypatch):
    state = install_runtime(authority, monkeypatch, runtime="e" * 64)
    result = evaluate(authority)
    assert not result["evaluation_completed"]
    assert result["supervision_exclusion_reason"] == "original replay runtime mismatch"
    assert state["closed"]


def test_files_remain_pinned_after_loading(authority):
    result = load(authority)
    verification = authority[1]
    verification.write_text(verification.read_text() + " ")
    with pytest.raises(ValueError, match="changed during"):
        result.verify_unchanged(authority[0])


@pytest.mark.parametrize("artifact", ["input.json", "calls.json"])
def test_review_must_match_the_exact_input_and_successful_model_call(authority, artifact):
    root = authority[2]
    value = json.loads((root / artifact).read_text())
    if artifact == "input.json":
        value["public_problem"] = "a different problem"
    else:
        value[0]["successful"] = False
    write_json(root / artifact, value)
    with pytest.raises(ValueError, match="review"):
        load(authority)
