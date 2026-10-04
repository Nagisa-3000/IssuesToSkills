import json
from copy import deepcopy

import pytest

from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.history_learning import (
    observable_evidence,
    reuse_unchanged_reviews,
    review_identity,
    review_population,
)
from arex_skill_graph.history_text_recovery import load_text_recovery, project_past_body
from arex_skill_graph.history_timeline import temporal_event_view
from arex_skill_graph.llm_http import OpenAICompatibleConfig

CUTOFF = "2024-01-01T00:00:00Z"
BEFORE = "2023-06-01T00:00:00Z"
AFTER = "2025-01-01T00:00:00Z"


def test_recovery_uses_verified_complete_versions_and_the_actual_edit_date():
    node = {"createdAt": "2022-01-01T00:00:00Z", "lastEditedAt": AFTER, "body": "Later text"}
    edits = [
        {"id": "latest", "editedAt": AFTER, "createdAt": AFTER, "diff": "Later text"},
        {"id": "boundary", "editedAt": CUTOFF, "createdAt": AFTER, "diff": "Boundary text"},
        {"id": "old", "editedAt": BEFORE, "createdAt": AFTER, "diff": "Historical public text"},
    ]
    result = project_past_body(node, edits, CUTOFF)
    assert result["body"] == "Historical public text"
    assert result["version_available_at"] == BEFORE
    assert result["current-version-equality-verified"] is True
    wrong = deepcopy(edits)
    wrong[0]["diff"] = "A textual delta rather than a verified full version"
    assert project_past_body(node, wrong, CUTOFF)["body"] is None
    wrong = deepcopy(edits)
    wrong[-1]["diff"] = None
    assert project_past_body(node, wrong, CUTOFF)["status"] == "unrecoverable"
    with pytest.raises(ValueError, match="post-cutoff"):
        project_past_body({**node, "createdAt": CUTOFF}, edits, CUTOFF)


def test_as_of_view_withholds_related_prs_future_merge_identity_without_changing_archive():
    event = {
        "__typename": "CrossReferencedEvent",
        "createdAt": BEFORE,
        "source": {
            "__typename": "PullRequest",
            "createdAt": BEFORE,
            "mergedAt": AFTER,
            "mergeCommit": {"oid": "f" * 40},
        },
    }
    result = temporal_event_view(event, CUTOFF)
    assert result["source"]["mergedAt"] is None
    assert result["source"]["mergeCommit"] is None
    assert result["source"]["post_cutoff_resolution_withheld"] is True
    assert event["source"]["mergeCommit"]["oid"] == "f" * 40
    event["source"]["createdAt"] = AFTER
    assert temporal_event_view(event, CUTOFF)["source"] is None


def versioned_fixture(tmp_path):
    folder = tmp_path / "census" / "example__repo"
    identity = {
        "repository": "example/repo",
        "node_id": "issue-node",
        "number": 1,
        "created_at": "2022-01-01T00:00:00Z",
        "url": "https://github.com/example/repo/issues/1",
    }
    issue_page = {
        "records": [
            {
                "identity": identity,
                "as_of": {
                    "title": "Historical title",
                    "body": None,
                    "state": "OPEN",
                    "state_title_events": [],
                },
                "audit": {"observed_last_body_edit_at": AFTER},
            }
        ]
    }
    comment_page = {
        "records": [
            {"id": 10, "issue_number": 1, "body": None, "available_at": "2022-02-01T00:00:00Z"}
        ]
    }
    timeline = [
        {
            "identity": identity,
            "events": [
                {
                    "__typename": "IssueComment",
                    "id": "comment-node",
                    "databaseId": 10,
                    "createdAt": "2022-02-01T00:00:00Z",
                    "lastEditedAt": AFTER,
                    "body": None,
                }
            ],
            "unavailable_event_metadata": [
                {"event_type": "AddedToProjectV2Event", "reason": "unavailable-project-scope"}
            ],
        }
    ]
    write_json(folder / "issues.json", issue_page)
    write_json(folder / "comments.json", comment_page)
    write_json(folder / "timeline.json", {"records": timeline})
    write_json(
        folder / "manifest.json",
        {
            "repository": "example/repo",
            "cutoff_exclusive": CUTOFF,
            "issue_pagination_complete": True,
            "identity_second_pass_verified": True,
            "comments_pagination_complete": True,
            "identity_set_sha256": "fixture-identities",
            "issue_pages": [{"file": "issues.json", "sha256": fingerprint(issue_page)}],
            "comment_pages": [{"file": "comments.json", "sha256": fingerprint(comment_page)}],
        },
    )
    write_json(
        folder / "timeline-manifest.json",
        {
            "cutoff_exclusive": CUTOFF,
            "identity_set_sha256": "fixture-identities",
            "batches": [{"file": "timeline.json", "sha256": fingerprint(timeline)}],
        },
    )
    common = {
        "repository": "example/repo",
        "issue_number": 1,
        "body": "Recovered public text",
        "status": "recovered",
        "version_available_at": BEFORE,
        "body_edit_pagination_complete": True,
        "current-version-equality-verified": True,
        "recovery_basis": "github-user-content-edit-full-version",
    }
    rows = [
        {**common, "kind": "Issue", "node_id": "issue-node"},
        {**common, "kind": "IssueComment", "node_id": "comment-node", "comment_id": 10},
    ]
    recovery = tmp_path / "recovery" / "text-recovery-manifest.json"
    write_recovery(recovery, rows)
    return folder.parent, recovery


def write_recovery(path, rows):
    write_json(
        path.parent / "page.json",
        {
            "config": {"cutoff_exclusive": CUTOFF},
            "records": rows,
            "sha256": fingerprint(rows),
            "current-post-cutoff-text-persisted": False,
        },
    )
    write_json(
        path,
        {
            "schema": "historical-github-body-version-recovery-v1",
            "cutoff_exclusive": CUTOFF,
            "target_count": len(rows),
            "recovered_count": len(rows),
            "records": rows,
            "pages": [{"file": "page.json", "sha256": fingerprint(rows)}],
            "post_cutoff_text_persisted": False,
        },
    )


def test_explicit_supplement_adds_old_versions_without_replacing_base_census(tmp_path):
    root, supplement = versioned_fixture(tmp_path)
    before = observable_evidence(root, "example/repo", CUTOFF)
    after = observable_evidence(
        root, "example/repo", CUTOFF, text_recovery=supplement, strict_metadata=True
    )
    assert before[0]["missing_original_body"] is True
    assert after[0]["missing_original_body"] is False
    assert after[0]["timeline_metadata_complete"] is False
    assert after[0]["timeline_metadata_gaps"][0]["event_type"] == "AddedToProjectV2Event"
    entries = {entry["id"]: entry for entry in after[0]["evidence"]}
    assert entries["example/repo:1:body"]["available_at"] == BEFORE
    assert entries["example/repo:1:comment:10"]["available_at"] == BEFORE
    assert observable_evidence(root, "example/repo", CUTOFF) == before
    assert "Later text" not in json.dumps(after)


def test_text_supplement_hash_identity_and_cutoff_are_enforced(tmp_path):
    root, path = versioned_fixture(tmp_path)
    assert len(load_text_recovery(path, CUTOFF)) == 2
    with pytest.raises(ValueError, match="identity/cutoff"):
        load_text_recovery(path, AFTER)
    page = path.parent / "page.json"
    page.write_text(page.read_text().replace("Recovered public text", "Tampered"))
    with pytest.raises(ValueError, match="integrity"):
        load_text_recovery(path, CUTOFF)
    report = json.loads(path.read_text())
    report["records"][0]["node_id"] = "wrong-issue"
    write_recovery(path, report["records"])
    with pytest.raises(ValueError, match="different identity"):
        observable_evidence(root, "example/repo", CUTOFF, text_recovery=path)
    report["records"][0]["node_id"] = "issue-node"
    report["records"][0]["version_available_at"] = CUTOFF
    write_recovery(path, report["records"])
    with pytest.raises(ValueError, match="pre-cutoff"):
        load_text_recovery(path, CUTOFF)


def review_fixture(tmp_path):
    records = [
        {
            "issue_id": f"example/repo:{number}",
            "resolution_candidates": [],
            "evidence": [
                {"id": f"example/repo:{number}:body", "text": "Public historical evidence"}
            ],
        }
        for number in (1, 2)
    ]
    reviews = [
        {
            "issue_id": row["issue_id"],
            "disposition": "unresolved_hypothesis",
            "issue_type": "code_defect",
            "mechanism": "A scoped inference failure",
            "reason": "The available discussion has no implemented repair",
            "evidence_refs": [row["evidence"][0]["id"]],
        }
        for row in records
    ]
    config = OpenAICompatibleConfig(
        "synthetic-runtime-fixture", "https://example.invalid/v1", "fixture-model"
    )
    prior = tmp_path / "prior"
    write_json(
        prior / "review-00001.json",
        {
            "config": review_identity(records, config),
            "reviews": reviews,
            "sha256": fingerprint(reviews),
        },
    )
    return records, reviews, config, prior


def test_only_unchanged_complete_inputs_reuse_prior_semantic_reviews(tmp_path):
    records, reviews, config, prior = review_fixture(tmp_path)
    changed = deepcopy(records)
    changed[1]["evidence"][0]["text"] = "Recovered additional evidence"
    reused = reuse_unchanged_reviews(changed, records, prior, config)
    assert [row["issue_id"] for row in reused] == ["example/repo:1"]
    assert reused[0]["review"] == reviews[0]
    with pytest.raises(ValueError, match="population"):
        reuse_unchanged_reviews(changed[:1], records, prior, config)
    bad_config = OpenAICompatibleConfig(
        "synthetic-runtime-fixture", config.base_url, "different-model"
    )
    with pytest.raises(ValueError, match="integrity"):
        reuse_unchanged_reviews(changed, records, prior, bad_config)


def test_full_unchanged_population_reuses_reviews_without_model_calls(tmp_path, monkeypatch):
    records, _, config, prior = review_fixture(tmp_path)

    def forbidden_call(*args, **kwargs):
        raise AssertionError("unchanged evidence should not trigger a model call")

    monkeypatch.setattr(
        "arex_skill_graph.history_learning.OpenAICompatibleTransport", forbidden_call
    )
    result = review_population(
        records, tmp_path / "new", config, prior_records=records, prior_output=prior
    )
    assert result["all_issues_reviewed"] is True
    assert result["reviewed_issue_count"] == result["reused_unchanged_issue_count"] == 2
    assert result["new_review_population_count"] == 0
    assert result["full_history_qualified"] is False
    with pytest.raises(ValueError, match="separate"):
        review_population(records, prior, config, prior_records=records, prior_output=prior)


def _set_state_title_coverage(root, state_events, events, *, omit_timeline_row=False):
    folder = root / "example__repo"
    issue = json.loads((folder / "issues.json").read_text())
    issue["records"][0]["as_of"]["state_title_events"] = state_events
    write_json(folder / "issues.json", issue)
    manifest = json.loads((folder / "manifest.json").read_text())
    manifest["issue_pages"][0]["sha256"] = fingerprint(issue)
    write_json(folder / "manifest.json", manifest)
    timeline = json.loads((folder / "timeline.json").read_text())
    timeline["records"][0]["events"] = events
    timeline["records"][0]["all_event_types_paginated"] = True
    timeline["records"][0]["unavailable_event_metadata"] = []
    if omit_timeline_row:
        timeline["records"] = []
    write_json(folder / "timeline.json", timeline)
    tm = json.loads((folder / "timeline-manifest.json").read_text())
    tm["batches"][0]["sha256"] = fingerprint(timeline["records"])
    tm["all_event_types_paginated"] = True
    write_json(folder / "timeline-manifest.json", tm)


def test_paginated_timeline_cannot_hide_independently_observed_closure_or_rename(tmp_path):
    # Pylint #8120's archived all-type timeline had a PR mention and comments,
    # but omitted the closure and rename retained by the earlier state census.
    root, _ = versioned_fixture(tmp_path)
    states = [
        {"kind": "RenamedTitleEvent", "available_at": "2023-01-27T19:34:35Z"},
        {"kind": "ClosedEvent", "available_at": "2023-01-28T09:29:30Z"},
    ]
    mention = {
        "__typename": "CrossReferencedEvent",
        "id": "pr-mention",
        "createdAt": "2023-01-27T21:16:31Z",
        "willCloseTarget": False,
        "source": {
            "__typename": "PullRequest",
            "number": 2,
            "repository": {"nameWithOwner": "example/repo"},
            "createdAt": "2023-01-27T21:16:31Z",
            "mergedAt": "2023-01-28T09:29:29Z",
            "mergeCommit": {"oid": "a" * 40},
        },
    }
    _set_state_title_coverage(root, states, [mention])
    files = {p: p.read_bytes() for p in root.rglob("*.json")}
    result = observable_evidence(
        root, "example/repo", CUTOFF, strict_metadata=True,
        repair_locator_mode="all_pre_cutoff_mentions",
    )[0]
    assert result["timeline_metadata_complete"] is False
    assert {gap["event_type"] for gap in result["timeline_metadata_gaps"]} == {
        "ClosedEvent", "RenamedTitleEvent"
    }
    assert result["resolution_candidates"][0]["relationship"] == "mention_only_not_verified_resolution"
    assert not any(e["kind"] == "ClosedEvent" for e in result["evidence"])
    assert all(p.read_bytes() == content for p, content in files.items())


def test_current_timeline_with_all_known_state_events_retains_actual_closure_proof(tmp_path):
    root, _ = versioned_fixture(tmp_path)
    states = [{"kind": "ClosedEvent", "available_at": "2023-01-28T09:29:30Z"}]
    close = {
        "__typename": "ClosedEvent",
        "id": "actual-closure-node",
        "createdAt": "2023-01-28T09:29:30+00:00",
        "closer": {
            "__typename": "PullRequest",
            "number": 2,
            "repository": {"nameWithOwner": "example/repo"},
            "createdAt": "2023-01-27T21:16:31Z",
            "mergedAt": "2023-01-28T09:29:29Z",
            "mergeCommit": {"oid": "a" * 40},
        },
    }
    _set_state_title_coverage(root, states, [close])
    result = observable_evidence(
        root, "example/repo", CUTOFF, strict_metadata=True,
        repair_locator_mode="all_pre_cutoff_mentions",
    )[0]
    assert result["timeline_metadata_complete"] is True
    assert "timeline_metadata_gaps" not in result
    assert result["resolution_candidates"][0]["relationship"] == "direct_closure"
    assert result["resolution_candidates"][0]["source_event_id"].endswith("actual-closure-node")


def test_timeline_manifest_does_not_imply_coverage_for_an_absent_issue(tmp_path):
    root, _ = versioned_fixture(tmp_path)
    _set_state_title_coverage(root, [], [], omit_timeline_row=True)
    result = observable_evidence(root, "example/repo", CUTOFF, strict_metadata=True)[0]
    assert result["timeline_metadata_complete"] is False
    assert result["timeline_metadata_gaps"] == [
        {"reason": "issue-missing-from-paginated-timeline"}
    ]


def test_state_title_coverage_does_not_require_post_cutoff_events():
    from arex_skill_graph.history_timeline import state_title_coverage_gaps

    states = [
        {"kind": "ClosedEvent", "available_at": CUTOFF},
        {"kind": "ReopenedEvent", "available_at": AFTER},
    ]
    assert state_title_coverage_gaps(states, [], CUTOFF) == []
