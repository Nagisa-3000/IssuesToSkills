#!/usr/bin/env python3
"""Run a leakage-controlled guided-vs-no-skill held-out agent comparison.

The case manifest is produced by ``prepare_cross_project_holdout_cases.py``.
For every case the runner exports the first-parent tree into a fresh synthetic
Git repository, applies only the selected visible test-file patch, and starts
 two independent ``codex exec --ephemeral`` sessions:

* ``no_skill``: the issue/category and visible test paths only;
* ``guided``: the same task plus BM25/vector/HNSW retrieval, graph expansion,
  and an LLM applicability judgment over the training-only Skill graph.

The solution commit and its history never enter either workspace or prompt.
Agent JSONL events are retained so input/output/reasoning token usage and wall
clock time can be compared with the same model/provider settings.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import statistics
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.retrieval import SearchHit, SkillRetriever
from arex_skill_graph.store import CatalogStore


@dataclass(frozen=True)
class CommandResult:
    command: str
    returncode: int
    wall_seconds: float
    stdout_path: str
    stderr_path: str
    timed_out: bool = False


@dataclass(frozen=True)
class Case:
    case_id: str
    repository: str
    repository_path: Path
    base_ref: str
    solution_ref: str
    issue_number: int
    category: str
    issue_title: str
    issue_body: str
    visible_test_paths: tuple[str, ...]
    test_commands: tuple[str, ...]
    setup_commands: tuple[str, ...]
    test_patch_path: Path
    pre_patch_setup_commands: tuple[str, ...] = ()
    apply_visible_tests_to_solution: bool = False
    timeout_seconds: int = 900
    source: Mapping[str, Any] | None = None

    @property
    def query(self) -> str:
        source = self.source or {}
        families = source.get("module_families") or []
        family_text = " ".join(str(item) for item in families)
        return " ".join(
            filter(None, (self.category.replace("-", " "), self.issue_title, family_text))
        )


def load_cases(path: Path, cases_root: Path) -> list[Case]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError("case manifest must be a JSON array")
    result: list[Case] = []
    for item in raw:
        case_id = str(item["id"])
        case_dir = cases_root / "cases" / _safe_name(case_id)
        result.append(
            Case(
                case_id=case_id,
                repository=str(item["repository"]),
                repository_path=Path(str(item["repository_path"])).expanduser().resolve(),
                base_ref=str(item["base_ref"]),
                solution_ref=str(item["solution_ref"]),
                issue_number=int(item.get("issue_number", 0)),
                category=str(item["category"]),
                issue_title=str(item["issue_title"]),
                issue_body=str(item["issue_body"]),
                visible_test_paths=tuple(str(x) for x in item.get("visible_test_paths", [])),
                test_commands=tuple(str(x) for x in item.get("test_commands", [])),
                setup_commands=tuple(str(x) for x in item.get("setup_commands", [])),
                test_patch_path=case_dir / "visible-tests.patch",
                pre_patch_setup_commands=tuple(
                    str(x) for x in item.get("pre_patch_setup_commands", [])
                ),
                apply_visible_tests_to_solution=bool(
                    item.get("apply_visible_tests_to_solution", False)
                ),
                timeout_seconds=int(item.get("timeout_seconds", 900)),
                source=item.get("manifest_source")
                if isinstance(item.get("manifest_source"), Mapping)
                else item,
            )
        )
    return result


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
    )


def _run_command(
    command: str,
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout_seconds: int,
    stdout_path: Path,
    stderr_path: Path,
    stdin_text: str | None = None,
) -> CommandResult:
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    timed_out = False
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            env=dict(env),
            shell=True,
            executable="/bin/bash",
            input=stdin_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
        out, err, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, str) else ""
        err = exc.stderr if isinstance(exc.stderr, str) else ""
        err += f"\ncommand timed out after {timeout_seconds} seconds\n"
        code = 124
        timed_out = True
    stdout_path.write_text(out, encoding="utf-8", errors="replace")
    stderr_path.write_text(err, encoding="utf-8", errors="replace")
    return CommandResult(
        command,
        int(code),
        time.perf_counter() - started,
        str(stdout_path),
        str(stderr_path),
        timed_out,
    )


def _git_archive(repo: Path, ref: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        ["git", "-C", str(repo), "archive", "--format=tar", ref],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdout is not None
    extract = subprocess.run(
        ["tar", "-xf", "-", "-C", str(destination)],
        stdin=proc.stdout,
        capture_output=True,
        text=True,
        check=False,
    )
    proc.stdout.close()
    stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    returncode = proc.wait()
    if returncode or extract.returncode:
        raise RuntimeError(
            f"git archive failed ({returncode}/{extract.returncode}): {stderr} {extract.stderr}"
        )
    subprocess.run(["git", "-C", str(destination), "init", "-q"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(destination), "config", "user.email", "arex-eval@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "config", "user.name", "AREX evaluation"], check=True
    )
    subprocess.run(["git", "-C", str(destination), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(destination), "commit", "-q", "-m", "evaluation baseline"], check=True
    )


def _apply_visible_tests(case: Case, workspace: Path, artifact_dir: Path) -> CommandResult:
    patch = (
        case.test_patch_path.read_text(encoding="utf-8") if case.test_patch_path.exists() else ""
    )
    artifact_dir.mkdir(parents=True, exist_ok=True)
    patch_path = artifact_dir / "visible-tests.patch"
    patch_path.write_text(patch, encoding="utf-8")
    if not patch.strip():
        return CommandResult(
            "visible test patch (empty)",
            0,
            0.0,
            str(artifact_dir / "stdout"),
            str(artifact_dir / "stderr"),
        )
    result = _run_command(
        "git apply --index --whitespace=nowarn -",
        cwd=workspace,
        env=os.environ.copy(),
        timeout_seconds=120,
        stdout_path=artifact_dir / "stdout",
        stderr_path=artifact_dir / "stderr",
        stdin_text=patch,
    )
    if result.returncode == 0:
        subprocess.run(
            [
                "git",
                "-C",
                str(workspace),
                "commit",
                "-q",
                "-m",
                "evaluation visible regression tests",
            ],
            check=True,
        )
    return result


def _prepare_workspace(
    case: Case,
    workspace: Path,
    artifact_dir: Path,
    env: Mapping[str, str],
) -> dict[str, Any]:
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    _git_archive(case.repository_path, case.base_ref, workspace)
    pre_patch_setup = [
        _run_command(
            command,
            cwd=workspace,
            env=env,
            timeout_seconds=case.timeout_seconds,
            stdout_path=artifact_dir / "pre-patch-setup" / f"{index:02d}.stdout",
            stderr_path=artifact_dir / "pre-patch-setup" / f"{index:02d}.stderr",
        )
        for index, command in enumerate(case.pre_patch_setup_commands, start=1)
    ]
    visible = _apply_visible_tests(case, workspace, artifact_dir)
    return {
        "workspace": str(workspace),
        "base_ref": case.base_ref,
        "solution_ref_hidden": True,
        "snapshot_seconds": time.perf_counter() - started,
        "pre_patch_setup": [asdict(item) for item in pre_patch_setup],
        "pre_patch_setup_success": all(item.returncode == 0 for item in pre_patch_setup),
        "visible_test_patch": asdict(visible),
        "git_head": subprocess.check_output(
            ["git", "-C", str(workspace), "rev-parse", "HEAD"], text=True
        ).strip(),
    }


def _render_hit(hit: SearchHit, index: int) -> str:
    if hit.node.payload.get("skill_package"):
        from arex_skill_graph.skill_packages import hydrate_package

        hydrated = hydrate_package({**hit.node.payload, "id": hit.node.id,
                                    "lifecycle": hit.node.lifecycle})
        return f"## Retrieved Skill Package {index}\n\n" + hydrated["rendered"]
    node = hit.node
    lines = [
        f"## Retrieved node {index}: {node.node_type.value} — {node.title}",
        f"id: {node.id}",
        f"repository: {node.repository or '-'}",
        f"score: {hit.score:.6f}",
        f"sources: {json.dumps(hit.sources, ensure_ascii=False, sort_keys=True)}",
        "",
        node.summary,
    ]
    if node.facets:
        lines += ["", "facets:", json.dumps(node.facets, ensure_ascii=False, sort_keys=True)]
    if node.payload:
        # Keep prompts bounded and avoid dumping evidence blobs.
        payload = {
            key: value
            for key, value in node.payload.items()
            if key
            in {
                "goal",
                "entry_state",
                "exit_state",
                "when_to_use",
                "anti_goals",
                "not_applicable_when",
                "invariants",
                "action_template",
                "decision_points",
                "ordering_constraints",
                "validation_ladder",
                "known_failure_modes",
                "exclusions",
                "missing_probes",
                "stop_conditions",
                "repair_loops",
                "routing_terms",
                "atomic_ids",
                "workflow_ids",
                "supporting_workflows",
                "workflow_realizations",
                "steps",
            }
        }
        if payload:
            lines += ["", "payload:", json.dumps(payload, ensure_ascii=False, sort_keys=True)]
    if hit.trace:
        lines += ["", "retrieval trace:", *[f"- {item}" for item in hit.trace]]
    return "\n".join(lines)


def _payload_relation_ids(payload: Mapping[str, Any]) -> set[str]:
    related: set[str] = set()
    for key in (
        "workflow_ids",
        "atomic_ids",
        "action_ids",
        "supporting_workflows",
        "mandatory_actions",
        "optional_actions",
    ):
        value = payload.get(key)
        if isinstance(value, list):
            related.update(str(item) for item in value if isinstance(item, str))
    steps = payload.get("steps")
    if isinstance(steps, list):
        for step in steps:
            if not isinstance(step, Mapping):
                continue
            for key in ("action_id", "atomic_id", "workflow_id", "skill_id"):
                value = step.get(key)
                if isinstance(value, str):
                    related.add(value)
    realizations = payload.get("workflow_realizations")
    if isinstance(realizations, list):
        for realization in realizations:
            if not isinstance(realization, Mapping):
                continue
            workflow_id = realization.get("workflow_id")
            if isinstance(workflow_id, str):
                related.add(workflow_id)
            bindings = realization.get("role_bindings")
            if not isinstance(bindings, list):
                continue
            for binding in bindings:
                if not isinstance(binding, Mapping):
                    continue
                action_ids = binding.get("action_ids")
                if isinstance(action_ids, list):
                    related.update(str(item) for item in action_ids if isinstance(item, str))
    return related


BLOCKED_PATTERN_DECISIONS = {
    "defer",
    "deferred_by_semantic_judge",
    "reject",
    "rejected_by_semantic_judge",
}


def _guidance_eligibility(hit: SearchHit) -> tuple[bool, str]:
    payload = hit.node.payload if isinstance(hit.node.payload, Mapping) else {}
    decision = str(payload.get("promotion_status") or payload.get("decision") or "")
    if hit.node.node_type.value == "pattern" and decision in BLOCKED_PATTERN_DECISIONS:
        return False, decision
    return True, decision


def _split_guidance_hits(
    hits: Sequence[SearchHit],
    *, require_packages: bool = False,
) -> tuple[list[SearchHit], list[dict[str, Any]]]:
    """Exclude semantically deferred/rejected Patterns before LLM judging or use."""
    eligible: list[SearchHit] = []
    excluded: list[dict[str, Any]] = []
    for rank, hit in enumerate(hits, start=1):
        is_eligible, decision = _guidance_eligibility(hit)
        if is_eligible and require_packages:
            from arex_skill_graph.skill_packages import hydrate_package

            try:
                hydrate_package({**hit.node.payload, "id": hit.node.id,
                                 "lifecycle": hit.node.lifecycle})
            except ValueError as exc:
                is_eligible, decision = False, str(exc)
        if is_eligible:
            eligible.append(hit)
            continue
        excluded.append(
            {
                "rank": rank,
                "id": hit.node.id,
                "title": hit.node.title,
                "decision": decision,
                "reason": "record lacks an eligible, validated Skill Package" if require_packages
                          else "semantic Pattern decision is not eligible for guided use",
            }
        )
    return eligible, excluded


def _approved_guidance_hits(hits: Sequence[SearchHit], judge: Mapping[str, Any]) -> list[SearchHit]:
    """Keep only an eligible LLM-approved Skill and its retrieved graph neighborhood."""
    if judge.get("applicable") is not True:
        return []
    selected_id = judge.get("selected_skill_id")
    if not isinstance(selected_id, str):
        return []
    eligible_hits, _ = _split_guidance_hits(hits)
    by_id = {hit.node.id: hit for hit in eligible_hits}
    selected = by_id.get(selected_id)
    if selected is None:
        return []

    approved_ids = {selected_id}
    payload = selected.node.payload if isinstance(selected.node.payload, Mapping) else {}
    approved_ids.update(_payload_relation_ids(payload))

    related = [
        hit for hit in eligible_hits if hit.node.id in approved_ids and hit is not selected
    ]
    return [selected, *related]


def _parse_usage(path: Path) -> dict[str, Any]:
    usage_rows: list[Mapping[str, Any]] = []
    events = 0
    turns = 0
    errors: list[str] = []
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            events += 1
            if item.get("type") == "turn.completed" and isinstance(item.get("usage"), Mapping):
                usage_rows.append(item["usage"])
                turns += 1
            if item.get("type") == "error":
                errors.append(str(item.get("message", "")))
    totals = {
        key: 0
        for key in (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "reasoning_output_tokens",
        )
    }
    for usage in usage_rows:
        for key in totals:
            try:
                totals[key] += int(usage.get(key, 0) or 0)
            except (TypeError, ValueError):
                pass
    return {"events": events, "turns": turns, **totals, "errors": errors}


def _build_guidance(
    case: Case,
    store: CatalogStore,
    *,
    hnsw_path: Path | None,
    api_key: str | None,
    base_url: str,
    model: str,
    top_k: int,
    seed_k: int,
    expand_hops: int,
) -> dict[str, Any]:
    retriever = SkillRetriever(store)
    started = time.perf_counter()
    response = retriever.search(
        case.query,
        top_k=top_k,
        seed_k=seed_k,
        expand_hops=expand_hops,
        query_mode="solve",
        vector_backend="hnsw" if hnsw_path and hnsw_path.exists() else "exact",
        hnsw_path=str(hnsw_path) if hnsw_path and hnsw_path.exists() else None,
        include_inactive=False,
        require_skill_package=True,
    )
    latency_ms = (time.perf_counter() - started) * 1000.0
    hits = response.hits
    judge_hits, excluded_guidance_hits = _split_guidance_hits(hits, require_packages=True)
    judge: dict[str, Any] = {}
    judge_error: str | None = None
    transport: OpenAICompatibleTransport | None = None
    if api_key:
        try:
            transport = OpenAICompatibleTransport(
                OpenAICompatibleConfig(
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    timeout_seconds=180,
                    max_output_tokens=2500,
                    retries=2,
                )
            )
            governance = LLMGovernanceAdapter(
                transport,
                GovernanceContext(
                    repository=case.repository,
                    model=model,
                    prompt_version="held-out-retrieval-use-v2",
                    code_context={
                        "task_category": case.category,
                        "issue_title": case.issue_title,
                        "issue_body": case.issue_body,
                        "visible_test_paths": list(case.visible_test_paths),
                        "validation_commands": list(case.test_commands),
                        "solution_implementation_hidden": True,
                    },
                ),
            )
            judge = dict(governance.judge_retrieval_use(case.query, judge_hits))
        except Exception as exc:  # noqa: BLE001 - judge failure must degrade to no guidance
            judge_error = f"{type(exc).__name__}: {exc}"
    approved_hits = _approved_guidance_hits(judge_hits, judge)
    # The selected package already contains its explicit Action contracts.
    # Graph neighborhoods remain retrieval traces, not substitute guidance.
    approved_hits = approved_hits[:1]
    from arex_skill_graph.skill_packages import hydrate_package

    hydrated_packages = [hydrate_package({**hit.node.payload, "id": hit.node.id,
                                         "lifecycle": hit.node.lifecycle}) for hit in approved_hits]
    rendered = "\n\n".join(
        _render_hit(hit, index) for index, hit in enumerate(approved_hits, start=1)
    )
    if not rendered:
        rendered = "(The retrieval judge did not approve any retrieved Skill for use.)"
    return {
        "query": case.query,
        "retrieval_latency_ms": latency_ms,
        "seed_count": response.seed_count,
        "expanded_count": response.expanded_count,
        "unresolved": list(response.unresolved),
        "hits": [
            {
                "id": hit.node.id,
                "node_type": hit.node.node_type.value,
                "title": hit.node.title,
                "summary": hit.node.summary,
                "repository": hit.node.repository,
                "score": hit.score,
                "sources": dict(hit.sources),
                "trace": list(hit.trace),
            }
            for hit in hits
        ],
        "judge": judge,
        "judge_error": judge_error,
        "judge_eligible_hit_ids": [hit.node.id for hit in judge_hits],
        "excluded_guidance_hits": excluded_guidance_hits,
        "guidance_applicable": bool(approved_hits),
        "approved_hit_ids": [hit.node.id for hit in approved_hits],
        "hydrated_packages": [{key: value for key, value in package.items() if key != "rendered"}
                              for package in hydrated_packages],
        "transport_calls": list(transport.calls) if transport else [],
        "transport_transcripts": list(transport.transcripts) if transport else [],
        "rendered": rendered,
    }


def _prompt(case: Case, arm: str, guidance: Mapping[str, Any] | None) -> str:
    common = f"""You are solving a held-out implementation task in repository {case.repository}.\nThe workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.\n\n# Problem family\n{case.category.replace("-", " ")}\n\n# Issue/task\n{case.issue_title}\n\n{case.issue_body}\n\n# Visible regression tests retained for this evaluation\n"""
    tests = (
        "\n".join(f"- {path}" for path in case.visible_test_paths)
        or "- No target test path was available; use existing tests and a focused validation."
    )
    validation = (
        "\n".join(f"- `{command}`" for command in case.test_commands)
        or "- Run the narrowest relevant repository tests."
    )
    task_context = common + tests + "\n\n# Validation commands\n" + validation
    if arm == "no_skill":
        return (
            task_context
            + "\n\n# Arm\nno_skill\n\nSolve the task from the repository and visible tests without any retrieved Skill context."
        )
    context = (guidance or {}).get("rendered") or "(Retrieval returned no usable context.)"
    judge = json.dumps((guidance or {}).get("judge", {}), ensure_ascii=False, indent=2)
    return (
        task_context
        + f"""\n\n# Arm\nguided\n\n# Retrieved Skill Graph guidance\nThe following are hypotheses retrieved only from the training repositories using lexical/vector retrieval, optional HNSW, and typed graph expansion. Verify every step against the current code and tests; do not copy repository-specific names blindly.\n\n{context}\n\n# Applicability judgment\n{judge}\n\nUse the guidance to localize the problem and choose a safe implementation, but rely on the visible tests and current code as the oracle."""
    )


def _path_for_executable(path: Path, executable: str) -> str:
    """Convert WSL paths when the selected Codex binary is a Windows exe."""
    if Path(executable).suffix.lower() != ".exe":
        return str(path)
    try:
        converted = subprocess.run(
            ["wslpath", "-w", str(path)], text=True, capture_output=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return str(path)
    return converted or str(path)


def _agent_command(model: str, executable: str, profile: str | None = None) -> str:
    command = f"{shlex.quote(executable)} exec --ephemeral --model {shlex.quote(model)}"
    if profile:
        command += f" --profile {shlex.quote(profile)}"
    return command + " --sandbox danger-full-access --json -o {last} -C {worktree} -"


def _run_arm(
    case: Case,
    arm: str,
    *,
    output_dir: Path,
    workspace_root: Path,
    guidance: Mapping[str, Any] | None,
    model: str,
    codex_executable: str,
    codex_home: Path,
    codex_profile: str | None,
    api_key: str | None,
) -> dict[str, Any]:
    # Resolve before converting paths for a Windows Codex binary.  Passing a
    # relative WSL path through ``wslpath -w`` produces a relative
    # ``data\\...`` argument that the Windows process resolves against an
    # unrelated working directory, losing the last-message artifact.
    run_dir = (output_dir / "runs" / _safe_name(case.case_id) / arm).resolve()
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    workspace = workspace_root / _safe_name(case.case_id) / arm / "worktree"
    prompt = _prompt(case, arm, guidance)
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    if guidance is not None:
        _write_json(run_dir / "guidance.json", dict(guidance))
    env = os.environ.copy()
    codex_home_value = _path_for_executable(codex_home, codex_executable)
    env.update({"CODEX_HOME": codex_home_value, "AREX_CASE_ID": case.case_id, "AREX_ARM": arm})
    if api_key:
        env["OPENAI_API_KEY"] = api_key
    snapshot = _prepare_workspace(case, workspace, run_dir / "snapshot", env)
    setup_results = [
        _run_command(
            command,
            cwd=workspace,
            env=env,
            timeout_seconds=case.timeout_seconds,
            stdout_path=run_dir / "setup" / f"{index:02d}.stdout",
            stderr_path=run_dir / "setup" / f"{index:02d}.stderr",
        )
        for index, command in enumerate(case.setup_commands, start=1)
    ]
    setup_blockers: list[str] = []
    if not bool(snapshot["pre_patch_setup_success"]):
        setup_blockers.append("pre-patch setup failed")
    if int(snapshot["visible_test_patch"]["returncode"]) != 0:
        setup_blockers.append("visible test patch failed")
    if not all(item.returncode == 0 for item in setup_results):
        setup_blockers.append("post-patch setup failed")
    setup_ok = not setup_blockers
    command = _agent_command(model, codex_executable, codex_profile).format(
        last=shlex.quote(_path_for_executable(run_dir / "agent-last.txt", codex_executable)),
        worktree=shlex.quote(_path_for_executable(workspace, codex_executable)),
    )
    started = time.perf_counter()
    # Dependency setup is measured separately and must not silently turn the
    # agent arm into a no-op.  The model still receives the same source/test
    # workspace when setup is unavailable; the subsequent test result records
    # the missing-runtime failure explicitly.
    agent = _run_command(
        command,
        cwd=workspace,
        env=env,
        timeout_seconds=case.timeout_seconds,
        stdout_path=run_dir / "agent-events.jsonl",
        stderr_path=run_dir / "agent.stderr",
        stdin_text=prompt,
    )
    patch = subprocess.run(
        ["git", "-C", str(workspace), "diff", "--binary", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    changed_paths = subprocess.run(
        ["git", "-C", str(workspace), "diff", "--name-only", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "-C", str(workspace), "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.splitlines()
    edited_visible_tests = sorted(set(changed_paths) & set(case.visible_test_paths))
    (run_dir / "model.patch").write_text(patch, encoding="utf-8")
    tests = []
    if setup_ok and agent.returncode == 0:
        for index, test_command in enumerate(case.test_commands, start=1):
            result = _run_command(
                test_command,
                cwd=workspace,
                env=env,
                timeout_seconds=case.timeout_seconds,
                stdout_path=run_dir / "tests" / f"{index:02d}.stdout",
                stderr_path=run_dir / "tests" / f"{index:02d}.stderr",
            )
            tests.append(result)
            if result.returncode != 0:
                break
    usage = _parse_usage(run_dir / "agent-events.jsonl")
    raw_test_success = bool(tests) and all(item.returncode == 0 for item in tests)
    effective_test_success = raw_test_success and not edited_visible_tests
    row = {
        "case_id": case.case_id,
        "repository": case.repository,
        "category": case.category,
        "arm": arm,
        "status": "passed" if effective_test_success else "failed",
        "setup_success": setup_ok,
        "setup_blockers": setup_blockers,
        "agent_success": agent.returncode == 0,
        "patch_nonempty": bool(patch.strip()) or bool(untracked),
        "visible_tests_present": bool(case.visible_test_paths),
        "raw_test_success": raw_test_success,
        "test_success": effective_test_success,
        "total_wall_seconds": time.perf_counter() - started + float(snapshot["snapshot_seconds"]),
        "snapshot": snapshot,
        "setup": [asdict(item) for item in setup_results],
        "agent": asdict(agent),
        "tests": [asdict(item) for item in tests],
        "usage": usage,
        "model": model,
        "codex_profile": codex_profile,
        "prompt_characters": len(prompt),
        "prompt_estimated_tokens": (len(prompt) + 3) // 4,
        "changed_files": sorted(changed_paths),
        "changed_untracked_files": untracked,
        "edited_visible_tests": edited_visible_tests,
        "test_edit_violation": bool(edited_visible_tests),
        "solution_ref_in_prompt": case.solution_ref in prompt,
        "solution_ref_in_workspace_history": False,
    }
    _write_json(run_dir / "result.json", row)
    return row


def _aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for arm in sorted({str(row["arm"]) for row in rows}):
        items = [row for row in rows if row["arm"] == arm]
        mean_wall_seconds = (
            statistics.mean(float(item.get("total_wall_seconds", 0.0)) for item in items)
            if items
            else 0.0
        )
        mean_prompt_estimated_tokens = (
            statistics.mean(float(item.get("prompt_estimated_tokens", 0.0)) for item in items)
            if items
            else 0.0
        )
        result[arm] = {
            "cases": len(items),
            "test_successes": sum(bool(item.get("test_success")) for item in items),
            "test_success_rate": (
                sum(bool(item.get("test_success")) for item in items) / len(items)
            )
            if items
            else 0.0,
            "agent_success_rate": (
                sum(bool(item.get("agent_success")) for item in items) / len(items)
            )
            if items
            else 0.0,
            "mean_wall_seconds": mean_wall_seconds,
            "mean_input_tokens": statistics.mean(
                int(item.get("usage", {}).get("input_tokens", 0)) for item in items
            )
            if items
            else 0.0,
            "mean_cached_input_tokens": statistics.mean(
                int(item.get("usage", {}).get("cached_input_tokens", 0)) for item in items
            )
            if items
            else 0.0,
            "mean_output_tokens": statistics.mean(
                int(item.get("usage", {}).get("output_tokens", 0)) for item in items
            )
            if items
            else 0.0,
            "mean_reasoning_output_tokens": statistics.mean(
                int(item.get("usage", {}).get("reasoning_output_tokens", 0)) for item in items
            )
            if items
            else 0.0,
            "total_input_tokens": sum(
                int(item.get("usage", {}).get("input_tokens", 0)) for item in items
            ),
            "total_output_tokens": sum(
                int(item.get("usage", {}).get("output_tokens", 0)) for item in items
            ),
            "mean_prompt_estimated_tokens": mean_prompt_estimated_tokens,
        }
    return result


def main() -> int:
    # Explicit new SWE path dispatches before legacy visible-test/Codex setup.
    if "--adaptive-spec" in sys.argv[1:]:
        adaptive_parser = argparse.ArgumentParser(description="Run the isolated adaptive SWE protocol")
        adaptive_parser.add_argument("--adaptive-spec", type=Path, required=True)
        adaptive_args = adaptive_parser.parse_args()
        from arex_skill_graph.adaptive_cli import read_json
        from eval_pattern_crossbind_ranker import main as adaptive_main
        specification = read_json(adaptive_args.adaptive_spec)
        if not isinstance(specification, list) or any(not isinstance(arg, str) for arg in specification):
            raise ValueError("adaptive spec must contain the reviewed experiment argv array")
        return adaptive_main(specification)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--cases-root", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY"),
        help="Optional API key; omit to let Codex use CODEX_HOME login",
    )
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument(
        "--codex",
        default=os.environ.get("CODEX_EXECUTABLE", "/usr/local/bin/codex"),
        help="Codex executable used for both paired arms",
    )
    parser.add_argument("--codex-home", type=Path, required=True)
    parser.add_argument(
        "--codex-profile",
        help="Optional CODEX_HOME profile applied identically to both paired arms",
    )
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--seed-k", type=int, default=40)
    parser.add_argument("--expand-hops", type=int, default=2)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--skip-setup", action="store_true")
    args = parser.parse_args()
    if args.codex_profile:
        if Path(args.codex_profile).name != args.codex_profile:
            parser.error("--codex-profile must be a profile name, not a path")
        profile_path = args.codex_home / f"{args.codex_profile}.config.toml"
        if not profile_path.is_file():
            parser.error(f"Codex profile does not exist: {profile_path}")
    cases = load_cases(args.cases, args.cases_root)
    if args.max_cases is not None:
        cases = cases[: max(0, args.max_cases)]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.workspace_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    with CatalogStore(args.db) as store:
        store.initialize()
        for case in cases:
            guidance = _build_guidance(
                case,
                store,
                hnsw_path=args.hnsw,
                api_key=args.api_key,
                base_url=args.base_url,
                model=args.model,
                top_k=args.top_k,
                seed_k=args.seed_k,
                expand_hops=args.expand_hops,
            )
            _write_json(
                args.output_dir / "retrieval" / f"{_safe_name(case.case_id)}.json", guidance
            )
            if args.skip_setup:
                case = Case(
                    **{
                        **asdict(case),
                        "setup_commands": (),
                        "pre_patch_setup_commands": (),
                    }
                )
            # Each arm receives its own synthetic snapshot and its own fresh
            # ephemeral Codex session; there is no resume/fork relationship.
            rows.append(
                _run_arm(
                    case,
                    "no_skill",
                    output_dir=args.output_dir,
                    workspace_root=args.workspace_root,
                    guidance=None,
                    model=args.model,
                    codex_executable=args.codex,
                    codex_home=args.codex_home,
                    codex_profile=args.codex_profile,
                    api_key=args.api_key,
                )
            )
            rows.append(
                _run_arm(
                    case,
                    "guided",
                    output_dir=args.output_dir,
                    workspace_root=args.workspace_root,
                    guidance=guidance,
                    model=args.model,
                    codex_executable=args.codex,
                    codex_home=args.codex_home,
                    codex_profile=args.codex_profile,
                    api_key=args.api_key,
                )
            )
    report = {
        "schema_version": "cross-project-guided-agent-eval-v1",
        "generated_at": _utc_now(),
        "cases": len(cases),
        "arms": ["no_skill", "guided"],
        "execution_config": {
            "model": args.model,
            "base_url": args.base_url,
            "codex_executable": args.codex,
            "codex_profile": args.codex_profile,
        },
        "rows": rows,
        "aggregate": _aggregate(rows),
        "leakage_checks": {
            "all_solution_refs_absent_from_prompts": all(
                not row["solution_ref_in_prompt"] for row in rows
            ),
            "synthetic_history_only": all(
                not row["solution_ref_in_workspace_history"] for row in rows
            ),
        },
    }
    _write_json(args.output_dir / "report.json", report)
    print(
        json.dumps(
            {"cases": len(cases), "rows": len(rows), "aggregate": report["aggregate"]},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
