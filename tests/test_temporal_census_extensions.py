from copy import deepcopy

import pytest

from arex_skill_graph.benchmark_identity import (
    classify_original_issue_group,
    connect_issue_alias_clusters,
)
from arex_skill_graph.history_learning import validate_reviews
from arex_skill_graph.history_timeline import project_timeline_event, timeline_selection
from arex_skill_graph.history_verification import junit_observations, split_test_diff


def test_new_issue_backlog_and_exposure_are_determined_before_solver_execution():
    group = {"repository": "example/repo", "pull_number": 10034, "aliases": []}
    mapping = {
        "merged_at": "2025-01-01T00:00:00Z",
        "original_issues": [
            {"repository": "example/repo", "number": 1, "created_at": "2023-12-31T23:59:59Z"}
        ],
    }
    old = classify_original_issue_group(group, mapping, "2024-01-01T00:00:00Z")
    assert old["temporal_classification"] == "pre-cutoff-backlog-candidate"
    assert old["exposed_gold_development_only"]
    newer = deepcopy(mapping)
    newer["original_issues"][0]["created_at"] = "2024-01-01T00:00:00Z"
    assert (
        classify_original_issue_group(group, newer, "2024-01-01T00:00:00Z")[
            "temporal_classification"
        ]
        == "post-cutoff-new-issue-candidate"
    )
    both = deepcopy(newer)
    both["original_issues"].append(mapping["original_issues"][0])
    assert (
        classify_original_issue_group(group, both, "2024-01-01T00:00:00Z")[
            "temporal_classification"
        ]
        == "mixed-original-issue-dates-review-required"
    )
    mapping["original_issues"] = []
    assert not classify_original_issue_group(group, mapping, "2024-01-01T00:00:00Z")[
        "original_issue_mapping_verified"
    ]


def test_shared_original_issue_transitively_deduplicates_prs_and_propagates_exposure():
    def group(pull, issues, exposed=False):
        return {
            "repository": "example/repo",
            "pull_number": pull,
            "original_issues": [{"repository": "example/repo", "number": n} for n in issues],
            "exposed_gold_development_only": exposed,
        }

    groups = connect_issue_alias_clusters(
        [group(1, [1]), group(2, [1, 2]), group(3, [2], True), group(4, [4])]
    )
    assert len({g["issue_alias_cluster_id"] for g in groups}) == 2
    assert all(g["exposed_gold_development_only"] for g in groups[:3])
    assert not groups[-1]["exposed_gold_development_only"]
    assert all(not g["independent_bug_cluster_verified"] for g in groups)


def test_timeline_hides_later_edits_and_future_events_and_audits_scope_gap():
    cutoff = "2024-01-01T00:00:00Z"
    comment = {
        "__typename": "IssueComment",
        "id": "c",
        "createdAt": "2023-01-01T00:00:00Z",
        "lastEditedAt": "2025-01-01T00:00:00Z",
        "body": "Future solution",
    }
    assert project_timeline_event(comment, cutoff)["body"] is None
    comment["lastEditedAt"] = "2023-06-01T00:00:00Z"
    assert (
        project_timeline_event(comment, cutoff)["body_version_available_at"]
        == comment["lastEditedAt"]
    )
    comment["createdAt"] = cutoff
    assert project_timeline_event(comment, cutoff) is None
    assert project_timeline_event({"__typename": "AddedToProjectV2Event"}, cutoff) is None
    with pytest.raises(ValueError, match="unrecognized"):
        project_timeline_event({"__typename": "UnknownNewEvent"}, cutoff)
    schema = {
        "possibleTypes": [
            {"name": "AddedToProjectV2Event", "fields": []},
            {"name": "MentionedEvent", "fields": [{"name": "id"}, {"name": "createdAt"}]},
        ]
    }
    selection = timeline_selection(schema)
    assert "AddedToProjectV2Event" not in selection and "MentionedEvent" in selection


def test_model_fix_claim_without_locator_is_retained_as_audited_nonservable_disposition():
    records = [{"issue_id": "x:1", "resolution_candidates": [], "evidence": [{"id": "e"}]}]
    response = {
        "reviews": [
            {
                "issue_id": "x:1",
                "disposition": "repair_verification_pending",
                "issue_type": "code_defect",
                "mechanism": "binding scope",
                "reason": "Historical discussion describes a fix",
                "evidence_refs": ["e"],
            }
        ]
    }
    reviewed = validate_reviews(records, response)
    assert reviewed[0]["disposition"] == "insufficient_or_unrecoverable_evidence"
    assert reviewed[0]["model_requested_disposition"] == "repair_verification_pending"
    assert reviewed[0]["host_gate_reason"] == "independently-verifiable-repair-locator-missing"
    response["reviews"][0]["evidence_refs"] = ["invented"]
    with pytest.raises(ValueError, match="historical evidence"):
        validate_reviews(records, response)


def test_causal_verification_separates_test_hunks_and_interprets_individual_outcomes(tmp_path):
    patch = "diff --git a/src/checker.py b/src/checker.py\n--- a/src/checker.py\n+++ b/src/checker.py\n@@ -1 +1 @@\n-old\n+new\n"
    tests = patch.replace("src/checker.py", "tests/test_checker.py")
    production, regression, paths = split_test_diff(patch + tests)
    assert production == patch and regression == tests and paths == ["tests/test_checker.py"]
    with pytest.raises(ValueError, match="outside|escapes|contained|traverse"):
        split_test_diff(patch.replace("src/checker.py", "../../outside"))
    report = tmp_path / "junit.xml"
    report.write_text(
        '<testsuite><testcase classname="Suite" name="regression"><failure/></testcase>'
        '<testcase classname="Suite" name="adjacent"/>'
        '<testcase classname="Suite" name="unsupported"><skipped/></testcase></testsuite>'
    )
    assert junit_observations(report) == {
        "Suite::regression": "failed",
        "Suite::adjacent": "passed",
        "Suite::unsupported": "skipped",
    }
