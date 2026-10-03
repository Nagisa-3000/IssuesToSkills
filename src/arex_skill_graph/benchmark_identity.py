"""Pinned benchmark metadata projection; raw task files stay in anonymous memory."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
from contextlib import contextmanager
from urllib.parse import urlsplit

from .action_contracts import utc
from .history_census import fingerprint, redact_history

EXPOSED_PULL_NUMBERS = frozenset({9782, 10034, 10209, 10275, 10350})

METADATA_FIELDS = (
    "instance_id",
    "pull_number",
    "number",
    "id",
    "created_at",
    "base_commit",
    "version",
    "environment_setup_commit",
    "repo",
    "repository",
    "repo_name",
    "org",
    "issue_numbers",
)
METADATA_PROJECTION_VERSION = "benchmark-identity-projection-v2"


def project_issue_numbers(value):
    """Dataset issue references are identities, not issue or repair text."""
    if value is None:
        return []
    for _ in range(2):
        if isinstance(value, str):
            value = json.loads(value)
    if not isinstance(value, list):
        raise ValueError("dataset issue_numbers must be an array")  # noqa: TRY004 -- JSON contract errors consistently use ValueError.
    numbers = []
    for item in value:
        if type(item) is int and item > 0:
            numbers.append(item)
        elif isinstance(item, str) and re.fullmatch(r"[1-9][0-9]*", item):
            numbers.append(int(item))
        else:
            raise ValueError("dataset issue reference is not a positive issue number")
    return sorted(set(numbers))


@contextmanager
def public_file_in_memory(url, expected_sha256):
    """Windows HTTP bridge for WSL; no raw dataset or redirect URLs are persisted."""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc not in {"huggingface.co", "hf-mirror.com"}
        or "/resolve/" not in parsed.path
        or parsed.query
        or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256)
    ):
        raise ValueError("use a registered pinned public file and content hash")
    if not hasattr(os, "memfd_create"):
        raise RuntimeError("anonymous-memory dataset projection requires Linux")
    fd = os.memfd_create("arex-benchmark-metadata", os.MFD_CLOEXEC)
    literal = "'" + url.replace("'", "''") + "'"
    code = (
        "$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; "
        "Add-Type -AssemblyName System.Net.Http; "
        "$taskClient=[System.Net.Http.HttpClient]::new(); "
        "$taskClient.Timeout=[TimeSpan]::FromSeconds(180); "
        f"$taskBytes=$taskClient.GetByteArrayAsync({literal}).GetAwaiter().GetResult(); "
        "$taskStream=[Console]::OpenStandardOutput(); "
        "$taskStream.Write($taskBytes,0,$taskBytes.Length); $taskStream.Flush();"
    )
    encoded = base64.b64encode(code.encode("utf-16le")).decode()
    process = None
    try:
        process = subprocess.Popen(
            [
                "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-EncodedCommand",
                encoded,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        digest, size = hashlib.sha256(), 0
        with os.fdopen(os.dup(fd), "wb") as memory:
            for chunk in iter(lambda: process.stdout.read(1024 * 1024), b""):
                memory.write(chunk)
                digest.update(chunk)
                size += len(chunk)
        if process.wait(timeout=190) or digest.hexdigest() != expected_sha256:
            raise RuntimeError("pinned public dataset fetch/hash failed; native output suppressed")
        yield f"/proc/self/fd/{fd}", size
    finally:
        if process and process.poll() is None:
            process.kill()
            process.wait()
        if process and process.stdout:
            process.stdout.close()
        os.close(fd)


def repository_identity(value, organization=None):
    if isinstance(value, dict):
        owner = value.get("owner", value.get("org"))
        name = value.get("name", value.get("repo"))
        if isinstance(owner, dict):
            owner = owner.get("login")
        value = value.get("full_name") or (f"{owner}/{name}" if owner and name else name)
    if isinstance(value, str):
        value = value.removeprefix("https://github.com/").removesuffix(".git").strip("/")
        if "/" not in value and organization:
            value = organization + "/" + value
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
            return value
    raise ValueError("benchmark repository identity is not recoverable")


def project_metadata(connection, source, *, is_parquet=True, target="pylint-dev/pylint"):
    reader = (
        "read_parquet(?)"
        if is_parquet
        else "read_json_auto(?,format='newline_delimited',union_by_name=true)"
    )
    schema = connection.execute(f"DESCRIBE SELECT * FROM {reader}", [source]).fetchall()
    columns = {row[0] for row in schema}
    selected = [name for name in METADATA_FIELDS if name in columns]
    repo_field = next((key for key in ("repo", "repository", "repo_name") if key in columns), None)
    identity_field = next(
        (key for key in ("instance_id", "pull_number", "number", "id") if key in columns), None
    )
    if not repo_field or not identity_field:
        raise ValueError("benchmark lacks required repository/task identity fields")
    expressions = [
        f'to_json("{name}")'
        if name in {repo_field, "issue_numbers"}
        else f'CAST("{name}" AS VARCHAR)'
        for name in selected
    ]
    rows = connection.execute(f"SELECT {','.join(expressions)} FROM {reader}", [source]).fetchall()
    identities, results = set(), []
    aliases = (
        {target.lower(), "pycqa/pylint"} if target == "pylint-dev/pylint" else {target.lower()}
    )
    for values in rows:
        metadata = dict(zip(selected, values))
        repository = repository_identity(json.loads(metadata[repo_field]), metadata.get("org"))
        raw_id = metadata[identity_field]
        if raw_id is None:
            raise ValueError("missing benchmark task identity")
        identities.add(repository.lower() + ":" + raw_id)
        if repository.lower() not in aliases:
            continue
        explicit = metadata.get("pull_number") or metadata.get("number")
        match = re.search(r"(?:^|[-:])([0-9]+)$", explicit or raw_id)
        if not match:
            raise ValueError("benchmark PR identity cannot be recovered")
        base = metadata.get("base_commit")
        if base is not None and not re.fullmatch(r"[0-9a-f]{40}", base):
            raise ValueError("benchmark base commit is not pinned")
        results.append(
            {
                "repository": target,
                "source_repository": repository,
                "instance_id": raw_id,
                "pull_number": int(match.group(1)),
                "dataset_original_issue_numbers": project_issue_numbers(
                    metadata.get("issue_numbers")
                ),
                "original_issue_field_available": "issue_numbers" in columns,
                **{
                    key: redact_history(metadata[key]) if metadata[key] is not None else None
                    for key in ("created_at", "base_commit", "version", "environment_setup_commit")
                    if key in metadata
                },
            }
        )
    return results, {
        "projection_version": METADATA_PROJECTION_VERSION,
        "projection_fields_sha256": fingerprint(METADATA_FIELDS),
        "projected_columns": selected,
        "raw_rows": len(rows),
        "target_rows": len(results),
        "all_dataset_identity_set_sha256": hashlib.sha256(
            "\n".join(sorted(identities)).encode()
        ).hexdigest(),
        "solution_fields_returned": False,
    }


def alias_union(records):
    """Join protocol memberships by repository/PR; original issue mapping follows separately."""
    groups = {}
    for row in records:
        key = row["repository"] + ":" + str(row["pull_number"])
        group = groups.setdefault(
            key,
            {
                "repository": row["repository"],
                "pull_number": row["pull_number"],
                "aliases": [],
                "original_issues": [],
                "original_issue_mapping_verified": False,
                "temporal_classification": "original-issue-date-pending",
                "independent_bug_cluster_verified": False,
                "benchmark_qualification": "not-executed",
            },
        )
        alias = {
            key: value
            for key, value in row.items()
            if key not in {"repository", "pull_number", "source_repository"}
        }
        if alias not in group["aliases"]:
            group["aliases"].append(alias)
    return list(groups.values())


def dataset_issue_identities(api, repository, numbers):
    """Resolve only declared dataset issue identities; do not read issue bodies."""
    owner, name = repository.split("/")
    fields = " ".join(
        f"i{number}:issue(number:{number}) {{id number url createdAt repository {{nameWithOwner}}}}"
        for number in sorted(set(numbers))
    )
    if not fields:
        return {}
    result = api.graphql(
        f"query {{repository(owner:{json.dumps(owner)},name:{json.dumps(name)}) "
        + "{"
        + fields
        + "} rateLimit {remaining resetAt cost}}",
        {},
    )["repository"]
    return {number: result.get(f"i{number}") for number in numbers}


def reconcile_dataset_issue_references(group, mapping, identities):
    """Retain disagreements for qualification rather than silently choosing a source."""
    declared_sets = {
        tuple(alias.get("dataset_original_issue_numbers", []))
        for alias in group["aliases"]
        if alias.get("original_issue_field_available")
        and alias.get("dataset_original_issue_numbers")
    }
    declared = {number for numbers in declared_sets for number in numbers}
    missing = sorted(number for number in declared if not identities.get(number))
    closing = {issue["number"] for issue in mapping["original_issues"]}
    conflict = len(declared_sets) > 1 or bool(declared and closing and declared != closing)
    issues = list(mapping["original_issues"])
    for number in sorted(declared - closing):
        row = identities.get(number)
        if row:
            issues.append(
                {
                    "node_id": row["id"],
                    "repository": row["repository"]["nameWithOwner"],
                    "number": row["number"],
                    "url": row["url"],
                    "created_at": row["createdAt"],
                    "mapping_basis": "pinned-dataset-reference-with-github-issue-identity",
                }
            )
    basis = (
        "disagreement-review-required"
        if conflict
        else "unavailable-declared-issue"
        if missing
        else "agreement"
        if declared and closing
        else "dataset-reference-only"
        if declared
        else "closing-reference-only"
        if closing
        else "unmapped"
    )
    return {
        **mapping,
        "original_issues": issues,
        "dataset_original_issue_numbers": sorted(declared),
        "unavailable_dataset_issue_numbers": missing,
        "original_issue_reference_comparison": basis,
        "mapping_reference_conflict": conflict,
        "original_issue_identity_resolution_complete": not missing,
    }


PULL_IDENTITY_FIELDS = """
id number createdAt mergedAt baseRefOid mergeCommit {oid}
closingIssuesReferences(first:100,after:AFTER) {
 nodes {id number url createdAt repository {nameWithOwner}}
 pageInfo {hasNextPage endCursor}
}
"""


def original_issue_identities(api, repository, numbers):
    """Only project PR/issue identity metadata; never fetch repair text or patches."""
    owner, name = repository.split("/")
    fields = " ".join(
        f"p{n}: pullRequest(number:{n}) {{" + PULL_IDENTITY_FIELDS.replace("AFTER", "null") + "}"
        for n in numbers
    )
    result = api.graphql(
        f"query {{repository(owner:{json.dumps(owner)},name:{json.dumps(name)}) "
        + "{"
        + fields
        + "} rateLimit {remaining resetAt cost}}",
        {},
    )["repository"]
    rows = {}
    for number in numbers:
        row = result.get(f"p{number}")
        if not row:
            raise ValueError("registered benchmark PR identity is unavailable")
        connection = row["closingIssuesReferences"]
        issues, cursors = list(connection["nodes"]), set()
        while connection["pageInfo"]["hasNextPage"]:
            cursor = connection["pageInfo"]["endCursor"]
            if not cursor or cursor in cursors:
                raise ValueError("original issue reference cursor did not advance")
            cursors.add(cursor)
            fields = PULL_IDENTITY_FIELDS.replace("AFTER", json.dumps(cursor))
            connection = api.graphql(
                f"query {{repository(owner:{json.dumps(owner)},name:{json.dumps(name)}) "
                + f"{{pullRequest(number:{number}) {{"
                + fields
                + "}}} rateLimit {remaining resetAt cost}}",
                {},
            )["repository"]["pullRequest"]["closingIssuesReferences"]
            issues.extend(connection["nodes"])
        if len({i["id"] for i in issues}) != len(issues):
            raise ValueError("duplicate original issue identity")
        rows[number] = {
            "pull_node_id": row["id"],
            "pull_created_at": row["createdAt"],
            "merged_at": row["mergedAt"],
            "observed_base_ref_oid": row["baseRefOid"],
            "merge_commit": (row.get("mergeCommit") or {}).get("oid"),
            "closing_reference_pagination_complete": True,
            "original_issues": [
                {
                    "node_id": i["id"],
                    "repository": i["repository"]["nameWithOwner"],
                    "number": i["number"],
                    "url": i["url"],
                    "created_at": i["createdAt"],
                    "mapping_basis": "github-closing-issues-reference",
                }
                for i in issues
            ],
        }
    return rows


def classify_original_issue_group(group, mapping, cutoff):
    """Dates determine cohort before running solvers; PR date alone is insufficient."""
    result = {**group, **mapping}
    originals = mapping["original_issues"]
    result["original_issue_mapping_verified"] = (
        bool(originals)
        and not mapping.get("mapping_reference_conflict", False)
        and mapping.get("original_issue_identity_resolution_complete", True)
    )
    result["exposed_gold_development_only"] = group["pull_number"] in EXPOSED_PULL_NUMBERS
    merged = mapping["merged_at"]
    if not originals:
        classification = "unmapped-original-issue"
    elif not merged:
        classification = "unmerged-repair-reference"
    elif utc(merged) < utc(cutoff):
        classification = "pre-cutoff-historical-repair"
    elif all(utc(i["created_at"]) >= utc(cutoff) for i in originals):
        classification = "post-cutoff-new-issue-candidate"
    elif all(utc(i["created_at"]) < utc(cutoff) for i in originals):
        classification = "pre-cutoff-backlog-candidate"
    else:
        classification = "mixed-original-issue-dates-review-required"
    result["temporal_classification"] = classification
    result["benchmark_qualification"] = "not-executed"
    return result


def connect_issue_alias_clusters(groups):
    """PRs sharing any original issue form one evaluation unit, with aliases preserved."""
    parents = list(range(len(groups)))

    def root(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    seen = {}
    for index, group in enumerate(groups):
        for issue in group["original_issues"]:
            identity = issue["repository"].lower() + ":" + str(issue["number"])
            if identity in seen:
                parents[root(index)] = root(seen[identity])
            seen[identity] = index
    clusters = {}
    for i, group in enumerate(groups):
        clusters.setdefault(root(i), []).append(group)
    for members in clusters.values():
        identities = sorted(
            {
                i["repository"].lower() + ":" + str(i["number"])
                for g in members
                for i in g["original_issues"]
            }
        )
        basis = identities or [f"unmapped:{members[0]['repository']}:{members[0]['pull_number']}"]
        cluster = (
            "issue-alias-cluster:" + hashlib.sha256("\n".join(basis).encode()).hexdigest()[:20]
        )
        exposed = any(g["exposed_gold_development_only"] for g in members)
        for group in members:
            group["issue_alias_cluster_id"] = cluster
            group["exposed_gold_development_only"] = exposed
            group["cluster_original_issue_ids"] = identities
            group["independent_bug_cluster_verified"] = False
    return groups
