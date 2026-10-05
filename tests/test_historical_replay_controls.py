"""Replay gates tested with the actual published Pyflakes #574 control receipts."""

import importlib.util
import json
import os
from copy import deepcopy
from pathlib import Path

import pytest

from arex_skill_graph.historical_replay_controls import (
    freeze_replay_cohort,
    replay_assertion_changes,
    replay_task_identity,
    verify_replay_controls,
)
from arex_skill_graph.history_census import fingerprint
from arex_skill_graph.task_context import TaskContext

REPO = Path(__file__).resolve().parents[1]
CONTROL = REPO / "analysis/controls/pyflakes-574-original-current-source-20261006-v2"
QUERY = REPO / "analysis/history-query-recovery/pre2021-original-inputs-20261006-v1"


@pytest.fixture
def real_controls():
    task = TaskContext.from_dict(
        json.loads((QUERY / "cases/PyCQA__pyflakes-574/task.json").read_text())
    )
    spec = json.loads((CONTROL / "control-spec.json").read_text())
    phases = {
        "original_base": json.loads((CONTROL / "original_base.json").read_text()),
        "base_with_regression": json.loads(
            (CONTROL / "base_with_unchanged_regressions.json").read_text()
        ),
        "known_repair": json.loads(
            (CONTROL / "evaluator_current_api_known_repair.json").read_text()
        ),
    }
    # Reconstruct only the native target inventory used by the shipped control
    # spec; this fixture does not create a new native verification artifact.
    historical = {
        "schema": "historical-causal-verification-v1",
        "verified_resolution": True,
        "identity": {"issue_id": task.task_id, "base_commit": "e" * 40},
        "command": phases["original_base"]["focused_test_run"]["argv"][:-1],
        "fail_to_pass": spec["fail_to_pass"],
        "pass_to_pass": sorted(
            set(spec["original_current_tests"]) | set(spec["missing_historical_pass_to_pass"])
        ),
    }
    cohort = freeze_replay_cohort(
        task,
        historical,
        phases["original_base"]["observations"],
        phases["base_with_regression"]["observations"],
    )
    return task, historical, cohort, phases


def verify(cohort, phases, **kwargs):
    return verify_replay_controls(
        cohort,
        phases,
        source_files_unchanged=kwargs.get("source_files_unchanged", True),
        task_input_unchanged=kwargs.get("task_input_unchanged", True),
    )


def test_current_cohort_keeps_original_and_added_controls_without_promoting(real_controls):
    task, historical, cohort, phases = real_controls
    before = deepcopy(historical)
    result = verify(cohort, phases)
    assert result["mechanical_controls_passed"]
    assert cohort["task_identity"] == replay_task_identity(task)
    assert len(cohort["original_current_pass_to_pass"]) == 37
    assert len(cohort["current_pass_to_pass"]) == 39
    assert len(cohort["current_fail_to_pass"]) == 2
    assert len(cohort["expected_collected_tests"]) == 41
    assert len(cohort["missing_native_pass_to_pass"]) == 3
    assert historical == before
    assert result["complete_replay_acceptance"] is False
    assert result["independent_review_complete"] is False
    assert result["utility_labels_created"] == 0
    assert result["actor_may_read_known_repair"] is False


def test_actual_raw_copy_nameerror_cannot_qualify_as_candidate_failure(real_controls):
    _, _, cohort, phases = real_controls
    phases["known_repair"] = json.loads((CONTROL / "raw-historical/known_repair.json").read_text())
    result = verify(cohort, phases)
    assert not result["mechanical_controls_passed"]
    assert result["utility_labels_created"] == 0
    assert any(
        check["name"] == "current_failure_transition" and check["status"] == "FAIL"
        for check in result["checks"]
    )


@pytest.mark.parametrize("mutation", ["drop", "rename", "skip", "fail", "add"])
def test_known_repair_cannot_change_or_weaken_the_frozen_cohort(real_controls, mutation):
    _, _, cohort, phases = real_controls
    observed = phases["known_repair"]["observations"]
    target = cohort["original_current_pass_to_pass"][0]
    if mutation == "drop":
        observed.pop(target)
    elif mutation == "rename":
        observed[target + "_renamed"] = observed.pop(target)
    elif mutation == "skip":
        observed[target] = "skipped"
    elif mutation == "fail":
        observed[target] = "failed"
    else:
        observed["unregistered.extra_control"] = "passed"
    # A successful exit alone is insufficient.
    assert phases["known_repair"]["focused_test_run"]["exit_code"] == 0
    assert not verify(cohort, phases)["mechanical_controls_passed"]


def test_different_runtime_excludes_utility_despite_passing_tests(real_controls):
    _, _, cohort, phases = real_controls
    phases["known_repair"]["runtime_sha256"] = "a" * 64
    result = verify(cohort, phases)
    assert not result["mechanical_controls_passed"]
    assert result["utility_labels_created"] == 0
    assert any(
        check["name"] == "same_actual_runtime" and check["status"] == "FAIL"
        for check in result["checks"]
    )


@pytest.mark.parametrize("field", ["setup", "availability", "timeout", "collection"])
def test_unavailable_execution_is_unknown_and_never_a_skill_loss(real_controls, field):
    _, _, cohort, phases = real_controls
    repaired = phases["known_repair"]
    if field == "setup":
        repaired["setup_complete"] = False
    elif field == "availability":
        repaired["focused_test_run"]["execution_available"] = False
    elif field == "timeout":
        repaired["focused_test_run"]["timed_out"] = True
    else:
        repaired["observations"] = {}
    result = verify(cohort, phases)
    assert result["control_status"] == "UNKNOWN"
    assert result["mechanical_controls_passed"] is False
    assert result["utility_labels_created"] == 0


def test_original_release_that_does_not_reproduce_native_target_is_unqualified(real_controls):
    task, historical, _, phases = real_controls
    for target in historical["fail_to_pass"]:
        phases["base_with_regression"]["observations"][target] = "passed"
    phases["base_with_regression"]["focused_test_run"]["exit_code"] = 0
    cohort = freeze_replay_cohort(
        task,
        historical,
        phases["original_base"]["observations"],
        phases["base_with_regression"]["observations"],
    )
    result = verify(cohort, phases)
    assert not result["mechanical_controls_passed"]
    assert cohort["native_fail_to_pass_not_failed"] == historical["fail_to_pass"]
    assert result["utility_labels_created"] == 0


def test_frozen_outcomes_and_source_inputs_cannot_be_silently_changed(real_controls):
    _, _, cohort, phases = real_controls
    modified = deepcopy(cohort)
    modified["current_pass_to_pass"] = []
    with pytest.raises(ValueError, match="changed after freezing"):
        verify(modified, phases)
    assert not verify(cohort, phases, source_files_unchanged=False)["mechanical_controls_passed"]
    assert not verify(cohort, phases, task_input_unchanged=False)["mechanical_controls_passed"]
    target = cohort["original_current_pass_to_pass"][0]
    phases["original_base"]["observations"][target] = "skipped"
    assert not verify(cohort, phases)["mechanical_controls_passed"]


@pytest.mark.parametrize("invalid", ["identity", "qualification", "schema", "duplicate"])
def test_native_evidence_identity_and_targets_are_required(real_controls, invalid):
    task, historical, _, phases = real_controls
    if invalid == "identity":
        historical["identity"]["issue_id"] = "PyCQA/pyflakes:575"
    elif invalid == "qualification":
        historical["verified_resolution"] = False
    elif invalid == "schema":
        historical["schema"] = "unqualified-replay-fixture"
    else:
        historical["fail_to_pass"].append(historical["fail_to_pass"][0])
    with pytest.raises(ValueError):
        freeze_replay_cohort(
            task,
            historical,
            phases["original_base"]["observations"],
            phases["base_with_regression"]["observations"],
        )


def test_every_registered_query_and_input_gap_remains_in_cli_denominator(
    tmp_path, monkeypatch, real_controls
):
    task, _, _, _ = real_controls
    specification = importlib.util.spec_from_file_location(
        "replay_control_cli", REPO / "experiments/qualify_original_release_controls.py"
    )
    cli = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(cli)
    queried = []
    queries = [
        {
            "task": task.to_dict(),
            "fix_id": "PyCQA/pyflakes:pr:576",
        }
    ]
    register = {
        "queries_sha256": fingerprint(queries),
        "query_count": 1,
        "selected_targets": 2,
        "audits": [
            {"query_id": task.task_id},
            {"query_id": "PyCQA/pyflakes:419", "status": "original_input_unrecovered"},
        ],
    }
    inventory = {
        "results": [
            {
                "issue_id": task.task_id,
                "fix_id": "PyCQA/pyflakes:pr:576",
                "verified_resolution": True,
                "verification_path": "/nonexistent/native-control.json",
            }
        ]
    }

    def unavailable(task, *_args):
        queried.append(task.task_id)
        raise OSError("isolated runtime unavailable")

    monkeypatch.setattr(cli, "run_original_query_controls", unavailable)
    for key in ("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0"):
        monkeypatch.setenv(key, os.environ.get(key, ""))
    inputs = {
        "queries": queries,
        "query-register": register,
        "verifications": inventory,
        "runtime-map": {"PyCQA/pyflakes": "/nonexistent/runtime"},
    }
    argv = []
    for key, value in inputs.items():
        path = tmp_path / (key + ".json")
        path.write_text(json.dumps(value))
        argv.extend(["--" + key, str(path)])
    output = tmp_path / "control-output"
    assert cli.main([*argv, "--output-dir", str(output)]) == 0
    completion = json.loads((output / "completion.json").read_text())
    assert queried == [task.task_id]
    assert completion["completed_targets"] == 2
    assert len(completion["results"]) == 2
    assert completion["new_utility_labels"] == 0
    assert completion["mechanical_controls_passed"] == 0
    assert {row["status"] for row in completion["results"]} == {
        "original_input_unrecovered",
        "execution_or_input_gap",
    }
    with pytest.raises(ValueError, match="preserve existing"):
        cli.main([*argv, "--output-dir", str(output)])


def test_runtime_identity_must_be_a_real_hash_and_missing_source_proof_is_unknown(real_controls):
    _, _, cohort, phases = real_controls
    for row in phases.values():
        row["runtime_sha256"] = "z" * 64
    assert not verify(cohort, phases)["mechanical_controls_passed"]
    result = verify(cohort, phases, source_files_unchanged=None)
    assert result["control_status"] == "UNKNOWN"
    assert result["utility_labels_created"] == 0


def test_expanded_existing_case_can_be_f2p_with_a_changed_assertion_witness(real_controls):
    task, historical, _, phases = real_controls
    target = next(iter(phases["original_base"]["observations"]))
    historical["fail_to_pass"].append(target)
    phases["base_with_regression"]["observations"][target] = "failed"
    method = target.split("::")[-1].split("[")[0]
    before = f"class TestTypeAnnotations:\n    def {method}(self):\n        self.assertEqual(1, 1)\n".encode()
    after = f"class TestTypeAnnotations:\n    def {method}(self):\n        self.assertEqual(1, 1)\n        self.assertEqual(new_case(), 0)\n".encode()
    changes = replay_assertion_changes(
        {"pyflakes/test/test_type_annotations.py": before},
        {"pyflakes/test/test_type_annotations.py": after},
        [target],
    )
    assert target in changes
    without = freeze_replay_cohort(
        task,
        historical,
        phases["original_base"]["observations"],
        phases["base_with_regression"]["observations"],
    )
    assert not verify(without, phases)["mechanical_controls_passed"]
    with_proof = freeze_replay_cohort(
        task,
        historical,
        phases["original_base"]["observations"],
        phases["base_with_regression"]["observations"],
        assertion_changes=changes,
    )
    assert target in with_proof["native_target_identity_overlaps"]
    assert target in with_proof["current_fail_to_pass"]
    assert target not in with_proof["original_current_pass_to_pass"]
    assert verify(with_proof, phases)["mechanical_controls_passed"]
    assert verify(with_proof, phases)["utility_labels_created"] == 0


def test_witness_requires_changed_case_or_exact_fixture_not_an_unrelated_file():
    target = "tests.test_functional::test_functional[inconsistent_returns]"
    assert not replay_assertion_changes(
        {"tests/functional/unrelated.py": b"old"},
        {"tests/functional/unrelated.py": b"new"},
        [target],
    )
    proof = replay_assertion_changes(
        {"tests/functional/inconsistent_returns.py": b"old"},
        {"tests/functional/inconsistent_returns.py": b"new"},
        [target],
    )
    assert proof[target]["kind"] == "exact_parameterized_fixture"
    method = "module.TestOne::test_example"
    assert not replay_assertion_changes(
        {"tests/test_examples.py": b"class TestOther:\n def test_example(self): pass\n"},
        {"tests/test_examples.py": b"class TestOther:\n def test_example(self): assert False\n"},
        [method],
    )
