from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "prepare_cross_project_holdout_cases.py"
SPEC = importlib.util.spec_from_file_location("prepare_cross_project_holdout_cases", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_prepare_case_preserves_public_issue_text(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Holdout Test")
    _git(repo, "config", "user.email", "holdout@example.invalid")

    tests = repo / "tests"
    tests.mkdir()
    target = tests / "test_regression.py"
    target.write_text("def test_regression():\n    assert False\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "base")

    target.write_text("def test_regression():\n    assert True\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "solution")
    solution_ref = _git(repo, "rev-parse", "HEAD")

    title = "Public title with provider-specific detail"
    body = "Public body\n\nKeep this exact Markdown and punctuation: `max_tokens`."
    case = {
        "repository": "owner/repo",
        "checkout": str(repo),
        "ref": solution_ref,
        "issue": 42,
        "category": "context-budget-and-compaction",
        "issue_title": title,
        "issue_body": body,
        "extraction_forbidden": True,
        "solution_hidden_from_agent": True,
    }

    row = MODULE.prepare_case(case, output_dir=tmp_path / "prepared", max_test_paths=4)

    assert row["issue_title"] == title
    assert row["issue_body"] == body
    assert row["extraction_forbidden"] is True
    assert row["solution_hidden_from_agent"] is True
    assert row["manifest_source"]["issue_body"] == body

def test_pi_test_commands_are_scoped_to_their_workspaces() -> None:
    commands = MODULE._test_command(
        "earendil-works/pi",
        [
            "packages/ai/test/retry.test.ts",
            "packages/coding-agent/test/suite/regressions/9735.test.ts",
        ],
    )

    assert commands[0].endswith(
        "npm --prefix packages/ai test -- 'test/retry.test.ts'"
    )
    assert commands[1].endswith(
        "npm --prefix packages/coding-agent test -- "
        "'test/suite/regressions/9735.test.ts'"
    )
    assert commands[2] == "git diff --check HEAD"
