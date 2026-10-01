from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from compile_resolution_skill_package import compile_package

GRAPH = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-category-01-closed-loop-v1"
    / "pattern-induction"
    / "semantic-graph.json"
)
HOLDOUT_CASES = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-category-01-closed-loop-v1"
    / "holdout-cases"
    / "case-manifest.json"
)
QUALIFICATION = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-category-01-closed-loop-v1"
    / "holdout-qualification"
    / "qualification-report.json"
)
RETRIEVAL = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-category-01-closed-loop-v1"
    / "holdout"
    / "retrieval-evaluation.json"
)
EVALUATION_ROOT = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-category-01-closed-loop-v1"
    / "agent-evaluation"
    / "paired-run-v1"
)
WEIGHTED_EVALUATION = EVALUATION_ROOT / "weighted-evaluation.json"
EVALUATION_AGGREGATE = EVALUATION_ROOT / "aggregate.json"
VALIDATOR = (
    ROOT
    / "data"
    / "skill-extraction"
    / "packages"
    / "resolution-skill-creator"
    / "scripts"
    / "validate_skill_package.py"
)
PATTERN_ID = "pattern:5895d079305884e4"


def _compile(output: Path) -> dict[str, object]:
    return compile_package(
        GRAPH,
        PATTERN_ID,
        output,
        holdout_cases_path=HOLDOUT_CASES,
        qualification_path=QUALIFICATION,
        retrieval_path=RETRIEVAL,
        agent_evaluation_path=WEIGHTED_EVALUATION,
        evaluation_aggregate_path=EVALUATION_AGGREGATE,
    )


def test_compile_candidate_package_with_real_action_bindings(tmp_path: Path) -> None:
    output = tmp_path / "candidate-skill"

    result = _compile(output)

    assert result["status"] == "candidate"
    assert result["promotion_status"] == "candidate_pending_independent_holdouts"
    assert result["workflow_count"] == 4
    assert result["holdout_oracle_qualified"] is True
    assert result["holdout_repository_disjoint"] is True
    assert result["agent_pair_status"] == "pass_directional"
    assert result["promotion_supported"] is False

    skill = (output / "SKILL.md").read_text(encoding="utf-8")
    for heading in (
        "## Use this skill when",
        "## Do not use this skill when",
        "## Required inputs",
        "## Workflow",
        "## Validation",
        "## Stop, ask, or defer",
    ):
        assert heading in skill
    assert "persistent project-binding" in skill

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    pattern = next(item for item in graph["patterns"] if item["id"] == PATTERN_ID)
    bound_actions = {
        action_id
        for realization in pattern["workflow_realizations"]
        for binding in realization["role_bindings"]
        for action_id in binding["action_ids"]
    }
    action_contracts = (output / "references" / "action-contracts.md").read_text(encoding="utf-8")
    assert bound_actions
    assert all(action_id in action_contracts for action_id in bound_actions)

    provenance = json.loads((output / "references" / "provenance.yaml").read_text(encoding="utf-8"))
    assert provenance["package"]["status"] == "candidate"
    assert provenance["holdout"]["agent_pair_status"] == "pass_directional"
    assert provenance["holdout"]["repository_disjoint"] is True
    assert "solution_ref" not in provenance["holdout"]
    assert "base_ref" not in provenance["holdout"]
    assert provenance["agent_evaluation"]["lifecycle_decision"] == "retain_candidate"
    assert provenance["agent_evaluation"]["promotion_supported"] is False

    validation = subprocess.run(
        [sys.executable, str(VALIDATOR), str(output)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert validation.returncode == 0, validation.stdout + validation.stderr


def test_compilation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    _compile(first)
    _compile(second)

    first_files = {
        path.relative_to(first): path.read_bytes() for path in first.rglob("*") if path.is_file()
    }
    second_files = {
        path.relative_to(second): path.read_bytes() for path in second.rglob("*") if path.is_file()
    }
    assert first_files == second_files


def test_compiler_rejects_training_holdout_repository_overlap(tmp_path: Path) -> None:
    holdout = tmp_path / "holdout.json"
    holdout.write_text(
        json.dumps([{"id": "overlap", "repository": "Aider-AI/aider"}]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="overlap training repositories"):
        compile_package(
            GRAPH,
            PATTERN_ID,
            tmp_path / "candidate",
            holdout_cases_path=holdout,
        )


def test_compiler_refuses_to_force_replace_the_repository_root() -> None:
    with pytest.raises(ValueError, match="unsafe output directory"):
        compile_package(GRAPH, PATTERN_ID, ROOT, force=True)
