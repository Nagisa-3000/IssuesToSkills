from dataclasses import asdict

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import digest
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.historical_plan_pool import freeze_plan_candidates
from arex_skill_graph.plan_validation import TaskWorkflowPlan


def test_freeze_original_rewrite_and_composition_pool_is_repeatable_and_sourced(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    parents = [w.id for w in package.workflows]
    before = [asdict(w) for w in package.workflows]
    pool = freeze_plan_candidates(
        task, policy, parents, BudgetLedger(), pattern_id=package.pattern.id
    )
    repeat = freeze_plan_candidates(
        task, policy, parents, BudgetLedger(), pattern_id=package.pattern.id
    )
    assert pool == repeat
    assert len({c["plan"]["id"] for c in pool["candidates"]}) == len(pool["candidates"])
    assert {"original", "single_workflow_rewrite"}.issubset(
        {d for c in pool["candidates"] for d in c["derivations"]}
    )
    for candidate in pool["candidates"]:
        plan = TaskWorkflowPlan.from_dict(candidate["plan"])
        assert set(plan.parent_workflow_ids).issubset(parents)
        assert len(plan.parent_workflow_ids) <= 2
        assert not candidate["failure_label_created"]
    assert before == [asdict(w) for w in package.workflows]
    assert pool["candidate_pool_sha256"] == digest(
        {k: v for k, v in pool.items() if k != "candidate_pool_sha256"}
    )
    assert pool["behavior_verified"] is False
    assert pool["unrun_candidates_are_failure_labels"] is False


def test_frozen_pool_rejects_unsourced_candidates_and_parent_cap(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    parents = [w.id for w in package.workflows]
    for selected in ([*parents, parents[0]], ["invented:workflow"]):
        with pytest.raises(ValueError):
            freeze_plan_candidates(task, policy, selected, BudgetLedger())
    with pytest.raises(ValueError, match="Pattern"):
        freeze_plan_candidates(task, policy, parents, BudgetLedger(), pattern_id="invented:pattern")
    with pytest.raises(ValueError, match="cap"):
        freeze_plan_candidates(task, policy, parents, BudgetLedger(BudgetCaps(parent_workflows=1)))


def test_empty_catalog_retains_no_match_without_failure_label(tmp_path):
    _, task, policy = make_fixture(tmp_path)
    pool = freeze_plan_candidates(task, policy, (), BudgetLedger())
    assert pool["candidates"] == []
    assert pool["unrun_candidates_are_failure_labels"] is False
