"""Evaluate submissions on the frozen original Issue snapshot.

Known repairs, replay receipts and independent review remain evaluator-only.
Their current observation time never becomes a historical learned source.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path

from .adaptive_budget import BudgetCaps, BudgetLedger
from .adaptive_runner import make_namespace_tools, snapshot_base
from .historical_replay_controls import (
    project_replay_production_diff,
    replay_task_identity,
    verify_replay_controls,
)
from .historical_solver_evaluator import restore_evaluation_paths
from .history_census import fingerprint
from .history_verification import junit_observations
from .skill_packages import _resolve

REVIEW_SCHEMA = "original-query-replay-independent-review-v1"


@dataclass(frozen=True)
class OriginalReplayAuthority:
    cohort: dict
    completion: dict
    diff: dict
    review: dict | None
    pinned_files: tuple[tuple[Path, bytes], ...]

    def verify_unchanged(self, task):
        task.verify()
        if any(path.read_bytes() != raw for path, raw in self.pinned_files):
            raise ValueError("original replay authority changed during evaluation")
        if replay_task_identity(task) != self.cohort["task_identity"]:
            raise ValueError("original query identity changed during evaluation")

    @property
    def independently_reviewed(self):
        return self.review is not None and self.review["accepted_limited_replay"] is True


def load_original_replay_authority(task, verification_path, controls_dir, review_path=None):
    """Recompute actual control gates; a stored PASS alone is insufficient."""
    task.verify()
    root, verification = Path(controls_dir), Path(verification_path)
    paths = [
        verification,
        verification.parent / "historical-diff.json",
        root / "cohort.json",
        root / "completion.json",
        *(
            root / (phase + ".json")
            for phase in ("original_base", "base_with_regression", "known_repair")
        ),
    ]
    if review_path is not None:
        paths.extend(
            (
                Path(review_path),
                Path(review_path).with_name("input.json"),
                Path(review_path).with_name("calls.json"),
            )
        )
    pinned = tuple((path, path.read_bytes()) for path in paths)
    values = {path: json.loads(raw) for path, raw in pinned}
    report, diff = values[verification], values[paths[1]]
    cohort, completion = values[root / "cohort.json"], values[root / "completion.json"]
    phases = {
        name: values[root / (name + ".json")]
        for name in ("original_base", "base_with_regression", "known_repair")
    }
    if (
        report.get("schema") != "historical-causal-verification-v1"
        or report.get("verified_resolution") is not True
        or report["identity"]["issue_id"] != task.task_id
        or cohort.get("schema") != "original-query-replay-cohort-v1"
        or cohort["task_identity"] != replay_task_identity(task)
        or cohort["native_identity"] != report["identity"]
        or cohort["native_report_content_sha256"] != fingerprint(report)
        or cohort["command"] != report["command"]
        or completion["native_verification_file_sha256"] != hashlib.sha256(pinned[0][1]).hexdigest()
        or completion["historical_diff_file_sha256"] != hashlib.sha256(pinned[1][1]).hexdigest()
    ):
        raise ValueError("original replay source/query identity or artifact mismatch")
    recomputed = verify_replay_controls(
        cohort, phases, source_files_unchanged=True, task_input_unchanged=True
    )
    if recomputed["mechanical_controls_passed"] is not True or any(
        completion.get(key) != value for key, value in recomputed.items()
    ):
        raise ValueError("original replay causal controls are unqualified or changed")
    controlled, projection = project_replay_production_diff(
        diff["production_diff"], completion["production_projection"]["policy"]
    )
    if (
        completion["production_projection"] != projection
        or completion["raw_known_repair_file_sha256"]
        != hashlib.sha256(diff["production_diff"].encode()).hexdigest()
        or completion["controlled_known_repair_file_sha256"]
        != hashlib.sha256(controlled.encode()).hexdigest()
        or completion["known_repair_adapted"] != (controlled != diff["production_diff"])
        or completion["historical_regression_assertions_unchanged"] is not True
    ):
        raise ValueError("original replay production projection or assertion identity changed")
    review = values[Path(review_path)] if review_path is not None else None
    if review is not None:
        review_input = values[Path(review_path).with_name("input.json")]
        calls = values[Path(review_path).with_name("calls.json")]
        if (
            review.get("review_input_sha256") != fingerprint(review_input)
            or review_input.get("task_identity") != cohort["task_identity"]
            or review_input.get("public_problem") != task.public_problem
            or review_input.get("frozen_current_cohort") != cohort
            or review_input.get("mechanical_controls") != completion
            or review_input.get("native_regression_diff") != diff["regression_diff"]
            or review_input.get("evaluator_known_production_diff") != diff["production_diff"]
            or review_input.get("phase_receipts") != phases
            or not isinstance(calls, list)
            or len(calls) != review.get("actual_model_calls")
            or not any(
                call.get("successful") is True and call.get("model") == review.get("reviewer_model")
                for call in calls
            )
        ):
            raise ValueError("independent replay review input or model-call witness mismatch")
        gates = ("mechanism_alignment", "oracle_fidelity", "regression_coverage")
        if (
            review.get("schema") != REVIEW_SCHEMA
            or review.get("task_identity") != cohort["task_identity"]
            or review.get("control_completion_sha256") != fingerprint(completion)
            or review.get("cohort_sha256") != cohort["cohort_sha256"]
            or type(review.get("accepted_limited_replay")) is not bool
            or any(review.get(gate) not in {"PASS", "FAIL", "UNKNOWN"} for gate in gates)
            or (review["accepted_limited_replay"] and any(review[g] != "PASS" for g in gates))
            or not review.get("rationale")
            or not review.get("evidence_refs")
            or not review.get("limitations")
            or type(review.get("actual_model_calls")) is not int
            or review["actual_model_calls"] < 1
            or review.get("formal_SWE_run") is not False
        ):
            raise ValueError("independent replay review identity, evidence or gates mismatch")
    return OriginalReplayAuthority(cohort, completion, diff, review, pinned)


def original_query_evaluator(
    verification_path,
    dependency_root,
    controls_dir,
    *,
    independent_review_path=None,
    sandbox_backend="namespace-copy",
):
    """Load private authority after solver termination, then run current assertions."""

    def evaluate(task, patch):
        authority = load_original_replay_authority(
            task, verification_path, controls_dir, independent_review_path
        )
        cohort = authority.cohort
        f2p, p2p = cohort["current_fail_to_pass"], cohort["current_pass_to_pass"]
        spec_hash = fingerprint(
            {
                "cohort_sha256": cohort["cohort_sha256"],
                "control_completion_sha256": fingerprint(authority.completion),
                "review_sha256": fingerprint(authority.review) if authority.review else None,
                "test_restore_policy": "independent-regression-paths-from-original-base-v1",
            }
        )
        result = {
            "benchmark_resolved": False,
            "validated_resolved": False,
            "evaluation_completed": False,
            "mechanical_causal_controls_passed": True,
            "causal_controls_passed": authority.independently_reviewed,
            "independent_replay_review_complete": authority.independently_reviewed,
            "evaluator_version": "original-query-regression-acceptance-v1",
            "evaluation_spec_sha256": spec_hash,
            "cohort_sha256": cohort["cohort_sha256"],
            "causal_controls_sha256": fingerprint(authority.completion),
            "fail_to_pass_count": len(f2p),
            "pass_to_pass_count": len(p2p),
            "missing_native_pass_to_pass": cohort["missing_native_pass_to_pass"],
            "changed_test_files_only": True,
            "whole_project_regression_checked": False,
            "hidden_results_returned_to_solver": False,
            "native_source_record_replaced": False,
            "formal_SWE_run": False,
        }
        with (
            tempfile.TemporaryDirectory(prefix="arex-original-query-acceptance-") as scratch,
            ExitStack() as cleanup,
        ):
            work = Path(scratch) / "evaluation"
            snapshot_base(task, work)
            baseline = Path(scratch) / "test-base"
            baseline.mkdir()
            for relative in authority.diff["paths"]:
                source = _resolve(work, relative)
                if source.is_symlink():
                    raise ValueError("independent evaluation path must not be a symlink")
                if source.is_file():
                    target = _resolve(baseline, relative)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(source.read_bytes())
            tools = make_namespace_tools(
                work,
                BudgetLedger(BudgetCaps(seconds=600)),
                dependency_root,
                backend=sandbox_backend,
            )
            cleanup.callback(tools.close)
            tools.preflight()
            result.update(runtime_sha256=tools.runtime_sha256, isolation=tools.isolation)
            if tools.runtime_sha256 != authority.completion["runtime_sha256"]:
                result["supervision_exclusion_reason"] = "original replay runtime mismatch"
                authority.verify_unchanged(task)
                return result
            for phase, applied_patch in (
                ("submission", patch),
                ("independent-tests", authority.diff["regression_diff"]),
            ):
                if phase == "independent-tests":
                    restore_evaluation_paths(work, baseline, authority.diff["paths"])
                if applied_patch:
                    applied = tools.run(
                        ["git", "apply", "--whitespace=nowarn", "-"],
                        stdin=applied_patch.encode(),
                        timeout=60,
                    )
                    if applied["exit_code"]:
                        result.update(
                            setup_failure_phase=phase,
                            supervision_exclusion_reason="submission or oracle patch did not apply",
                        )
                        authority.verify_unchanged(task)
                        return result
            run = tools.run(
                [*cohort["command"], "--junitxml=/workspace/original-query-acceptance.xml"],
                timeout=120,
            )
            observed = junit_observations(work / "original-query-acceptance.xml")
            executed = bool(
                type(run.get("exit_code")) is int
                and run["exit_code"] in {0, 1}
                and run.get("execution_available", True) is True
                and run.get("timed_out", False) is False
                and sorted(observed) == cohort["expected_collected_tests"]
                and all(observed.get(k) in {"passed", "failed"} for k in [*f2p, *p2p])
            )
            preserved = all(observed.get(k) == "passed" for k in p2p)
            repaired = all(observed.get(k) == "passed" for k in f2p)
            resolved = executed and preserved and repaired and run["exit_code"] == 0
            qualified = executed and authority.independently_reviewed
            result.update(
                benchmark_resolved=resolved and qualified,
                validated_resolved=resolved and qualified,
                mechanically_resolved=resolved,
                evaluation_completed=qualified,
                fail_to_pass_outcomes=[observed.get(k) for k in f2p],
                pass_to_pass_outcomes=[observed.get(k) for k in p2p],
                test_identity_sha256=fingerprint(sorted(observed)),
                actual_test_exit_code=run.get("exit_code"),
                actual_test_execution_available=run.get("execution_available", True),
                actual_test_timed_out=run.get("timed_out", False),
                observed_test_count=len(observed),
                regression_exit_codes=[0 if preserved else 1],
            )
            if not qualified:
                result["supervision_exclusion_reason"] = (
                    "independent replay review not accepted"
                    if not authority.independently_reviewed
                    else "original replay test execution or collection unavailable"
                )
        authority.verify_unchanged(task)
        return result

    return evaluate
