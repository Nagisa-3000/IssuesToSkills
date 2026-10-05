import json

import pytest

from arex_skill_graph.history_census import fingerprint, write_json
from arex_skill_graph.history_learning import observable_evidence
from arex_skill_graph.history_timeline_recovery import recover_timeline_coverage

CUTOFF = "2024-01-01T00:00:00Z"
BEFORE = "2023-01-01T00:00:00Z"


def fixture_census(root):
    folder = root / "example__repo"
    identity = {
        "repository": "example/repo",
        "number": 1,
        "node_id": "issue-node",
        "created_at": BEFORE,
        "url": "https://github.com/example/repo/issues/1",
    }
    issue = {
        "records": [
            {
                "identity": identity,
                "as_of": {
                    "title": "Observed defect",
                    "body": "Original public report",
                    "state": "CLOSED",
                    "state_title_events": [
                        {"kind": "ClosedEvent", "available_at": "2023-02-01T00:00:00Z"}
                    ],
                },
                "audit": {"observed_last_body_edit_at": None},
            }
        ]
    }
    comments = {"records": []}
    old = {
        "identity": identity,
        "events": [{"__typename": "MentionedEvent", "id": "archived-mention", "createdAt": BEFORE}],
        "all_event_types_paginated": True,
        "unavailable_event_metadata": [],
        "selected_event_metadata_complete": True,
        "all_event_payload_fields_collected": False,
    }
    timeline = {"records": [old], "sha256": fingerprint([old]), "config": {}}
    write_json(folder / "issues/page.json", issue)
    write_json(folder / "comments/page.json", comments)
    write_json(folder / "timeline/page.json", timeline)
    write_json(
        folder / "manifest.json",
        {
            "repository": "example/repo",
            "cutoff_exclusive": CUTOFF,
            "issue_pagination_complete": True,
            "identity_second_pass_verified": True,
            "comments_pagination_complete": True,
            "identity_set_sha256": fingerprint([("issue-node", 1, BEFORE)]),
            "issue_pages": [{"file": "issues/page.json", "sha256": fingerprint(issue)}],
            "comment_pages": [{"file": "comments/page.json", "sha256": fingerprint(comments)}],
        },
    )
    write_json(
        folder / "timeline-manifest.json",
        {
            "cutoff_exclusive": CUTOFF,
            "identity_set_sha256": fingerprint([("issue-node", 1, BEFORE)]),
            "batches": [
                {
                    "file": "timeline/page.json",
                    "sha256": fingerprint([old]),
                    "issues": 1,
                    "events": 1,
                    "unavailable_events": 0,
                }
            ],
        },
    )
    write_json(
        root / "timeline-schema.json",
        {
            "possibleTypes": [
                {"name": "ClosedEvent", "fields": [{"name": "id"}, {"name": "createdAt"}]},
                {
                    "name": "IssueComment",
                    "fields": [
                        {"name": "id"},
                        {"name": "createdAt"},
                        {"name": "body"},
                        {"name": "lastEditedAt"},
                    ],
                },
            ]
        },
    )


class API:
    def __init__(self, *, missing=False, unavailable=False, fail_next=False):
        self.calls = 0
        self.rate_limit = {"remaining": 100}
        self.missing, self.unavailable, self.fail_next = missing, unavailable, fail_next

    def graphql(self, query, variables):
        self.calls += 1
        if self.fail_next:
            self.fail_next = False
            raise RuntimeError("temporary API failure")
        if "ids" in variables:
            if self.unavailable:
                return {"nodes": [None]}
            events = (
                []
                if self.missing
                else [
                    {
                        "__typename": "ClosedEvent",
                        "id": "real-closure",
                        "createdAt": "2023-02-01T00:00:00Z",
                        "closer": {
                            "__typename": "PullRequest",
                            "createdAt": BEFORE,
                            "mergedAt": "2025-01-01T00:00:00Z",
                            "mergeCommit": {"oid": "f" * 40},
                        },
                    }
                ]
            )
            return {
                "nodes": [
                    {
                        "id": "issue-node",
                        "timelineItems": {
                            "nodes": events,
                            "pageInfo": {"hasNextPage": not self.missing, "endCursor": "next"},
                        },
                    }
                ]
            }
        return {
            "node": {
                "timelineItems": {
                    "nodes": [
                        {
                            "__typename": "IssueComment",
                            "id": "edited-comment",
                            "databaseId": 2,
                            "createdAt": "2023-03-01T00:00:00Z",
                            "lastEditedAt": "2025-01-01T00:00:00Z",
                            "body": "FUTURE-ANSWER-TEXT",
                        },
                        {"__typename": "ReopenedEvent", "id": "future-event", "createdAt": CUTOFF},
                    ],
                    "pageInfo": {"hasNextPage": False, "endCursor": "end"},
                }
            }
        }


def test_recovery_preserves_source_and_uses_paginated_temporal_projection(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    originals = {p: p.read_bytes() for p in source.rglob("*.json")}
    api = API()
    result = recover_timeline_coverage(source, output, CUTOFF, api)
    assert result["completed"] and result["all_known_state_events_recovered"]
    assert api.calls == 2
    records = json.loads((output / "example__repo/timeline/page.json").read_text())["records"]
    events = {e["id"]: e for e in records[0]["events"]}
    assert set(events) == {"archived-mention", "real-closure", "edited-comment"}
    assert events["edited-comment"]["body"] is None
    assert events["real-closure"]["closer"]["mergedAt"] is None
    assert "FUTURE-ANSWER-TEXT" not in "".join(p.read_text() for p in output.rglob("*.json"))
    assert all(p.read_bytes() == content for p, content in originals.items())
    assert observable_evidence(output, "example/repo", CUTOFF, strict_metadata=True)[0][
        "timeline_metadata_complete"
    ]
    retry = API(fail_next=True)
    repeated = recover_timeline_coverage(source, output, CUTOFF, retry)
    assert repeated["all_known_state_events_recovered"] and retry.calls == 0


@pytest.mark.parametrize("unavailable", [False, True])
def test_missing_or_unavailable_events_stay_explicit_gaps(tmp_path, unavailable):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    result = recover_timeline_coverage(
        source, output, CUTOFF, API(missing=True, unavailable=unavailable)
    )
    assert result["completed"] and not result["all_known_state_events_recovered"]
    assert result["repositories"][0]["remaining_gap_issues"] == [1]
    record = observable_evidence(output, "example/repo", CUTOFF, strict_metadata=True)[0]
    assert not record["timeline_metadata_complete"]
    assert not any(e["kind"] == "ClosedEvent" for e in record["evidence"])


def test_failed_recovery_is_not_learning_input_and_resumes_same_checkpoint(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    with pytest.raises(RuntimeError, match="temporary API failure"):
        recover_timeline_coverage(source, output, CUTOFF, API(fail_next=True))
    with pytest.raises(ValueError, match="must finish"):
        observable_evidence(output, "example/repo", CUTOFF, strict_metadata=True)
    assert recover_timeline_coverage(source, output, CUTOFF, API())["completed"]


def test_changed_sources_and_tampered_recovery_checkpoints_are_rejected(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    recover_timeline_coverage(source, output, CUTOFF, API())
    checkpoint = output / "recovery/example__repo/batch-00001.json"
    old = checkpoint.read_bytes()
    changed = json.loads(old)
    changed["records"][0]["events"] = []
    write_json(checkpoint, changed)
    with pytest.raises(ValueError, match="checkpoint changed"):
        recover_timeline_coverage(source, output, CUTOFF, API())
    checkpoint.write_bytes(old)
    schema = source / "timeline-schema.json"
    value = json.loads(schema.read_text())
    value["new_metadata"] = True
    write_json(schema, value)
    with pytest.raises(ValueError, match="source/configuration changed"):
        recover_timeline_coverage(source, output, CUTOFF, API())


def test_recovery_refuses_to_replace_or_nest_source(tmp_path):
    source = tmp_path / "source"
    fixture_census(source)
    for output in [source, source / "nested", tmp_path]:
        with pytest.raises(ValueError, match="separate"):
            recover_timeline_coverage(source, output, CUTOFF, API())


def test_http_transport_keeps_authentication_out_of_query_and_suppresses_errors():
    import io
    from urllib.error import HTTPError

    from arex_skill_graph.history_census import GitHubAPIError
    from arex_skill_graph.history_http import GitHubHTTP

    class Opener:
        def __init__(self, result):
            self.result, self.requests = result, []

        def open(self, request, timeout):
            self.requests.append(request)
            if isinstance(self.result, Exception):
                raise self.result
            return io.BytesIO(json.dumps(self.result).encode())

    token = "synthetic-runtime-fixture"
    opener = Opener({"data": {"nodes": [], "rateLimit": {"remaining": 10}}})
    api = GitHubHTTP(token, opener=opener)
    assert (
        api.graphql("query($ids:[ID!]!){nodes(ids:$ids){id}}", {"ids": ["public-node"]})["nodes"]
        == []
    )
    request = opener.requests[0]
    assert request.get_header("Authorization") == "Bearer " + token
    assert token.encode() not in request.data
    assert api.calls == 1 and api.rate_limit["remaining"] == 10
    failure = Opener(
        HTTPError("https://api.github.com/graphql", 403, "private diagnostic", {}, None)
    )
    with pytest.raises(GitHubAPIError) as error:
        GitHubHTTP(token, opener=failure).graphql("query", {})
    assert "private diagnostic" not in str(error.value) and token not in str(error.value)
    partial = Opener({"data": {"nodes": []}, "errors": [{"message": "private diagnostic"}]})
    with pytest.raises(RuntimeError, match="native output suppressed") as error:
        GitHubHTTP(token, opener=partial).graphql("query", {})
    assert "private diagnostic" not in str(error.value)


def test_manifest_paths_cannot_escape_census_or_copy_nonpublic_files(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    manifest_path = source / "example__repo/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["issue_pages"][0]["file"] = "../../outside.json"
    write_json(manifest_path, manifest)
    api = API()
    with pytest.raises(ValueError, match="contained|escapes|traverse|outside"):
        recover_timeline_coverage(source, output, CUTOFF, api)
    assert api.calls == 0
    (source / "runtime-config.txt").write_text("non-census data")
    with pytest.raises(ValueError, match="public JSON census"):
        recover_timeline_coverage(source, tmp_path / "another", CUTOFF, api)


def test_failed_request_journal_is_retained_and_counted_across_resume(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    with pytest.raises(RuntimeError, match="temporary API failure"):
        recover_timeline_coverage(source, output, CUTOFF, API(fail_next=True))
    first = json.loads((output / "recovery-api-calls/request-000001.json").read_text())
    assert first["status"] == "failed" and first["transport_calls_delta"] == 1
    assert first["failure_type"] == "RuntimeError"
    assert "temporary API failure" not in json.dumps(first)
    result = recover_timeline_coverage(source, output, CUTOFF, API())
    assert result["api_journal"]["request_attempts"] == 3
    assert result["api_journal"]["failed_requests"] == 1
    assert result["api_journal"]["successful_requests"] == 2
    assert result["api_journal"]["transport_calls_recorded"] == 3
    replay = API(fail_next=True)
    repeated = recover_timeline_coverage(source, output, CUTOFF, replay)
    assert replay.calls == 0 and repeated["api_journal"] == result["api_journal"]


def test_recovery_rejects_changed_population_and_copied_schema(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    recover_timeline_coverage(source, output, CUTOFF, API())
    copied = output / "timeline-schema.json"
    value = json.loads(copied.read_text())
    value["changed"] = True
    write_json(copied, value)
    with pytest.raises(ValueError, match="copied census/schema changed"):
        recover_timeline_coverage(source, output, CUTOFF, API())
    copied.write_bytes((source / "timeline-schema.json").read_bytes())
    manifest_path = source / "example__repo/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["identity_set_sha256"] = "incorrect-population-seal"
    write_json(manifest_path, manifest)
    timeline_path = source / "example__repo/timeline-manifest.json"
    timeline = json.loads(timeline_path.read_text())
    timeline["identity_set_sha256"] = "incorrect-population-seal"
    write_json(timeline_path, timeline)
    with pytest.raises(ValueError, match="population seal changed"):
        recover_timeline_coverage(source, tmp_path / "new-output", CUTOFF, API())


def test_recovery_rejects_symlinked_output_checkpoint(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    recover_timeline_coverage(source, output, CUTOFF, API())
    checkpoint = output / "recovery/example__repo/batch-00001.json"
    outside = tmp_path / "outside.json"
    outside.write_bytes(checkpoint.read_bytes())
    checkpoint.unlink()
    checkpoint.symlink_to(outside)
    with pytest.raises(ValueError, match="symlinks"):
        recover_timeline_coverage(source, output, CUTOFF, API())


class StateViewAPI(API):
    def graphql(self, query, variables):
        self.calls += 1
        state_view = "itemTypes:[CLOSED_EVENT,REOPENED_EVENT,RENAMED_TITLE_EVENT]" in query
        if "ids" in variables:
            events = []
            if state_view:
                events = [
                    {
                        "__typename": "RenamedTitleEvent",
                        "id": "real-title",
                        "createdAt": BEFORE,
                        "previousTitle": "old",
                        "currentTitle": "Observed defect",
                    }
                ]
            return {
                "nodes": [
                    {
                        "id": "issue-node",
                        "timelineItems": {
                            "nodes": events,
                            "pageInfo": {"hasNextPage": state_view, "endCursor": "state-next"},
                        },
                    }
                ]
            }
        assert state_view, "state-view pagination must preserve its explicit item filter"
        return {
            "node": {
                "timelineItems": {
                    "nodes": [
                        {
                            "__typename": "ClosedEvent",
                            "id": "real-closure",
                            "createdAt": "2023-02-01T00:00:00Z",
                        }
                    ],
                    "pageInfo": {"hasNextPage": False, "endCursor": "state-end"},
                }
            }
        }


def test_explicit_state_view_recovers_real_omitted_events_and_preserves_filtered_pagination(
    tmp_path,
):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    api = StateViewAPI()
    result = recover_timeline_coverage(source, output, CUTOFF, api)
    assert result["all_known_state_events_recovered"] and api.calls == 3
    record = json.loads((output / "example__repo/timeline/page.json").read_text())["records"][0]
    assert {e["id"] for e in record["events"]} == {"archived-mention", "real-title", "real-closure"}
    assert record["all_event_types_paginated"]
    assert record["state_title_view_lineage"]["events_observed"] == 2
    assert record["state_title_view_lineage"]["all_selected_state_event_types_paginated"]
    assert result["api_journal"]["successful_requests"] == 3
    repeated = recover_timeline_coverage(source, output, CUTOFF, API(fail_next=True))
    assert repeated["api_journal"] == result["api_journal"]


def test_default_recovery_reader_withholds_future_resolution_on_untargeted_records(tmp_path):
    source, output = tmp_path / "source", tmp_path / "recovered"
    fixture_census(source)
    page_path = source / "example__repo/timeline/page.json"
    content = json.loads(page_path.read_text())
    events = content["records"][0]["events"]
    events.extend(
        [
            {
                "__typename": "ClosedEvent",
                "id": "existing-closure",
                "createdAt": "2023-02-01T00:00:00Z",
            },
            {
                "__typename": "CrossReferencedEvent",
                "id": "pre-cutoff-reference",
                "createdAt": BEFORE,
                "source": {
                    "__typename": "PullRequest",
                    "id": "pr-node",
                    "number": 2,
                    "createdAt": BEFORE,
                    "mergedAt": "2025-01-01T00:00:00Z",
                    "mergeCommit": {"oid": "f" * 40},
                    "repository": {"nameWithOwner": "example/repo"},
                },
            },
        ]
    )
    content["sha256"] = fingerprint(content["records"])
    write_json(page_path, content)
    manifest_path = source / "example__repo/timeline-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["batches"][0]["sha256"] = fingerprint(content["records"])
    write_json(manifest_path, manifest)
    api = API(fail_next=True)
    result = recover_timeline_coverage(source, output, CUTOFF, api)
    assert result["all_known_state_events_recovered"] and api.calls == 0
    record = observable_evidence(
        output, "example/repo", CUTOFF, repair_locator_mode="all_pre_cutoff_mentions"
    )[0]
    event = next(e for e in record["evidence"] if e["kind"] == "CrossReferencedEvent")
    assert event["metadata"]["source"]["mergedAt"] is None
    assert event["metadata"]["source"]["mergeCommit"] is None
    assert event["metadata"]["source"]["post_cutoff_resolution_withheld"]
    assert not record["resolution_candidates"]
