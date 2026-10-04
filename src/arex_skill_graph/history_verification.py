"""Independent causal verification of a pre-cutoff historical repair.

These runs qualify historical sources. They are not formal SWE evaluations or
evidence that a model can repair a new issue. Verification time is recorded
separately from when the historical implementation/tests became public.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from .action_contracts import utc
from .adaptive_budget import BudgetCaps, BudgetLedger
from .adaptive_runner import TOOL_BACKENDS, make_namespace_tools
from .git_tree_export import exact_git_tar
from .history_census import fingerprint, now, redact_history, write_json
from .public_snapshot import extract_public_archive
from .skill_packages import _resolve


def archive_revision(repository, revision, destination):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("historical revision must be pinned")
    destination = Path(destination)
    if destination.exists():
        raise ValueError("historical verification checkout already exists")
    raw = exact_git_tar(["git", "--git-dir", str(repository)], revision)
    destination.mkdir(parents=True)
    extract_public_archive(raw, destination)


def split_test_diff(patch):
    production, tests, paths = [], [], []
    for section in re.split(r"(?=^diff --git )", patch, flags=re.MULTILINE):
        if not section.strip():
            continue
        match = re.match(r"diff --git a/(.*?) b/(.*?)\n", section)
        if not match or match[1] != match[2] or '"' in match[1]:
            raise ValueError("rename/quoted diff needs explicit historical verifier")
        path = match[2]
        _resolve(Path("/tmp/arex-contained-diff"), path)
        if any(p in {"test", "tests", "fixtures", "snapshots"} for p in Path(path).parts):
            tests.append(section)
            paths.append(path)
        else:
            production.append(section)
    return "".join(production), "".join(tests), paths


def junit_observations(path):
    if not Path(path).exists():
        return {}
    root = ET.parse(path).getroot()
    observations = {}
    for test in root.iter("testcase"):
        identity = test.attrib.get("classname", "") + "::" + test.attrib["name"]
        if identity in observations:
            raise ValueError("duplicate historical test identity")
        status = "passed"
        if test.find("failure") is not None or test.find("error") is not None:
            status = "failed"
        elif test.find("skipped") is not None:
            status = "skipped"
        observations[identity] = status
    return observations


def infer_historical_pytest_command(paths, repository_files):
    """Select actual test harnesses, never execute Pylint fixture files as tests."""
    files = set(repository_files)
    functional = [p for p in paths if p.startswith("tests/functional/")]
    targets = {
        p
        for p in paths
        if p.endswith(".py") and Path(p).name.startswith("test_") and p not in functional
    }
    if functional:
        if "tests/test_functional.py" not in files:
            raise ValueError("historical functional fixture layout requires an explicit verifier")
        # Existing cases beside each changed fixture are included as neighboring
        # controls. Selection depends on the pinned base tree, not solver results.
        directories = {Path(p).parent for p in functional}
        names = sorted(
            {Path(p).stem for p in functional if Path(p).suffix in {".py", ".txt", ".rc"}}
            | {
                Path(p).stem
                for p in files
                if Path(p).parent in directories and Path(p).suffix == ".py"
            }
        )
        if not names or any(not re.fullmatch(r"[A-Za-z0-9_]+", name) for name in names):
            raise ValueError("historical functional selector is unavailable or ambiguous")
        # Mixing unit tests with -k fixture names would silently deselect units.
        # Run their modules in full together with the functional harness instead.
        if targets:
            return ["python3", "-m", "pytest", *sorted(targets), "tests/test_functional.py", "-q"]
        return [
            "python3",
            "-m",
            "pytest",
            "tests/test_functional.py",
            "-k",
            " or ".join(names),
            "-q",
        ]
    if not targets:
        raise ValueError("historical test framework requires an explicit verifier command")
    return ["python3", "-m", "pytest", *sorted(targets), "-q"]


def verify_historical_repair(
    repository,
    metadata,
    issue_id,
    cutoff,
    output,
    dependency_root,
    command=None,
    *,
    sandbox_backend="namespace-bind",
):
    if sandbox_backend not in TOOL_BACKENDS:
        raise ValueError("unknown historical verification sandbox backend")
    output = Path(output)
    if utc(metadata["mergedAt"]) >= utc(cutoff):
        raise ValueError("historical repair was not public before cutoff")
    merged = metadata["mergeCommit"]
    base = merged["parents"]["nodes"][0]["oid"]
    for revision in (base, merged["oid"]):
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("historical verification requires pinned base and fix revisions")
        present = subprocess.run(
            ["git", "--git-dir", str(repository), "cat-file", "-e", revision + "^{commit}"],
            capture_output=True,
            check=False,
        )
        if present.returncode:
            raise ValueError(
                "historical base/fix object is missing from the prepared source repository"
            )
    expected = {
        "issue_id": issue_id,
        "pull_number": metadata["number"],
        "base_commit": base,
        "merge_commit": merged["oid"],
        "repair_available_at": metadata["mergedAt"],
        "cutoff_exclusive": cutoff,
    }
    if metadata.get("fix_id"):
        expected["fix_id"] = metadata["fix_id"]
    if metadata.get("resolution_relationship"):
        expected["resolution_relationship"] = metadata["resolution_relationship"]
        expected["resolution_relationship_evidence_refs"] = metadata.get(
            "resolution_relationship_evidence_refs", []
        )
    if sandbox_backend != "namespace-bind":
        expected["sandbox_backend"] = sandbox_backend
    report_path = output / "verification.json"
    if report_path.exists():
        saved = json.loads(report_path.read_text())
        if (
            saved["identity"] != expected
            or fingerprint(saved["observations"]) != saved["observations_sha256"]
        ):
            raise ValueError("historical verification checkpoint changed")
        return saved
    patch = subprocess.check_output(
        ["git", "--git-dir", str(repository), "diff", "--binary", base, merged["oid"]], text=True
    )
    production, tests, paths = split_test_diff(patch)
    if not production.strip() or not tests.strip():
        raise ValueError("repair lacks independently executable changed regression tests")
    if command is None:
        files = subprocess.check_output(
            ["git", "--git-dir", str(repository), "ls-tree", "-r", "--name-only", base], text=True
        ).splitlines()
        command = infer_historical_pytest_command(paths, files)
    output.mkdir(parents=True, exist_ok=True)
    observations, runs = {}, {}
    ledger = BudgetLedger(BudgetCaps(seconds=1800, tool_calls=20))
    runtime_hash = None
    for phase, revision in [
        ("original_base", base),
        ("base_with_regression", base),
        ("historical_fixed", merged["oid"]),
    ]:
        checkout = output / phase
        archive_revision(repository, revision, checkout)
        if phase == "base_with_regression":
            prior = {
                p: (checkout / p).read_bytes() if (checkout / p).exists() else None for p in paths
            }
            applied = subprocess.run(
                ["git", "-C", str(checkout), "apply", "--whitespace=nowarn", "-"],
                input=tests,
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "GIT_CEILING_DIRECTORIES": str(checkout.parent.resolve())},
            )
            if applied.returncode:
                raise ValueError("historical regression patch could not be applied")
            changed = {
                p: (checkout / p).read_bytes() if (checkout / p).exists() else None for p in paths
            }
            if any(prior[p] == changed[p] for p in paths):
                raise ValueError(
                    "historical test patch was ignored or did not change its declared files"
                )
        with make_namespace_tools(
            checkout, ledger, dependency_root, backend=sandbox_backend
        ) as tools:
            tools.preflight()
            runtime_hash = tools.runtime_sha256
            run = tools.run(
                [*command, "--junitxml=/workspace/verification-results.xml"], timeout=120
            )
        runs[phase] = run
        observations[phase] = junit_observations(checkout / "verification-results.xml")
    original, before, after = (
        observations[p] for p in ["original_base", "base_with_regression", "historical_fixed"]
    )
    f2p = sorted(k for k, v in before.items() if v == "failed" and after.get(k) == "passed")
    p2p = sorted(k for k, v in original.items() if v == "passed")
    verified = (
        runs["original_base"]["exit_code"] == 0
        and runs["base_with_regression"]["exit_code"] == 1
        and runs["historical_fixed"]["exit_code"] == 0
        and bool(f2p)
        and bool(p2p)
        and set(before) == set(after)
        and all(after.get(k) == "passed" for k in p2p)
        and all(v in {"passed", "skipped"} for v in after.values())
    )
    # Executable regression controls establish the repair artifact's effect.
    # A mention alone does not establish that it resolves this particular issue.
    relationship = metadata.get("resolution_relationship")
    related = (
        (
            relationship in {"direct_closure", "closing_reference"}
            and bool(metadata.get("resolution_relationship_evidence_refs"))
        )
        if relationship
        else None
    )
    source_verified = verified and related is not False
    report = {
        "schema": "historical-causal-verification-v1",
        "identity": expected,
        "checked_at": now(),
        "verified_resolution": source_verified,
        "historical_artifact_verified": verified,
        "issue_relationship_verified": related,
        "issue_relationship_requires_legacy_register_check": related is None,
        "qualification_scope": "changed-test-files-with-original-base-control",
        "runtime_sha256": runtime_hash,
        "command": command,
        "fail_to_pass": f2p,
        "pass_to_pass": p2p,
        "observations": observations,
        "observations_sha256": fingerprint(observations),
        "runs": runs,
        "whole_project_regression_checked": False,
        "formal_SWE_run": False,
        "verification_does_not_backdate_new_information": True,
    }
    write_json(report_path, report)
    write_json(
        output / "historical-diff.json",
        {
            "production_diff": redact_history(production),
            "regression_diff": redact_history(tests),
            "available_at": metadata["mergedAt"],
            "paths": paths,
        },
    )
    return report
