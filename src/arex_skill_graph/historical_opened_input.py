"""Recover original public Issue inputs without importing their later repair discussion."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC
from urllib.parse import urlsplit

from .action_contracts import utc
from .history_census import redact_history


@dataclass(frozen=True)
class OriginalIssueTarget:
    query_issue: str
    repository_id: int
    created_at: str

    def __post_init__(self):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:[1-9][0-9]*", self.query_issue):
            raise ValueError("invalid original Issue identity")
        if type(self.repository_id) is not int or self.repository_id <= 0:
            raise ValueError("original Issue requires authoritative repository ID")
        utc(self.created_at)

    @property
    def repository(self):
        return self.query_issue.rsplit(":", 1)[0]

    @property
    def number(self):
        return int(self.query_issue.rsplit(":", 1)[1])

    @property
    def archive_url(self):
        at = utc(self.created_at).astimezone(UTC)
        return f"https://data.gharchive.org/{at:%Y-%m-%d}-{at.hour}.json.gz"


def original_opened_input(raw_event, target, archive_url):
    """Project only an exact original opened event; all other event data stays in memory."""
    event = json.loads(raw_event)
    issue = event.get("payload", {}).get("issue", {})
    repository = event.get("repo", {})
    if (
        event.get("type") != "IssuesEvent"
        or event.get("payload", {}).get("action") != "opened"
        or repository.get("id") != target.repository_id
        or issue.get("number") != target.number
    ):
        raise ValueError("archive event differs from requested original Issue identity")
    if (
        utc(issue["created_at"]) != utc(target.created_at)
        or utc(issue["updated_at"]) != utc(issue["created_at"])
        or utc(event["created_at"]) < utc(issue["created_at"])
        or not isinstance(event.get("id"), (int, str))
        or not str(event["id"]).isdigit()
        or event.get("public") is not True
    ):
        raise ValueError("archive event lacks exact original public input chronology")
    url = urlsplit(issue.get("html_url", ""))
    name = repository.get("name", "")
    if (
        url.scheme != "https"
        or url.hostname != "github.com"
        or url.username
        or url.password
        or url.query
        or url.fragment
        or url.path.casefold() != f"/{name}/issues/{target.number}".casefold()
        or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name)
    ):
        raise ValueError("original Issue URL differs from archived repository identity")
    source = urlsplit(archive_url)
    if (
        source.scheme != "https"
        or source.hostname != "data.gharchive.org"
        or source.username
        or source.password
        or source.query
        or source.fragment
        or not re.fullmatch(r"/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{1,2}\.json\.gz", source.path)
    ):
        raise ValueError("untrusted original Issue archive source")
    archive_day, archive_hour = source.path[1:-8].rsplit("-", 1)
    event_at = utc(event["created_at"]).astimezone(UTC)
    if archive_day != event_at.strftime("%Y-%m-%d") or int(archive_hour) != event_at.hour:
        raise ValueError("original event timestamp differs from archive hour")
    body, title = issue.get("body"), issue.get("title")
    if not isinstance(body, str) or not body.strip() or not isinstance(title, str) or not title:
        raise ValueError("original public Issue requires nonempty title and body")
    if redact_history(title + "\n\n" + body) != title + "\n\n" + body:
        raise ValueError("credential-like original text is excluded from persisted inputs")
    return {
        "query_issue": target.query_issue,
        "event_id": str(event["id"]),
        "event_type": "IssuesEvent",
        "event_created_at": event["created_at"],
        "repository_id": target.repository_id,
        "repository_name_at_event": name,
        "archive_url": archive_url,
        "raw_event_sha256": hashlib.sha256(raw_event).hexdigest(),
        "input": {
            key: issue[key]
            for key in ("number", "title", "body", "created_at", "updated_at", "html_url")
        },
        "purpose": "Original opened-event input only; later discussion and repairs excluded.",
    }


def scan_original_opened_inputs(
    stream, targets, archive_url, *, max_bytes=1024**3, max_line_bytes=8 * 1024**2
):
    """Bound decompressed reads and retain only matching original opened projections."""
    targets = tuple(targets)
    by_identity = {(t.repository_id, t.number): t for t in targets}
    if len(by_identity) != len(targets):
        raise ValueError("duplicate original Issue scan target")
    if max_bytes <= 0 or max_line_bytes <= 0:
        raise ValueError("archive scan limits must be positive")
    found, invalid, total, count = {}, {}, 0, 0
    while True:
        raw = stream.readline(min(max_line_bytes + 1, max_bytes - total + 1))
        if not raw:
            break
        total += len(raw)
        if total > max_bytes or len(raw) > max_line_bytes:
            raise ValueError("original Issue archive scan bound reached")
        event = json.loads(raw)
        count += 1
        if event.get("type") != "IssuesEvent" or event.get("payload", {}).get("action") != "opened":
            continue
        issue = event.get("payload", {}).get("issue", {})
        target = by_identity.get((event.get("repo", {}).get("id"), issue.get("number")))
        if target is None:
            continue
        try:
            opened = original_opened_input(raw, target, archive_url)
        except (ValueError, KeyError, TypeError) as error:
            invalid[target.query_issue] = str(error)
            continue
        previous = found.get(target.query_issue)
        if previous is not None and previous != opened:
            raise ValueError("conflicting original opened events for one Issue")
        found[target.query_issue] = opened
    for query_issue in invalid:
        found.pop(query_issue, None)
    return found, {
        "archive_url": archive_url,
        "decompressed_bytes_scanned": total,
        "events_scanned": count,
        "archive_scan_complete": True,
        "invalid_targets": invalid,
        "unrelated_raw_events_persisted": False,
    }


def original_input_qualification(opened, input_artifact_sha256):
    if not re.fullmatch(r"[0-9a-f]{64}", input_artifact_sha256):
        raise ValueError("original input requires exact saved artifact hash")
    return {
        "schema": "historical-query-original-opened-input-qualification-v1",
        **{
            key: opened[key]
            for key in ("query_issue", "event_id", "repository_id", "raw_event_sha256")
        },
        "canonical_repository": opened["query_issue"].rsplit(":", 1)[0],
        "input_available_at": opened["event_created_at"],
        "original_body_version_at": opened["input"]["created_at"],
        "input_artifact_sha256": input_artifact_sha256,
        "public_event_verified": True,
        "query_text_as_of_input_time_verified": True,
        "repair_tests_patch_and_later_comments_supplied": False,
        "qualification_does_not_backdate_new_information": True,
        "actual_LLM_calls": 0,
        "formal_SWE_queries": 0,
    }
