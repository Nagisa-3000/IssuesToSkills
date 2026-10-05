import importlib.util
import json
from pathlib import Path

from arex_skill_graph.history_census import fingerprint


def test_replay_cli_preserves_registration_stage_gaps_and_entire_denominator(tmp_path):
    source = (
        Path(__file__).resolve().parents[1] / "experiments/qualify_original_release_controls.py"
    )
    spec = importlib.util.spec_from_file_location("replay_registration_cli_test", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    queries = []
    audits = [
        {"query_id": "project/repo:1", "status": "original_input_unrecovered"},
        {
            "query_id": "project/repo:2",
            "status": "public_branch_source_or_input_gap",
            "failure_class": "TimeoutError",
            "reason": "archive read timed out",
        },
        {"query_id": "project/repo:3", "status": "registered_original_public_branch_query"},
        {"query_id": "project/repo:4", "status": "mechanical_pass"},
    ]
    register = {
        "queries_sha256": fingerprint(queries),
        "query_count": 0,
        "selected_targets": 4,
        "audits": audits,
    }
    arguments = []
    for name, value in [
        ("queries", queries),
        ("query-register", register),
        ("verifications", {"results": []}),
        ("runtime-map", {}),
    ]:
        path = tmp_path / (name + ".json")
        path.write_text(json.dumps(value))
        arguments.extend(["--" + name, str(path)])
    output = tmp_path / "results"
    assert module.main([*arguments, "--output-dir", str(output)]) == 0
    completion = json.loads((output / "completion.json").read_text())
    rows = {row["query_id"]: row for row in completion["results"]}
    assert len(rows) == completion["completed_targets"] == completion["selected_targets"] == 4
    assert rows["project/repo:1"]["status"] == "original_input_unrecovered"
    assert rows["project/repo:2"]["status"] == "public_branch_source_or_input_gap"
    assert rows["project/repo:2"]["failure_reason"] == "archive read timed out"
    assert rows["project/repo:2"]["failure_class"] == "TimeoutError"
    assert rows["project/repo:3"]["status"] == "registered_query_unavailable"
    assert rows["project/repo:4"]["status"] == "registered_query_unavailable"
    assert rows["project/repo:4"]["registration_status"] == "mechanical_pass"
    assert all(row["mechanical_controls_passed"] is False for row in rows.values())
    assert all(row["utility_labels_created"] == 0 for row in rows.values())
    assert completion["mechanical_controls_passed"] == 0
    assert completion["complete_replay_acceptances"] == 0
    assert completion["actual_LLM_calls"] == completion["new_utility_labels"] == 0
    assert completion["actor_may_read_known_repairs"] is False
