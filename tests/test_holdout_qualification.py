from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from qualify_cross_project_holdout_cases import oracle_blocker
from run_cross_project_holdout_agent_eval import (
    Case,
    CommandResult,
    _approved_guidance_hits,
    _prompt,
)

from arex_skill_graph.retrieval import SearchHit
from arex_skill_graph.schema import Node, NodeType


def _case(tmp_path: Path) -> Case:
    patch = tmp_path / "visible-tests.patch"
    patch.write_text("diff --git a/test.py b/test.py\n", encoding="utf-8")
    return Case(
        case_id="owner__repo__1__category",
        repository="owner/repo",
        repository_path=tmp_path,
        base_ref="base",
        solution_ref="solution",
        issue_number=1,
        category="provider-interface-adaptation",
        issue_title="respect the configured endpoint",
        issue_body="Use the selected provider and endpoint consistently.",
        visible_test_paths=("test.py",),
        test_commands=("pytest -q test.py", "git diff --check HEAD"),
        setup_commands=(),
        test_patch_path=patch,
    )


def _command(returncode: int = 0) -> dict[str, object]:
    return {
        "command": "prepare dependencies",
        "returncode": returncode,
        "wall_seconds": 0.1,
        "stdout_path": "stdout",
        "stderr_path": "stderr",
        "timed_out": False,
    }


def _patch_result(returncode: int = 0) -> CommandResult:
    return CommandResult("git apply", returncode, 0.1, "stdout", "stderr")


def test_oracle_blocker_rejects_failed_pre_patch_setup(tmp_path: Path) -> None:
    case = _case(tmp_path)

    blocker = oracle_blocker(
        case,
        ("pytest -q test.py",),
        base_pre_patch_setup=[_command(returncode=137)],
        base_patch=_patch_result(),
        base_setup=[],
        base_tests=[],
        solution_pre_patch_setup=[_command()],
        solution_setup=[],
        solution_tests=[_command()],
    )

    assert blocker == "base pre-patch setup failed (exit 137): prepare dependencies"


def test_oracle_blocker_accepts_runnable_discriminating_oracle(tmp_path: Path) -> None:
    case = _case(tmp_path)

    blocker = oracle_blocker(
        case,
        ("pytest -q test.py",),
        base_pre_patch_setup=[_command()],
        base_patch=_patch_result(),
        base_setup=[],
        base_tests=[_command(returncode=1)],
        solution_pre_patch_setup=[_command()],
        solution_setup=[],
        solution_tests=[_command()],
    )

    assert blocker is None


def test_agent_prompt_exposes_exact_validation_commands(tmp_path: Path) -> None:
    prompt = _prompt(_case(tmp_path), "no_skill", None)

    assert "# Validation commands" in prompt
    assert "`pytest -q test.py`" in prompt
    assert "`git diff --check HEAD`" in prompt


def test_guidance_uses_only_selected_skill_and_related_expansion() -> None:
    selected = SearchHit(
        Node(
            "pattern:1",
            NodeType.PATTERN,
            "Contract-first adaptation",
            "Adapt the provider contract safely.",
            payload={"supporting_workflows": ["workflow:1"]},
        ),
        1.0,
    )
    related = SearchHit(
        Node(
            "workflow:1",
            NodeType.WORKFLOW,
            "Adapt request contract",
            "Preserve shared behavior while adapting one endpoint.",
        ),
        0.8,
    )
    unrelated = SearchHit(
        Node(
            "workflow:2",
            NodeType.WORKFLOW,
            "Unrelated error formatting",
            "Format an HTTP error.",
        ),
        0.7,
    )

    approved = _approved_guidance_hits(
        [selected, related, unrelated],
        {"applicable": True, "selected_skill_id": "pattern:1"},
    )

    assert [hit.node.id for hit in approved] == ["pattern:1", "workflow:1"]
    assert _approved_guidance_hits(
        [selected, related],
        {"applicable": False, "selected_skill_id": None},
    ) == []
