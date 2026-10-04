from pathlib import Path

import pytest

from arex_skill_graph.historical_solver_evaluator import restore_evaluation_paths


def test_restore_oracle_paths_preserves_production_and_removes_new_test(tmp_path):
    work, baseline = tmp_path / "work", tmp_path / "base"
    work.mkdir()
    baseline.mkdir()
    (baseline / "test_existing.py").write_text("base assertions")
    (work / "test_existing.py").write_text("solver assertions")
    (work / "test_new.py").write_text("solver added same regression file")
    (work / "checker.py").write_text("solver production repair")
    restore_evaluation_paths(work, baseline, ["test_existing.py", "test_new.py"])
    assert (work / "test_existing.py").read_text() == "base assertions"
    assert not (work / "test_new.py").exists()
    assert (work / "checker.py").read_text() == "solver production repair"
    with pytest.raises(ValueError):
        restore_evaluation_paths(work, baseline, ["../outside.py"])


def test_oracle_restoration_rejects_symlinks(tmp_path):
    work, baseline = tmp_path / "work", tmp_path / "base"
    work.mkdir()
    baseline.mkdir()
    (work / "production.py").write_text("repair")
    (work / "test.py").symlink_to(Path("production.py"))
    with pytest.raises(ValueError):
        restore_evaluation_paths(work, baseline, ["test.py"])
    assert (work / "production.py").read_text() == "repair"


def make_causal_case(tmp_path, monkeypatch, *, fault=None):
    """Run real git patches and pytest assertions through a local test-only tool adapter."""
    import json
    import os
    import shutil
    import subprocess
    import sys
    from types import SimpleNamespace

    import arex_skill_graph.historical_solver_evaluator as module

    root = tmp_path / "source"
    root.mkdir()
    source = "def value():\n    return 0\n\ndef control():\n    return True\n"
    tests = (
        "from service import value, control\n\ndef test_control():\n    assert control() is True\n"
    )
    (root / "service.py").write_text(source)
    (root / "test_regression.py").write_text(tests)
    for argv in (
        ["git", "init", "-q"],
        ["git", "add", "."],
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.test",
            "commit",
            "-qm",
            "base",
        ],
    ):
        subprocess.run(argv, cwd=root, check=True, capture_output=True)
    base_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    (root / "service.py").write_text(source.replace("return 0", "return 1"))
    production_diff = subprocess.check_output(
        ["git", "diff", "--", "service.py"], cwd=root, text=True
    )
    (root / "service.py").write_text(source)
    target = "\ndef test_target():\n    assert value() == 1\n"
    if fault == "nonfailing_base":
        target = target.replace("== 1", "== 0")
    if fault == "missing_test":
        target = ""
    (root / "test_regression.py").write_text(tests + target)
    regression_diff = subprocess.check_output(
        ["git", "diff", "--", "test_regression.py"], cwd=root, text=True
    )
    (root / "test_regression.py").write_text(tests)
    verification = tmp_path / "verification.json"
    report = {
        "identity": {"issue_id": "historical:causal", "base_commit": base_commit},
        "verified_resolution": True,
        "command": [sys.executable, "-m", "pytest", "-q", "test_regression.py"],
        "fail_to_pass": ["test_regression::test_target"],
        "pass_to_pass": ["test_regression::test_control"],
    }
    verification.write_text(json.dumps(report))
    (tmp_path / "historical-diff.json").write_text(
        json.dumps(
            {
                "production_diff": production_diff if fault != "wrong_repair" else "",
                "regression_diff": regression_diff,
                "paths": ["test_regression.py"],
            }
        )
    )
    invocations = []

    class LocalTestTools:
        isolation = "local-test-adapter-no-production-isolation-claim"

        def __init__(self, checkout, *_args, **_kwargs):
            self.checkout = checkout
            self.ordinal = len(invocations) + 1
            invocations.append(self)
            self.runtime_sha256 = "runtime-test-v1"
            if fault == "candidate_runtime_changed" and self.ordinal == 3:
                self.runtime_sha256 = "changed-runtime"

        def preflight(self):
            return True

        def close(self):
            pass

        def run(self, argv, *, stdin=None, timeout=60):
            actual = [
                "--junitxml=" + str(self.checkout / "independent-results.xml")
                if item == "--junitxml=/workspace/independent-results.xml"
                else item
                for item in argv
            ]
            env = {
                **os.environ,
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            result = subprocess.run(
                actual,
                cwd=self.checkout,
                input=stdin,
                capture_output=True,
                timeout=timeout,
                env=env,
            )
            test_run = "--junitxml=/workspace/independent-results.xml" in argv
            return {
                "exit_code": result.returncode,
                "output": (result.stdout + result.stderr).decode(),
                "timed_out": test_run and fault == "timeout",
                "execution_available": not (test_run and fault == "unavailable"),
            }

    monkeypatch.setattr(module, "snapshot_base", lambda _task, work: shutil.copytree(root, work))
    monkeypatch.setattr(module, "make_namespace_tools", LocalTestTools)
    return (
        SimpleNamespace(task_id="historical:causal", base_commit=base_commit),
        verification,
        production_diff,
        invocations,
    )


def test_causal_controls_reproduce_actual_base_and_known_repair(tmp_path, monkeypatch):
    from arex_skill_graph.historical_solver_evaluator import historical_evaluator

    task, verification, repair, calls = make_causal_case(tmp_path, monkeypatch)
    result = historical_evaluator(verification, tmp_path)(task, repair)
    assert len(calls) == 3
    assert result["causal_controls_passed"] is True
    assert result["validated_resolved"] is True
    controls = result["causal_controls"]
    assert controls["base_target_failed"] and controls["base_controls_preserved"]
    assert controls["known_repair_passed"] and controls["same_protocol"]
    assert controls["solver_input_contains_control_results"] is False
    assert result["fail_to_pass_outcomes"] == ["passed"]
    assert result["pass_to_pass_outcomes"] == ["passed"]


@pytest.mark.parametrize(
    "fault",
    [
        "wrong_repair",
        "nonfailing_base",
        "missing_test",
        "timeout",
        "unavailable",
        "candidate_runtime_changed",
    ],
)
def test_inconsistent_causal_controls_exclude_utility_instead_of_failure(
    tmp_path, monkeypatch, fault
):
    from arex_skill_graph.historical_solver_evaluator import historical_evaluator

    task, verification, repair, _ = make_causal_case(tmp_path, monkeypatch, fault=fault)
    result = historical_evaluator(verification, tmp_path)(task, repair)
    assert result["causal_controls_passed"] is False
    assert result["evaluation_completed"] is False
    assert result["benchmark_resolved"] is False
    assert "causal controls" in result["supervision_exclusion_reason"]


def test_controlled_candidate_failure_remains_a_valid_execution_outcome(tmp_path, monkeypatch):
    from arex_skill_graph.historical_solver_evaluator import historical_evaluator

    task, verification, _repair, _ = make_causal_case(tmp_path, monkeypatch)
    result = historical_evaluator(verification, tmp_path)(task, "")
    assert result["causal_controls_passed"] is True
    assert result["evaluation_completed"] is True
    assert result["validated_resolved"] is False
    assert result["fail_to_pass_outcomes"] == ["failed"]
    assert result["pass_to_pass_outcomes"] == ["passed"]
