"""Independent historical regression acceptance, invoked after solver termination."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from .adaptive_budget import BudgetCaps, BudgetLedger
from .adaptive_runner import NamespaceTools, snapshot_base
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


def historical_evaluator(verification_path, dependency_root):
    def evaluate(task, patch):
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
        with tempfile.TemporaryDirectory(prefix="arex-history-acceptance-") as scratch:
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
            tools = NamespaceTools(work, BudgetLedger(BudgetCaps(seconds=600)), dependency_root)
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
                            "evaluator_version": "historical-regression-acceptance-v2",
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
            resolved = fixed and preserved and run["exit_code"] == 0
            return {
                "benchmark_resolved": resolved,
                "validated_resolved": resolved,
                "evaluation_completed": bool(observed)
                and all(test in observed for test in [*f2p, *p2p]),
                "evaluator_version": "historical-regression-acceptance-v2",
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

    return evaluate
