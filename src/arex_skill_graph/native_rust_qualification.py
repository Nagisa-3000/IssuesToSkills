"""Versioned exact Rust libtest controls; no exit-code normalization or promotion."""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import PurePosixPath

from .history_census import fingerprint

SCHEMA = "historical-rust-test-causal-verification-v1"
SCOPE = "exact-rust-libtest-with-original-base-control-v1"
PHASES = ("original_base", "base_with_regression", "historical_fixed")


def _hash(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _path(value, *, absolute=False):
    if not isinstance(value, str) or not value:
        return False
    p = PurePosixPath(value)
    return p.is_absolute() == absolute and ".." not in p.parts and str(p) == value


def _check_command(argv, spec, test_id):
    binary, cwd = spec["binary_path"], spec["working_directory"]
    if not _path(binary, absolute=True) or not _path(cwd, absolute=True):
        raise ValueError("native Rust execution paths are not canonical")
    direct = [binary, test_id, "--exact", "--nocapture", "--test-threads=1"]
    # The existing sealed runner relocates Insta through this specific wrapper.
    # AST equality permits formatting changes but rejects added commands, shell
    # execution, dynamic argv, altered environments, or hidden trailing checks.
    script = (
        f"import os,subprocess,sys;os.chdir({cwd!r});"
        "os.environ['INSTA_WORKSPACE_ROOT']='/workspace';"
        "os.environ['INSTA_UPDATE']='no';os.environ['INSTA_FORCE_PASS']='0';"
        f"p=subprocess.run({direct!r});sys.exit(p.returncode)"
    )
    if not isinstance(argv, list) or len(argv) != 3 or argv[:2] != ["python3", "-c"]:
        raise ValueError("native Rust command is not the sealed exact execution wrapper")
    try:
        matches = ast.dump(ast.parse(argv[2])) == ast.dump(ast.parse(script))
    except (ValueError, TypeError, SyntaxError):
        matches = False
    if not matches:
        raise ValueError("native Rust command differs from the exact execution contract")


def validate_native_rust_controls(report):
    """Recompute one named test and preservation from complete sealed receipts.

    These are validation provenance, not independent Skill evals or evidence
    that can be learned before its historical availability.
    """
    native = report["native_controls"]
    receipts = native["phase_receipts"]
    test_id = native["test_id"]
    if (
        native.get("schema") != "rust-libtest-causal-controls-v1"
        or not isinstance(test_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_:]+", test_id)
        or set(receipts) != set(PHASES)
        or fingerprint(receipts) != native["phase_receipts_sha256"]
        or native.get("expected_snapshots_regenerated") is not False
    ):
        raise ValueError("native Rust control identities or receipt hash changed")
    roles = native["protected_resource_roles"]
    if set(roles) != {"fixtures", "implementation", "expected_snapshots", "lockfile"}:
        raise ValueError("native Rust resource roles incomplete")
    groups = [roles[k] for k in ("fixtures", "implementation", "expected_snapshots")]
    if any(not isinstance(g, list) or not g or any(not _path(p) for p in g) for g in groups):
        raise ValueError("native Rust protected resource paths invalid")
    paths = [p for g in groups for p in g] + [roles["lockfile"]]
    if roles["lockfile"] != "Cargo.lock" or len(set(paths)) != len(paths):
        raise ValueError("native Rust lockfile or resource ownership invalid")
    deps = native["locked_dependencies"]
    if (
        deps.get("schema") != "rust-locked-dependency-receipt-v1"
        or deps.get("cargo_lock_unchanged") is not True
        or deps.get("offline_vendor_exit_code") != 0
        or not _hash(deps.get("cargo_lock_sha256"))
        or not _hash(deps.get("vendor_manifest_sha256"))
        or not _hash(deps.get("receipt_file_sha256"))
        or not re.fullmatch(r"[0-9]+[.][0-9]+[.][0-9]+-[A-Za-z0-9_-]+", deps.get("toolchain", ""))
        or type(deps.get("vendor_packages")) is not int
        or deps["vendor_packages"] < 1
        or type(deps.get("verified_vendor_files")) is not int
        or deps["verified_vendor_files"] < deps["vendor_packages"]
    ):
        raise ValueError("native Rust locked dependency receipt incomplete")
    inputs = []
    for phase, exit_code, result_label, passed, failed in zip(
        PHASES, (0, 101, 0), ("ok", "FAILED", "ok"), (1, 0, 1), (0, 1, 0)
    ):
        receipt, run, spec = (
            receipts[phase],
            report["runs"][phase],
            native["execution_specs"][phase],
        )
        observation = receipt["observation"]
        output = observation["output"]
        before, after = receipt["protected_hashes_before"], receipt["protected_hashes_after"]
        seal = receipt["workspace_execution_sha256_before"]
        if (
            run != observation
            or type(observation.get("exit_code")) is not int
            or observation["exit_code"] != exit_code
            or observation.get("timed_out") is not False
            or observation.get("workspace_adopted") is not False
            or observation.get("isolation") != receipt["isolation"]
            or observation.get("runtime_sha256") != receipt["runtime_sha256"]
            or receipt["runtime_sha256"] != report["runtime_sha256"]
            or receipt.get("protected_inputs_unchanged") is not True
            or not _hash(seal)
            or seal != receipt["workspace_execution_sha256_after"]
            or before != after
            or set(before) != set(paths)
            or any(not _hash(h) for h in before.values())
            or before["Cargo.lock"] != deps["cargo_lock_sha256"]
            or receipt.get("insta_update") != "no"
            or receipt.get("insta_force_pass") != "0"
            or receipt.get("binary_sha256") != spec["binary_sha256"]
            or not _hash(spec["binary_sha256"])
            or type(receipt.get("actual_Rust_tests_executed")) is not int
            or receipt["actual_Rust_tests_executed"] != 1
            or receipt.get("rust_passed") != passed
            or receipt.get("rust_failed") != failed
            or not isinstance(output, str)
            or hashlib.sha256(output.encode()).hexdigest() != native["output_sha256"][phase]
        ):
            raise ValueError("native Rust runtime, resource seal or actual execution changed")
        _check_command(observation["argv"], spec, test_id)
        summaries = re.findall(
            r"^test result: (ok|FAILED)[.] ([0-9]+) passed; ([0-9]+) failed; "
            r"([0-9]+) ignored; ([0-9]+) measured; [0-9]+ filtered out; finished in [^\n]+$",
            output,
            re.M,
        )
        if (
            re.findall(r"^running ([0-9]+) test(?:s)?$", output, re.M) != ["1"]
            or summaries != [(result_label, str(passed), str(failed), "0", "0")]
            or len(re.findall(r"^test " + re.escape(test_id) + r" [.]{3} ", output, re.M)) != 1
            or report["observations"][phase] != {test_id: "failed" if failed else "passed"}
        ):
            raise ValueError("native Rust output did not execute exactly the declared test")
        if passed and not re.search(r"^test " + re.escape(test_id) + r" [.]{3} ok$", output, re.M):
            raise ValueError("native Rust positive control lacks named test success")
        if failed:
            panic = native["negative_panic"]
            if (
                panic["source_path"] not in roles["implementation"]
                or not isinstance(panic["message"], str)
                or not panic["message"]
                or not re.search(
                    "thread '"
                    + re.escape(test_id)
                    + "' panicked at "
                    + re.escape(panic["source_path"])
                    + r":[0-9]+:[0-9]+:",
                    output,
                )
                or not re.search(r"^" + re.escape(panic["message"]) + r"$", output, re.M)
            ):
                raise ValueError("native Rust negative control lacks the declared defect panic")
        inputs.append(before)
    original, regression, fixed = inputs
    original_spec, regression_spec = (native["execution_specs"][p] for p in PHASES[:2])
    if (
        original_spec != regression_spec
        or any(
            original[p] != regression[p]
            for p in roles["implementation"] + roles["expected_snapshots"]
        )
        or not any(original[p] != regression[p] for p in roles["fixtures"])
        or any(regression[p] != fixed[p] for p in roles["fixtures"])
        or not any(regression[p] != fixed[p] for p in roles["implementation"])
    ):
        raise ValueError("native Rust regression/fixed source boundaries do not recompute")
