#!/usr/bin/env python3
"""Qualify held-out visible-test oracles before running coding agents."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from run_cross_project_holdout_agent_eval import (
    Case,
    _apply_visible_tests,
    _git_archive,
    _run_command,
    _safe_name,
    _write_json,
    load_cases,
)


def run_commands(commands: tuple[str, ...], cwd: Path, env: dict[str, str], timeout: int, directory: Path) -> list[dict]:
    results=[]
    for index, command in enumerate(commands, 1):
        result=_run_command(command, cwd=cwd, env=env, timeout_seconds=timeout, stdout_path=directory/f"{index:02d}.stdout", stderr_path=directory/f"{index:02d}.stderr")
        results.append(asdict(result))
        if result.returncode != 0:
            break
    return results


def functional_commands(commands: tuple[str, ...]) -> tuple[str, ...]:
    """Return commands that can actually falsify an implementation.

    ``git diff --check`` is useful as a hygiene check, but it is not a
    behavioural oracle: it passes for both the pre-change and post-change
    trees.  A holdout may be prepared with that check for diagnostics, but it
    must not enter the causal success denominator.
    """
    return tuple(
        command
        for command in commands
        if command.strip() and not command.strip().startswith("git diff --check")
    )


def first_command_failure(stage: str, results: list[dict]) -> str | None:
    """Describe the first failed prerequisite command for a qualification stage."""
    for result in results:
        returncode = int(result.get("returncode", 1))
        if returncode != 0:
            command = str(result.get("command", "<unknown command>"))
            return f"{stage} failed (exit {returncode}): {command}"
    return None


def oracle_blocker(
    case: Case,
    functional: tuple[str, ...],
    *,
    base_pre_patch_setup: list[dict],
    base_patch: object,
    base_setup: list[dict],
    base_tests: list[dict],
    solution_pre_patch_setup: list[dict],
    solution_setup: list[dict],
    solution_tests: list[dict],
) -> str | None:
    """Return why the visible-test oracle is not runnable on both snapshots.

    ``oracle_qualified`` is an infrastructure/readiness signal. A base test
    failure is expected for a useful holdout, while a failed dependency setup,
    patch application, or missing test execution means the oracle was never
    exercised and must not be reported as qualified.
    """
    if not case.visible_test_paths:
        return "no visible test path"
    if not case.test_patch_path.exists():
        return "visible test patch is missing"
    if not case.test_patch_path.read_text(encoding="utf-8").strip():
        return "visible test patch is empty"
    if not functional:
        return "no functional test command; hygiene-only checks are insufficient"

    stage_failures = (
        first_command_failure("base pre-patch setup", base_pre_patch_setup),
        (
            f"base visible test patch failed (exit {int(getattr(base_patch, 'returncode', 1))})"
            if int(getattr(base_patch, "returncode", 1)) != 0
            else None
        ),
        first_command_failure("base setup", base_setup),
        first_command_failure("solution pre-patch setup", solution_pre_patch_setup),
        first_command_failure("solution setup", solution_setup),
    )
    for failure in stage_failures:
        if failure:
            return failure
    if not base_tests:
        return "base functional tests were not executed"
    if not solution_tests:
        return "solution functional tests were not executed"
    return None


def qualify(case: Case, output: Path, workspace_root: Path) -> dict:
    row={"case_id":case.case_id,"repository":case.repository,"category":case.category,"base_ref":case.base_ref,"solution_ref":case.solution_ref}
    case_dir=output/"cases"/_safe_name(case.case_id)
    if case_dir.exists(): shutil.rmtree(case_dir)
    case_dir.mkdir(parents=True)
    env=os.environ.copy()
    base=workspace_root/_safe_name(case.case_id)/"base"
    solution=workspace_root/_safe_name(case.case_id)/"solution"
    for path in (base,solution):
        if path.exists(): shutil.rmtree(path)
    start=time.perf_counter()
    _git_archive(case.repository_path,case.base_ref,base)
    base_pre_patch_setup=run_commands(case.pre_patch_setup_commands,base,env,case.timeout_seconds,case_dir/"base-pre-patch-setup")
    base_patch=_apply_visible_tests(case,base,case_dir/"base-visible-tests")
    base_setup=run_commands(case.setup_commands,base,env,case.timeout_seconds,case_dir/"base-setup")
    functional = functional_commands(case.test_commands)
    base_tests=run_commands(functional,base,env,case.timeout_seconds,case_dir/"base-tests") if base_patch.returncode==0 and all(x["returncode"]==0 for x in base_pre_patch_setup) and all(x["returncode"]==0 for x in base_setup) and functional else []
    _git_archive(case.repository_path,case.solution_ref,solution)
    solution_pre_patch_setup=run_commands(case.pre_patch_setup_commands,solution,env,case.timeout_seconds,case_dir/"solution-pre-patch-setup")
    solution_setup=run_commands(case.setup_commands,solution,env,case.timeout_seconds,case_dir/"solution-setup")
    solution_tests=run_commands(functional,solution,env,case.timeout_seconds,case_dir/"solution-tests") if all(x["returncode"]==0 for x in solution_pre_patch_setup) and all(x["returncode"]==0 for x in solution_setup) and functional else []
    base_pass=bool(base_tests) and all(x["returncode"]==0 for x in base_tests)
    solution_pass=bool(solution_tests) and all(x["returncode"]==0 for x in solution_tests)
    blocker = oracle_blocker(
        case,
        functional,
        base_pre_patch_setup=base_pre_patch_setup,
        base_patch=base_patch,
        base_setup=base_setup,
        base_tests=base_tests,
        solution_pre_patch_setup=solution_pre_patch_setup,
        solution_setup=solution_setup,
        solution_tests=solution_tests,
    )
    oracle_qualified = blocker is None
    row.update({"base_pre_patch_setup":base_pre_patch_setup,"base_visible_test_patch":asdict(base_patch),"base_setup":base_setup,"base_tests":base_tests,"solution_pre_patch_setup":solution_pre_patch_setup,"solution_setup":solution_setup,"solution_tests":solution_tests,"base_passes":base_pass,"solution_passes":solution_pass,"oracle_qualified":oracle_qualified,"oracle_blocker":blocker,"qualified":(oracle_qualified and not base_pass and solution_pass),"wall_seconds":time.perf_counter()-start})
    _write_json(case_dir/"qualification.json",row)
    return row


def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--cases",type=Path,required=True)
    p.add_argument("--cases-root",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--workspace-root",type=Path,required=True)
    p.add_argument("--max-cases",type=int)
    p.add_argument("--repository", action="append", help="Only qualify cases from this repository; may be repeated")
    p.add_argument("--category", action="append", help="Only qualify cases from this category; may be repeated")
    args=p.parse_args()
    cases=load_cases(args.cases,args.cases_root)
    if args.repository:
        cases = [case for case in cases if case.repository in set(args.repository)]
    if args.category:
        cases = [case for case in cases if case.category in set(args.category)]
    if args.max_cases is not None: cases=cases[:max(0,args.max_cases)]
    args.output_dir.mkdir(parents=True,exist_ok=True); args.workspace_root.mkdir(parents=True,exist_ok=True)
    rows=[qualify(case,args.output_dir,args.workspace_root) for case in cases]
    report={"schema_version":"cross-project-heldout-qualification-v1","cases":len(rows),"qualified":sum(bool(row["qualified"]) for row in rows),"rows":rows}
    _write_json(args.output_dir/"qualification-report.json",report)
    print(json.dumps({"cases":len(rows),"qualified":report["qualified"]},ensure_ascii=False))
    return 0
if __name__=="__main__": raise SystemExit(main())
