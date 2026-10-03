"""Recover past GitHub body snapshots; current later text stays only in memory."""

from __future__ import annotations

import json
from pathlib import Path

from .action_contracts import utc
from .history_census import fingerprint, now, redact_history, write_json
from .skill_packages import _resolve

BODY_FIELDS = """
id createdAt lastEditedAt body
userContentEdits(first:100,after:AFTER) {
 nodes {id editedAt deletedAt diff}
 pageInfo {hasNextPage endCursor}
}
"""


def load_text_recovery(path, cutoff):
    """Read an explicitly versioned supplement without altering the original census."""
    path = Path(path)
    report = json.loads(path.read_text())
    if (
        report.get("schema") != "historical-github-body-version-recovery-v1"
        or report.get("cutoff_exclusive") != cutoff
        or report.get("post_cutoff_text_persisted") is not False
    ):
        raise ValueError("historical text supplement identity/cutoff changed")
    rows = []
    for page in report["pages"]:
        payload = json.loads(_resolve(path.parent, page["file"]).read_text())
        if (
            payload["config"]["cutoff_exclusive"] != cutoff
            or payload.get("current-post-cutoff-text-persisted") is not False
            or fingerprint(payload["records"]) != page["sha256"]
            or payload["sha256"] != page["sha256"]
        ):
            raise ValueError("historical text supplement checkpoint integrity failed")
        rows.extend(payload["records"])
    if rows != report["records"] or len(rows) != report["target_count"]:
        raise ValueError("historical text supplement inventory differs from its pages")
    result = {}
    for row in rows:
        identity = (row["repository"], row["kind"], row["issue_number"], row.get("comment_id"))
        if row["kind"] not in {"Issue", "IssueComment"} or identity in result:
            raise ValueError("duplicate/invalid historical text supplement identity")
        if row["status"] == "recovered":
            if (
                not isinstance(row["body"], str)
                or redact_history(row["body"]) != row["body"]
                or utc(row["version_available_at"]) >= utc(cutoff)
                or row.get("body_edit_pagination_complete") is not True
            ):
                raise ValueError("historical text recovery lacks a safe pre-cutoff version")
            basis = row["recovery_basis"]
            if basis not in {
                "github-user-content-edit-full-version",
                "current-body-last-edit-before-cutoff",
            }:
                raise ValueError("unverified historical text recovery format")
            if (
                basis == "github-user-content-edit-full-version"
                and row.get("current-version-equality-verified") is not True
            ):
                raise ValueError("historical text recovery format equality was not verified")
        elif row["status"] != "unrecoverable" or row.get("body") is not None:
            raise ValueError("unrecoverable historical text cannot contain a later body")
        result[identity] = row
    return result


def project_past_body(node, edits, cutoff):
    if utc(node["createdAt"]) >= utc(cutoff):
        raise ValueError("post-cutoff text identity cannot enter the history")
    current_at = node.get("lastEditedAt") or node["createdAt"]
    if utc(current_at) < utc(cutoff):
        return {
            "body": redact_history(node["body"] or ""),
            "version_available_at": current_at,
            "recovery_basis": "current-body-last-edit-before-cutoff",
            "status": "recovered",
        }
    # In the observable GitHub API, diff contains a complete body version.
    # Require the newest edit to agree with both the current edit timestamp and
    # body before interpreting earlier values as snapshots. Do not reverse an
    # unverified textual diff or fill gaps with a newer version.
    ordered = sorted(edits, key=lambda e: utc(e["editedAt"]), reverse=True)
    if not ordered or ordered[0]["editedAt"] != current_at or ordered[0]["diff"] != node["body"]:
        return {
            "body": None,
            "status": "unrecoverable",
            "reason": "edit-version-format-not-verified",
        }
    eligible = [e for e in ordered if utc(e["editedAt"]) < utc(cutoff)]
    if not eligible or eligible[0]["diff"] is None:
        return {
            "body": None,
            "status": "unrecoverable",
            "reason": "historical-version-deleted-or-unavailable",
        }
    chosen = eligible[0]
    return {
        "body": redact_history(chosen["diff"]),
        "version_available_at": chosen["editedAt"],
        "recovery_basis": "github-user-content-edit-full-version",
        "edit_node_id": chosen["id"],
        "current-version-equality-verified": True,
        "status": "recovered",
    }


def recovery_targets(root):
    result = []
    for folder in sorted(Path(root).glob("*/")):
        if not (folder / "manifest.json").exists():
            continue
        manifest = json.loads((folder / "manifest.json").read_text())
        for page in manifest["issue_pages"]:
            for row in json.loads((folder / page["file"]).read_text())["records"]:
                if row["as_of"]["body"] is None:
                    result.append(
                        {
                            "kind": "Issue",
                            "repository": manifest["repository"],
                            "issue_number": row["identity"]["number"],
                            "node_id": row["identity"]["node_id"],
                        }
                    )
        comment_nodes = {}
        timeline_path = folder / "timeline-manifest.json"
        if timeline_path.exists():
            timeline = json.loads(timeline_path.read_text())
            for page in timeline["batches"]:
                for row in json.loads((folder / page["file"]).read_text())["records"]:
                    for event in row["events"]:
                        if event["__typename"] == "IssueComment":
                            comment_nodes[event["databaseId"]] = event["id"]
        for page in manifest["comment_pages"]:
            for row in json.loads((folder / page["file"]).read_text())["records"]:
                if row["body"] is None:
                    result.append(
                        {
                            "kind": "IssueComment",
                            "repository": manifest["repository"],
                            "issue_number": row["issue_number"],
                            "comment_id": row["id"],
                            "node_id": comment_nodes.get(row["id"]),
                        }
                    )
    return result


def recover_text_versions(root, output, cutoff, api):
    targets = recovery_targets(root)
    records, pages = [], []
    output = Path(output)
    for start in range(0, len(targets), 25):
        batch = targets[start : start + 25]
        path = output / f"text-recovery-{start // 25 + 1:05}.json"
        config = {"targets_sha256": fingerprint(batch), "cutoff_exclusive": cutoff}
        if path.exists():
            payload = json.loads(path.read_text())
            if payload["config"] != config or fingerprint(payload["records"]) != payload["sha256"]:
                raise ValueError("text recovery checkpoint changed")
        else:
            identified = [row for row in batch if row["node_id"]]
            query = "query($ids:[ID!]!){nodes(ids:$ids){__typename ... on Issue{" + (
                BODY_FIELDS.replace("AFTER", "null")
                + "} ... on IssueComment{"
                + BODY_FIELDS.replace("AFTER", "null")
                + "}} rateLimit{cost remaining resetAt}}"
            )
            nodes = api.graphql(query, {"ids": [r["node_id"] for r in identified]})["nodes"]
            by_node = {n["id"]: n for n in nodes if n}
            projected = []
            for target in batch:
                node = by_node.get(target["node_id"])
                if not node:
                    projected.append(
                        {
                            **target,
                            "body": None,
                            "status": "unrecoverable",
                            "reason": "content-node-unavailable",
                        }
                    )
                    continue
                if node["__typename"] != target["kind"]:
                    raise ValueError("text recovery entity identity changed")
                connection = node["userContentEdits"]
                edits, cursors = list(connection["nodes"]), set()
                while connection["pageInfo"]["hasNextPage"]:
                    cursor = connection["pageInfo"]["endCursor"]
                    if not cursor or cursor in cursors:
                        raise ValueError("body edit version cursor did not advance")
                    cursors.add(cursor)
                    fields = BODY_FIELDS.replace("AFTER", json.dumps(cursor))
                    connection = api.graphql(
                        "query($id:ID!){node(id:$id){... on "
                        + target["kind"]
                        + "{"
                        + fields
                        + "}} rateLimit{cost remaining resetAt}}",
                        {"id": target["node_id"]},
                    )["node"]["userContentEdits"]
                    edits.extend(connection["nodes"])
                projected.append(
                    {
                        **target,
                        **project_past_body(node, edits, cutoff),
                        "body_edit_pagination_complete": True,
                    }
                )
            payload = {
                "config": config,
                "records": projected,
                "sha256": fingerprint(projected),
                "current-post-cutoff-text-persisted": False,
            }
            write_json(path, payload)
        records.extend(payload["records"])
        pages.append({"file": path.name, "sha256": payload["sha256"]})
        print(f"Historical text version recovery: {len(records)}/{len(targets)}", flush=True)
    report = {
        "schema": "historical-github-body-version-recovery-v1",
        "checked_at": now(),
        "cutoff_exclusive": cutoff,
        "records": records,
        "pages": pages,
        "target_count": len(targets),
        "recovered_count": sum(r["status"] == "recovered" for r in records),
        "post_cutoff_text_persisted": False,
        "api_calls": api.calls,
        "full_history_qualified": False,
    }
    write_json(output / "text-recovery-manifest.json", report)
    return report
