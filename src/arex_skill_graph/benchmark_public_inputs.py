"""Recover original public issue inputs before any possible repair publication."""

from __future__ import annotations

import json

from .action_contracts import utc
from .history_census import (
    ISSUE_FIELDS,
    complete_state_title_timeline,
    fingerprint,
    project_issue,
    redact_history,
)
from .history_text_recovery import BODY_FIELDS, project_past_body
from .task_context import assert_public


def recover_issue_input(api, repository, number, repair_before):
    """Only the projected past body is returned; current later text stays in memory."""
    owner, name = repository.split("/")
    node = api.graphql(
        "query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){"
        "issue(number:$number){" + ISSUE_FIELDS + "}} rateLimit{cost remaining resetAt}}",
        {"owner": owner, "name": name, "number": number},
    )["repository"]["issue"]
    if not node or node["number"] != number:
        raise ValueError("original issue identity is unavailable")
    events = complete_state_title_timeline(api, node)
    projected = project_issue(node, events, repository, repair_before)
    if projected["as_of"]["body"] is not None:
        body = {
            "body": projected["as_of"]["body"],
            "version_available_at": node.get("lastEditedAt") or node["createdAt"],
            "recovery_basis": "current-body-last-edit-before-cutoff",
            "status": "recovered",
        }
    else:
        fields = BODY_FIELDS.replace("AFTER", "null")
        content = api.graphql(
            "query($id:ID!){node(id:$id){... on Issue{"
            + fields
            + "}} rateLimit{cost remaining resetAt}}",
            {"id": node["id"]},
        )["node"]
        if not content or content["id"] != node["id"]:
            raise ValueError("original body version identity is unavailable")
        connection = content["userContentEdits"]
        edits, cursors = list(connection["nodes"]), set()
        while connection["pageInfo"]["hasNextPage"]:
            cursor = connection["pageInfo"]["endCursor"]
            if not cursor or cursor in cursors:
                raise ValueError("original issue body edit pagination did not advance")
            cursors.add(cursor)
            fields = BODY_FIELDS.replace("AFTER", json.dumps(cursor))
            connection = api.graphql(
                "query($id:ID!){node(id:$id){... on Issue{"
                + fields
                + "}} rateLimit{cost remaining resetAt}}",
                {"id": node["id"]},
            )["node"]["userContentEdits"]
            edits.extend(connection["nodes"])
        body = project_past_body(content, edits, repair_before)
    if body["status"] != "recovered" or not body["body"].strip():
        raise ValueError("nonempty pre-repair original issue body cannot be recovered")
    title_at = max(
        [
            node["createdAt"],
            *[
                event["createdAt"]
                for event in events
                if event["__typename"] == "RenamedTitleEvent"
                and utc(event["createdAt"]) < utc(repair_before)
            ],
        ],
        key=utc,
    )
    result = {
        "issue_id": repository + ":" + str(number),
        "node_id": node["id"],
        "url": node["url"],
        "created_at": node["createdAt"],
        "title": projected["as_of"]["title"],
        "title_available_at": title_at,
        "body": body["body"],
        "body_available_at": body["version_available_at"],
        "body_recovery_basis": body["recovery_basis"],
        "repair_exclusion_before": repair_before,
        "state_title_pagination_complete": True,
        "comments_exported": False,
        "post_repair_text_persisted": False,
    }
    assert_public(result)
    if any(
        utc(result[field]) >= utc(repair_before)
        for field in ("created_at", "title_available_at", "body_available_at")
    ):
        raise ValueError("original input does not strictly precede possible repair publication")
    return result


def compose_public_problem(issues, *, base_committed_at, repair_before, main_cutoff):
    if not issues or len({row["issue_id"] for row in issues}) != len(issues):
        raise ValueError("public input needs unique original issue identities")
    if any(utc(row["created_at"]) < utc(main_cutoff) for row in issues):
        raise ValueError("pre-cutoff backlog cannot enter the new-issue cohort")
    available = max(
        [
            base_committed_at,
            *[
                row[field]
                for row in issues
                for field in ("title_available_at", "body_available_at")
            ],
        ],
        key=utc,
    )
    if utc(available) >= utc(repair_before):
        raise ValueError("public base/input chronology does not precede possible repair")
    for row in issues:
        if row.get("post_repair_text_persisted") is not False:
            raise ValueError("original input has not excluded later text")
        for field in ("created_at", "title_available_at", "body_available_at"):
            if utc(row[field]) >= utc(repair_before):
                raise ValueError("future original input cannot enter the solver")
        if not row["body"].strip() or redact_history(row["body"]) != row["body"]:
            raise ValueError("unsafe or empty original public issue body")
    problem = "\n\n".join(row["title"] + "\n\n" + row["body"] for row in issues)
    assert_public(problem)
    return {
        "public_problem": problem,
        "input_available_at": available,
        "original_issue_ids": [row["issue_id"] for row in issues],
        "original_inputs_sha256": fingerprint(issues),
        "base_committed_at": base_committed_at,
        "base_publication_limit": "Git committer time is observable; exact public push time is not separately proven.",
        "repair_exclusion_before": repair_before,
        "solution_fields_exported": False,
        "comments_exported": False,
    }
