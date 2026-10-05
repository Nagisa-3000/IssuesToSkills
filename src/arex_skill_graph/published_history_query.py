"""Prepare replay queries from qualified original inputs and published source bytes."""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import tarfile
from pathlib import Path
from urllib.parse import urlsplit

from .action_contracts import utc
from .public_snapshot import extract_public_archive
from .task_context import EvidenceAnchor, TaskContext, assert_public


def verified_original_query_input(raw_input, raw_qualification):
    """Validate exact original opened-input bytes and their existing attestation."""
    if not isinstance(raw_input, bytes) or not isinstance(raw_qualification, bytes):
        raise TypeError("original query validation requires exact bytes")
    opened, qualified = json.loads(raw_input), json.loads(raw_qualification)
    if (
        qualified.get("schema") != "historical-query-original-opened-input-qualification-v1"
        or qualified.get("public_event_verified") is not True
        or qualified.get("query_text_as_of_input_time_verified") is not True
        or qualified.get("repair_tests_patch_and_later_comments_supplied") is not False
        or hashlib.sha256(raw_input).hexdigest() != qualified.get("input_artifact_sha256")
    ):
        raise ValueError("original public query qualification is missing or changed")
    for field in ("query_issue", "event_id", "repository_id", "raw_event_sha256"):
        if opened.get(field) != qualified.get(field):
            raise ValueError("original query event identity differs from its qualification")
    issue = opened["input"]
    at = qualified["input_available_at"]
    if (
        opened.get("event_type") != "IssuesEvent"
        or type(opened.get("repository_id")) is not int
        or opened["repository_id"] <= 0
        or utc(opened["event_created_at"]) != utc(at)
        or utc(issue["created_at"]) != utc(issue["updated_at"])
        or utc(issue["updated_at"]) > utc(at)
        or utc(qualified["original_body_version_at"]) != utc(issue["created_at"])
        or int(opened["query_issue"].rsplit(":", 1)[1]) != issue["number"]
    ):
        raise ValueError("original opened input chronology or identity is invalid")
    repository = qualified["canonical_repository"]
    if opened["query_issue"].rsplit(":", 1)[0] != repository:
        raise ValueError("canonical repository differs from original query identity")
    if (
        not isinstance(issue.get("title"), str)
        or not isinstance(issue.get("body"), str)
        or not issue["body"].strip()
    ):
        raise ValueError("original query needs its title and nonempty body")
    problem = issue["title"] + "\n\n" + issue["body"]
    assert_public(problem)
    return opened, qualified, problem


def prepare_published_query(
    input_path, qualification_path, metadata_path, archive_path, destination, *, environment=()
):
    """Import an exact pre-input PyPI sdist and original opened-event text.

    Input and registry receipts are current validation attestations. No discussion,
    repair or current Git-tag content enters this checkout. The new synthetic Git
    commit is created now and is never presented as historical publication.
    """
    paths = [Path(x) for x in (input_path, qualification_path, metadata_path, archive_path)]
    raw_input, raw_qualification, raw_metadata, archive = [x.read_bytes() for x in paths]
    opened, qualified, problem = verified_original_query_input(raw_input, raw_qualification)
    metadata = json.loads(raw_metadata)
    at = qualified["input_available_at"]
    repository = qualified["canonical_repository"]
    selected = [x for x in metadata["urls"] if x["filename"] == paths[3].name]
    if len(selected) != 1:
        raise ValueError("published archive identity is ambiguous or missing")
    artifact = selected[0]
    url = urlsplit(artifact["url"])
    if (
        artifact.get("packagetype") != "sdist"
        or url.scheme != "https"
        or url.hostname != "files.pythonhosted.org"
        or url.username
        or url.password
        or url.query
        or url.fragment
        or utc(artifact["upload_time_iso_8601"]) >= utc(at)
    ):
        raise ValueError("source archive is not a public PyPI sdist strictly before the input")
    archive_hash = hashlib.sha256(archive).hexdigest()
    if len(archive) != artifact["size"] or archive_hash != artifact["digests"]["sha256"]:
        raise ValueError("published source archive bytes differ from registry identity")
    if len(archive) > 64 * 1024 * 1024:
        raise ValueError("published source archive exceeds replay extraction limit")
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        members = stream.getmembers()
        if len(members) > 100000 or sum(x.size for x in members) > 256 * 1024 * 1024:
            raise ValueError("published source contents exceed replay extraction limit")
        tops = {Path(x.name).parts[0] for x in members if Path(x.name).parts}
    if len(tops) != 1:
        raise ValueError("source distribution requires one archive root")
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("preserve existing replay; choose a new destination")
    destination.mkdir(parents=True)
    extract_public_archive(archive, destination)
    root = destination / next(iter(tops))
    if not root.is_dir() or root.is_symlink():
        raise ValueError("source distribution root is not a real directory")
    hashes, expected_blobs = {}, {}
    for path in root.rglob("*"):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            data = os.fsencode(os.readlink(path))
            expected_blobs[relative] = ("120000", data)
        elif path.is_file():
            data = path.read_bytes()
            assert_public(data.decode("utf-8", errors="replace"))
            hashes[relative] = hashlib.sha256(data).hexdigest()
            expected_blobs[relative] = ("100755" if path.stat().st_mode & 0o111 else "100644", data)
    git = ["git", "-C", str(root)]
    subprocess.run([*git, "init", "-q", "--template="], check=True, capture_output=True)
    info = root / ".git/info"
    info.mkdir(exist_ok=True)
    (info / "attributes").write_text("* -text -filter -working-tree-encoding -ident\n")
    subprocess.run(
        [*git, "-c", "core.autocrlf=false", "add", "--force", "--all"],
        check=True,
        capture_output=True,
    )
    entries = subprocess.check_output([*git, "ls-files", "--stage", "-z"]).split(b"\0")
    actual_names = set()
    for entry in entries:
        if not entry:
            continue
        fields, raw_path = entry.split(b"\t", 1)
        mode, blob, stage = fields.decode().split()
        relative = os.fsdecode(raw_path)
        actual_names.add(relative)
        expected_mode, data = expected_blobs[relative]
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if stage != "0" or mode != expected_mode or blob != digest:
            raise ValueError("synthetic Git index changed published bytes or modes")
    if actual_names != set(expected_blobs):
        raise ValueError("synthetic Git index omitted published artifacts")
    tree = subprocess.check_output([*git, "write-tree"], text=True).strip()
    raw_commit = subprocess.check_output(
        [
            *git,
            "-c",
            "commit.gpgsign=false",
            "-c",
            "user.name=Published source replay",
            "-c",
            "user.email=public-replay@arex.invalid",
            "commit-tree",
            tree,
        ],
        input=(
            "Synthetic replay of published " + metadata["name"] + " " + metadata["version"] + "\n"
        ).encode(),
    )
    base = raw_commit.decode().strip()
    subprocess.run(
        [*git, "update-ref", "refs/heads/public-base", base], check=True, capture_output=True
    )
    subprocess.run(
        [*git, "symbolic-ref", "HEAD", "refs/heads/public-base"], check=True, capture_output=True
    )
    task = TaskContext(
        opened["query_issue"],
        repository,
        base,
        str(root),
        problem,
        at,
        (EvidenceAnchor("current:issue", "public_issue", problem, base, available_at=at),),
        environment=tuple(environment),
    )
    task.verify()
    audit = {
        "schema": "published-source-original-input-query-preparation-v1",
        "query_issue": task.task_id,
        "input_available_at": at,
        "input_file_sha256": hashlib.sha256(raw_input).hexdigest(),
        "input_qualification_file_sha256": hashlib.sha256(raw_qualification).hexdigest(),
        "registry_metadata_file_sha256": hashlib.sha256(raw_metadata).hexdigest(),
        "published_artifact": artifact,
        "archive_sha256": archive_hash,
        "published_file_count": len(hashes),
        "published_file_sha256": hashes,
        "synthetic_git_base": base,
        "synthetic_git_tree": tree,
        "published_index_artifacts_verified": len(expected_blobs),
        "synthetic_commit_is_not_a_historical_publication_event": True,
        "original_reported_environment_is_not_claimed_as_observed": True,
        "runtime_environment": list(task.environment),
        "runtime_environment_inferred_from_repository": False,
        "later_comments_repairs_and_git_tag_contents_imported": False,
        "registry_attestation_not_backdated": True,
        "formal_SWE_query": False,
        "actual_LLM_calls": 0,
    }
    return task, audit
