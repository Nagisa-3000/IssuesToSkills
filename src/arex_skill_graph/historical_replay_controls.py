"""Versioned evaluator-only controls for an original-input published-source replay.

These records qualify a current replay cohort. They do not replace the immutable
historical source verification or authorize guidance, promotion, or utility labels.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import shlex
import tempfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from .adaptive_budget import BudgetCaps, BudgetLedger
from .adaptive_runner import make_namespace_tools, snapshot_base
from .history_census import fingerprint, redact_history, write_json
from .history_verification import junit_observations
from .skill_packages import _resolve


def replay_assertion_changes(original_sources, regression_sources, test_ids):
    """Identify changed test bodies or exact parameterized fixture cases."""
    result = {}
    for test_id in test_ids:
        parts = test_id.split("::")
        method = parts[-1].split("[", 1)[0]
        owner = parts[-2].rsplit(".", 1)[-1] if len(parts) > 1 else None
        parameter = parts[-1].split("[", 1)[1].removesuffix("]") if "[" in parts[-1] else None
        for path in sorted(set(original_sources) & set(regression_sources)):
            before, after = original_sources[path], regression_sources[path]
            if before is None or after is None or before == after:
                continue
            kind, prior, current = None, None, None
            if parameter == Path(path).stem:
                kind, prior, current = "exact_parameterized_fixture", before, after
            elif Path(path).suffix == ".py":

                def body(content, method=method, owner=owner, path=path):
                    try:
                        tree = ast.parse(content.decode())
                    except (SyntaxError, UnicodeDecodeError):
                        return None
                    nodes = []
                    for node in tree.body:
                        if (
                            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                            and node.name == method
                            and owner == Path(path).stem
                        ):
                            nodes.append(node)
                        elif isinstance(node, ast.ClassDef) and node.name == owner:
                            nodes.extend(
                                member
                                for member in node.body
                                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                                and member.name == method
                            )
                    return (
                        ast.dump(nodes[0], include_attributes=False).encode()
                        if len(nodes) == 1
                        else None
                    )

                prior, current = body(before), body(after)
                if prior is not None and current is not None and prior != current:
                    kind = "changed_test_body"
            if kind:
                result[test_id] = {
                    "path": path,
                    "kind": kind,
                    "original_assertion_sha256": hashlib.sha256(prior).hexdigest(),
                    "regression_assertion_sha256": hashlib.sha256(current).hexdigest(),
                }
                break
    return result


def replay_task_identity(task):
    return {
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "input_available_at": task.input_available_at,
        "public_problem_sha256": hashlib.sha256(task.public_problem.encode()).hexdigest(),
    }


def _observations(value):
    if not isinstance(value, dict) or any(
        not isinstance(key, str) or not key or status not in {"passed", "failed", "skipped"}
        for key, status in value.items()
    ):
        raise ValueError("replay needs identified test observations")
    return dict(value)


def freeze_replay_cohort(task, historical_report, original, regression, *, assertion_changes=None):
    """Freeze the actual current cohort before running the known repair."""
    if (
        historical_report.get("schema") != "historical-causal-verification-v1"
        or historical_report.get("verified_resolution") is not True
        or historical_report["identity"]["issue_id"] != task.task_id
    ):
        raise ValueError("replay needs matching qualified native historical evidence")
    original, regression = _observations(original), _observations(regression)
    native_f2p = historical_report["fail_to_pass"]
    native_p2p = historical_report["pass_to_pass"]
    for names in (native_f2p, native_p2p):
        if (
            not isinstance(names, list)
            or not names
            or len(set(names)) != len(names)
            or any(not isinstance(name, str) or not name for name in names)
        ):
            raise ValueError("native regression targets must be unique and identified")
    assertion_changes = assertion_changes or {}
    redefined = sorted(
        key
        for key, value in original.items()
        if value == "passed" and regression.get(key) == "failed"
    )
    witnessed = set()
    for key in redefined:
        change = assertion_changes.get(key, {})
        old_hash = change.get("original_assertion_sha256", "")
        new_hash = change.get("regression_assertion_sha256", "")
        if (
            change.get("kind") in {"changed_test_body", "exact_parameterized_fixture"}
            and change.get("path")
            and re.fullmatch(r"[0-9a-f]{64}", old_hash)
            and re.fullmatch(r"[0-9a-f]{64}", new_hash)
            and old_hash != new_hash
        ):
            witnessed.add(key)
    payload = {
        "schema": "original-query-replay-cohort-v1",
        "frozen_at_utc": datetime.now(UTC).isoformat(),
        "task_identity": replay_task_identity(task),
        "native_identity": historical_report["identity"],
        "native_report_content_sha256": fingerprint(historical_report),
        "command": historical_report["command"],
        "original_observations_sha256": fingerprint(original),
        "regression_observations_sha256": fingerprint(regression),
        "original_collected_tests": sorted(original),
        "expected_collected_tests": sorted(regression),
        "original_current_pass_to_pass": sorted(
            key for key, value in original.items() if value == "passed" and key not in witnessed
        ),
        "current_fail_to_pass": sorted(
            key for key, value in regression.items() if value == "failed"
        ),
        "current_pass_to_pass": sorted(
            key for key, value in regression.items() if value == "passed"
        ),
        "current_skipped": sorted(key for key, value in regression.items() if value == "skipped"),
        "native_target_identity_overlaps": sorted(set(native_f2p) & set(native_p2p)),
        "original_current_redefined_by_regression": redefined,
        "regression_assertion_changes": {key: assertion_changes[key] for key in sorted(witnessed)},
        "unwitnessed_original_failure_transitions": sorted(set(redefined) - witnessed),
        "native_fail_to_pass": sorted(native_f2p),
        "missing_native_fail_to_pass": sorted(set(native_f2p) - set(regression)),
        "native_fail_to_pass_not_failed": sorted(
            key for key in native_f2p if key in regression and regression[key] != "failed"
        ),
        "missing_native_pass_to_pass": sorted(set(native_p2p) - set(original)),
        "missing_original_current_tests": sorted(set(original) - set(regression)),
        "native_source_record_replaced": False,
        "actor_may_read_known_repair": False,
        "scope": "unchanged native regression assertions on original-input published source",
    }
    payload["cohort_sha256"] = fingerprint(payload)
    return payload


def verify_replay_controls(cohort, phases, *, source_files_unchanged, task_input_unchanged):
    """Check actual phase receipts; failed/unavailable controls produce no utility labels."""
    if cohort.get("cohort_sha256") != fingerprint(
        {key: value for key, value in cohort.items() if key != "cohort_sha256"}
    ):
        raise ValueError("replay cohort changed after freezing")
    if set(phases) != {"original_base", "base_with_regression", "known_repair"}:
        raise ValueError("replay requires all three phase receipts")
    checks = []

    def check(name, value, reason):
        checks.append(
            {
                "name": name,
                "status": "UNKNOWN" if value is None else "PASS" if value else "FAIL",
                "reason": reason,
            }
        )

    for name, phase in phases.items():
        run = phase.get("focused_test_run", {})
        ready = bool(
            phase.get("setup_complete") is True
            and type(run.get("exit_code")) is int
            and run.get("execution_available", True) is True
            and run.get("timed_out", False) is False
            and phase.get("observations")
        )
        check(name + "_execution", True if ready else None, "setup and actual test execution")
    available = all(row["status"] == "PASS" for row in checks)
    check("source_files_unchanged", source_files_unchanged, "native verification and diff retained")
    check(
        "task_input_unchanged", task_input_unchanged, "public input and immutable source retained"
    )
    if available:
        original = phases["original_base"]
        regression = phases["base_with_regression"]
        repaired = phases["known_repair"]
        original_obs = _observations(original["observations"])
        before = _observations(regression["observations"])
        after = _observations(repaired["observations"])
        hashes = [row.get("runtime_sha256") for row in phases.values()]
        check(
            "same_actual_runtime",
            all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) for value in hashes)
            and len(set(hashes)) == 1,
            "three phases must share the measured runtime",
        )
        check(
            "frozen_original_observations",
            fingerprint(original_obs) == cohort["original_observations_sha256"],
            "original collection and outcomes match the frozen cohort",
        )
        check(
            "frozen_regression_observations",
            fingerprint(before) == cohort["regression_observations_sha256"],
            "pre-repair collection and outcomes match the frozen cohort",
        )
        check(
            "original_base_passed",
            original["focused_test_run"]["exit_code"] == 0
            and bool(cohort["original_current_pass_to_pass"])
            and all(value in {"passed", "skipped"} for value in original_obs.values()),
            "the published original source must have working baseline controls",
        )
        check(
            "exact_known_repair_cohort",
            sorted(after) == cohort["expected_collected_tests"],
            "known repair must not delete, add, or rename collected evaluation tests",
        )
        check(
            "original_tests_retained",
            not cohort["missing_original_current_tests"]
            and all(
                before.get(test) == after.get(test) == "passed"
                for test in cohort["original_current_pass_to_pass"]
            ),
            "preserve all original passing controls on the selected current source",
        )
        check(
            "redefined_original_targets_witnessed",
            not cohort["unwitnessed_original_failure_transitions"],
            "original passing cases may become F2P only with changed assertion or exact fixture evidence",
        )
        check(
            "native_targets_reproduced",
            not cohort["missing_native_fail_to_pass"]
            and not cohort["native_fail_to_pass_not_failed"],
            "native failing targets must actually fail on this selected replay version",
        )
        check(
            "current_failure_transition",
            regression["focused_test_run"]["exit_code"] == 1
            and bool(cohort["current_fail_to_pass"])
            and all(
                before.get(test) == "failed" and after.get(test) == "passed"
                for test in cohort["current_fail_to_pass"]
            ),
            "all current test failures must transition to passing with the known repair",
        )
        check(
            "current_pass_controls",
            bool(cohort["current_pass_to_pass"])
            and all(after.get(test) == "passed" for test in cohort["current_pass_to_pass"]),
            "include passing unchanged historical assertions in the current PTP cohort",
        )
        check(
            "known_repair_passed",
            repaired["focused_test_run"]["exit_code"] == 0
            and all(value in {"passed", "skipped"} for value in after.values()),
            "known repair passes the entire frozen focused cohort",
        )
    passed = all(row["status"] == "PASS" for row in checks)
    return {
        "schema": "original-query-replay-controls-completion-v1",
        "task_identity": cohort["task_identity"],
        "cohort_sha256": cohort["cohort_sha256"],
        "phase_receipts_sha256": fingerprint(phases),
        "checks": checks,
        "mechanical_controls_passed": passed,
        "control_status": "PASS"
        if passed
        else "UNKNOWN"
        if any(row["status"] == "UNKNOWN" for row in checks)
        else "FAIL",
        "runtime_sha256": phases["original_base"].get("runtime_sha256"),
        "current_fail_to_pass_count": len(cohort["current_fail_to_pass"]),
        "current_pass_to_pass_count": len(cohort["current_pass_to_pass"]),
        "missing_native_pass_to_pass": cohort["missing_native_pass_to_pass"],
        "independent_review_complete": False,
        "complete_replay_acceptance": False,
        "utility_labels_created": 0,
        "actual_LLM_calls": 0,
        "solver_branches": 0,
        "formal_SWE_runs": 0,
        "native_source_record_replaced": False,
        "actor_may_read_known_repair": False,
        "scope": cohort["scope"],
    }


def project_replay_production_diff(patch, policy="native"):
    """Keep native code hunks byte-for-byte; optionally omit only explicit release metadata."""
    if policy not in {"native", "omit-release-metadata"}:
        raise ValueError("unsupported evaluator production projection policy")
    excluded, retained, pieces = [], [], []
    if policy == "native":
        projected = patch
    else:
        for section in re.split(r"(?=^diff --git )", patch, flags=re.MULTILINE):
            if not section:
                continue
            header = shlex.split(section.splitlines()[0])
            if len(header) != 4 or header[:2] != ["diff", "--git"]:
                raise ValueError("production projection needs complete Git diff sections")
            if not header[2].startswith("a/") or not header[3].startswith("b/"):
                raise ValueError("production projection has unsupported path prefixes")
            paths = [value[2:] for value in header[2:]]
            if any(
                PurePosixPath(value).is_absolute()
                or ".." in PurePosixPath(value).parts
                or ".git" in PurePosixPath(value).parts
                or "\\" in value
                for value in paths
            ):
                raise ValueError("production projection path escapes public source")
            informational = all(
                value in {"ChangeLog", "CONTRIBUTORS.txt"}
                or (value.startswith("doc/whatsnew/") and value.endswith((".rst", ".md")))
                for value in paths
            )
            modes = re.findall(
                r"^(?:old mode|new mode|new file mode|deleted file mode) ([0-7]{6})$",
                section,
                flags=re.MULTILINE,
            ) + re.findall(
                r"^index [0-9a-f]+\.\.[0-9a-f]+ ([0-7]{6})$", section, flags=re.MULTILINE
            )
            special_file = any(mode != "100644" for mode in modes) or (
                "GIT binary patch" in section or "Binary files " in section
            )
            record = {
                "before_path": paths[0],
                "after_path": paths[1],
                "section_sha256": hashlib.sha256(section.encode()).hexdigest(),
            }
            if informational and not special_file:
                excluded.append({**record, "reason": "explicit non-executable release metadata"})
            else:
                retained.append(record)
                pieces.append(section)
        projected = "".join(pieces)
        if not projected.strip():
            raise ValueError("release metadata projection leaves no production repair")
    return projected, {
        "schema": "evaluator-production-projection-v1",
        "policy": policy,
        "native_production_sha256": hashlib.sha256(patch.encode()).hexdigest(),
        "controlled_production_sha256": hashlib.sha256(projected.encode()).hexdigest(),
        "excluded_sections": excluded,
        "retained_sections": retained,
        "retained_section_bytes_unchanged": True,
        "regression_assertions_modified": False,
        "native_source_records_replaced": False,
        "actor_may_read_known_repair": False,
        "functional_control_scope_only": policy != "native",
    }


def run_original_query_controls(
    task, verification_path, dependency_root, output_dir, *, production_projection="native"
):
    """Execute unchanged historical tests and production diff in separate current snapshots."""
    output = Path(output_dir)
    if output.exists():
        raise ValueError("preserve prior replay controls; use a new output version")
    output.mkdir(parents=True)
    path = Path(verification_path)
    diff_path = path.parent / "historical-diff.json"
    report_raw, diff_raw = path.read_bytes(), diff_path.read_bytes()
    report, diff = json.loads(report_raw), json.loads(diff_raw)
    if (
        report["identity"]["issue_id"] != task.task_id
        or report.get("verified_resolution") is not True
    ):
        raise ValueError("replay control native identity or qualification mismatch")
    if any(
        redact_history(diff[key]) != diff[key] for key in ("production_diff", "regression_diff")
    ):
        raise ValueError("credential-like historical patch cannot enter replay controls")
    task.verify()
    production, projection = project_replay_production_diff(
        diff["production_diff"], production_projection
    )
    write_json(output / "production-projection.json", projection)
    phases, cohort = {}, None
    phase_inputs = (
        ("original_base", ()),
        ("base_with_regression", (diff["regression_diff"],)),
        ("known_repair", (production, diff["regression_diff"])),
    )
    for name, patches in phase_inputs:
        if (
            name == "known_repair"
            and cohort is not None
            and json.loads((output / "cohort.json").read_text()) != cohort
        ):
            raise ValueError("saved cohort changed before known-repair execution")
        with tempfile.TemporaryDirectory(prefix="arex-original-query-private-control-") as scratch:
            work = Path(scratch) / "workspace"
            snapshot_base(task, work)
            original_sources = {
                relative: _resolve(work, relative).read_bytes()
                if _resolve(work, relative).is_file()
                else None
                for relative in diff["paths"]
            }
            ledger = BudgetLedger(BudgetCaps(seconds=600))
            tools = make_namespace_tools(work, ledger, dependency_root, backend="namespace-copy")
            row = {"phase": name, "setup_complete": False, "patch_application": []}
            try:
                tools.preflight()
                row["runtime_sha256"] = tools.runtime_sha256
                for patch in patches:
                    applied = tools.run(
                        ["git", "apply", "--whitespace=nowarn", "-"],
                        stdin=patch.encode(),
                        timeout=60,
                    )
                    row["patch_application"].append(applied)
                    if applied["exit_code"] != 0:
                        break
                if all(item["exit_code"] == 0 for item in row["patch_application"]):
                    row["setup_complete"] = True
                    row["focused_test_run"] = tools.run(
                        [*report["command"], "--junitxml=/workspace/replay-controls.xml"],
                        timeout=120,
                    )
                    row["observations"] = junit_observations(work / "replay-controls.xml")
            except (ValueError, OSError) as error:
                row["failure_class"] = type(error).__name__
                row["failure_reason"] = redact_history(str(error))
            finally:
                tools.close()
            if name == "base_with_regression":
                changed_sources = {
                    relative: _resolve(work, relative).read_bytes()
                    if _resolve(work, relative).is_file()
                    else None
                    for relative in diff["paths"]
                }
                assertion_changes = replay_assertion_changes(
                    original_sources,
                    changed_sources,
                    phases["original_base"].get("observations", {}),
                )
            phases[name] = row
            write_json(output / (name + ".json"), row)
            if name == "base_with_regression":
                cohort = freeze_replay_cohort(
                    task,
                    report,
                    phases["original_base"].get("observations", {}),
                    row.get("observations", {}),
                    assertion_changes=assertion_changes,
                )
                write_json(output / "cohort.json", cohort)
            write_json(
                output / "progress.json",
                {"completed_phases": len(phases), "phase": name, "actual_LLM_calls": 0},
            )
    task.verify()
    if cohort is None:
        raise ValueError("replay did not freeze a current cohort")
    if json.loads((output / "cohort.json").read_text()) != cohort:
        raise ValueError("saved cohort changed during known-repair execution")
    result = verify_replay_controls(
        cohort,
        phases,
        source_files_unchanged=path.read_bytes() == report_raw
        and diff_path.read_bytes() == diff_raw,
        task_input_unchanged=True,
    )
    result.update(
        native_verification_file_sha256=hashlib.sha256(report_raw).hexdigest(),
        historical_diff_file_sha256=hashlib.sha256(diff_raw).hexdigest(),
        raw_known_repair_file_sha256=hashlib.sha256(diff["production_diff"].encode()).hexdigest(),
        historical_regression_assertions_unchanged=True,
        known_repair_adapted=production != diff["production_diff"],
        production_projection=projection,
        controlled_known_repair_file_sha256=hashlib.sha256(production.encode()).hexdigest(),
    )
    write_json(output / "completion.json", result)
    return result
