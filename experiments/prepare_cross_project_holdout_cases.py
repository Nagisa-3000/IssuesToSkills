#!/usr/bin/env python3
"""Prepare held-out issue/PR cases without leaking implementation history.

A case is exported from the first parent of the known solution commit. Only a
bounded, prioritized set of test/fixture files changed by the solution is
retained in the evaluation workspace; implementation files and the solution
history are never copied into an agent prompt or synthetic repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

NODE_TOOL = Path(__file__).resolve().with_name("run_holdout_node_tool.py")


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}: {proc.stderr.strip()}")
    return proc.stdout


def commit_parents(repo: Path, ref: str) -> list[str]:
    line = run_git(repo, "rev-list", "--parents", "-n", "1", ref).strip().split()
    if len(line) < 2:
        raise ValueError(f"solution ref {ref} has no parent")
    return line[1:]


def first_parent(repo: Path, ref: str) -> str:
    return commit_parents(repo, ref)[0]


def changed_files(repo: Path, parent: str, ref: str) -> list[dict[str, str]]:
    raw = run_git(repo, "diff", "--name-status", "--no-renames", parent, ref)
    result: list[dict[str, str]] = []
    for line in raw.splitlines():
        fields = line.split("\t")
        if len(fields) >= 2:
            result.append({"status": fields[0], "path": fields[-1]})
    return result


def looks_like_test(path: str) -> bool:
    p = path.lower().replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    return p.startswith(("test/", "tests/", "__tests__/", "spec/", "specs/")) or any(marker in p for marker in ("/test/", "/tests/", "/__tests__/", "/spec/", "/specs/", "/fixtures/", "/snapshots/", "/expected/")) or any(
        name.endswith(suffix)
        for suffix in (".test.ts", ".test.tsx", ".test.js", ".test.mjs", ".test.py", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.mjs", ".spec.py", "_test.py", "_tests.py")
    ) or name.startswith("test_")


def is_runnable_test(path: str) -> bool:
    """Whether a path should be passed to the test runner, not just patched.

    Test helpers such as ``tests/.../_pm.py`` are part of the visible oracle
    patch but are not themselves pytest/Vitest targets.
    """
    p = path.lower().replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    return any(
        name.endswith(suffix)
        for suffix in (".test.ts", ".test.tsx", ".test.js", ".test.mjs", ".test.py", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.mjs", ".spec.py", "_test.py", "_tests.py")
    ) or name.startswith("test_")


def test_priority(path: str) -> tuple[int, int, str]:
    p = path.lower().replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    support = any(marker in p for marker in ("/fixtures/", "/snapshots/", "/expected/"))
    direct = any(name.endswith(suffix) for suffix in (".test.ts", ".test.tsx", ".test.js", ".test.mjs", ".test.py", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.mjs", ".spec.py", "_test.py", "_tests.py")) or name.startswith("test_")
    return (0 if direct and not support else 1 if direct else 2 if not support else 3, len(path), path)


def test_patch(repo: Path, parent: str, ref: str, paths: list[str]) -> str:
    if not paths:
        return ""
    proc = subprocess.run(
        ["git", "-C", str(repo), "diff", "--binary", "--full-index", parent, ref, "--", *paths],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"could not create test patch: {proc.stderr.strip()}")
    return proc.stdout


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in value)


def _test_command(repository: str, paths: list[str], *, node_tool: Path = NODE_TOOL) -> list[str]:
    if not paths:
        return ["git diff --check HEAD"]
    quoted = " ".join("'" + path.replace("'", "'\\''") + "'" for path in paths)
    if repository == "deepseek-ai/deepseek-harness":
        node_path = "/home/chenyujia/.local/nodeenvs/node-22.19.0/bin"
        return [f"PATH={node_path}:$PATH pnpm exec vitest run {quoted}", "git diff --check HEAD"]
    if repository == "NousResearch/hermes-agent":
        python_paths = [path for path in paths if path.endswith(".py")]
        typescript_paths = [path for path in paths if path.endswith((".ts", ".tsx", ".js", ".jsx", ".mjs"))]
        commands: list[str] = []
        if python_paths:
            py_quoted = " ".join("'" + path.replace("'", "'\\''") + "'" for path in python_paths)
            commands.append(f"./.venv/bin/pytest -q {py_quoted}")
        if typescript_paths:
            # Desktop tests are owned by the apps/desktop workspace. Keep
            # their paths relative to that workspace for npm/Vitest.
            desktop_paths = [path.removeprefix("apps/desktop/") for path in typescript_paths if path.startswith("apps/desktop/")]
            if desktop_paths:
                ts_quoted = " ".join("'" + path.replace("'", "'\\''") + "'" for path in desktop_paths)
                commands.append(f"cd apps/desktop && python3 {node_tool} npm exec -- vitest run {ts_quoted}")
        return commands + ["git diff --check HEAD"]
    if repository == "Aider-AI/aider":
        return [f"pytest -q {quoted}", "git diff --check HEAD"]
    if repository == "QwenLM/qwen-code":
        return [f"python3 {node_tool} pnpm exec vitest run --config ./vitest.config.ts {quoted}", "git diff --check HEAD"]
    if repository == "google-gemini/gemini-cli":
        return [f"python3 {node_tool} npm exec -- vitest run --config ./vitest.config.ts {quoted}", "git diff --check HEAD"]
    if repository == "openai/codex":
        return [f"python3 {node_tool} pnpm exec vitest run {quoted}", "git diff --check HEAD"]
    if repository == "earendil-works/pi":
        node_path = "/home/chenyujia/.local/nodeenvs/node-22.19.0/bin"
        return [f"PATH={node_path}:$PATH npm test -- {quoted}", "git diff --check HEAD"]
    return ["git diff --check HEAD"]


def prepare_case(case: dict[str, Any], *, output_dir: Path, max_test_paths: int) -> dict[str, Any]:
    repo = Path(str(case["checkout"])).expanduser().resolve()
    ref = str(case.get("ref") or case.get("solution_ref") or "").strip()
    if not ref:
        raise ValueError(f"case {case} has no ref")
    parents = commit_parents(repo, ref)
    parent = parents[0]
    # For a merge commit, use the first-parent -> second-parent PR branch diff
    # to choose relevant tests.  The evaluation base remains the first parent,
    # and the visible patch is still generated against the merge result.
    change_ref = parents[1] if len(parents) > 1 else ref
    changes = changed_files(repo, parent, change_ref)
    changed_candidates = [item["path"] for item in changes if item["status"] != "D" and looks_like_test(item["path"])]
    # The manifest's sampled files are selected from the PR/commit evidence and
    # are more relevant than arbitrary tests touched by a large merge commit.
    # Put sampled tests first, then fill from the bounded changed-file pool.
    sampled = [str(path) for path in (case.get("file_sample") or []) if looks_like_test(str(path))]
    candidates = sampled + changed_candidates
    ordered = sorted(dict.fromkeys(candidates), key=lambda path: (0 if path in sampled else 1, *test_priority(path)))
    # Prefer direct executable tests, then fixtures/snapshots. The cap keeps
    # visible-test context and patch application bounded on monorepo PRs.
    visible_files = ordered[:max_test_paths]
    test_paths = [path for path in visible_files if is_runnable_test(path)]
    support_paths = [path for path in visible_files if path not in test_paths]
    patch = test_patch(repo, parent, ref, visible_files)
    repository = str(case["repository"])
    issue = int(case["issue"])
    category = str(case.get("category") or case.get("theme") or "uncategorized")
    case_id = f"{repository.replace('/', '__')}__{issue}__{category}"
    has_python_tests = any(path.endswith(".py") for path in test_paths)
    has_node_tests = any(path.endswith((".ts", ".tsx", ".js", ".jsx", ".mjs")) for path in test_paths)
    has_pnpm_lock = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{parent}:pnpm-lock.yaml"],
        capture_output=True,
        check=False,
    ).returncode == 0
    pyproject_text = run_git(repo, "show", f"{parent}:pyproject.toml", check=False)
    python_minor = "3.14" if "python_version >= '3.14'" in pyproject_text else "3.11"
    setup_commands: list[str] = []
    if repository == "NousResearch/hermes-agent" and has_python_tests:
        # Hermes keeps its Python dependency lock in the repository.  Install
        # dependencies without installing the project itself so pytest imports
        # the snapshot under test rather than a host checkout.
        setup_commands.append(
            f"uv sync --python {python_minor} --extra dev --no-install-project || "
            f"uv sync --python {python_minor} --no-install-project; "
            "uv pip install --python .venv/bin/python -e . pytest pytest-asyncio"
        )
    if repository in {"NousResearch/hermes-agent", "google-gemini/gemini-cli"} and has_node_tests:
        setup_commands.append(f"python3 {NODE_TOOL} npm ci --ignore-scripts --no-audit --no-fund")
    if repository in {"QwenLM/qwen-code", "openai/codex"} and has_node_tests:
        if has_pnpm_lock:
            setup_commands.append(f"python3 {NODE_TOOL} pnpm install --frozen-lockfile --ignore-scripts")
        else:
            setup_commands.append(f"python3 {NODE_TOOL} npm ci --ignore-scripts --no-audit --no-fund")
    if repository == "deepseek-ai/deepseek-harness":
        setup_commands.append("PATH=/home/chenyujia/.local/nodeenvs/node-22.19.0/bin:$PATH pnpm install --frozen-lockfile --ignore-scripts")
    row = {
        "id": case_id,
        "repository": repository,
        "repository_path": str(repo),
        "base_ref": parent,
        "solution_ref": ref,
        "issue_number": issue,
        "category": category,
        "theme": case.get("theme", category.replace("-", " ")),
        "issue_title": str(case.get("title") or f"Implement the {category.replace('-', ' ')} behavior"),
        "issue_body": f"Held-out cross-project task in the {category.replace('-', ' ')} family. Implement the behavior required by the visible regression tests while preserving existing compatibility and error semantics. The original implementation commit is intentionally absent from this snapshot.",
        "visible_test_paths": test_paths,
        "visible_support_paths": support_paths,
        "test_commands": _test_command(repository, test_paths),
        "setup_commands": setup_commands,
        "apply_visible_tests_to_solution": bool(
            case.get("apply_visible_tests_to_solution", False)
        ),
        "changed_file_count": len(changes),
        "changed_files_sample": changes[:100],
        "test_patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
        "test_patch_characters": len(patch),
        "split": "held_out_test",
        "held_out_repository": case.get("held_out_repository"),
        "manifest_source": case,
    }
    case_dir = output_dir / "cases" / _safe_name(case_id)
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "visible-tests.patch").write_text(patch, encoding="utf-8")
    (case_dir / "case.json").write_text(json.dumps(row, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-test-paths", type=int, default=12)
    args = parser.parse_args()
    raw = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError("manifest must be a JSON array")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = [prepare_case(dict(case), output_dir=args.output_dir, max_test_paths=max(1, args.max_test_paths)) for case in raw]
    report = {
        "schema_version": "cross-project-held-out-case-v1",
        "cases": len(rows),
        "categories": len({row["category"] for row in rows}),
        "test_path_cases": sum(bool(row["visible_test_paths"]) for row in rows),
        "by_category": dict(Counter(row["category"] for row in rows)),
        "rows": rows,
    }
    (args.output_dir / "case-manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "preparation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("cases", "categories", "test_path_cases")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
