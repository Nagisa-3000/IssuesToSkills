"""Paginate every observable timeline type, separating identities from usable evidence."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from .action_contracts import utc
from .history_census import fingerprint, now, redact_history, write_json

RELATED_IDENTITY = """
__typename
... on Issue {id number url createdAt repository {nameWithOwner}}
... on PullRequest {id number url createdAt mergedAt mergeCommit {oid} repository {nameWithOwner}}
"""
EVENT_RELATIONS = {
    "CrossReferencedEvent": "source {" + RELATED_IDENTITY + "}",
    "ConnectedEvent": "source {" + RELATED_IDENTITY + "}",
    "DisconnectedEvent": "source {" + RELATED_IDENTITY + "}",
    "MarkedAsDuplicateEvent": "canonical {" + RELATED_IDENTITY + "}",
    "UnmarkedAsDuplicateEvent": "canonical {" + RELATED_IDENTITY + "}",
    "ClosedEvent": """closer {__typename
        ... on PullRequest {id number url createdAt mergedAt mergeCommit {oid} repository {nameWithOwner}}
        ... on Commit {oid committedDate repository {nameWithOwner}}
    } duplicateOf {"""
    + RELATED_IDENTITY
    + "}",
    "ReferencedEvent": "commit {oid committedDate repository {nameWithOwner}}",
    "TransferredEvent": "fromRepository {nameWithOwner}",
}
SCALAR_FIELDS = frozenset(
    {
        "id",
        "createdAt",
        "updatedAt",
        "lastEditedAt",
        "databaseId",
        "url",
        "body",
        "currentTitle",
        "previousTitle",
        "stateReason",
        "lockReason",
        "isCrossRepository",
        "isDirectReference",
        "willCloseTarget",
        "referencedAt",
        "milestoneTitle",
        "projectColumnName",
        "wasAutomated",
        "previousStatus",
        "status",
        "value",
        "previousValue",
        "newValue",
    }
)
UNAVAILABLE_EVENT_TYPES = frozenset(
    {
        "AddedToProjectV2Event",
        "RemovedFromProjectV2Event",
        "ConvertedFromDraftEvent",
        "ProjectV2ItemStatusChangedEvent",
    }
)


def timeline_selection(schema):
    fragments = []
    for entry in schema["possibleTypes"]:
        if entry["name"] in UNAVAILABLE_EVENT_TYPES:
            # Field authorization is checked even when the public repository has
            # no such events. Keep the typename to audit the gap without asking
            # for broader project access or assigning an invented event date.
            continue
        fields = {f["name"] for f in entry["fields"] if f["name"] in SCALAR_FIELDS}
        if not {"id", "createdAt"} <= fields:
            raise ValueError("new timeline type requires explicit timestamp/identity handling")
        fragments.append(
            "... on "
            + entry["name"]
            + " {"
            + " ".join(sorted(fields))
            + " "
            + EVENT_RELATIONS.get(entry["name"], "")
            + "}"
        )
    return "__typename " + " ".join(fragments)


def redact_event(value):
    if isinstance(value, str):
        return redact_history(value)
    if isinstance(value, list):
        return [redact_event(x) for x in value]
    if isinstance(value, dict):
        return {k: redact_event(v) for k, v in value.items()}
    return value


def project_timeline_event(event, cutoff):
    if "createdAt" not in event:
        if event["__typename"] not in UNAVAILABLE_EVENT_TYPES:
            raise ValueError("unrecognized timeline event without a timestamp")
        return None
    if utc(event["createdAt"]) >= utc(cutoff):
        return None
    result = redact_event(event)
    if event["__typename"] == "IssueComment":
        edited = event.get("lastEditedAt")
        if edited and utc(edited) >= utc(cutoff):
            result["body"] = None
            result["body_status"] = "post-cutoff-edit-history-unrecovered"
        else:
            result["body_status"] = "available"
        result["body_version_available_at"] = edited or event["createdAt"]
    # Related nodes are identity pointers. Their text/current state is never
    # included, and their repair availability must be checked independently.
    result["related_nodes_are_identity_only"] = True
    return result


def temporal_event_view(event, cutoff):
    """Hide related nodes' mutable resolutions that occurred after the cutoff."""
    result = deepcopy(event)
    for field in ("source", "closer", "canonical", "duplicateOf"):
        related = result.get(field)
        if not isinstance(related, dict):
            continue
        if related.get("createdAt") and utc(related["createdAt"]) >= utc(cutoff):
            result[field] = None
            result["post_cutoff_related_node_withheld"] = True
        elif (
            related.get("__typename") == "PullRequest"
            and related.get("mergedAt")
            and utc(related["mergedAt"]) >= utc(cutoff)
        ):
            related["mergedAt"] = None
            related["mergeCommit"] = None
            related["post_cutoff_resolution_withheld"] = True
    return result


def state_title_coverage_gaps(state_title_events, events, cutoff):
    """Reconcile independent state/title observations with a paginated timeline.

    Pagination and archive hashes establish what was saved, not that GitHub
    returned every historical event. Missing observations stay gaps; this does
    not manufacture timeline IDs, closure proofs, or repair knowledge.
    """
    kinds = {"ClosedEvent", "ReopenedEvent", "RenamedTitleEvent"}
    observed = {
        (event["__typename"], utc(event["createdAt"]))
        for event in events
        if event.get("__typename") in kinds and event.get("createdAt")
    }
    gaps = []
    for event in state_title_events:
        if event.get("kind") not in kinds or utc(event["available_at"]) >= utc(cutoff):
            continue
        identity = (event["kind"], utc(event["available_at"]))
        if identity not in observed:
            gaps.append(
                {
                    "event_type": event["kind"],
                    "available_at": event["available_at"],
                    "reason": "known-state-title-event-missing-from-paginated-timeline",
                }
            )
    return gaps


class TimelineCensus:
    def __init__(self, root, repository, cutoff, api, progress=print):
        self.root = Path(root) / repository.replace("/", "__")
        self.repository, self.cutoff, self.api, self.progress = repository, cutoff, api, progress
        base = json.loads((self.root / "manifest.json").read_text())
        if base["cutoff_exclusive"] != cutoff or not base["issue_pagination_complete"]:
            raise ValueError("timeline census needs the matching complete issue population")
        self.issues = [
            row
            for page in base["issue_pages"]
            for row in json.loads((self.root / page["file"]).read_text())["records"]
        ]
        self.config = {
            "repository": repository,
            "cutoff_exclusive": cutoff,
            "identity_set_sha256": base["identity_set_sha256"],
        }
        schema_path = Path(root) / "timeline-schema.json"
        if not schema_path.exists():
            schema = api.graphql(
                'query {__type(name:"IssueTimelineItems"){possibleTypes{name fields{name}}} '
                "rateLimit{cost remaining resetAt}}",
                {},
            )["__type"]
            write_json(schema_path, schema)
        self.schema = json.loads(schema_path.read_text())
        self.selection = timeline_selection(self.schema)

    def collect_issue(self, identity, initial, *, state_title_only=False):
        connection, events, cursors, unavailable = initial, [], set(), []
        while True:
            for event in connection["nodes"]:
                if "createdAt" not in event:
                    unavailable.append(
                        {
                            "event_type": event["__typename"],
                            "reason": "event-fields-require-unavailable-project-scope",
                        }
                    )
                projected = project_timeline_event(event, self.cutoff)
                if projected is not None:
                    events.append(projected)
            if not connection["pageInfo"]["hasNextPage"]:
                break
            after = connection["pageInfo"]["endCursor"]
            if not after or after in cursors:
                raise ValueError("complete timeline cursor did not advance")
            cursors.add(after)
            query = "query($id:ID!,$after:String){node(id:$id){... on Issue{" + (
                "timelineItems(first:100,after:$after"
                + (
                    ",itemTypes:[CLOSED_EVENT,REOPENED_EVENT,RENAMED_TITLE_EVENT]"
                    if state_title_only
                    else ""
                )
                + "){nodes{"
                + self.selection
                + "} pageInfo{hasNextPage endCursor}}}} rateLimit{cost remaining resetAt}}"
            )
            connection = self.api.graphql(query, {"id": identity["node_id"], "after": after})[
                "node"
            ]["timelineItems"]
        if len({e["id"] for e in events}) != len(events):
            raise ValueError("duplicate timeline event")
        return {
            "identity": identity,
            "events": events,
            "all_event_types_paginated": True,
            "unavailable_event_metadata": unavailable,
            "selected_event_metadata_complete": not unavailable,
            "all_event_payload_fields_collected": False,
        }

    def collect(self, batch_size=75, initial_events=30):
        saved = []
        for start in range(0, len(self.issues), batch_size):
            batch = self.issues[start : start + batch_size]
            path = self.root / "timeline" / f"batch-{start // batch_size + 1:05}.json"
            config = {
                **self.config,
                "batch_size": batch_size,
                "initial_events": initial_events,
                "selection_sha256": fingerprint(self.selection),
                "issue_numbers": [x["identity"]["number"] for x in batch],
            }
            if path.exists():
                payload = json.loads(path.read_text())
                if (
                    payload["config"] != config
                    or fingerprint(payload["records"]) != payload["sha256"]
                ):
                    raise ValueError("timeline checkpoint configuration/integrity mismatch")
            else:
                query = (
                    "query($ids:[ID!]!){nodes(ids:$ids){... on Issue{id timelineItems(first:"
                    + (
                        str(initial_events)
                        + "){nodes{"
                        + self.selection
                        + "} pageInfo{hasNextPage endCursor}}}} rateLimit{cost remaining resetAt}}"
                    )
                )
                nodes = self.api.graphql(query, {"ids": [x["identity"]["node_id"] for x in batch]})[
                    "nodes"
                ]
                if [n["id"] if n else None for n in nodes] != [
                    x["identity"]["node_id"] for x in batch
                ]:
                    raise ValueError("timeline population identity changed")
                records = [
                    self.collect_issue(row["identity"], node["timelineItems"])
                    for row, node in zip(batch, nodes)
                ]
                payload = {"config": config, "records": records, "sha256": fingerprint(records)}
                write_json(path, payload)
            saved.append(
                {
                    "file": path.relative_to(self.root).as_posix(),
                    "sha256": payload["sha256"],
                    "issues": len(payload["records"]),
                    "events": sum(len(r["events"]) for r in payload["records"]),
                    "unavailable_events": sum(
                        len(r["unavailable_event_metadata"]) for r in payload["records"]
                    ),
                }
            )
            self.progress(
                f"{self.repository}: full timeline identities {start + len(batch)}/{len(self.issues)}"
            )
        report = {
            **self.config,
            "schema": "observable-timeline-metadata-census-v1",
            "observed_at": now(),
            "batches": saved,
            "issue_count": sum(b["issues"] for b in saved),
            "event_count": sum(b["events"] for b in saved),
            "unavailable_event_metadata_count": sum(b["unavailable_events"] for b in saved),
            "all_event_types_paginated": True,
            "all_event_payload_fields_collected": False,
            "full_history_qualified": False,
            "api_calls": self.api.calls,
            "last_rate_limit": self.api.rate_limit,
        }
        write_json(self.root / "timeline-manifest.json", report)
        return report
