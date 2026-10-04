#!/usr/bin/env python3
"""Prepare and actually calibrate native overload inspection fixtures without LLM calls."""

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.adaptive_cli import new_ledger, read_references
from arex_skill_graph.copied_sandbox import CopiedNamespaceTools
from arex_skill_graph.git_tree_export import exact_git_tar
from arex_skill_graph.history_census import write_json
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workspace_state import public_workspace_sha256

BASE = "5ed30a6b9e4b9c1bb4042e5c5b3b506e52133da4"
FIX = "ee1eb0670a473a30f32208b7bd811282834486a6"
ACTION = "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-inspect"

PROBE = r"""
import ast, hashlib, inspect, json, sys, traceback
import pyflakes.checker as implementation
original = implementation.is_typing_overload
traces = []
def observed(value, scopes):
    result = original(value, scopes)
    family = (ast.FunctionDef,) + ((ast.AsyncFunctionDef,) if hasattr(ast, "AsyncFunctionDef") else ())
    if isinstance(value.source, family):
        bindings = [
            {"scope": type(scope).__name__, "name": "overload",
             "binding_class": type(scope["overload"]).__name__,
             "full_name": getattr(scope["overload"], "fullName", None)}
            for scope in reversed(scopes) if "overload" in scope
        ]
        traces.append({"function": value.name, "node_kind": type(value.source).__name__,
                       "decorators": [ast.dump(d) for d in value.source.decorator_list],
                       "typing_bindings": bindings, "recognizer_result": result})
    return result
implementation.is_typing_overload = observed
codes = {
    "ordinary": "from typing import overload\n@overload\ndef f(s):\n    # type: (None) -> None\n    pass\n@overload\ndef f(s):\n    # type: (int) -> int\n    pass\ndef f(s):\n    return s\n",
    "asynchronous": "from typing import overload\n@overload\nasync def g(s):\n    # type: (None) -> None\n    pass\n@overload\nasync def g(s):\n    # type: (int) -> int\n    pass\nasync def g(s):\n    return s\n",
    "ordinary_control": "def h(s):\n    pass\n\ndef h(s):\n    return s\n",
}
paths = ("pyflakes/checker.py", "pyflakes/test/test_type_annotations.py")
before = {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in paths}
print(json.dumps({"record": "runtime-and-policy", "runtime": sys.version,
                  "PY35_PLUS": implementation.PY35_PLUS,
                  "supported_async_ast": hasattr(ast, "AsyncFunctionDef"),
                  "function_family": [c.__name__ for c in getattr(implementation, "FUNCTION_TYPES", ())],
                  "recognizer_source": inspect.getsource(original)}))
failed = False
for name, code in codes.items():
    traces[:] = []
    try:
        checker = implementation.Checker(ast.parse(code), filename="<public-overload-probe>")
        diagnostics = [{"class": type(m).__name__, "line": m.lineno,
                        "column": getattr(m, "col", None), "message": str(m)}
                       for m in checker.messages]
        print(json.dumps({"record": "counterpart", "case": name,
                          "diagnostics": diagnostics, "recognizer_trace": traces,
                          "exception": None}))
        if name != "ordinary_control":
            failed = failed or bool(diagnostics)
    except Exception as exc:
        failed = True
        print(json.dumps({"record": "counterpart", "case": name,
                          "exception": type(exc).__name__, "detail": str(exc),
                          "trace": traceback.format_exc()}))
after = {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in paths}
print(json.dumps({"record": "preservation", "before": before, "after": after,
                  "source_and_expectations_unchanged": before == after}))
raise SystemExit(1 if failed else 0)
""".lstrip()


def export(repository, revision, target):
    target.mkdir()
    git = ["git", "-c", "safe.directory=" + str(repository), "-C", str(repository)]
    with tarfile.open(fileobj=io.BytesIO(exact_git_tar(git, revision)), mode="r") as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not member.isfile():
                raise ValueError("fixture export requires closed regular public files")
        archive.extractall(target, filter="fully_trusted")  # Closed regular files only.


def git_commit(root):
    argv = ["git", "-C", str(root)]
    for command in [
        ["init", "-q"],
        ["add", "--all"],
        [
            "-c",
            "user.name=AREX development fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-q",
            "-m",
            "Pin public native overload development fixture",
        ],
    ]:
        subprocess.run([*argv, *command], check=True, capture_output=True)
    return subprocess.check_output([*argv, "rev-parse", "HEAD"], text=True).strip()


def counterpart_records(result):
    records = []
    for line in result["output"].splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return {r["case"]: r for r in records if r.get("record") == "counterpart"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source-root", "references", "dependency-root", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    if os.geteuid() != 0:
        parser.error(
            "actual copied-namespace calibration requires the authorized privileged broker"
        )
    if args.output_dir.exists():
        raise ValueError("preserve existing development fixtures; use a new version")
    matches = []
    for reference in read_references(args.references):
        candidate_package = load_native_package(reference, TemporalPolicy("2024-01-01T00:00:00Z"))
        if any(action.id == ACTION for action in candidate_package.actions):
            matches.append(candidate_package)
    if len(matches) != 1:
        raise ValueError("fixture must identify one authoritative native Action")
    package = matches[0]
    args.output_dir.mkdir(parents=True)
    specs = [
        ("q0", BASE, "causal-function-kind-omission"),
        ("q1", FIX, "already-async-aware"),
        ("q2", FIX, "controlled-decorator-identity-fault"),
        ("q3", BASE, "controlled-probe-execution-unavailable"),
    ]
    public_problem = (
        "Perform only the supplied native overload-inspect Action on this current public checkout. "
        "Do not repair or modify source or diagnostic expectations. Execute the bound public "
        "ordinary/asynchronous typing-overload sequences and ordinary redefinition control; "
        "inspect decorator identity, source-node classification, runtime policy and existing coverage. "
        "Record overload-review only when actual evidence establishes supported causal classification "
        "omission. Contrary or unavailable causal evidence must not produce confirmed context. "
        "Additional read-only inspection is allowed. This is a native definition development exercise."
    )
    cases = []
    for case_id, revision, variant in specs:
        checkout = args.output_dir / (case_id + "-checkout")
        export(args.source_root.resolve(), revision, checkout)
        if case_id == "q2":
            path = checkout / "pyflakes/checker.py"
            source = path.read_text()
            start = source.index("def is_typing_overload(value, scope_stack):")
            end = source.index("\ndef make_tokens(", start)
            segment = source[start:end]
            if segment.count("'typing.overload'") != 1:
                raise ValueError("decorator control no longer identifies a single name predicate")
            changed = segment.replace("'typing.overload'", "'typing.overload_unrecognized'")
            path.write_text(source[:start] + changed + source[end:])
        (checkout / "public-overload-probe.py").write_text(PROBE)
        head = git_commit(checkout)
        anchors = [
            {
                "id": "current:public-probe-spec",
                "kind": "public_issue",
                "observation": public_problem,
                "base_commit": head,
            }
        ]
        for suffix, path in [
            ("checker", "pyflakes/checker.py"),
            ("tests", "pyflakes/test/test_type_annotations.py"),
            ("probe", "public-overload-probe.py"),
        ]:
            anchors.append(
                {
                    "id": "current:code:" + suffix,
                    "kind": "current_code",
                    "observation": "Current public development fixture resource: " + path,
                    "base_commit": head,
                    "path": path,
                    "sha256": hashlib.sha256((checkout / path).read_bytes()).hexdigest(),
                }
            )
        task = TaskContext.from_dict(
            {
                "task_id": "native-action-exercise:overload:" + case_id,
                "repository": "PyCQA/pyflakes",
                "base_commit": head,
                "root": str(checkout.resolve()),
                "public_problem": public_problem,
                "input_available_at": datetime.now(timezone.utc).isoformat(),
                "anchors": anchors,
                "facts": [
                    {
                        "key": "public-inspection-oracles-bound",
                        "value": True,
                        "evidence_refs": ["current:public-probe-spec", "current:code:probe"],
                    }
                ],
                "checks": [],
                "bindings": [],
                "port_values": [],
                "goals": [],
                "environment": [],
                "revision": 0,
                "oracles": [
                    {
                        "action_id": ACTION,
                        "source_oracle_id": "confirm-overload-omission",
                        "instruction": "Execute the public counterparts and control, inspect the current "
                        "recognizer, node-family and runtime policy. Confirm context only "
                        "when correct decorator identity and an omitted supported async "
                        "node kind explain sync acceptance and async rejection. Already "
                        "correct classification, decorator defects or unavailable causal "
                        "observations prevent confirmation.",
                        "command": ["python3", "-B", "public-overload-probe.py"],
                        "evidence_refs": ["current:public-probe-spec", "current:code:probe"],
                    }
                ],
            }
        )
        task.verify()
        task_path = args.output_dir / (case_id + "-task.json")
        write_json(task_path, task.to_dict())
        snapshot = args.output_dir / (case_id + "-calibration-public")
        export(checkout, head, snapshot)
        cases.append(
            {
                "opaque_id": case_id,
                "variant": variant,
                "source_revision": revision,
                "task_context": str(task_path.resolve()),
                "task_context_sha256": hashlib.sha256(task_path.read_bytes()).hexdigest(),
                "base_commit": head,
                "public_snapshot": str(snapshot.resolve()),
                "output_dir": str((args.output_dir / (case_id + "-output")).resolve()),
                "probe_execution_unavailable": case_id == "q3",
            }
        )
    ledger = new_ledger(tokenizer="cl100k_base")
    observations = []
    tools = CopiedNamespaceTools(Path(cases[0]["public_snapshot"]), ledger, args.dependency_root)
    try:
        for case in cases[:3]:
            tools.checkout = Path(case["public_snapshot"])
            before = public_workspace_sha256(tools.checkout)
            for scope, command in [
                ("public-counterparts-and-control", ["python3", "-B", "public-overload-probe.py"]),
                (
                    "affected-annotation-suite",
                    ["python3", "-B", "-m", "unittest", "pyflakes.test.test_type_annotations"],
                ),
            ]:
                result = tools.run(command, timeout=90, readonly_workspace=True)
                if result.get("timed_out") or result.get("exit_code") not in {0, 1}:
                    raise ValueError("calibration unavailable or not a behavioral observation")
                observations.append({"case_id": case["opaque_id"], "scope": scope, **result})
            if before != public_workspace_sha256(tools.checkout):
                raise ValueError("read-only behavior calibration changed its public checkout")
    finally:
        tools.close()
    targets = {
        r["case_id"]: counterpart_records(r)
        for r in observations
        if r["scope"] == "public-counterparts-and-control"
    }
    if any(
        set(records) != {"ordinary", "asynchronous", "ordinary_control"}
        or any(record.get("exception") for record in records.values())
        for records in targets.values()
    ):
        raise ValueError("public fixture produced incomplete or exceptional counterparts")
    if targets["q0"]["ordinary"]["diagnostics"] or not targets["q0"]["asynchronous"]["diagnostics"]:
        raise ValueError("base does not establish the claimed sync/async contrast")
    if any(targets["q1"][kind]["diagnostics"] for kind in ("ordinary", "asynchronous")):
        raise ValueError("already-correct control does not accept both counterparts")
    if not all(targets["q2"][kind]["diagnostics"] for kind in ("ordinary", "asynchronous")):
        raise ValueError("decorator-fault control does not reject both counterparts")

    def signature(records):
        return [
            (d["class"], d["line"], d["column"]) for d in records["ordinary_control"]["diagnostics"]
        ]

    controls = {case_id: signature(records) for case_id, records in targets.items()}
    if not controls["q0"] or len({json.dumps(value) for value in controls.values()}) != 1:
        raise ValueError("ordinary preservation control baseline is not stable")
    manifest = {
        "schema": "native-overload-inspection-functional-dispatch-v1",
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
    }
    write_json(args.output_dir / "dispatch-manifest.json", manifest)
    write_json(args.output_dir / "calibration-observations.json", observations)
    write_json(
        args.output_dir / "calibration-summary.json",
        {
            "schema": "native-overload-fixture-behavior-calibration-v1",
            "case_ids_actually_executed": ["q0", "q1", "q2"],
            "actual_commands": len(observations),
            "ordinary_control_signatures": controls,
            "runtime_sha256": observations[0]["runtime_sha256"],
            "read_only_snapshots_unchanged": True,
            "unavailable_case_is_pending_control_policy": True,
            "authored_Action_executed": False,
            "actual_model_calls": 0,
            "formal_SWE_runs": 0,
        },
    )
    print(
        json.dumps(
            {
                "prepared_cases": len(cases),
                "behavior_calibrated_cases": 3,
                "actual_commands": len(observations),
                "actual_model_calls": 0,
                "authored_Action_executed": False,
                "formal_SWE_runs": 0,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
