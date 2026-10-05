from copy import deepcopy
from dataclasses import asdict, replace

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import digest
from arex_skill_graph.guidance_attribution import controlled_guidance_attribution
from arex_skill_graph.ranker_training import calibration_utility
from arex_skill_graph.temporal_ranker_data import HistoricalQuery, execution_label_from_run


def controlled_run(task):
    return {
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "solver_ended": True,
        "solver_terminated": True,
        "benchmark_resolved": True,
        "failure": "",
        "requests": [
            {
                "operation": "drop_guidance",
                "arguments": {},
                "rationale": "Current prerequisites unavailable",
            },
            {
                "operation": "write_file",
                "arguments": {"path": "checker.py"},
                "rationale": "Solve normally",
            },
            {
                "operation": "record_action_observation",
                "arguments": {},
                "rationale": "Record public tests",
            },
            {"operation": "finish", "arguments": {}, "rationale": "End"},
        ],
        "public_observations": [
            {
                "operation": "drop_guidance",
                "request_index": 0,
                "observation_id": "public:observation:0",
                "fallback_reason": "Current prerequisites unavailable",
            },
            {
                "operation": "record_action_observation",
                "request_index": 2,
                "observation_id": "public:observation:2",
                "record": {"id": "action-result:0"},
            },
        ],
        "action_observations": [{"id": "action-result:0", "semantic_validation": "unreviewed"}],
        "guidance_usage": [{"plan_id": "plan:a", "parent_workflow_ids": ["workflow:a"]}],
        "guidance_request_contexts": [
            {
                "request_index": index,
                "plan_id": "plan:a" if index == 0 else None,
                "parent_workflow_ids": ["workflow:a"] if index == 0 else [],
                "context_revision": index,
                "pending_guidance_refresh": False,
                "authorization_mode": "probe_only" if index == 0 else None,
            }
            for index in range(4)
        ],
        "budget": {"model_tokens": 123},
        "evaluation": {
            "evaluation_completed": True,
            "causal_controls_passed": True,
            "evaluator_version": "synthetic-controlled",
            "evaluation_spec_sha256": "a" * 64,
            "regression_exit_codes": [0],
        },
    }


def test_success_after_drop_is_assignment_utility_and_action_record_is_unassigned(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    run = controlled_run(task)
    attribution = controlled_guidance_attribution(run)
    assert attribution["guidance_disposition"] == "explicit_fallback"
    assert attribution["active_plan_request_count"] == 1
    assert attribution["unguided_request_count"] == 3
    assert attribution["action_records_without_active_plan"] == 1
    assert not attribution["plan_execution_established"]
    run["guidance_attribution"] = attribution
    label = execution_label_from_run(
        HistoricalQuery(task, "query:cluster", "query:fix"),
        "workflow:a",
        "workflow",
        run,
        sampling_probability=1,
    )
    assert label.outcome and label.applicability is None
    assert label.execution_scope == "assigned_candidate_policy"
    assert label.guidance_disposition == "explicit_fallback"
    assert label.guidance_attribution_sha256 == digest(attribution)
    assert calibration_utility([asdict(label)]) == 1
    with pytest.raises(ValueError, match="assigned candidate policy"):
        replace(label, execution_scope="successful_workflow_execution")
    run["guidance_attribution"] = {**attribution, "plan_execution_established": True}
    with pytest.raises(ValueError, match="differs"):
        execution_label_from_run(
            HistoricalQuery(task, "query:cluster", "query:fix"),
            "workflow:a",
            "workflow",
            run,
            sampling_probability=1,
        )


def test_legacy_trace_fallback_is_known_but_active_plan_and_action_attribution_are_unknown(
    tmp_path,
):
    _, task, _ = make_fixture(tmp_path)
    run = controlled_run(task)
    del run["guidance_request_contexts"]
    for row in run["public_observations"]:
        row.pop("request_index")
    attribution = controlled_guidance_attribution(run)
    assert attribution["guidance_disposition"] == "explicit_fallback"
    assert not attribution["per_request_contexts_complete"]
    assert attribution["active_plan_request_count"] is None
    assert attribution["action_records_without_active_plan"] is None
    assert not attribution["plan_execution_established"]


def test_requested_or_denied_drop_without_successful_receipt_is_unknown(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    run = controlled_run(task)
    run["public_observations"][0] = {"operation": "drop_guidance", "denied": "Denied"}
    assert controlled_guidance_attribution(run)["guidance_disposition"] == "unknown"


@pytest.mark.parametrize("mutation", ["missing", "reordered", "false_mode", "nonboolean"])
def test_incomplete_or_invalid_request_state_fails_closed(tmp_path, mutation):
    _, task, _ = make_fixture(tmp_path)
    run = deepcopy(controlled_run(task))
    contexts = run["guidance_request_contexts"]
    if mutation == "missing":
        contexts.pop()
    elif mutation == "reordered":
        contexts[0]["request_index"] = 1
    elif mutation == "false_mode":
        contexts[0]["authorization_mode"] = None
    else:
        contexts[0]["pending_guidance_refresh"] = "false"
    with pytest.raises(ValueError, match="per-request"):
        controlled_guidance_attribution(run)


def test_legacy_execution_is_retained_but_cannot_calibrate_or_create_pairs(tmp_path):
    from arex_skill_graph.temporal_ranker_data import TrainingExample, pair_preferences

    _, task, _ = make_fixture(tmp_path)
    label = execution_label_from_run(
        HistoricalQuery(task, "query:cluster", "query:fix"),
        "workflow:a",
        "workflow",
        controlled_run(task),
        sampling_probability=1,
    )
    old = replace(
        label, execution_scope=None, guidance_disposition=None, guidance_attribution_sha256=""
    )
    with pytest.raises(ValueError, match="calibration requires"):
        calibration_utility([asdict(old)])
    a = TrainingExample(
        task.task_id,
        "cluster",
        "train",
        {},
        {"id": "workflow:a", "candidate_kind": "workflow"},
        asdict(old),
        "a" * 64,
        task.input_available_at,
    )
    b = replace(a, candidate={"id": "workflow:b", "candidate_kind": "workflow"})
    assert pair_preferences([a, b]) == ()
    attributed = [replace(a, label=asdict(label)), replace(b, label=asdict(label))]
    pairs = pair_preferences(attributed)
    assert pairs[0]["execution_scope"] == "assigned_candidate_policy"
    assert pairs[0]["target"] == 0.5
