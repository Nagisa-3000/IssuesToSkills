#!/usr/bin/env python3
"""Prepare and behavior-calibrate native async scope lifecycle development cases.

This exposed historical source is for native Action definition acceptance only.
It cannot establish new-Issue transfer, a Pattern, KB promotion, or SWE gains.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import new_ledger, read_references
from arex_skill_graph.copied_sandbox import CopiedNamespaceTools
from arex_skill_graph.git_tree_export import exact_git_tar
from arex_skill_graph.history_census import write_json
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.public_snapshot import extract_public_archive
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workspace_state import public_workspace_sha256

BASE = "eb950615d77a6b979af6e0d9954fdb4197f4a722"
FIX = "660405e6218258cee90570e8037c3b5e1440dcb6"
WORKFLOW = "workflow:verified-history:9a2315892fecfccf9d5c6c14"
ACTION = WORKFLOW + ":inspect"
RUNTIME_SHA256 = "eee998d7c1d7da5741652022ce4ac3dd5875190009a9ae99784d0a341e0e90b1"
PROBE = 'import hashlib, inspect, io, json, sys, tempfile, traceback\nfrom contextlib import redirect_stderr, redirect_stdout\nfrom pathlib import Path\nimport astroid\nfrom pylint.lint import Run\nfrom pylint.extensions.redefined_variable_type import MultipleTypesChecker\nfrom pylint.utils.ast_walker import ASTWalker\n\nCODES = {\n    "separate_async_functions": "async def first():\\n    reused = []\\n    return reused\\n\\nasync def second():\\n    reused = {}\\n    return reused\\n",\n    "separate_async_methods": "class Example:\\n    async def first(self):\\n        reused = 1\\n        return reused\\n\\n    async def second(self):\\n        reused = {}\\n        return reused\\n",\n    "separate_sync_functions": "def first():\\n    reused = []\\n    return reused\\n\\ndef second():\\n    reused = {}\\n    return reused\\n",\n    "separate_sync_methods": "class Example:\\n    def first(self):\\n        reused = 1\\n        return reused\\n\\n    def second(self):\\n        reused = {}\\n        return reused\\n",\n    "within_async_function": "async def first():\\n    reused = []\\n    reused = {}\\n    return reused\\n",\n    "within_sync_function": "def first():\\n    reused = []\\n    reused = {}\\n    return reused\\n",\n    "within_class": "class Example:\\n    reused = []\\n    reused = {}\\n",\n    "within_module": "reused = []\\nreused = {}\\n",\n    "separate_classes": "class First:\\n    reused = []\\n\\nclass Second:\\n    reused = {}\\n",\n}\nQUIET = {name for name in CODES if name.startswith("separate_")}\nPOSITIVE = set(CODES) - QUIET\nRESOURCES = (\n    "pylint/extensions/redefined_variable_type.py",\n    "pylint/utils/ast_walker.py",\n    "tests/functional/ext/redefined_variable_type/redefined_variable_type.py",\n    "tests/functional/ext/redefined_variable_type/redefined_variable_type.txt",\n    "tests/test_functional.py",\n)\ndef hashes():\n    return {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in RESOURCES}\nbefore = hashes()\nhooks = {}\nfor name in ("visit_asyncfunctiondef", "leave_asyncfunctiondef"):\n    sync = name.replace("asyncfunctiondef", "functiondef")\n    hook = getattr(MultipleTypesChecker, name, None)\n    hooks[name] = {"present": hook is not None,\n                   "same_as_sync": hook is not None and hook is getattr(MultipleTypesChecker, sync, None)}\nstdout, stderr = io.StringIO(), io.StringIO()\nrecords, exception = {}, None\ntry:\n    with tempfile.TemporaryDirectory(prefix="public-async-scope-probe-") as directory:\n        paths = []\n        for name, code in CODES.items():\n            path = Path(directory) / (name + ".py")\n            path.write_text(code)\n            paths.append(str(path))\n        with redirect_stdout(stdout), redirect_stderr(stderr):\n            run = Run(["--load-plugins=pylint.extensions.redefined_variable_type",\n                       "--disable=all", "--enable=redefined-variable-type",\n                       "--output-format=json", "--reports=no", "--score=no",\n                       "--persistent=no", "--jobs=1", *paths], do_exit=False)\n        diagnostics = json.loads(stdout.getvalue())\n        if not isinstance(diagnostics, list):\n            raise ValueError("Pylint JSON diagnostics are not a list")\n        for name in CODES:\n            records[name] = {"diagnostics": [\n                {key: d[key] for key in ("symbol", "message", "line", "column", "obj")}\n                for d in diagnostics if Path(d["path"]).stem == name\n            ]}\n        recognized = [d for d in diagnostics if Path(d["path"]).stem in CODES]\n        if len(recognized) != len(diagnostics):\n            raise ValueError("unexpected diagnostic source outside public probe cases")\n        lint_status = run.linter.msg_status\nexcept Exception as exc:\n    exception = {"type": type(exc).__name__, "detail": str(exc), "trace": traceback.format_exc()}\n    lint_status = None\nafter = hashes()\ncomplete = exception is None and set(records) == set(CODES)\nmatches = complete and all(not records[name]["diagnostics"] for name in QUIET)\nmatches = matches and all(\n    len(records[name]["diagnostics"]) == 1\n    and records[name]["diagnostics"][0]["symbol"] == "redefined-variable-type"\n    for name in POSITIVE\n)\nresult = {\n    "schema": "public-async-lifecycle-observation-v1",\n    "runtime": sys.version, "astroid_version": astroid.__version__,\n    "owner": "MultipleTypesChecker", "hooks": hooks,\n    "owner_source": inspect.getsource(MultipleTypesChecker),\n    "dispatcher_source": inspect.getsource(ASTWalker),\n    "cases": records, "lint_status": lint_status,\n    "stderr": stderr.getvalue(), "exception": exception,\n    "preservation": {"before": before, "after": after, "unchanged": before == after},\n    "expected_quiet": sorted(QUIET), "expected_positive": sorted(POSITIVE),\n    "matches_current_public_behavior_spec": bool(matches),\n}\nprint(json.dumps(result))\nraise SystemExit(0 if matches and before == after else 1)\n'
SUITE = [
    "python3",
    "-B",
    "-m",
    "pytest",
    "tests/test_functional.py",
    "-k",
    "redefined_variable_type or regression_newtype_fstring",
    "-q",
    "-p",
    "no:cacheprovider",
]
PROBE_COMMAND = ["python3", "-B", "public-async-lifecycle-probe.py"]
CODE_PATHS = {
    "checker": "pylint/extensions/redefined_variable_type.py",
    "dispatcher": "pylint/utils/ast_walker.py",
    "fixture": "tests/functional/ext/redefined_variable_type/redefined_variable_type.py",
    "expectations": "tests/functional/ext/redefined_variable_type/redefined_variable_type.txt",
    "suite": "tests/test_functional.py",
    "probe": "public-async-lifecycle-probe.py",
}
QUIET_CASES = {
    "separate_async_functions",
    "separate_async_methods",
    "separate_sync_functions",
    "separate_sync_methods",
    "separate_classes",
}
POSITIVE_CASES = {"within_async_function", "within_sync_function", "within_class", "within_module"}


def export(repository, revision, target):
    target.mkdir()
    git = ["git", "-c", "safe.directory=" + str(repository), "-C", str(repository)]
    extract_public_archive(exact_git_tar(git, revision), target)


def pin_public_fixture(root):
    git = ["git", "-C", str(root)]
    for command in [
        ["init", "-q"],
        ["-c", "core.autocrlf=false", "add", "--force", "--all"],
        [
            "-c",
            "user.name=AREX development fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-q",
            "-m",
            "Pin exposed public async lifecycle development fixture",
        ],
    ]:
        subprocess.run([*git, *command], check=True, capture_output=True)
    return subprocess.check_output([*git, "rev-parse", "HEAD"], text=True).strip()


def dispatch_control(source):
    needle = "        cid = astroid.__class__.__name__.lower()"
    if source.count(needle) != 1:
        raise ValueError("control requires one exact current dispatch site")
    return source.replace(
        needle,
        needle
        + '\n        if cid == "asyncfunctiondef":'
        + '\n            cid = "controlled_async_dispatch_gap"',
    )


def parse_probe(observation):
    if observation.get("timed_out") or observation.get("exit_code") not in {0, 1}:
        raise ValueError("probe did not produce a behavioral observation")
    records = []
    for line in observation["output"].splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(value, dict)
            and value.get("schema") == "public-async-lifecycle-observation-v1"
        ):
            records.append(value)
    if len(records) != 1:
        raise ValueError("probe requires exactly one complete structured observation")
    result = records[0]
    if result.get("exception") or set(result.get("cases", {})) != QUIET_CASES | POSITIVE_CASES:
        raise ValueError("public scope cases are incomplete or exceptional")
    if not result.get("preservation", {}).get("unchanged"):
        raise ValueError("probe changed source or expectation files")
    return result


def diagnostic_signature(probe, name):
    return [
        (d["symbol"], d["line"], d["column"], d["obj"], d["message"])
        for d in probe["cases"][name]["diagnostics"]
    ]


def validate_calibration(observations):
    probes = {
        row["case_id"]: parse_probe(row)
        for row in observations
        if row["scope"] == "public-scope-counterparts"
    }
    if set(probes) != {"q0", "q1", "q2"}:
        raise ValueError("calibration requires all three executable controls")
    for ident in ("q0", "q2"):
        if not all(
            probes[ident]["cases"][name]["diagnostics"]
            for name in ("separate_async_functions", "separate_async_methods")
        ):
            raise ValueError("causal or dispatcher control lost the async fault")
        if any(
            probes[ident]["cases"][name]["diagnostics"]
            for name in ("separate_sync_functions", "separate_sync_methods", "separate_classes")
        ):
            raise ValueError("control unexpectedly breaks synchronous or class isolation")
    if any(row["present"] for row in probes["q0"]["hooks"].values()):
        raise ValueError("base no longer has omitted async hooks")
    if not all(
        row["present"] and row["same_as_sync"]
        for ident in ("q1", "q2")
        for row in probes[ident]["hooks"].values()
    ):
        raise ValueError(
            "already-fixed and dispatcher controls must retain both hook registrations"
        )
    if not probes["q1"]["matches_current_public_behavior_spec"]:
        raise ValueError("fixed control does not satisfy the complete public behavior spec")
    for name in POSITIVE_CASES:
        signatures = [diagnostic_signature(probes[ident], name) for ident in ("q0", "q1", "q2")]
        if len(signatures[0]) != 1 or len({json.dumps(x) for x in signatures}) != 1:
            raise ValueError("positive diagnostic preservation is not stable")
    suites = [row for row in observations if row["scope"] == "affected-public-suite"]
    if len(suites) != 3 or {row["case_id"] for row in suites} != {"q0", "q1", "q2"}:
        raise ValueError("affected suite requires all three preparation controls")
    expected_exits = {"q0": 0, "q1": 0, "q2": 1}
    if any(
        row.get("timed_out") or row.get("exit_code") != expected_exits[row["case_id"]]
        for row in suites
    ):
        raise ValueError("affected suite did not observe the intended passing and failing controls")
    runtimes = {row["runtime_sha256"] for row in observations}
    if runtimes != {RUNTIME_SHA256}:
        raise ValueError("calibration runtime differs from the qualified historical runtime")
    return {
        "actually_executed_cases": sorted(probes),
        "actual_commands": len(observations),
        "public_scope_cases_per_probe": len(QUIET_CASES | POSITIVE_CASES),
        "positive_preservation_cases": sorted(POSITIVE_CASES),
        "runtime_sha256": RUNTIME_SHA256,
        "read_only_snapshots_unchanged": True,
        "actual_model_calls": 0,
        "authored_Action_executed": False,
        "formal_SWE_runs": 0,
    }


def current_oracles():
    instructions = {
        "confirm-leakage-mechanism": (
            "Actually execute the public probe. Inspect both checker hooks and the real dispatch site; "
            "compare separate async functions/methods, synchronous counterparts, and positive same-scope, "
            "class and module diagnostics. Review occurrence is distinct from causal confirmation. "
            "Already-present hook parity makes missing-async-lifecycle-confirmed FAIL; a broken dispatcher "
            "makes async-dispatch-binding-confirmed FAIL. Unavailable execution stays UNKNOWN."
        ),
        "review-hook-parity": (
            "Execute the probe and inspect the current checker diff. Both async entry and exit must "
            "use the established synchronous lifecycle; retain synchronous, class/module and diagnostic "
            "behavior. Do not change dispatcher or weaken diagnostics. This is post-edit evidence."
        ),
        "review-regression-coverage": (
            "Inspect the bound current fixture and expected-output file; new separate async functions "
            "and methods must reuse local names with different types without accepting cross-scope "
            "warnings. Retain the existing positive diagnostic expectations. Run the focused suite."
        ),
        "run-checker-regressions": (
            "Execute the focused public functional suite; require actual successful results and "
            "unchanged positive expectations after checker and fixture edits. Inspect the final diff."
        ),
        "compare-public-scope-cases": (
            "Actually execute all nine public scope cases. Require no separate-scope warnings, one "
            "expected redefined-variable-type diagnostic for each within-async, within-sync, class and "
            "module case, both registered async hooks, and retained current source/expectation hashes."
        ),
    }
    actions = {
        "confirm-leakage-mechanism": "inspect",
        "review-hook-parity": "repair",
        "review-regression-coverage": "regressions",
        "run-checker-regressions": "validate",
        "compare-public-scope-cases": "validate",
    }
    return [
        {
            "action_id": WORKFLOW + ":" + actions[ident],
            "source_oracle_id": ident,
            "instruction": instruction,
            "command": SUITE
            if ident in {"review-regression-coverage", "run-checker-regressions"}
            else PROBE_COMMAND,
            "evidence_refs": [
                "current:public-probe-spec",
                "current:code:probe",
                "current:code:suite",
            ],
        }
        for ident, instruction in instructions.items()
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source-root", "references", "dependency-root", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    if os.geteuid() != 0:
        parser.error("actual namespace-copy calibration requires the authorized privileged broker")
    if args.output_dir.exists():
        raise ValueError("preserve old development fixtures; use a new output version")
    matches = [
        load_native_package(ref, TemporalPolicy("2024-01-01T00:00:00Z"))
        for ref in read_references(args.references)
    ]
    matches = [p for p in matches if any(a.id == ACTION for a in p.actions)]
    if len(matches) != 1:
        raise ValueError("fixture requires one authoritative native inspection Action")
    package = matches[0]
    if {a.id for a in package.actions} != {
        WORKFLOW + ":" + x for x in ("inspect", "repair", "regressions", "validate")
    }:
        raise ValueError("native package's four Action identities changed")
    args.output_dir.mkdir(parents=True)
    problem = (
        "Perform only the supplied native async lifecycle inspect Action on this exposed public "
        "development checkout. Do not repair or edit tracked source or expected diagnostics. "
        "Bind the current checker, dispatcher, fixture and public test entry point. Execute the "
        "public scope counterparts and inspect state ownership to decide whether missing async "
        "entry/exit hooks cause cross-scope type warnings. Record review and binding effects "
        "separately from missing-async-lifecycle-confirmed and async-dispatch-binding-confirmed. "
        "Use PASS/FAIL/UNKNOWN honestly; existing hooks, broken dispatch, legitimate within-scope "
        "warnings or unavailable observations must not authorize missing-hook repair. "
        "This is source-definition development, not a new Issue or formal SWE task."
    )
    cases = []
    for ident, revision, variant in [
        ("q0", BASE, "historical-missing-async-hooks"),
        ("q1", FIX, "already-fixed-hooks"),
        ("q2", FIX, "controlled-current-dispatcher-fault"),
        ("q3", BASE, "controlled-execution-unavailable"),
    ]:
        checkout = args.output_dir / (ident + "-checkout")
        export(args.source_root.resolve(), revision, checkout)
        if ident == "q2":
            path = checkout / CODE_PATHS["dispatcher"]
            path.write_text(dispatch_control(path.read_text()))
        (checkout / CODE_PATHS["probe"]).write_text(PROBE)
        head = pin_public_fixture(checkout)
        anchors = [
            {
                "id": "current:public-probe-spec",
                "kind": "public_issue",
                "observation": problem,
                "base_commit": head,
            }
        ]
        for role, relative in CODE_PATHS.items():
            anchors.append(
                {
                    "id": "current:code:" + role,
                    "kind": "current_code",
                    "base_commit": head,
                    "observation": "Current public development fixture resource: " + relative,
                    "path": relative,
                    "sha256": hashlib.sha256((checkout / relative).read_bytes()).hexdigest(),
                }
            )
        task = TaskContext.from_dict(
            {
                "task_id": "native-action-exercise:async-lifecycle:" + ident,
                "repository": "pylint-dev/pylint",
                "base_commit": head,
                "root": str(checkout.resolve()),
                "public_problem": problem,
                "input_available_at": datetime.now(timezone.utc).isoformat(),
                "anchors": anchors,
                "facts": [
                    {
                        "key": "public-current-base-pinned",
                        "value": True,
                        "evidence_refs": ["current:public-probe-spec"],
                    },
                    {
                        "key": "current-public-oracles-bound",
                        "value": True,
                        "evidence_refs": [
                            "current:public-probe-spec",
                            "current:code:probe",
                            "current:code:suite",
                        ],
                    },
                ],
                "checks": [],
                "bindings": [],
                "port_values": [],
                "goals": [],
                "environment": [],
                "revision": 0,
                "oracles": current_oracles(),
            }
        )
        task.verify()
        task_path = args.output_dir / (ident + "-task.json")
        write_json(task_path, task.to_dict())
        snapshot = args.output_dir / (ident + "-calibration-public")
        export(checkout, head, snapshot)
        if public_workspace_sha256(checkout) != public_workspace_sha256(snapshot):
            raise ValueError("synthetic public Git commit omitted or changed exported source files")
        cases.append(
            {
                "opaque_id": ident,
                "variant": variant,
                "source_revision": revision,
                "task_context": str(task_path.resolve()),
                "task_context_sha256": hashlib.sha256(task_path.read_bytes()).hexdigest(),
                "base_commit": head,
                "public_snapshot": str(snapshot.resolve()),
                "output_dir": str((args.output_dir / (ident + "-output")).resolve()),
                "probe_execution_unavailable": ident == "q3",
            }
        )
    observations = []
    write_json(
        args.output_dir / "preparation-progress.json",
        {"phase": "calibrating_public_controls", "actual_model_calls": 0},
    )
    tools = CopiedNamespaceTools(
        Path(cases[0]["public_snapshot"]), new_ledger(tokenizer="cl100k_base"), args.dependency_root
    )
    try:
        for case in cases[:3]:
            tools.checkout = Path(case["public_snapshot"])
            before = public_workspace_sha256(tools.checkout)
            for scope, command in [
                ("public-scope-counterparts", PROBE_COMMAND),
                ("affected-public-suite", SUITE),
            ]:
                result = tools.run(command, timeout=120, readonly_workspace=True)
                observations.append({"case_id": case["opaque_id"], "scope": scope, **result})
                write_json(args.output_dir / "calibration-observations.json", observations)
                if result.get("timed_out") or result.get("exit_code") not in {0, 1}:
                    raise ValueError("calibration unavailable or not a behavioral observation")
            if before != public_workspace_sha256(tools.checkout):
                raise ValueError("read-only calibration altered the public workspace")
    finally:
        tools.close()
    summary = validate_calibration(observations)
    write_json(args.output_dir / "calibration-summary.json", summary)
    write_json(
        args.output_dir / "dispatch-manifest.json",
        {
            "schema": "native-async-lifecycle-functional-dispatch-v1",
            "action_id": ACTION,
            "package_sha256": package.reference["package_sha256"],
            "references": str(args.references.resolve()),
            "dependency_root": str(args.dependency_root.resolve()),
            "cases": cases,
            "historical_source_definition_exercise": True,
            "source_project_count": 1,
            "same_model_family_limit": True,
            "formal_SWE_runs": 0,
            "formal_KB_admitted": False,
            "fixture_behavior_calibrated": True,
            "actual_model_calls": 0,
            "authored_Action_executed": False,
            "functional_case_validation_complete": False,
            "unavailable_case_actual_probe_execution": False,
        },
    )
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
