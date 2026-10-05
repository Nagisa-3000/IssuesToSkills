"""Synthetic protocol fixtures verify strict native guards, not real qualification."""

import copy
import hashlib

import pytest
from test_qualification_authority import POLICY, report_for, source, write_inventory

from arex_skill_graph.history_census import fingerprint
from arex_skill_graph.qualification_authority import (
    load_source_qualifications,
    validate_historical_qualification,
)

TEST = "rules::test_async_binding"


def native_report():
    report = report_for(source())
    report["schema"] = "historical-rust-test-causal-verification-v1"
    report["qualification_scope"] = "exact-rust-libtest-with-original-base-control-v1"
    observations = {
        "original_base": {TEST: "passed"},
        "base_with_regression": {TEST: "failed"},
        "historical_fixed": {TEST: "passed"},
    }
    report.update(
        observations=observations,
        observations_sha256=fingerprint(observations),
        fail_to_pass=[TEST],
        pass_to_pass=[TEST],
    )
    receipts, specs, outputs = {}, {}, {}
    for index, (phase, code) in enumerate(zip(observations, (0, 101, 0))):
        binary = "/opt/venv/bin/test-" + ("fixed" if index == 2 else "base")
        argv = [binary, TEST, "--exact", "--nocapture", "--test-threads=1"]
        script = (
            "import os,subprocess,sys;os.chdir('/workspace/crate');"
            "os.environ['INSTA_WORKSPACE_ROOT']='/workspace';"
            "os.environ['INSTA_UPDATE']='no';os.environ['INSTA_FORCE_PASS']='0';"
            f"p=subprocess.run({argv!r});sys.exit(p.returncode)"
        )
        if code:
            line = (
                f"thread '{TEST}' panicked at src/checker.rs:1:1:\nunsupported async node\nFAILED"
            )
            summary = "FAILED. 0 passed; 1 failed"
        else:
            line, summary = "ok", "ok. 1 passed; 0 failed"
        output = (
            f"\nrunning 1 test\ntest {TEST} ... {line}\n\n"
            f"test result: {summary}; 0 ignored; 0 measured; 10 filtered out; "
            "finished in 0.01s\n"
        )
        run = {
            "argv": ["python3", "-c", script],
            "output": output,
            "exit_code": code,
            "timed_out": False,
            "workspace_adopted": False,
            "isolation": "synthetic-isolation",
            "runtime_sha256": "1" * 64,
        }
        resources = {
            "tests/fixture.py": ("a" if index == 0 else "b") * 64,
            "src/checker.rs": ("c" if index < 2 else "d") * 64,
            "tests/expected.snap": ("e" if index < 2 else "f") * 64,
            "Cargo.lock": "9" * 64,
        }
        binary_hash = ("2" if index < 2 else "3") * 64
        receipts[phase] = {
            "observation": run,
            "runtime_sha256": "1" * 64,
            "isolation": "synthetic-isolation",
            "protected_hashes_before": resources,
            "protected_hashes_after": copy.deepcopy(resources),
            "workspace_execution_sha256_before": str(index + 4) * 64,
            "workspace_execution_sha256_after": str(index + 4) * 64,
            "protected_inputs_unchanged": True,
            "insta_update": "no",
            "insta_force_pass": "0",
            "binary_sha256": binary_hash,
            "actual_Rust_tests_executed": 1,
            "rust_passed": 0 if code else 1,
            "rust_failed": 1 if code else 0,
        }
        specs[phase] = {
            "binary_path": binary,
            "working_directory": "/workspace/crate",
            "binary_sha256": binary_hash,
        }
        outputs[phase] = hashlib.sha256(output.encode()).hexdigest()
    report["runs"] = {phase: r["observation"] for phase, r in receipts.items()}
    report["native_controls"] = {
        "schema": "rust-libtest-causal-controls-v1",
        "test_id": TEST,
        "phase_receipts": receipts,
        "phase_receipts_sha256": fingerprint(receipts),
        "expected_snapshots_regenerated": False,
        "execution_specs": specs,
        "output_sha256": outputs,
        "negative_panic": {"source_path": "src/checker.rs", "message": "unsupported async node"},
        "protected_resource_roles": {
            "fixtures": ["tests/fixture.py"],
            "implementation": ["src/checker.rs"],
            "expected_snapshots": ["tests/expected.snap"],
            "lockfile": "Cargo.lock",
        },
        "locked_dependencies": {
            "schema": "rust-locked-dependency-receipt-v1",
            "cargo_lock_unchanged": True,
            "offline_vendor_exit_code": 0,
            "cargo_lock_sha256": "9" * 64,
            "vendor_manifest_sha256": "a" * 64,
            "receipt_file_sha256": "b" * 64,
            "toolchain": "1.74.1-x86_64-unknown-linux-gnu",
            "vendor_packages": 5,
            "verified_vendor_files": 15,
        },
    }
    return report


def refresh_receipt_hashes(report):
    native = report["native_controls"]
    native["phase_receipts_sha256"] = fingerprint(native["phase_receipts"])
    native["output_sha256"] = {
        phase: hashlib.sha256(run["output"].encode()).hexdigest()
        for phase, run in report["runs"].items()
    }


def test_native_schema_retains_101_and_loads_one_canonical_source(tmp_path):
    report = native_report()
    validate_historical_qualification(report, source(), POLICY)
    (qualification,) = load_source_qualifications(
        write_inventory(tmp_path, source(), report), [source()], POLICY
    )
    assert [qualification.report["runs"][p]["exit_code"] for p in report["observations"]] == [
        0,
        101,
        0,
    ]
    assert qualification.to_dict()["purpose"].startswith("validation-only")
    assert qualification.report["checked_at"] > POLICY.cutoff


@pytest.mark.parametrize(
    "mutation",
    [
        "normalize_101",
        "wrong_test",
        "no_tests",
        "skipped",
        "missing_panic",
        "wrong_panic_site",
        "empty_output",
        "extra_execution",
        "alter_environment",
        "dynamic_argv",
        "timeout",
        "workspace_adoption",
        "workspace_changed",
        "protected_changed",
        "lock_changed",
        "snapshot_changed_in_regression",
        "implementation_changed_in_regression",
        "fixture_not_added",
        "fixed_fixture_differs",
        "no_repair",
        "binary_changed",
        "resource_role_overlap",
        "dependency_unlocked",
        "missing_vendor_hash",
        "toolchain_missing",
        "regenerated_snapshot",
        "receipt_hash",
        "output_hash",
    ],
)
def test_native_guard_rejects_defect_and_infrastructure_conflation(mutation):
    report = native_report()
    native = report["native_controls"]
    negative = report["runs"]["base_with_regression"]
    receipt = native["phase_receipts"]["base_with_regression"]
    if mutation == "normalize_101":
        negative["exit_code"] = 1
    elif mutation == "wrong_test":
        negative["output"] = negative["output"].replace(TEST, "rules::other")
    elif mutation == "no_tests":
        negative["output"] = negative["output"].replace("running 1 test", "running 0 tests")
    elif mutation == "skipped":
        negative["output"] = negative["output"].replace(
            "1 failed; 0 ignored", "0 failed; 1 ignored"
        )
    elif mutation == "missing_panic":
        negative["output"] = negative["output"].replace("unsupported async node", "linker failure")
    elif mutation == "wrong_panic_site":
        negative["output"] = negative["output"].replace(
            "src/checker.rs:1:1", "src/unrelated.rs:1:1"
        )
    elif mutation == "empty_output":
        negative["output"] = ""
    elif mutation == "extra_execution":
        negative["argv"][2] += ";print('unsupported confirmation')"
    elif mutation == "alter_environment":
        negative["argv"][2] = negative["argv"][2].replace("'no'", "'always'")
    elif mutation == "dynamic_argv":
        negative["argv"][2] = negative["argv"][2].replace(
            "subprocess.run([", "subprocess.run(list(["
        )
    elif mutation == "timeout":
        negative["timed_out"] = True
    elif mutation == "workspace_adoption":
        negative["workspace_adopted"] = True
    elif mutation == "workspace_changed":
        receipt["workspace_execution_sha256_after"] = "0" * 64
    elif mutation == "protected_changed":
        receipt["protected_hashes_after"]["tests/expected.snap"] = "0" * 64
    elif mutation in {
        "lock_changed",
        "snapshot_changed_in_regression",
        "implementation_changed_in_regression",
    }:
        path = {
            "lock_changed": "Cargo.lock",
            "snapshot_changed_in_regression": "tests/expected.snap",
            "implementation_changed_in_regression": "src/checker.rs",
        }[mutation]
        for field in ("protected_hashes_before", "protected_hashes_after"):
            receipt[field][path] = "0" * 64
    elif mutation == "fixture_not_added":
        for field in ("protected_hashes_before", "protected_hashes_after"):
            receipt[field]["tests/fixture.py"] = "a" * 64
    elif mutation in {"fixed_fixture_differs", "no_repair"}:
        fixed = native["phase_receipts"]["historical_fixed"]
        path, val = (
            ("tests/fixture.py", "0")
            if mutation == "fixed_fixture_differs"
            else ("src/checker.rs", "c")
        )
        for field in ("protected_hashes_before", "protected_hashes_after"):
            fixed[field][path] = val * 64
    elif mutation == "binary_changed":
        receipt["binary_sha256"] = "0" * 64
    elif mutation == "resource_role_overlap":
        native["protected_resource_roles"]["fixtures"] += ["src/checker.rs"]
    elif mutation == "dependency_unlocked":
        native["locked_dependencies"]["cargo_lock_unchanged"] = False
    elif mutation == "missing_vendor_hash":
        native["locked_dependencies"]["vendor_manifest_sha256"] = ""
    elif mutation == "toolchain_missing":
        native["locked_dependencies"]["toolchain"] = ""
    elif mutation == "regenerated_snapshot":
        native["expected_snapshots_regenerated"] = True
    refresh_receipt_hashes(report)
    if mutation == "receipt_hash":
        native["phase_receipts_sha256"] = "0" * 64
    if mutation == "output_hash":
        native["output_sha256"]["base_with_regression"] = "0" * 64
    with pytest.raises(ValueError):
        validate_historical_qualification(report, source(), POLICY)


def test_python_v1_cannot_be_reinterpreted_as_rust_by_normalization():
    report = report_for(source())
    report["runs"]["base_with_regression"]["exit_code"] = 101
    with pytest.raises(ValueError, match="causal outcomes"):
        validate_historical_qualification(report, source(), POLICY)
    validate_historical_qualification(report_for(source()), source(), POLICY)
