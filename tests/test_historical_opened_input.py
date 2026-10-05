import copy
import hashlib
import io
import json

import pytest

from arex_skill_graph.historical_opened_input import (
    OriginalIssueTarget,
    original_input_qualification,
    scan_original_opened_inputs,
)

TARGET = OriginalIssueTarget("canonical/repository:42", 123, "2020-08-16T18:20:14Z")
URL = TARGET.archive_url


def event_bytes(**changes):
    event = {
        "id": "456",
        "type": "IssuesEvent",
        "public": True,
        "created_at": "2020-08-16T18:20:15Z",
        "repo": {"id": 123, "name": "previous/repository"},
        "actor": {"login": "unrelated-actor"},
        "payload": {
            "action": "opened",
            "issue": {
                "number": 42,
                "title": "Original problem",
                "body": "Public reproducer; no later repair discussion.",
                "created_at": TARGET.created_at,
                "updated_at": TARGET.created_at,
                "html_url": "https://github.com/previous/repository/issues/42",
            },
        },
    }
    for key, value in changes.items():
        if key.startswith("issue_"):
            event["payload"]["issue"][key[6:]] = value
        else:
            event[key] = value
    return (json.dumps(event) + "\n").encode()


def test_exact_opened_event_with_repository_rename_excludes_unrelated_events():
    raw = event_bytes()
    other = event_bytes(repo={"id": 999, "name": "unrelated/repository"})
    later = event_bytes(
        payload={
            "action": "closed",
            "issue": {
                "number": 42,
                "body": "LATER REPAIR must not persist",
            },
        }
    )
    found, audit = scan_original_opened_inputs(io.BytesIO(other + raw + later), [TARGET], URL)
    opened = found[TARGET.query_issue]
    assert opened["raw_event_sha256"] == hashlib.sha256(raw).hexdigest()
    assert opened["repository_name_at_event"] == "previous/repository"
    assert "LATER REPAIR" not in json.dumps(found)
    assert "unrelated-actor" not in json.dumps(found)
    assert audit["archive_scan_complete"] and audit["events_scanned"] == 3
    assert not audit["unrelated_raw_events_persisted"]
    saved = json.dumps(opened).encode()
    qualification = original_input_qualification(opened, hashlib.sha256(saved).hexdigest())
    assert qualification["input_available_at"] == opened["event_created_at"]
    assert qualification["original_body_version_at"] == TARGET.created_at


@pytest.mark.parametrize(
    "changes",
    [
        {"issue_updated_at": "2020-08-17T00:00:00Z"},
        {"issue_created_at": "2020-08-16T18:20:13Z"},
        {"issue_body": ""},
        {"public": False},
        {"issue_html_url": "https://example.invalid/previous/repository/issues/42"},
        {"created_at": "2020-08-16T18:20:13Z"},
        {"issue_body": "Credential " + "sk-" + "A" * 24},
    ],
)
def test_invalid_original_input_is_rejected_without_persisted_text(changes):
    found, audit = scan_original_opened_inputs(io.BytesIO(event_bytes(**changes)), [TARGET], URL)
    assert not found and TARGET.query_issue in audit["invalid_targets"]
    assert "body" not in audit and "Credential" not in json.dumps(audit)


def test_conflicting_opened_events_do_not_select_a_convenient_body():
    with pytest.raises(ValueError, match="conflicting"):
        scan_original_opened_inputs(
            io.BytesIO(event_bytes() + event_bytes(issue_body="Different original text")),
            [TARGET],
            URL,
        )


@pytest.mark.parametrize("limit", ["bytes", "line"])
def test_archive_read_is_bounded(limit):
    raw = event_bytes()
    options = {"max_bytes": len(raw) - 1} if limit == "bytes" else {"max_line_bytes": len(raw) - 1}
    with pytest.raises(ValueError, match="bound reached"):
        scan_original_opened_inputs(io.BytesIO(raw), [TARGET], URL, **options)


def test_duplicate_target_and_untrusted_archive_are_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        scan_original_opened_inputs(io.BytesIO(b""), [TARGET, copy.copy(TARGET)], URL)
    found, audit = scan_original_opened_inputs(
        io.BytesIO(event_bytes()), [TARGET], "https://example.invalid/2020-08-16-18.json.gz"
    )
    assert not found and "untrusted" in audit["invalid_targets"][TARGET.query_issue]


def test_opened_event_cannot_be_replayed_under_another_archive_hour():
    found, audit = scan_original_opened_inputs(
        io.BytesIO(event_bytes()), [TARGET], "https://data.gharchive.org/2020-08-16-19.json.gz"
    )
    assert not found and "archive hour" in audit["invalid_targets"][TARGET.query_issue]
