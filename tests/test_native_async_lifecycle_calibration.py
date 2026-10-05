"""Fail-closed calibration checks for real native async lifecycle fixtures."""

import copy
import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments/prepare_native_async_lifecycle_functional_cases.py"
)
spec = importlib.util.spec_from_file_location("native_async_lifecycle_preparer", MODULE_PATH)
preparer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preparer)


def control_observations():
    rows = []
    for ident in ("q0", "q1", "q2"):
        cases = {
            name: {"diagnostics": []} for name in preparer.QUIET_CASES | preparer.POSITIVE_CASES
        }
        for name in preparer.POSITIVE_CASES:
            cases[name]["diagnostics"] = [
                {
                    "symbol": "redefined-variable-type",
                    "line": 3,
                    "column": 4,
                    "obj": "current_scope",
                    "message": "Redefinition of reused type from list to dict",
                }
            ]
        if ident in ("q0", "q2"):
            for name in ("separate_async_functions", "separate_async_methods"):
                cases[name]["diagnostics"] = [
                    {
                        "symbol": "redefined-variable-type",
                        "line": 7,
                        "column": 4,
                        "obj": "second",
                        "message": "Redefinition of reused type from list to dict",
                    }
                ]
        probe = {
            "schema": "public-async-lifecycle-observation-v1",
            "exception": None,
            "cases": cases,
            "preservation": {"unchanged": True},
            "hooks": {
                name: {"present": ident != "q0", "same_as_sync": ident != "q0"}
                for name in ("visit_asyncfunctiondef", "leave_asyncfunctiondef")
            },
            "matches_current_public_behavior_spec": ident == "q1",
        }
        rows.append(
            {
                "case_id": ident,
                "scope": "public-scope-counterparts",
                "exit_code": 0 if ident == "q1" else 1,
                "timed_out": False,
                "runtime_sha256": preparer.RUNTIME_SHA256,
                "output": json.dumps(probe),
            }
        )
        rows.append(
            {
                "case_id": ident,
                "scope": "affected-public-suite",
                "exit_code": 1 if ident == "q2" else 0,
                "timed_out": False,
                "runtime_sha256": preparer.RUNTIME_SHA256,
                "output": "",
            }
        )
    return rows


def mutate_probe(rows, ident, mutation):
    row = next(
        x for x in rows if x["case_id"] == ident and x["scope"] == "public-scope-counterparts"
    )
    probe = json.loads(row["output"])
    mutation(probe)
    row["output"] = json.dumps(probe)


def test_calibration_records_real_failure_controls_without_skill_execution_claim():
    summary = preparer.validate_calibration(control_observations())
    assert summary["actually_executed_cases"] == ["q0", "q1", "q2"]
    assert summary["public_scope_cases_per_probe"] == 9
    assert summary["actual_model_calls"] == 0
    assert summary["authored_Action_executed"] is False
    assert summary["formal_SWE_runs"] == 0


@pytest.mark.parametrize(
    "defect", ["within_async_function", "within_sync_function", "within_class", "within_module"]
)
def test_calibration_rejects_lost_positive_diagnostic(defect):
    rows = control_observations()
    mutate_probe(rows, "q1", lambda p: p["cases"][defect].update(diagnostics=[]))
    with pytest.raises(ValueError, match="positive diagnostic preservation"):
        preparer.validate_calibration(rows)


def test_dispatch_fault_cannot_masquerade_as_missing_hook_control():
    rows = control_observations()
    mutate_probe(rows, "q2", lambda p: p["hooks"]["leave_asyncfunctiondef"].update(present=False))
    with pytest.raises(ValueError, match="retain both hook"):
        preparer.validate_calibration(rows)


def test_fixed_source_must_satisfy_complete_public_behavior():
    rows = control_observations()
    mutate_probe(rows, "q1", lambda p: p.update(matches_current_public_behavior_spec=False))
    with pytest.raises(ValueError, match="complete public behavior"):
        preparer.validate_calibration(rows)


@pytest.mark.parametrize(
    "change",
    [
        {"exit_code": None},
        {"timed_out": True},
        {"output": "{}"},
        {"runtime_sha256": "a" * 64},
    ],
)
def test_unavailable_incomplete_or_changed_runtime_is_not_calibration(change):
    rows = control_observations()
    rows[0].update(change)
    with pytest.raises(ValueError):
        preparer.validate_calibration(rows)


def test_execution_unavailable_case_must_not_be_counted_as_observed():
    rows = control_observations()
    extra = copy.deepcopy(rows[0])
    extra["case_id"] = "q3"
    rows.append(extra)
    with pytest.raises(ValueError, match="three executable controls"):
        preparer.validate_calibration(rows)


def test_failed_dispatcher_regression_is_required_and_not_overwritten():
    rows = control_observations()
    next(r for r in rows if r["case_id"] == "q2" and r["scope"] == "affected-public-suite")[
        "exit_code"
    ] = 0
    with pytest.raises(ValueError, match="passing and failing controls"):
        preparer.validate_calibration(rows)


def test_probe_exception_and_source_edit_block_calibration():
    for mutation in (
        lambda p: p.update(exception={"type": "RuntimeError"}),
        lambda p: p["preservation"].update(unchanged=False),
    ):
        rows = control_observations()
        mutate_probe(rows, "q0", mutation)
        with pytest.raises(ValueError):
            preparer.validate_calibration(rows)


def test_public_pin_retains_ignored_diagnostic_expectations(tmp_path):
    import subprocess

    (tmp_path / ".gitignore").write_text("*.txt\n")
    (tmp_path / "expected-diagnostics.txt").write_text("retained public expectations\n")
    head = preparer.pin_public_fixture(tmp_path)
    tracked = subprocess.check_output(
        ["git", "-C", str(tmp_path), "ls-tree", "-r", "--name-only", head], text=True
    ).splitlines()
    assert "expected-diagnostics.txt" in tracked
    exported = tmp_path.parent / "public-export"
    preparer.export(tmp_path, head, exported)
    assert (exported / "expected-diagnostics.txt").read_text() == "retained public expectations\n"
    assert not (exported / ".git").exists()
