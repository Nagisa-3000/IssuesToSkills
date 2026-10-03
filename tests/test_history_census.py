import json
import subprocess
from copy import deepcopy
from typing import ClassVar

import pytest

from arex_skill_graph.history_census import (
    GitHubAPIError,
    HistoryCensus,
    project_issue,
    redact_history,
)

CUTOFF = "2024-01-01T00:00:00Z"


def test_cli_timeout_suppresses_native_output_and_retains_attempt(monkeypatch):
    from arex_skill_graph.history_census import GitHubCLI

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(["gh", "api"], 60, output="private native diagnostic")

    monkeypatch.setattr(subprocess, "run", timeout)
    api = GitHubCLI()
    with pytest.raises(RuntimeError, match="native output suppressed") as error:
        api.rest("public/path")
    assert "private native diagnostic" not in str(error.value)
    assert api.calls == 1


BEFORE = "2023-01-01T00:00:00Z"
AFTER = "2025-01-01T00:00:00Z"


def node(number=1, created=BEFORE):
    return {
        "id": "node:" + str(number),
        "number": number,
        "url": f"https://github.com/example/repo/issues/{number}",
        "title": "Current title",
        "body": "Current public problem",
        "createdAt": created,
        "updatedAt": AFTER,
        "lastEditedAt": None,
        "state": "OPEN",
        "closedAt": None,
        "comments": {"totalCount": 1},
        "timelineItems": {"nodes": [], "pageInfo": {"hasNextPage": False, "endCursor": None}},
    }


def test_as_of_title_state_body_and_fix_are_independent():
    current = node()
    current["lastEditedAt"] = AFTER
    events = [
        {
            "__typename": "ClosedEvent",
            "createdAt": "2023-02-01T00:00:00Z",
            "closer": {
                "__typename": "PullRequest",
                "number": 8,
                "mergedAt": "2023-02-01T00:00:00Z",
                "mergeCommit": {"oid": "a" * 40},
                "repository": {"nameWithOwner": "example/repo"},
            },
        },
        {
            "__typename": "RenamedTitleEvent",
            "createdAt": AFTER,
            "previousTitle": "Historical title",
            "currentTitle": "Current title",
        },
        {"__typename": "ReopenedEvent", "createdAt": AFTER},
    ]
    result = project_issue(current, events, "example/repo", CUTOFF)
    assert result["as_of"]["title"] == "Historical title"
    assert result["as_of"]["state"] == "CLOSED"
    assert result["as_of"]["body"] is None
    assert len(result["as_of"]["state_title_events"]) == 1
    assert (
        result["as_of"]["state_title_events"][0]["resolution_candidate"]["verified_resolution"]
        is False
    )
    assert result["servable_repair_knowledge"] is False
    assert result["audit"]["all_event_types_complete"] is False
    current["lastEditedAt"] = BEFORE
    assert (
        project_issue(current, events, "example/repo", CUTOFF)["as_of"]["body"] == current["body"]
    )
    events[1]["currentTitle"] = "Incorrect history"
    with pytest.raises(ValueError, match="title history"):
        project_issue(current, events, "example/repo", CUTOFF)


class FakeAPI:
    rate_limit: ClassVar[dict] = {"remaining": 100}

    def __init__(self):
        self.calls = []
        self.initial = node()
        self.changed_verification = False

    def graphql(self, query, variables):
        self.calls.append(variables)
        if variables.get("after") is None:
            values = [deepcopy(self.initial)]
            if self.changed_verification and "title body" not in query:
                values[0]["number"] = 9
            page = {"hasNextPage": True, "endCursor": "next"}
        else:
            values = [node(2, CUTOFF), node(3, AFTER)]
            page = {"hasNextPage": False, "endCursor": "end"}
        return {
            "repository": {
                "nameWithOwner": "example/repo",
                "issues": {"nodes": values, "totalCount": 3, "pageInfo": page},
            }
        }

    def rest(self, endpoint):
        return [
            {
                "id": 1,
                "created_at": BEFORE,
                "updated_at": BEFORE,
                "issue_url": "https://api.github.com/repos/example/repo/issues/1",
                "html_url": "https://github.com/example/repo/issues/1#issuecomment-1",
                "body": "Historical public observation",
            },
            {
                "id": 2,
                "created_at": BEFORE,
                "updated_at": AFTER,
                "issue_url": "https://api.github.com/repos/example/repo/issues/1",
                "html_url": "https://github.com/example/repo/issues/1#issuecomment-2",
                "body": "Unavailable later edited observation",
            },
            {
                "id": 3,
                "created_at": BEFORE,
                "updated_at": BEFORE,
                "issue_url": "https://api.github.com/repos/example/repo/issues/99",
                "html_url": "https://github.com/example/repo/pull/99#issuecomment-3",
                "body": "PR evidence is separate",
            },
            {
                "id": 4,
                "created_at": CUTOFF,
                "updated_at": CUTOFF,
                "issue_url": "https://api.github.com/repos/example/repo/issues/1",
                "html_url": "https://github.com/example/repo/issues/1#issuecomment-4",
                "body": "Boundary comment",
            },
        ]


def test_full_cursor_population_resume_independent_pass_and_comment_boundary(tmp_path):
    api = FakeAPI()
    census = HistoryCensus(tmp_path, "example/repo", CUTOFF, api, progress=lambda _: None)
    report = census.census()
    assert report["observable_pre_cutoff_issues"] == 1
    assert report["issue_pagination_complete"] is True
    assert len(api.calls) == 2
    assert report["full_history_qualified"] is False
    assert report["all_issues_have_disposition"]
    resumed = HistoryCensus(tmp_path, "example/repo", CUTOFF, api, progress=lambda _: None)
    resumed.census()
    assert len(api.calls) == 2
    assert resumed.verify_identities()["identity_second_pass_verified"] is True
    comments = resumed.collect_comments()
    assert comments["comments_pagination_complete"] is True
    page = json.loads((resumed.root / comments["comment_pages"][0]["file"]).read_text())
    assert [row["id"] for row in page["records"]] == [1, 2]
    assert page["records"][0]["body"] == "Historical public observation"
    assert page["records"][1]["body"] is None
    assert "Unavailable later edited observation" not in json.dumps(page)
    api.changed_verification = True
    with pytest.raises(ValueError, match="population changed"):
        resumed.verify_identities()
    with pytest.raises(ValueError, match="identity/cutoff"):
        HistoryCensus(tmp_path, "example/repo", BEFORE, api)
    stored = resumed.root / report["issue_pages"][0]["file"]
    stored.write_text(stored.read_text().replace("Current title", "Tampered title"))
    with pytest.raises(ValueError, match="integrity"):
        HistoryCensus(tmp_path, "example/repo", CUTOFF, api)


def test_history_redaction_covers_short_examples_auth_and_private_key():
    fixture = "fixture"
    values = [
        "password" + "='" + fixture + "'",
        "API_KEY" + "=" + fixture,
        "Authorization" + ": Basic " + fixture,
        "https://user:" + fixture + "@example.invalid/",
        "-----BEGIN PRIVATE KEY-----\n" + fixture + "\n-----END PRIVATE KEY-----",
        "sk-" + "A" * 32,
    ]
    for value in values:
        assert fixture not in redact_history(value)
        assert "REDACTED" in redact_history(value)
    assert redact_history("An AST value changes scope.") == "An AST value changes scope."


def test_deep_comment_pagination_switches_windows_without_losing_or_replacing_snapshot(tmp_path):
    class LimitedAPI(FakeAPI):
        def rest(self, endpoint):
            if "since=" not in endpoint and "page=2" in endpoint:
                raise GitHubAPIError(status="422", pagination_limited=True)
            rows = super().rest(endpoint)[:1]
            if "since=" in endpoint:
                # since filters updated_at, so this overlaps an already archived
                # comment. Its newer text must not replace the prior version.
                rows[0]["body"] = "Later edited overlapping text"
                rows.extend(
                    [
                        {
                            **rows[0],
                            "id": 2,
                            "body": "Previously unseen comment",
                            "created_at": "2023-06-01T00:00:00Z",
                        },
                        {**rows[0], "id": 3, "created_at": CUTOFF},
                    ]
                )
                return rows
            return rows * 100  # simulate API limit with 100 distinct comments

    api = LimitedAPI()
    original = api.rest

    def unique_first_page(endpoint):
        rows = original(endpoint)
        if "since=" not in endpoint:
            rows = [{**row, "id": i + 100} for i, row in enumerate(rows)]
            rows[0]["id"] = 1
        return rows

    api.rest = unique_first_page
    census = HistoryCensus(tmp_path, "example/repo", CUTOFF, api, progress=lambda _: None)
    census.census()
    report = census.collect_comments()
    assert report["comments_pagination_complete"]
    pages = [json.loads((census.root / p["file"]).read_text()) for p in report["comment_pages"]]
    records = [row for page in pages for row in page["records"]]
    assert len(records) == 101
    assert len({row["id"] for row in records}) == 101
    assert records[0]["body"] == "Historical public observation"
    assert records[-1]["body"] == "Previously unseen comment"
    assert "Later edited overlapping text" not in json.dumps(pages)
    assert pages[-1]["request_parameters"]["since"] == BEFORE
    assert HistoryCensus(tmp_path, "example/repo", CUTOFF, api).collect_comments()[
        "comments_pagination_complete"
    ]
