"""Independent historical regression acceptance, invoked after solver termination."""

from __future__ import annotations

import hashlib
import json
import tempfile
from contextlib import ExitStack
from pathlib import Path

from .adaptive_budget import BudgetCaps, BudgetLedger
from .adaptive_runner import make_namespace_tools, snapshot_base
from .history_census import fingerprint
from .history_verification import junit_observations
from .skill_packages import _resolve


def restore_evaluation_paths(work, baseline, paths):
    """Restore only oracle-owned paths before applying independent assertions."""
    for relative in paths:
        _resolve(work, relative)
        _resolve(baseline, relative)
        target, source = Path(work) / relative, Path(baseline) / relative
        for root, candidate in ((Path(work), target), (Path(baseline), source)):
            if any(
                p.is_symlink() for p in [candidate, *candidate.parents] if p.is_relative_to(root)
            ):
                raise ValueError("evaluation test path must be a regular file")
        if source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        elif target.is_file():
            target.unlink()
        elif target.exists():
            raise ValueError("evaluation test path is not a regular file")


def historical_evaluator(
    verification_path,
    dependency_root,
    *,
    sandbox_backend="namespace-bind",
    require_causal_controls=True,
):
    def evaluate_raw(task, patch):
        # The verification record and hidden assertions are deliberately loaded
        # here, after AdaptiveSolver's last possible model/public tool request.
        path = Path(verification_path)
        report = json.loads(path.read_text())
        diff = json.loads((path.parent / "historical-diff.json").read_text())
        if (
            report["identity"]["issue_id"] != task.task_id
            or report["identity"]["base_commit"] != task.base_commit
            or report.get("verified_resolution") is not True
        ):
            raise ValueError("historical solver evaluator identity/qualification mismatch")
        spec_hash = fingerprint(
            {
                "identity": report["identity"],
                "command": report["command"],
                "fail_to_pass": report["fail_to_pass"],
                "pass_to_pass": report["pass_to_pass"],
                "test_assertions_sha256": hashlib.sha256(
                    diff["regression_diff"].encode()
                ).hexdigest(),
                "test_restore_policy": "independent-regression-paths-from-base-v1",
            }
        )
        with (
            tempfile.TemporaryDirectory(prefix="arex-history-acceptance-") as scratch,
            ExitStack() as cleanup,
        ):
            work = Path(scratch) / "evaluation"
            snapshot_base(task, work)
            baseline = Path(scratch) / "test-base"
            baseline.mkdir()
            for relative in diff["paths"]:
                source = _resolve(work, relative)
                if source.is_file() and not source.is_symlink():
                    copied = _resolve(baseline, relative)
                    copied.parent.mkdir(parents=True, exist_ok=True)
                    copied.write_bytes(source.read_bytes())
            tools = make_namespace_tools(
                work,
                BudgetLedger(BudgetCaps(seconds=600)),
                dependency_root,
                backend=sandbox_backend,
            )
            cleanup.callback(tools.close)
            tools.preflight()
            for phase, applied_patch in (
                ("submission", patch),
                ("independent-tests", diff["regression_diff"]),
            ):
                if phase == "independent-tests":
                    restore_evaluation_paths(work, baseline, diff["paths"])
                if applied_patch:
                    applied = tools.run(
                        ["git", "apply", "--whitespace=nowarn", "-"], stdin=applied_patch.encode()
                    )
                    if applied["exit_code"]:
                        return {
                            "benchmark_resolved": False,
                            "validated_resolved": False,
                            "reason": "submitted or independent regression patch did not apply",
                            "evaluation_completed": False,
                            "setup_failure_phase": phase,
                            "isolation": tools.isolation,
                            "runtime_sha256": tools.runtime_sha256,
                            "evaluator_version": "historical-regression-acceptance-v3",
                            "evaluation_spec_sha256": spec_hash,
                            "regression_exit_codes": [],
                        }
            run = tools.run(
                [*report["command"], "--junitxml=/workspace/independent-results.xml"], timeout=120
            )
            observed = junit_observations(work / "independent-results.xml")
            f2p = report["fail_to_pass"]
            p2p = report["pass_to_pass"]
            fixed = bool(f2p) and all(observed.get(test) == "passed" for test in f2p)
            preserved = bool(p2p) and all(observed.get(test) == "passed" for test in p2p)
            executed = run.get("execution_available", True) is True and not run.get(
                "timed_out", False
            )
            resolved = executed and fixed and preserved and run["exit_code"] == 0
            return {
                "benchmark_resolved": resolved,
                "validated_resolved": resolved,
                "evaluation_completed": executed
                and bool(observed)
                and all(test in observed for test in [*f2p, *p2p]),
                "fail_to_pass_outcomes": [observed.get(test) for test in f2p],
                "pass_to_pass_outcomes": [observed.get(test) for test in p2p],
                "test_identity_sha256": fingerprint(sorted(observed)),
                "actual_test_exit_code": run["exit_code"],
                "actual_test_execution_available": run.get("execution_available", True),
                "actual_test_timed_out": run.get("timed_out", False),
                "isolation": tools.isolation,
                "runtime_sha256": tools.runtime_sha256,
                "evaluator_version": "historical-regression-acceptance-v3",
                "evaluation_spec_sha256": spec_hash,
                "regression_exit_codes": [0 if preserved else 1],
                "fail_to_pass_count": len(f2p),
                "pass_to_pass_count": len(p2p),
                "observed_test_count": len(observed),
                "changed_test_files_only": True,
                "whole_project_regression_checked": False,
                "hidden_results_returned_to_solver": False,
                "test_restore_policy": "independent-regression-paths-from-base-v1",
                "formal_SWE_run": False,
            }

    def evaluate(task, patch):
        if not require_causal_controls:
            result = evaluate_raw(task, patch)
            result["causal_controls_passed"] = False
            return result
        controls = calibrate_historical_evaluator(
            task, verification_path, dependency_root, sandbox_backend=sandbox_backend
        )
        result = evaluate_raw(task, patch)
        result["causal_controls"] = controls
        result["causal_controls_sha256"] = fingerprint(controls)
        reconciled = bool(
            controls["passed"]
            and result.get("runtime_sha256") == controls.get("runtime_sha256")
            and result.get("test_identity_sha256") == controls.get("test_identity_sha256")
            and result.get("evaluation_spec_sha256") == controls.get("evaluation_spec_sha256")
        )
        result["causal_controls_passed"] = reconciled
        if not reconciled:
            result.update(
                benchmark_resolved=False,
                validated_resolved=False,
                evaluation_completed=False,
                supervision_exclusion_reason="independent evaluator causal controls did not reconcile",
            )
        return result

    return evaluate


def calibrate_historical_evaluator(
    task, verification_path, dependency_root, *, sandbox_backend="namespace-bind"
):
    """Reproduce the failing base and known repair in the actual acceptance runtime.

    The result stays outside every solver/model input. Unavailable or inconsistent
    controls exclude utility supervision rather than creating failed Skill labels.
    """
    path = Path(verification_path)
    diff = json.loads((path.parent / "historical-diff.json").read_text())
    evaluator = historical_evaluator(
        path, dependency_root, sandbox_backend=sandbox_backend, require_causal_controls=False
    )
    base = evaluator(task, "")
    repaired = evaluator(task, diff["production_diff"])
    same_protocol = all(
        base.get(k) == repaired.get(k) and base.get(k)
        for k in ("runtime_sha256", "evaluation_spec_sha256", "test_identity_sha256")
    )
    passed = bool(
        same_protocol
        and base.get("evaluation_completed")
        and repaired.get("evaluation_completed")
        and base.get("fail_to_pass_outcomes")
        and all(x == "failed" for x in base["fail_to_pass_outcomes"])
        and bool(base.get("pass_to_pass_outcomes"))
        and all(x == "passed" for x in base["pass_to_pass_outcomes"])
        and type(base.get("actual_test_exit_code")) is int
        and base["actual_test_exit_code"] > 0
        and base.get("benchmark_resolved") is False
        and repaired.get("validated_resolved") is True
    )
    return {
        "schema": "historical-acceptance-causal-controls-v1",
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "verification_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "known_production_change_sha256": hashlib.sha256(
            diff["production_diff"].encode()
        ).hexdigest(),
        "base_result_sha256": fingerprint(base),
        "known_repair_result_sha256": fingerprint(repaired),
        "runtime_sha256": base.get("runtime_sha256"),
        "evaluation_spec_sha256": base.get("evaluation_spec_sha256"),
        "test_identity_sha256": base.get("test_identity_sha256"),
        "base_target_failed": bool(base.get("fail_to_pass_outcomes"))
        and all(x == "failed" for x in base["fail_to_pass_outcomes"]),
        "base_controls_preserved": bool(base.get("pass_to_pass_outcomes"))
        and all(x == "passed" for x in base["pass_to_pass_outcomes"]),
        "known_repair_passed": repaired.get("validated_resolved") is True,
        "same_protocol": bool(same_protocol),
        "passed": passed,
        "solver_input_contains_control_results": False,
        "formal_SWE_run": False,
    }
