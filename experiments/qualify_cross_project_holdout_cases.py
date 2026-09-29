#!/usr/bin/env python3
"""Qualify held-out visible-test oracles before running coding agents."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from run_cross_project_holdout_agent_eval import Case, _apply_visible_tests, _git_archive, _run_command, _safe_name, load_cases, _write_json


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
    base_patch=_apply_visible_tests(case,base,case_dir/"base-visible-tests")
    base_setup=run_commands(case.setup_commands,base,env,case.timeout_seconds,case_dir/"base-setup")
    functional = functional_commands(case.test_commands)
    base_tests=run_commands(functional,base,env,case.timeout_seconds,case_dir/"base-tests") if base_patch.returncode==0 and all(x["returncode"]==0 for x in base_setup) and functional else []
    _git_archive(case.repository_path,case.solution_ref,solution)
    solution_setup=run_commands(case.setup_commands,solution,env,case.timeout_seconds,case_dir/"solution-setup")
    solution_tests=run_commands(functional,solution,env,case.timeout_seconds,case_dir/"solution-tests") if all(x["returncode"]==0 for x in solution_setup) and functional else []
    base_pass=bool(base_tests) and all(x["returncode"]==0 for x in base_tests)
    solution_pass=bool(solution_tests) and all(x["returncode"]==0 for x in solution_tests)
    oracle_blocker = None
    if not case.visible_test_paths:
        oracle_blocker = "no visible test path"
    elif not case.test_patch_path.read_text(encoding="utf-8").strip():
        oracle_blocker = "visible test patch is empty"
    elif not functional:
        oracle_blocker = "no functional test command; hygiene-only checks are insufficient"
    oracle_qualified = oracle_blocker is None
    row.update({"base_visible_test_patch":asdict(base_patch),"base_setup":base_setup,"base_tests":base_tests,"solution_setup":solution_setup,"solution_tests":solution_tests,"base_passes":base_pass,"solution_passes":solution_pass,"oracle_qualified":oracle_qualified,"oracle_blocker":oracle_blocker,"qualified":(oracle_qualified and not base_pass and solution_pass),"wall_seconds":time.perf_counter()-start})
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
