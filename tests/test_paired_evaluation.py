from arex_skill_graph.paired_evaluation import (
    EvaluationWeights,
    aggregate_evaluations,
    leakage_gate,
    score_pair,
)


def row(arm: str, *, passed: bool, tokens: int, wall: float, leaked: bool = False) -> dict:
    return {
        "arm": arm,
        "test_success": passed,
        "patch_nonempty": True,
        "total_wall_seconds": wall,
        "usage": {"input_tokens": tokens, "output_tokens": 0, "reasoning_output_tokens": 0},
        "snapshot": {"solution_ref_hidden": not leaked},
        "solution_ref_in_prompt": leaked,
        "solution_ref_in_workspace_history": False,
        "test_edit_violation": False,
        "edited_visible_tests": [],
    }


def judgment(score: float, *, postcondition: bool = True) -> dict:
    return {
        "semantic_completion": score,
        "patch_scope_precision": score,
        "maintainability_style": score,
        "validation_quality": score,
        "issue_postcondition_satisfied": postcondition,
    }


def test_correctness_win_dominates_cost() -> None:
    result = score_pair(
        [
            row("no_skill", passed=False, tokens=10, wall=1),
            row("guided", passed=True, tokens=1000, wall=100),
        ],
        {
            "no_skill": judgment(20, postcondition=False),
            "guided": judgment(90),
        },
        oracle_qualified=True,
    )
    assert result["outcome"] == "guided_correctness_win"
    assert result["eligible_for_causal_comparison"] is True
    assert result["arms"]["guided"]["overall_score"] > result["arms"]["no_skill"]["overall_score"]


def test_efficiency_breaks_correctness_tie() -> None:
    result = score_pair(
        [
            row("no_skill", passed=True, tokens=100, wall=10),
            row("guided", passed=True, tokens=200, wall=20),
        ],
        {"no_skill": judgment(90), "guided": judgment(90)},
        oracle_qualified=True,
    )
    assert result["outcome"] == "correctness_tie_no_skill_quality_efficiency_win"
    assert result["arms"]["no_skill"]["efficiency"]["combined"] == 100
    assert result["arms"]["guided"]["efficiency"]["combined"] == 50


def test_leakage_invalidates_pair() -> None:
    leaked = row("guided", passed=True, tokens=100, wall=10, leaked=True)
    result = score_pair(
        [row("no_skill", passed=True, tokens=100, wall=10), leaked],
        {"no_skill": judgment(90), "guided": judgment(100)},
        oracle_qualified=True,
    )
    assert leakage_gate(leaked)["passed"] is False
    assert result["outcome"] == "invalid_leakage"
    assert result["arms"]["guided"]["overall_score"] is None


def test_passing_visible_tests_without_postcondition_is_not_solved() -> None:
    result = score_pair(
        [
            row("no_skill", passed=True, tokens=100, wall=10),
            row("guided", passed=True, tokens=100, wall=10),
        ],
        {
            "no_skill": judgment(60, postcondition=False),
            "guided": judgment(65, postcondition=False),
        },
        oracle_qualified=True,
    )
    assert result["outcome"] == "neither_arm_solved"
    assert result["arms"]["guided"]["task_solved"] is False
    assert result["arms"]["guided"]["efficiency"]["combined"] == 0


def test_no_selected_skill_is_descriptive_not_causal() -> None:
    result = score_pair(
        [
            row("no_skill", passed=False, tokens=100, wall=10),
            row("guided", passed=True, tokens=100, wall=10),
        ],
        {
            "no_skill": judgment(20, postcondition=False),
            "guided": judgment(90),
        },
        oracle_qualified=True,
        retrieval_judgment={
            "applicable": False,
            "selected_skill_id": None,
            "confidence": 0.95,
            "rationale": "No retrieved skill matches the response-validation contract.",
        },
    )
    assert result["outcome"] == "descriptive_only_no_applicable_skill_selected"
    assert result["eligible_for_causal_comparison"] is False


def test_setup_failure_invalidates_causal_pair() -> None:
    baseline = row("no_skill", passed=False, tokens=100, wall=10)
    baseline["setup_success"] = False
    guided = row("guided", passed=True, tokens=100, wall=10)
    guided["setup_success"] = True
    result = score_pair(
        [baseline, guided],
        {
            "no_skill": judgment(0, postcondition=False),
            "guided": judgment(90),
        },
        oracle_qualified=True,
        retrieval_judgment={"applicable": True, "selected_skill_id": "workflow:test"},
    )
    assert result["outcome"] == "invalid_setup"
    assert result["eligible_for_causal_comparison"] is False


def test_weights_are_normalized() -> None:
    assert EvaluationWeights(6, 2.5, 1.5).to_json() == {
        "correctness": 0.6,
        "code_quality": 0.25,
        "efficiency": 0.15,
    }


def test_aggregate_does_not_count_retries_as_independent_cases() -> None:
    def evaluation(case_id: str, guided: bool, baseline: bool) -> dict:
        return {
            "case_id": case_id,
            "eligible_for_causal_comparison": True,
            "outcome": "guided_correctness_win" if guided and not baseline else "neither_arm_solved",
            "arms": {
                "guided": {"task_solved": guided},
                "no_skill": {"task_solved": baseline},
            },
        }

    result = aggregate_evaluations(
        [
            {"evaluations": [evaluation("case-a", True, False)]},
            {"evaluations": [evaluation("case-a", False, False)]},
            {"evaluations": [evaluation("case-b", False, False)]},
        ]
    )
    assert result["replicates"] == 3
    assert result["independent_cases"] == 2
    assert result["independent_case_advantage"]["guided"] == 1
    assert result["pattern_promotion_supported"] is False
    assert "insufficient_independent_holdout_cases" in result["promotion_blockers"]
