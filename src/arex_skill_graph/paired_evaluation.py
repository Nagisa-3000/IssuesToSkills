"""Scoring for leakage-controlled no-skill versus guided agent runs.

Correctness remains the primary gate.  The weighted score is intentionally a
secondary summary: a fast or stylistically clean patch cannot compensate for
failing the task oracle, and an invalid/leaky run is never scored.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class EvaluationWeights:
    correctness: float = 0.60
    code_quality: float = 0.25
    efficiency: float = 0.15

    def normalized(self) -> EvaluationWeights:
        total = self.correctness + self.code_quality + self.efficiency
        if total <= 0:
            raise ValueError("evaluation weights must sum to a positive value")
        return EvaluationWeights(
            correctness=self.correctness / total,
            code_quality=self.code_quality / total,
            efficiency=self.efficiency / total,
        )

    def to_json(self) -> dict[str, float]:
        value = self.normalized()
        return {
            "correctness": value.correctness,
            "code_quality": value.code_quality,
            "efficiency": value.efficiency,
        }


DEFAULT_WEIGHTS = EvaluationWeights()

WEIGHT_BASIS = {
    "policy": (
        "Correctness receives the majority weight because repository-level coding "
        "benchmarks treat issue resolution through regression tests as the primary "
        "outcome. Quality and efficiency are reported separately and only break ties "
        "between oracle-passing arms. The 60/25/15 split is an AREX operational "
        "choice, not a weight copied from any cited benchmark."
    ),
    "references": [
        {
            "name": "SWE-bench",
            "url": "https://arxiv.org/abs/2310.06770",
            "relevance": "Uses repository tests to determine whether a real issue is resolved.",
        },
        {
            "name": "SWE-agent",
            "url": "https://arxiv.org/abs/2405.15793",
            "relevance": "Reports issue-resolution performance together with agent trajectory cost.",
        },
        {
            "name": "SWE-bench Verified",
            "url": "https://openai.com/index/introducing-swe-bench-verified/",
            "relevance": "Emphasizes validated problem statements and reliable test oracles.",
        },
    ],
}

PROMOTION_POLICY = {
    "minimum_independent_holdout_cases": 3,
    "minimum_independent_guided_advantage_cases": 2,
    "minimum_guided_solved_rate_delta": 0.20,
    "no_leakage_or_oracle_failures": True,
    "note": "Repeated runs of one case measure stability and are not independent holdouts.",
}


def _bounded_score(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return min(100.0, max(0.0, number))


def _usage_tokens(row: Mapping[str, Any]) -> int:
    usage = row.get("usage") if isinstance(row.get("usage"), Mapping) else {}
    return sum(
        max(0, int(usage.get(key, 0) or 0))
        for key in ("input_tokens", "output_tokens", "reasoning_output_tokens")
    )


def leakage_gate(row: Mapping[str, Any]) -> dict[str, Any]:
    snapshot = row.get("snapshot") if isinstance(row.get("snapshot"), Mapping) else {}
    violations: list[str] = []
    if not bool(snapshot.get("solution_ref_hidden")):
        violations.append("solution_ref_not_hidden")
    if bool(row.get("solution_ref_in_prompt")):
        violations.append("solution_ref_in_prompt")
    if bool(row.get("solution_ref_in_workspace_history")):
        violations.append("solution_ref_in_workspace_history")
    if bool(row.get("test_edit_violation")) or row.get("edited_visible_tests"):
        violations.append("visible_test_edited")
    return {"passed": not violations, "violations": violations}


def _task_solved(row: Mapping[str, Any], judgment: Mapping[str, Any]) -> bool:
    return bool(row.get("test_success")) and bool(judgment.get("issue_postcondition_satisfied"))


def _relative_efficiency(
    rows: Sequence[Mapping[str, Any]],
    judgments: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, float]]:
    solved = [row for row in rows if _task_solved(row, judgments.get(str(row.get("arm")), {}))]
    if not solved:
        return {str(row.get("arm")): {"token": 0.0, "wall": 0.0, "combined": 0.0} for row in rows}
    positive_tokens = [_usage_tokens(row) for row in solved if _usage_tokens(row) > 0]
    positive_wall = [float(row.get("total_wall_seconds", 0) or 0) for row in solved if float(row.get("total_wall_seconds", 0) or 0) > 0]
    min_tokens = min(positive_tokens) if positive_tokens else 0
    min_wall = min(positive_wall) if positive_wall else 0.0
    result: dict[str, dict[str, float]] = {}
    for row in rows:
        arm = str(row.get("arm"))
        if not _task_solved(row, judgments.get(arm, {})):
            result[arm] = {"token": 0.0, "wall": 0.0, "combined": 0.0}
            continue
        tokens = _usage_tokens(row)
        wall = float(row.get("total_wall_seconds", 0) or 0)
        token_score = 100.0 if not min_tokens or not tokens else 100.0 * min_tokens / tokens
        wall_score = 100.0 if not min_wall or not wall else 100.0 * min_wall / wall
        result[arm] = {
            "token": round(_bounded_score(token_score), 4),
            "wall": round(_bounded_score(wall_score), 4),
            "combined": round(0.60 * _bounded_score(token_score) + 0.40 * _bounded_score(wall_score), 4),
        }
    return result


def score_pair(
    rows: Sequence[Mapping[str, Any]],
    judgments: Mapping[str, Mapping[str, Any]],
    *,
    oracle_qualified: bool | None,
    retrieval_judgment: Mapping[str, Any] | None = None,
    weights: EvaluationWeights = DEFAULT_WEIGHTS,
) -> dict[str, Any]:
    """Score one matched pair while preserving correctness and leakage gates."""
    by_arm = {str(row.get("arm")): row for row in rows}
    if set(by_arm) != {"no_skill", "guided"}:
        raise ValueError("a paired evaluation requires exactly no_skill and guided rows")
    normalized = weights.normalized()
    efficiency = _relative_efficiency([by_arm["no_skill"], by_arm["guided"]], judgments)
    arm_scores: dict[str, Any] = {}
    for arm in ("no_skill", "guided"):
        row = by_arm[arm]
        judge = judgments.get(arm, {})
        gate = leakage_gate(row)
        test_score = 100.0 if bool(row.get("test_success")) else 0.0
        semantic_score = _bounded_score(judge.get("semantic_completion"))
        task_solved = _task_solved(row, judge)
        correctness = 0.80 * test_score + 0.20 * semantic_score
        quality_parts = {
            "patch_scope_precision": _bounded_score(judge.get("patch_scope_precision")),
            "maintainability_style": _bounded_score(judge.get("maintainability_style")),
            "validation_quality": _bounded_score(judge.get("validation_quality")),
        }
        code_quality = sum(quality_parts.values()) / len(quality_parts)
        efficiency_score = efficiency[arm]["combined"]
        overall = (
            normalized.correctness * correctness
            + normalized.code_quality * code_quality
            + normalized.efficiency * efficiency_score
        )
        arm_scores[arm] = {
            "eligible": gate["passed"],
            "leakage_gate": gate,
            "setup_success": bool(row.get("setup_success", True)),
            "test_success": bool(row.get("test_success")),
            "issue_postcondition_satisfied": bool(judge.get("issue_postcondition_satisfied")),
            "task_solved": task_solved,
            "correctness": round(correctness, 4),
            "code_quality": round(code_quality, 4),
            "quality_components": quality_parts,
            "efficiency": efficiency[arm],
            "overall_score": round(overall, 4) if gate["passed"] else None,
            "usage_tokens": _usage_tokens(row),
            "wall_seconds": float(row.get("total_wall_seconds", 0) or 0),
            "judge": dict(judge),
        }

    gates_pass = all(value["eligible"] for value in arm_scores.values())
    setup_gate_passed = all(value["setup_success"] for value in arm_scores.values())
    retrieval_checked = retrieval_judgment is not None
    selected_skill_id = (
        str(retrieval_judgment.get("selected_skill_id"))
        if retrieval_judgment and retrieval_judgment.get("selected_skill_id")
        else None
    )
    retrieval_passed = (
        not retrieval_checked
        or (bool(retrieval_judgment.get("applicable")) and selected_skill_id is not None)
    )
    retrieval_gate = {
        "checked": retrieval_checked,
        "passed": retrieval_passed,
        "applicable": (
            bool(retrieval_judgment.get("applicable")) if retrieval_judgment else None
        ),
        "selected_skill_id": selected_skill_id,
        "confidence": retrieval_judgment.get("confidence") if retrieval_judgment else None,
        "rationale": retrieval_judgment.get("rationale") if retrieval_judgment else None,
    }
    baseline_passed = arm_scores["no_skill"]["task_solved"]
    guided_passed = arm_scores["guided"]["task_solved"]
    if not gates_pass:
        outcome = "invalid_leakage"
    elif not setup_gate_passed:
        outcome = "invalid_setup"
    elif oracle_qualified is False:
        outcome = "descriptive_only_oracle_unqualified"
    elif not retrieval_passed:
        outcome = "descriptive_only_no_applicable_skill_selected"
    elif guided_passed and not baseline_passed:
        outcome = "guided_correctness_win"
    elif baseline_passed and not guided_passed:
        outcome = "no_skill_correctness_win"
    elif not baseline_passed and not guided_passed:
        outcome = "neither_arm_solved"
    else:
        baseline_score = float(arm_scores["no_skill"]["overall_score"] or 0)
        guided_score = float(arm_scores["guided"]["overall_score"] or 0)
        if guided_score >= baseline_score + 2.0:
            outcome = "correctness_tie_guided_quality_efficiency_win"
        elif baseline_score >= guided_score + 2.0:
            outcome = "correctness_tie_no_skill_quality_efficiency_win"
        else:
            outcome = "full_tie"

    return {
        "schema_version": "paired-agent-evaluation-v1",
        "oracle_qualified": oracle_qualified,
        "setup_gate": {"passed": setup_gate_passed},
        "retrieval_gate": retrieval_gate,
        "eligible_for_causal_comparison": (
            gates_pass and setup_gate_passed and oracle_qualified is True and retrieval_passed
        ),
        "weights": normalized.to_json(),
        "weight_basis": WEIGHT_BASIS,
        "arms": arm_scores,
        "outcome": outcome,
        "guided_minus_no_skill": {
            "overall_score": (
                None
                if not gates_pass
                else round(
                    float(arm_scores["guided"]["overall_score"] or 0)
                    - float(arm_scores["no_skill"]["overall_score"] or 0),
                    4,
                )
            ),
            "usage_tokens": arm_scores["guided"]["usage_tokens"] - arm_scores["no_skill"]["usage_tokens"],
            "wall_seconds": round(arm_scores["guided"]["wall_seconds"] - arm_scores["no_skill"]["wall_seconds"], 4),
        },
    }


def aggregate_evaluations(documents: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate repeated weighted evaluations without treating retries as new cases."""
    records: list[Mapping[str, Any]] = []
    for document in documents:
        for value in document.get("evaluations", []):
            if isinstance(value, Mapping):
                records.append(value)
    outcome_counts = Counter(str(item.get("outcome")) for item in records)
    eligible = [item for item in records if bool(item.get("eligible_for_causal_comparison"))]
    by_case: dict[str, list[Mapping[str, Any]]] = {}
    for item in eligible:
        by_case.setdefault(str(item.get("case_id")), []).append(item)

    case_summaries: list[dict[str, Any]] = []
    independent_guided_advantage = 0
    independent_baseline_advantage = 0
    for case_id, items in sorted(by_case.items()):
        guided_solved = sum(bool(item.get("arms", {}).get("guided", {}).get("task_solved")) for item in items)
        baseline_solved = sum(bool(item.get("arms", {}).get("no_skill", {}).get("task_solved")) for item in items)
        runs = len(items)
        guided_rate = guided_solved / runs
        baseline_rate = baseline_solved / runs
        if guided_rate > baseline_rate:
            independent_guided_advantage += 1
        elif baseline_rate > guided_rate:
            independent_baseline_advantage += 1
        case_summaries.append(
            {
                "case_id": case_id,
                "replicates": runs,
                "guided_solved": guided_solved,
                "no_skill_solved": baseline_solved,
                "guided_solved_rate": guided_rate,
                "no_skill_solved_rate": baseline_rate,
                "outcomes": Counter(str(item.get("outcome")) for item in items),
            }
        )

    replicate_count = len(eligible)
    guided_solved_total = sum(
        bool(item.get("arms", {}).get("guided", {}).get("task_solved")) for item in eligible
    )
    baseline_solved_total = sum(
        bool(item.get("arms", {}).get("no_skill", {}).get("task_solved")) for item in eligible
    )
    guided_rate = guided_solved_total / replicate_count if replicate_count else 0.0
    baseline_rate = baseline_solved_total / replicate_count if replicate_count else 0.0
    rate_delta = guided_rate - baseline_rate
    promotion_supported = (
        len(by_case) >= int(PROMOTION_POLICY["minimum_independent_holdout_cases"])
        and independent_guided_advantage
        >= int(PROMOTION_POLICY["minimum_independent_guided_advantage_cases"])
        and rate_delta >= float(PROMOTION_POLICY["minimum_guided_solved_rate_delta"])
        and independent_baseline_advantage == 0
        and len(eligible) == len(records)
    )
    reasons: list[str] = []
    if len(by_case) < int(PROMOTION_POLICY["minimum_independent_holdout_cases"]):
        reasons.append("insufficient_independent_holdout_cases")
    if independent_guided_advantage < int(
        PROMOTION_POLICY["minimum_independent_guided_advantage_cases"]
    ):
        reasons.append("insufficient_independent_guided_advantage_cases")
    if rate_delta < float(PROMOTION_POLICY["minimum_guided_solved_rate_delta"]):
        reasons.append("guided_solved_rate_delta_below_threshold")
    if independent_baseline_advantage:
        reasons.append("at_least_one_independent_case_favors_no_skill")
    if len(eligible) != len(records):
        reasons.append("at_least_one_run_failed_causal_gate")

    return {
        "schema_version": "weighted-agent-evaluation-aggregate-v1",
        "documents": len(documents),
        "replicates": len(records),
        "eligible_replicates": replicate_count,
        "independent_cases": len(by_case),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "paired_task_completion": {
            "no_skill_solved": baseline_solved_total,
            "guided_solved": guided_solved_total,
            "no_skill_solved_rate": baseline_rate,
            "guided_solved_rate": guided_rate,
            "guided_minus_no_skill_solved_rate": rate_delta,
        },
        "independent_case_advantage": {
            "guided": independent_guided_advantage,
            "no_skill": independent_baseline_advantage,
            "tie": len(by_case) - independent_guided_advantage - independent_baseline_advantage,
        },
        "cases": case_summaries,
        "promotion_policy": PROMOTION_POLICY,
        "pattern_promotion_supported": promotion_supported,
        "promotion_blockers": reasons,
    }
