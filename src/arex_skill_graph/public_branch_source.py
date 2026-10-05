"""Public pre-input branch snapshots, qualified by archived push events."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from .action_contracts import utc
from .history_census import fingerprint, redact_history
from .published_history_query import verified_original_query_input
from .task_context import EvidenceAnchor, TaskContext, assert_public


@dataclass(frozen=True)
class PublicPushTarget:
    query_issue: str
    repository_id: int
    input_available_at: str
    ref: str

    def __post_init__(self):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:[1-9][0-9]*", self.query_issue):
            raise ValueError("invalid public source query identity")
        if type(self.repository_id) is not int or self.repository_id <= 0:
            raise ValueError("public source requires stable numeric repository identity")
        if not re.fullmatch(r"refs/heads/[A-Za-z0-9_.-]+", self.ref) or ".." in self.ref:
            raise ValueError("public source needs an explicit supported branch ref")
        utc(self.input_available_at)


def archive_hour(url):
    parsed = urlsplit(url)
    match = re.fullmatch(r"/([0-9]{4}-[0-9]{2}-[0-9]{2})-([0-9]{1,2})\.json\.gz", parsed.path)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "data.gharchive.org"
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or not match
    ):
        raise ValueError("public push requires a trusted GH Archive hour URL")
    return datetime.fromisoformat(match[1]).replace(hour=int(match[2]), tzinfo=UTC)


def qualified_public_push(raw_event, target, archive_url):
    event = json.loads(raw_event)
    repo, payload = event.get("repo", {}), event.get("payload", {})
    if (
        event.get("type") != "PushEvent"
        or event.get("public") is not True
        or repo.get("id") != target.repository_id
        or type(repo.get("id")) is not int
        or payload.get("ref") != target.ref
        or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo.get("name", ""))
        or not str(event.get("id", "")).isdigit()
    ):
        raise ValueError("push is not the requested public repository and branch")
    at = utc(event["created_at"])
    if at >= utc(target.input_available_at):
        raise ValueError("public push does not strictly precede original input")
    if at.replace(minute=0, second=0, microsecond=0) != archive_hour(archive_url):
        raise ValueError("public push differs from archive hour")
    head = payload.get("head", "")
    if not re.fullmatch(r"[0-9a-f]{40}", head) or head == "0" * 40:
        raise ValueError("public push lacks a concrete Git head")
    return {
        "schema": "archived-pre-input-public-push-v1",
        "query_issue": target.query_issue,
        "repository_id": target.repository_id,
        "repository_name_at_event": repo["name"],
        "ref": target.ref,
        "head_commit": head,
        "event_id": str(event["id"]),
        "event_created_at": event["created_at"],
        "input_available_at": target.input_available_at,
        "archive_url": archive_url,
        "raw_event_sha256": hashlib.sha256(raw_event).hexdigest(),
        "public_event_verified": True,
        "commit_dates_used_as_publication_proof": False,
        "raw_commit_messages_and_unrelated_events_persisted": False,
    }


def scan_public_pushes(
    stream, targets, archive_url, *, max_bytes=1024**3, max_line_bytes=8 * 1024**2
):
    archive_hour(archive_url)
    targets = tuple(targets)
    if (
        len({t.query_issue for t in targets}) != len(targets)
        or max_bytes <= 0
        or max_line_bytes <= 0
    ):
        raise ValueError("public push scan needs unique targets and positive bounds")
    found, invalid, total, count = {t.query_issue: [] for t in targets}, {}, 0, 0
    seen = {}
    while True:
        raw = stream.readline(min(max_line_bytes + 1, max_bytes - total + 1))
        if not raw:
            break
        total += len(raw)
        if total > max_bytes or len(raw) > max_line_bytes:
            raise ValueError("public push archive scan bound reached")
        event = json.loads(raw)
        count += 1
        if event.get("type") != "PushEvent":
            continue
        for target in targets:
            if (
                event.get("repo", {}).get("id") != target.repository_id
                or event.get("payload", {}).get("ref") != target.ref
            ):
                continue
            try:
                if utc(event["created_at"]) >= utc(target.input_available_at):
                    continue
                projection = qualified_public_push(raw, target, archive_url)
                key = (target.query_issue, projection["event_id"])
                if key in seen and seen[key] != projection:
                    raise ValueError("conflicting archived publication identity")
                if key not in seen:
                    found[target.query_issue].append(projection)
                    seen[key] = projection
            except (ValueError, KeyError, TypeError) as error:
                invalid[target.query_issue] = redact_history(str(error))
    for query_issue in invalid:
        found[query_issue] = []
    return found, {
        "archive_url": archive_url,
        "archive_scan_complete": True,
        "decompressed_bytes_scanned": total,
        "events_scanned": count,
        "invalid_targets": invalid,
        "unrelated_raw_events_persisted": False,
    }


def latest_archived_push(projections):
    if not projections:
        raise ValueError("no qualified public push in the located archive")
    at = max(utc(p["event_created_at"]) for p in projections)
    latest = [p for p in projections if utc(p["event_created_at"]) == at]
    if len({p["head_commit"] for p in latest}) != 1:
        raise ValueError("different public heads at latest observed second; ordering unknown")
    return min(latest, key=lambda p: p["event_id"])


def _git(git_dir, *args):
    result = subprocess.run(
        ["git", "--git-dir", str(git_dir), *args], capture_output=True, timeout=120, check=False
    )
    if result.returncode:
        raise ValueError("selected public Git object is unavailable; no gold-parent fallback")
    return result.stdout


def _public_objects(git_dir, head):
    raw_commit = _git(git_dir, "cat-file", "commit", head)
    actual = hashlib.sha1(
        b"commit " + str(len(raw_commit)).encode() + b"\0" + raw_commit
    ).hexdigest()
    if actual != head:
        raise ValueError("selected public commit bytes do not match archived identity")
    assert_public(raw_commit.decode("utf-8", errors="replace"))
    entries = []
    for row in _git(git_dir, "ls-tree", "-rz", "--full-tree", head).split(b"\0"):
        if not row:
            continue
        fields, raw_path = row.split(b"\t", 1)
        mode, kind, sha = fields.decode().split()
        name = os.fsdecode(raw_path)
        if (
            kind != "blob"
            or mode not in {"100644", "100755", "120000"}
            or PurePosixPath(name).is_absolute()
            or any(p in {".", "..", ".git"} for p in PurePosixPath(name).parts)
            or "\\" in name
        ):
            raise ValueError("public source contains unsupported or escaping Git entry")
        assert_public(name)
        entries.append((name, mode, sha))
    if not entries or len(entries) > 100000:
        raise ValueError("public source tree is empty or exceeds object bound")
    result = subprocess.run(
        ["git", "--git-dir", str(git_dir), "cat-file", "--batch"],
        input=b"".join(sha.encode() + b"\n" for _, _, sha in entries),
        capture_output=True,
        timeout=120,
        check=False,
    )
    if result.returncode or len(result.stdout) > 256 * 1024**2:
        raise ValueError("public source blob read failed or exceeds bound")
    data, cursor, expected = result.stdout, 0, {}
    for name, mode, sha in entries:
        end = data.index(b"\n", cursor)
        actual_sha, kind, length = data[cursor:end].decode().split()
        length = int(length)
        blob = data[end + 1 : end + 1 + length]
        cursor = end + 2 + length
        actual = hashlib.sha1(b"blob " + str(length).encode() + b"\0" + blob).hexdigest()
        if actual_sha != sha or kind != "blob" or len(blob) != length or actual != sha:
            raise ValueError("public source blob differs from selected Git identity")
        assert_public(blob.decode("utf-8", errors="replace"))
        if mode == "120000":
            target = os.fsdecode(blob)
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
            if (
                target.startswith("/")
                or (resolved == ".." or resolved.startswith("../"))
                or ".git" in PurePosixPath(resolved).parts
            ):
                raise ValueError("public source symlink escapes the selected checkout")
        expected[name] = {
            "mode": mode,
            "blob_sha": sha,
            "content_sha256": hashlib.sha256(blob).hexdigest(),
        }
    return expected


def prepare_public_branch_query(input_path, qualification_path, publication, git_dir, destination):
    raw_input, raw_qualification = (
        Path(input_path).read_bytes(),
        Path(qualification_path).read_bytes(),
    )
    opened, qualified, problem = verified_original_query_input(raw_input, raw_qualification)
    target = PublicPushTarget(
        opened["query_issue"],
        opened["repository_id"],
        qualified["input_available_at"],
        publication["ref"],
    )
    if (
        publication.get("schema") != "archived-pre-input-public-push-v1"
        or publication.get("public_event_verified") is not True
        or publication.get("query_issue") != target.query_issue
        or publication.get("repository_id") != target.repository_id
        or utc(publication["input_available_at"]) != utc(target.input_available_at)
        or utc(publication["event_created_at"]) >= utc(target.input_available_at)
        or not re.fullmatch(r"[0-9a-f]{64}", publication.get("raw_event_sha256", ""))
        or not re.fullmatch(r"[0-9a-f]{40}", publication.get("head_commit", ""))
        or publication.get("commit_dates_used_as_publication_proof") is not False
    ):
        raise ValueError("public source publication differs from qualified original input")
    at = utc(publication["event_created_at"])
    if at.replace(minute=0, second=0, microsecond=0) != archive_hour(publication["archive_url"]):
        raise ValueError("saved publication differs from archived hour")
    head, git_dir = publication["head_commit"], Path(git_dir).resolve()
    expected = _public_objects(git_dir, head)
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("preserve existing public source query; choose a new version")
    destination.mkdir(parents=True)
    git = ["git", "-C", str(destination)]
    for args in (["init", "-q", "--template="], ["config", "core.autocrlf", "false"]):
        subprocess.run([*git, *args], check=True, capture_output=True)
    info = destination / ".git/info"
    info.mkdir(exist_ok=True)
    (info / "attributes").write_text("* -text -filter -working-tree-encoding -ident\n")
    subprocess.run(
        [*git, "fetch", "-q", "--no-tags", "--depth=1", str(git_dir), head],
        check=True,
        capture_output=True,
        timeout=120,
    )
    subprocess.run(
        [*git, "checkout", "-q", "--detach", head], check=True, capture_output=True, timeout=120
    )
    for name, item in expected.items():
        path = destination / name
        data = os.fsencode(os.readlink(path)) if item["mode"] == "120000" else path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item["content_sha256"]:
            raise ValueError("checkout filters or filesystem changed published source bytes")
        mode = (
            "120000" if path.is_symlink() else "100755" if path.stat().st_mode & 0o111 else "100644"
        )
        if mode != item["mode"]:
            raise ValueError("checkout changed published source mode")
    task = TaskContext(
        target.query_issue,
        qualified["canonical_repository"],
        head,
        str(destination),
        problem,
        target.input_available_at,
        (
            EvidenceAnchor(
                "current:issue",
                "public_issue",
                problem,
                head,
                available_at=target.input_available_at,
            ),
        ),
    )
    task.verify()
    audit = {
        "schema": "original-input-public-branch-query-preparation-v1",
        "query_issue": task.task_id,
        "base_commit": head,
        "source_publication": publication,
        "source_publication_sha256": fingerprint(publication),
        "input_file_sha256": hashlib.sha256(raw_input).hexdigest(),
        "input_qualification_sha256": hashlib.sha256(raw_qualification).hexdigest(),
        "public_git_objects": expected,
        "git_objects_sha256": fingerprint(expected),
        "all_public_blob_bytes_and_modes_verified": True,
        "commit_dates_used_as_publication_proof": False,
        "git_source_is_current_observation_not_backdated": True,
        "native_source_records_replaced": False,
        "known_repairs_or_later_comments_supplied": False,
        "runtime_environment_claimed_as_observed": False,
        "independent_replay_controls_completed": False,
        "actual_LLM_calls": 0,
        "formal_SWE_runs": 0,
    }
    return task, audit
