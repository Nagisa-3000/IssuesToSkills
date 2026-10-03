"""Complete observable issue census with strictly separated as-of text."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode

from .action_contracts import utc
from .direct_skill_extraction import safe_text

ISSUE_FIELDS = """
id number url title body createdAt updatedAt lastEditedAt state closedAt
comments { totalCount }
timelineItems(first:10,itemTypes:[CLOSED_EVENT,REOPENED_EVENT,RENAMED_TITLE_EVENT]) {
  nodes {
    __typename
    ... on ClosedEvent {
      createdAt
      closer {
        __typename
        ... on PullRequest { number mergedAt mergeCommit { oid } repository { nameWithOwner } }
        ... on Commit { oid committedDate repository { nameWithOwner } }
      }
    }
    ... on ReopenedEvent { createdAt }
    ... on RenamedTitleEvent { createdAt previousTitle currentTitle }
  }
  pageInfo { hasNextPage endCursor }
}
"""
ISSUES_QUERY = """
query($owner:String!,$name:String!,$after:String) {
 repository(owner:$owner,name:$name) {
  nameWithOwner
  issues(first:100,after:$after,orderBy:{field:CREATED_AT,direction:ASC}) {
   totalCount nodes { FIELDS } pageInfo {hasNextPage endCursor}
  }
 }
 rateLimit {cost remaining resetAt}
}
""".replace("FIELDS", ISSUE_FIELDS)
TIMELINE_QUERY = """
query($id:ID!,$after:String) {
 node(id:$id) { ... on Issue {
  timelineItems(first:100,after:$after,itemTypes:[CLOSED_EVENT,REOPENED_EVENT,RENAMED_TITLE_EVENT]) {
   nodes {
    __typename
    ... on ClosedEvent {
     createdAt
     closer {
      __typename
      ... on PullRequest { number mergedAt mergeCommit {oid} repository {nameWithOwner} }
      ... on Commit {oid committedDate repository {nameWithOwner}}
     }
    }
    ... on ReopenedEvent {createdAt}
    ... on RenamedTitleEvent {createdAt previousTitle currentTitle}
   }
   pageInfo {hasNextPage endCursor}
  }
 } }
 rateLimit {cost remaining resetAt}
}
"""
IDENTITIES_QUERY = """
query($owner:String!,$name:String!,$after:String) {
 repository(owner:$owner,name:$name) {
  issues(first:100,after:$after,orderBy:{field:CREATED_AT,direction:ASC}) {
   nodes {id number createdAt} pageInfo {hasNextPage endCursor}
  }
 }
 rateLimit {cost remaining resetAt}
}
"""


def now():
    return datetime.now(UTC).isoformat()


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()


def redact_history(value):
    """Redact public credential examples as well as recognizable real literals."""
    value = safe_text(value)
    value = re.sub(
        r"-----BEGIN [^\n]*PRIVATE KEY-----[\s\S]*?-----END [^\n]*PRIVATE KEY-----",
        "[REDACTED PRIVATE KEY]",
        value,
    )
    value = re.sub(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/=-]+", "[REDACTED AUTH]", value)
    value = re.sub(
        r"(?im)^.*\b(?:api[_-]?key|password|passwd|access[_-]?token|refresh[_-]?token|"
        r"client[_-]?secret|authorization|cookie|aws_secret_access_key|"
        r"[A-Z][A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API_KEY))"
        r"""["']?\s*(?:[:=]|\bis\b).*$""",
        "[REDACTED CREDENTIAL LINE]",
        value,
    )
    value = re.sub(r"(?i)(https?://)[^\s/:@]+:[^\s/@]+@", r"\1[REDACTED]@", value)
    return value


def write_json(path, value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if safe_text(encoded) != encoded:
        raise ValueError("credential-like artifact rejected; values suppressed")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".pending")
    temporary.write_text(encoded)
    temporary.replace(path)


class GitHubAPIError(RuntimeError):
    def __init__(self, *, status=None, pagination_limited=False):
        self.status = status
        self.pagination_limited = pagination_limited
        super().__init__(f"public GitHub API failed (status={status}); native output suppressed")


class GitHubCLI:
    """Use the configured CLI credential broker without reading credentials."""

    def __init__(self, executable="gh"):
        self.executable = str(executable)
        self.calls = 0
        self.rate_limit = None

    def _call(self, arguments, payload=None):
        self.calls += 1
        try:
            result = subprocess.run(
                [self.executable, "api", *arguments],
                input=json.dumps(payload) if payload is not None else None,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                "public GitHub request timed out; native output suppressed"
            ) from None
        if result.returncode:
            try:
                error = json.loads(result.stdout.lstrip("\ufeff"))
            except (ValueError, TypeError):
                error = {}
            raise GitHubAPIError(
                status=error.get("status"),
                pagination_limited="pagination is limited for this resource"
                in error.get("message", ""),
            )
        response = json.loads(result.stdout.lstrip("\ufeff"))
        if isinstance(response, dict) and response.get("errors"):
            raise RuntimeError("public GraphQL query failed; native output suppressed")
        return response

    def graphql(self, query, variables):
        result = self._call(["graphql", "--input", "-"], {"query": query, "variables": variables})[
            "data"
        ]
        self.rate_limit = result.get("rateLimit")
        return result

    def rest(self, endpoint):
        return self._call([endpoint, "--method", "GET"])


def complete_state_title_timeline(api, node):
    connection = node["timelineItems"]
    events = list(connection["nodes"])
    seen = set()
    while connection["pageInfo"]["hasNextPage"]:
        cursor = connection["pageInfo"]["endCursor"]
        if not cursor or cursor in seen:
            raise ValueError("state/title timeline pagination did not advance")
        seen.add(cursor)
        result = api.graphql(TIMELINE_QUERY, {"id": node["id"], "after": cursor})
        connection = result["node"]["timelineItems"]
        events.extend(connection["nodes"])
    dates = [utc(event["createdAt"]) for event in events]
    if dates != sorted(dates):
        raise ValueError("state/title timeline chronology is inconsistent")
    return events


def project_issue(node, events, repository, cutoff):
    limit = utc(cutoff)
    if utc(node["createdAt"]) >= limit:
        raise ValueError("post-cutoff issue cannot enter history")
    title = node["title"]
    for event in reversed(events):
        if event["__typename"] == "RenamedTitleEvent":
            if title != event["currentTitle"]:
                raise ValueError("title history cannot reconstruct current title")
            if utc(event["createdAt"]) >= limit:
                title = event["previousTitle"]
            else:
                break
    edited = node["lastEditedAt"]
    recoverable = edited is None or utc(edited) < limit
    historical_events = []
    for event in events:
        if utc(event["createdAt"]) >= limit:
            continue
        row = {"kind": event["__typename"], "available_at": event["createdAt"]}
        if event["__typename"] == "RenamedTitleEvent":
            row["previous_title"] = redact_history(event["previousTitle"])
            row["title"] = redact_history(event["currentTitle"])
        closer = event.get("closer")
        if closer:
            if closer["__typename"] == "PullRequest":
                merged = closer["mergedAt"]
                if merged and utc(merged) < limit:
                    row["resolution_candidate"] = {
                        "repository": closer["repository"]["nameWithOwner"],
                        "pull_number": closer["number"],
                        "merged_at": merged,
                        "commit": (closer.get("mergeCommit") or {}).get("oid"),
                        "verified_resolution": False,
                    }
            elif closer["__typename"] == "Commit":
                row["resolution_candidate"] = {
                    "repository": closer["repository"]["nameWithOwner"],
                    "commit": closer["oid"],
                    "verified_resolution": False,
                }
        historical_events.append(row)
    state = node["state"]
    for event in reversed(events):
        if utc(event["createdAt"]) < limit:
            break
        if event["__typename"] == "ClosedEvent":
            state = "OPEN"
        elif event["__typename"] == "ReopenedEvent":
            state = "CLOSED"
    body = redact_history(node["body"] or "") if recoverable else None
    return {
        "identity": {
            "repository": repository,
            "number": node["number"],
            "node_id": node["id"],
            "url": node["url"],
            "created_at": node["createdAt"],
        },
        "as_of": {
            "cutoff_exclusive": cutoff,
            "title": redact_history(title),
            "body": body,
            "body_status": "available" if recoverable else "post-cutoff-edit-history-unrecovered",
            "state": state,
            "state_title_events": historical_events,
        },
        "audit": {
            "observed_updated_at": node["updatedAt"],
            "observed_last_body_edit_at": edited,
            "current_comment_count": node["comments"]["totalCount"],
            "state_title_timeline_complete": True,
            "all_event_types_complete": False,
            "comments_complete": False,
            "text_redacted_before_persistence": True,
        },
        "disposition": "insufficient_or_unrecoverable_evidence",
        "disposition_reasons": [
            "resolution-and-semantic-review-pending",
            *([] if recoverable else ["original-body-version-unrecovered"]),
        ],
        "servable_repair_knowledge": False,
    }


class HistoryCensus:
    def __init__(self, output, repository, cutoff, api, progress=print):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("invalid repository identity")
        utc(cutoff)
        self.root = Path(output) / repository.replace("/", "__")
        self.repository, self.cutoff, self.api, self.progress = repository, cutoff, api, progress
        path = self.root / "manifest.json"
        self.manifest = (
            json.loads(path.read_text())
            if path.exists()
            else {
                "schema": "temporal-observable-history-census-v1",
                "repository": repository,
                "cutoff_exclusive": cutoff,
                "started_at": now(),
                "issue_pages": [],
                "comment_pages": [],
                "issue_cursor": None,
                "issue_pagination_complete": False,
                "comments_pagination_complete": False,
                "identity_second_pass_verified": False,
                "full_history_qualified": False,
                "deleted_or_transferred_unobservable_issues_complete": False,
                "all_timeline_event_types_collected": False,
                "repair_evidence_verified": False,
            }
        )
        if self.manifest["repository"] != repository or self.manifest["cutoff_exclusive"] != cutoff:
            raise ValueError("history snapshot identity/cutoff changed")
        self.validate_pages()

    def validate_pages(self):
        for page in (*self.manifest["issue_pages"], *self.manifest["comment_pages"]):
            payload = json.loads((self.root / page["file"]).read_text())
            if fingerprint(payload) != page["sha256"]:
                raise ValueError("history checkpoint page integrity failed")

    def checkpoint(self):
        self.manifest["updated_at"] = now()
        self.manifest["last_rate_limit"] = self.api.rate_limit
        write_json(self.root / "manifest.json", self.manifest)

    def issues(self):
        return [
            row
            for page in self.manifest["issue_pages"]
            for row in json.loads((self.root / page["file"]).read_text())["records"]
        ]

    def census(self):
        existing = self.issues()
        ids = {row["identity"]["node_id"] for row in existing}
        previous = max((utc(r["identity"]["created_at"]) for r in existing), default=None)
        owner, name = self.repository.split("/")
        while not self.manifest["issue_pagination_complete"]:
            after = self.manifest["issue_cursor"]
            data = self.api.graphql(ISSUES_QUERY, {"owner": owner, "name": name, "after": after})
            repo = data["repository"]
            if repo["nameWithOwner"].lower() != self.repository.lower():
                raise ValueError("repository moved; explicit alias review required")
            connection = repo["issues"]
            records, boundary = [], None
            for node in connection["nodes"]:
                created = utc(node["createdAt"])
                if previous is not None and created < previous:
                    raise ValueError("issue chronology moved backwards")
                previous = created
                if created >= utc(self.cutoff):
                    boundary = {"number": node["number"], "created_at": node["createdAt"]}
                    break
                if node["id"] in ids:
                    raise ValueError("duplicate issue across cursor pages")
                events = complete_state_title_timeline(self.api, node)
                records.append(project_issue(node, events, self.repository, self.cutoff))
                ids.add(node["id"])
            index = len(self.manifest["issue_pages"]) + 1
            payload = {
                "repository": self.repository,
                "cutoff": self.cutoff,
                "records": records,
                "boundary_probe": boundary,
            }
            relative = f"issues/page-{index:06}.json"
            write_json(self.root / relative, payload)
            page_info = connection["pageInfo"]
            complete = bool(boundary) or not page_info["hasNextPage"]
            if not complete and (not page_info["endCursor"] or page_info["endCursor"] == after):
                raise ValueError("issue cursor did not advance")
            self.manifest["issue_pages"].append(
                {"file": relative, "sha256": fingerprint(payload), "records": len(records)}
            )
            self.manifest["issue_cursor"] = page_info["endCursor"]
            self.manifest["issue_pagination_complete"] = complete
            self.manifest["completion_boundary"] = boundary
            self.manifest["observable_pre_cutoff_issues"] = len(ids)
            self.checkpoint()
            self.progress(f"{self.repository}: issue page {index}; {len(ids)} pre-cutoff issues")
        return self.summary()

    def verify_identities(self):
        if not self.manifest["issue_pagination_complete"]:
            raise ValueError("complete issue pagination first")
        owner, name = self.repository.split("/")
        found, seen_cursors, after, previous = set(), set(), None, None
        while True:
            result = self.api.graphql(
                IDENTITIES_QUERY, {"owner": owner, "name": name, "after": after}
            )["repository"]["issues"]
            boundary = False
            for node in result["nodes"]:
                created = utc(node["createdAt"])
                if previous is not None and created < previous:
                    raise ValueError("second-pass issue chronology is inconsistent")
                previous = created
                if created >= utc(self.cutoff):
                    boundary = True
                    break
                identity = (node["id"], node["number"], node["createdAt"])
                if identity in found:
                    raise ValueError("second-pass duplicate identity")
                found.add(identity)
            if boundary or not result["pageInfo"]["hasNextPage"]:
                break
            after = result["pageInfo"]["endCursor"]
            if not after or after in seen_cursors:
                raise ValueError("second-pass cursor did not advance")
            seen_cursors.add(after)
        expected = {
            (row["identity"]["node_id"], row["identity"]["number"], row["identity"]["created_at"])
            for row in self.issues()
        }
        if expected != found:
            raise ValueError("observable issue population changed between independent passes")
        self.manifest["identity_second_pass_verified"] = True
        self.manifest["identity_set_sha256"] = fingerprint(sorted(found))
        self.checkpoint()
        return self.summary()

    def collect_comments(self):
        if not self.manifest["issue_pagination_complete"]:
            raise ValueError("complete issue census before comments")
        numbers = {row["identity"]["number"] for row in self.issues()}
        seen_ids = {
            row["id"]
            for page in self.manifest["comment_pages"]
            for row in json.loads((self.root / page["file"]).read_text())["records"]
        }
        window = self.manifest.setdefault(
            "comment_api_window",
            {
                "since": None,
                "page": len(self.manifest["comment_pages"]) + 1,
                "last_created_at": self.manifest.get("last_comment_created_at"),
            },
        )
        while not self.manifest["comments_pagination_complete"]:
            index = len(self.manifest["comment_pages"]) + 1
            parameters = {
                "sort": "created",
                "direction": "asc",
                "per_page": 100,
                "page": window["page"],
            }
            if window["since"]:
                # GitHub's since filters updated_at. It therefore overlaps older
                # comments; retain their earlier snapshot and deduplicate IDs.
                parameters["since"] = window["since"]
            try:
                rows = self.api.rest(
                    f"repos/{self.repository}/issues/comments?{urlencode(parameters)}"
                )
            except GitHubAPIError as error:
                if not error.pagination_limited:
                    raise
                boundary = window["last_created_at"]
                if not boundary or (window["since"] and utc(boundary) <= utc(window["since"])):
                    raise ValueError("comment pagination window cannot advance") from None
                self.manifest.setdefault("comment_window_boundaries", []).append(boundary)
                window.update({"since": boundary, "page": 1, "last_created_at": None})
                self.checkpoint()
                continue
            records, boundary = [], False
            previous = window["last_created_at"]
            for row in rows:
                if previous and utc(row["created_at"]) < utc(previous):
                    raise ValueError("repository comment chronology moved backwards")
                previous = row["created_at"]
                if utc(row["created_at"]) >= utc(self.cutoff):
                    boundary = True
                    break
                number = int(row["issue_url"].rsplit("/", 1)[1])
                if number not in numbers:
                    continue  # PR comments are separate evidence, not Issue population.
                if row["id"] in seen_ids:
                    if window["since"]:
                        continue
                    raise ValueError("duplicate issue comment across pages")
                seen_ids.add(row["id"])
                usable = utc(row["updated_at"]) < utc(self.cutoff)
                records.append(
                    {
                        "id": row["id"],
                        "issue_number": number,
                        "url": row["html_url"],
                        "available_at": row["created_at"],
                        "body_version_available_at": row["updated_at"] if usable else None,
                        "body": redact_history(row["body"] or "") if usable else None,
                        "body_status": "available"
                        if usable
                        else "post-cutoff-edit-history-unrecovered",
                    }
                )
            payload = {
                "repository": self.repository,
                "cutoff": self.cutoff,
                "records": records,
                "request_parameters": parameters,
            }
            relative = f"comments/page-{index:06}.json"
            write_json(self.root / relative, payload)
            self.manifest["comment_pages"].append(
                {"file": relative, "sha256": fingerprint(payload), "records": len(records)}
            )
            self.manifest["last_comment_created_at"] = previous
            window["last_created_at"] = previous
            window["page"] += 1
            self.manifest["comments_pagination_complete"] = boundary or len(rows) < 100
            self.checkpoint()
            self.progress(f"{self.repository}: comment page {index}; {len(records)} retained")
        return self.summary()

    def summary(self):
        issues = self.issues()
        return {
            **self.manifest,
            "states_as_of": dict(Counter(row["as_of"]["state"] for row in issues)),
            "body_statuses": dict(Counter(row["as_of"]["body_status"] for row in issues)),
            "dispositions": dict(Counter(row["disposition"] for row in issues)),
            "resolution_candidates": sum(
                any("resolution_candidate" in event for event in row["as_of"]["state_title_events"])
                for row in issues
            ),
            "all_issues_have_disposition": len(issues)
            == sum(Counter(row["disposition"] for row in issues).values()),
        }
