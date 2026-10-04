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


def _prepared_study(tmp_path, package, task, policy):
    import json
    from arex_skill_graph.historical_plan_pool import load_prepared_plan_study

    pool = freeze_plan_candidates(task, policy, [w.id for w in package.workflows], BudgetLedger())
    expected = {
        "queries_sha256": "public-query-population",
        "references_sha256": "source-catalog",
        "training_cutoff": "2021-01-01T00:00:00Z",
        "main_cutoff": "2024-01-01T00:00:00Z",
        "seed": 42,
        "encoder": {"version": "frozen-encoder"},
    }
    identity = {
        **expected,
        "candidate_kind": "both",
        "candidate_generation_frozen": True,
        "development_population": True,
    }
    schedule = [
        {
            "query_id": task.task_id,
            "candidate_kind": "baseline",
            "candidate_id": None,
            "sampling_probability": 1.0,
            "relative_output": "query/baseline",
        }
    ]
    schedule += [
        {
            "query_id": task.task_id,
            "candidate_kind": "plan",
            "candidate_id": row["plan"]["id"],
            "sampling_probability": 1.0,
            "relative_output": "query/plan-" + str(number),
        }
        for number, row in enumerate(pool["candidates"])
    ]
    documents = {
        "study-identity.json": identity,
        "plan-pools.json": {task.task_id: pool},
        "plans.json": {task.task_id: [row["plan"] for row in pool["candidates"]]},
        "controlled-schedule.json": schedule,
        "candidate-coverage.json": [
            {"query_id": task.task_id, "unrun_candidates_are_failure_labels": False}
        ],
    }
    directory = tmp_path / "prepared-study"
    directory.mkdir()
    for name, value in documents.items():
        (directory / name).write_text(json.dumps(value))
    return directory, expected, load_prepared_plan_study(directory, expected)


def test_prepared_pool_loads_without_generation_or_modifying_artifacts(tmp_path, monkeypatch):
    from arex_skill_graph import historical_plan_pool as module

    package, task, policy = make_fixture(tmp_path)
    directory, expected, loaded = _prepared_study(tmp_path, package, task, policy)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}

    def forbidden(*args, **kwargs):
        raise AssertionError("frozen execution must not generate or reselect candidates")

    for name in ("freeze_plan_candidates", "rewrite_workflow", "bind_and_compose"):
        monkeypatch.setattr(module, name, forbidden)
    pool = loaded["plan_pools"][task.task_id]
    plans = module.verify_frozen_plan_pool(pool, task, policy, BudgetLedger())
    assert [digest(plan.to_dict()) for plan in plans] == [
        digest(row["plan"]) for row in pool["candidates"]
    ]
    reloaded = module.load_prepared_plan_study(directory, expected)
    assert reloaded == loaded
    assert loaded["lineage"]["candidate_generation_reexecuted"] is False
    assert before == {p.name: p.read_bytes() for p in directory.iterdir()}


@pytest.mark.parametrize("field", ["public_task_sha256", "catalog_cutoff", "source_package_hashes"])
def test_frozen_execution_rejects_changed_task_time_or_source_even_with_new_digest(tmp_path, field):
    from copy import deepcopy
    from arex_skill_graph.historical_plan_pool import verify_frozen_plan_pool

    package, task, policy = make_fixture(tmp_path)
    pool = freeze_plan_candidates(task, policy, [w.id for w in package.workflows], BudgetLedger())
    corrupt = deepcopy(pool)
    corrupt[field] = {} if field == "source_package_hashes" else "changed"
    corrupt["candidate_pool_sha256"] = digest(
        {key: value for key, value in corrupt.items() if key != "candidate_pool_sha256"}
    )
    with pytest.raises(ValueError, match="changed"):
        verify_frozen_plan_pool(corrupt, task, policy, BudgetLedger())


def test_frozen_execution_rejects_modified_plan_digest(tmp_path):
    from arex_skill_graph.historical_plan_pool import verify_frozen_plan_pool

    package, task, policy = make_fixture(tmp_path)
    pool = freeze_plan_candidates(task, policy, [w.id for w in package.workflows], BudgetLedger())
    pool["candidates"][0]["plan"]["stop_conditions"] = []
    with pytest.raises(ValueError, match="digest"):
        verify_frozen_plan_pool(pool, task, policy, BudgetLedger())


@pytest.mark.parametrize(
    "variant", ["missing_plan", "projection", "traversal", "identity", "kind", "probability"]
)
def test_prepared_execution_rejects_population_and_schedule_drift(tmp_path, variant):
    import json
    from arex_skill_graph.historical_plan_pool import load_prepared_plan_study

    package, task, policy = make_fixture(tmp_path)
    directory, expected, _ = _prepared_study(tmp_path, package, task, policy)
    name = "controlled-schedule.json"
    content = json.loads((directory / name).read_text())
    if variant == "missing_plan":
        content.pop()
    elif variant == "traversal":
        content[0]["relative_output"] = "../outside"
    elif variant == "kind":
        content.append({**content[0], "candidate_kind": "invented"})
    elif variant == "probability":
        content[0]["sampling_probability"] = 0
    elif variant == "projection":
        name = "plans.json"
        content = {}
    else:
        name = "study-identity.json"
        content = json.loads((directory / name).read_text())
        content["queries_sha256"] = "changed"
    (directory / name).write_text(json.dumps(content))
    with pytest.raises(ValueError):
        load_prepared_plan_study(directory, expected)
