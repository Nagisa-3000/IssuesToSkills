import hashlib
import io
import json
import subprocess

import pytest

from arex_skill_graph.historical_opened_input import original_input_qualification
from arex_skill_graph.public_branch_source import (
    PublicPushTarget,
    latest_archived_push,
    prepare_public_branch_query,
    qualified_public_push,
    scan_public_pushes,
)

TARGET = PublicPushTarget("old/project:1", 123, "2020-01-02T00:00:00Z", "refs/heads/master")
URL = "https://data.gharchive.org/2020-01-01-12.json.gz"


def event(head="a" * 40, at="2020-01-01T12:00:00Z", event_id="100"):
    return {
        "id": event_id,
        "type": "PushEvent",
        "public": True,
        "repo": {"id": 123, "name": "renamed/project"},
        "created_at": at,
        "payload": {
            "ref": "refs/heads/master",
            "head": head,
            "commits": [{"message": "unrelated discussion must stay outside saved projection"}],
        },
    }


def test_projection_uses_stable_repository_and_publication_not_git_dates():
    raw = json.dumps(event()).encode()
    result = qualified_public_push(raw, TARGET, URL)
    assert result["head_commit"] == "a" * 40
    assert result["repository_name_at_event"] == "renamed/project"
    assert result["raw_event_sha256"] == hashlib.sha256(raw).hexdigest()
    assert "discussion" not in json.dumps(result)
    assert result["commit_dates_used_as_publication_proof"] is False


@pytest.mark.parametrize(
    "change",
    [
        {"public": False},
        {"type": "PullRequestEvent"},
        {"repo": {"id": 124, "name": "renamed/project"}},
        {"payload": {"ref": "refs/heads/other", "head": "a" * 40}},
        {"payload": {"ref": "refs/heads/master", "head": "0" * 40}},
        {"payload": {"ref": "refs/heads/master", "head": "not-a-head"}},
        {"created_at": TARGET.input_available_at},
        {"created_at": "2020-01-03T12:00:00Z"},
        {"id": "missing"},
    ],
)
def test_projection_rejects_unproved_publication(change):
    with pytest.raises(ValueError):
        qualified_public_push(json.dumps({**event(), **change}).encode(), TARGET, URL)


@pytest.mark.parametrize(
    "url",
    [
        "http://data.gharchive.org/2020-01-01-12.json.gz",
        "https://other.invalid/2020-01-01-12.json.gz",
        "https://data.gharchive.org/2020-01-01-13.json.gz",
        URL + "?extra=1",
    ],
)
def test_archive_identity_is_not_a_locator_claim(url):
    with pytest.raises(ValueError):
        qualified_public_push(json.dumps(event()).encode(), TARGET, url)


def test_scan_ignores_future_and_other_repository_and_selects_actual_latest():
    rows = [
        event("b" * 40, "2020-01-01T12:02:00Z", "101"),
        event("a" * 40),
        event("c" * 40, TARGET.input_available_at, "102"),
        {**event("d" * 40), "repo": {"id": 124, "name": "other/project"}},
    ]
    stream = io.BytesIO(b"".join(json.dumps(row).encode() + b"\n" for row in rows))
    found, audit = scan_public_pushes(stream, [TARGET], URL)
    assert latest_archived_push(found[TARGET.query_issue])["head_commit"] == "b" * 40
    assert len(found[TARGET.query_issue]) == 2
    assert audit["archive_scan_complete"] is True
    assert audit["unrelated_raw_events_persisted"] is False


def test_same_second_conflicting_heads_need_probe_not_event_id_order():
    rows = [
        qualified_public_push(json.dumps(event(head=head, event_id=str(n))).encode(), TARGET, URL)
        for n, head in enumerate(["a" * 40, "b" * 40])
    ]
    with pytest.raises(ValueError, match="ordering unknown"):
        latest_archived_push(rows)


def test_invalid_matching_event_does_not_silently_keep_an_older_head():
    rows = [event(), event(head="invalid", event_id="101")]
    found, audit = scan_public_pushes(
        io.BytesIO(b"".join(json.dumps(row).encode() + b"\n" for row in rows)), [TARGET], URL
    )
    assert not found[TARGET.query_issue]
    assert TARGET.query_issue in audit["invalid_targets"]


def test_bounded_scan_cannot_claim_complete_archive():
    with pytest.raises(ValueError, match="scan bound"):
        scan_public_pushes(io.BytesIO(json.dumps(event()).encode()), [TARGET], URL, max_bytes=20)


def git(root, *args):
    return (
        subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL)
        .decode()
        .strip()
    )


def original_input(tmp_path):
    opened = {
        "query_issue": TARGET.query_issue,
        "event_id": "200",
        "event_type": "IssuesEvent",
        "event_created_at": TARGET.input_available_at,
        "repository_id": TARGET.repository_id,
        "raw_event_sha256": "e" * 64,
        "input": {
            "number": 1,
            "title": "original public problem",
            "body": "The original input, without later discussion.",
            "created_at": TARGET.input_available_at,
            "updated_at": TARGET.input_available_at,
            "html_url": "https://github.com/old/project/issues/1",
        },
    }
    raw = json.dumps(opened).encode()
    source = tmp_path / "input.json"
    source.write_bytes(raw)
    qualified = tmp_path / "qualification.json"
    qualified.write_text(
        json.dumps(original_input_qualification(opened, hashlib.sha256(raw).hexdigest()))
    )
    return source, qualified


def repository(tmp_path):
    root = tmp_path / "native"
    root.mkdir()
    git(root, "init", "-q", "--template=")
    git(root, "config", "core.autocrlf", "false")
    git(root, "config", "user.name", "Source fixture")
    git(root, "config", "user.email", "source-fixture@arex.invalid")
    (root / "README.rst").write_text("https://api.travis-ci.org/old/project.svg?branch=master\n")
    (root / "source.py").write_bytes(b"current_public = 1\r\n")
    git(root, "add", ".")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "first public state")
    public = git(root, "rev-parse", "HEAD")
    (root / "future.py").write_text("later_repair = True\n")
    git(root, "add", ".")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "later state excluded")
    return root, public, git(root, "rev-parse", "HEAD")


def test_actual_git_snapshot_uses_only_archived_head_and_preserves_bytes(tmp_path):
    root, public, future = repository(tmp_path)
    source, qualified = original_input(tmp_path)
    publication = qualified_public_push(json.dumps(event(head=public)).encode(), TARGET, URL)
    checkout = tmp_path / "public"
    task, audit = prepare_public_branch_query(
        source, qualified, publication, root / ".git", checkout
    )
    assert task.base_commit == public
    assert git(root, "rev-parse", "HEAD") == future
    assert (checkout / "source.py").read_bytes() == b"current_public = 1\r\n"
    assert not (checkout / "future.py").exists()
    assert git(checkout, "rev-list", "--count", "HEAD") == "1"
    assert (
        subprocess.run(
            ["git", "-C", str(checkout), "cat-file", "-e", future], capture_output=True, check=False
        ).returncode
        != 0
    )
    assert task.public_problem.endswith("The original input, without later discussion.")
    assert audit["all_public_blob_bytes_and_modes_verified"] is True
    assert audit["known_repairs_or_later_comments_supplied"] is False
    assert not audit["independent_replay_controls_completed"]
    with pytest.raises(ValueError, match="preserve"):
        prepare_public_branch_query(source, qualified, publication, root / ".git", checkout)


def test_missing_public_git_head_cannot_fall_back_to_native_later_state(tmp_path):
    root, _, future = repository(tmp_path)
    source, qualified = original_input(tmp_path)
    publication = qualified_public_push(json.dumps(event()).encode(), TARGET, URL)
    with pytest.raises(ValueError, match="unavailable"):
        prepare_public_branch_query(
            source, qualified, publication, root / ".git", tmp_path / "public"
        )
    assert git(root, "rev-parse", "HEAD") == future
    assert not (tmp_path / "public").exists()


def test_publication_cannot_be_reused_for_another_original_query(tmp_path):
    root, public, _ = repository(tmp_path)
    source, qualified = original_input(tmp_path)
    publication = qualified_public_push(json.dumps(event(head=public)).encode(), TARGET, URL)
    publication["query_issue"] = "old/project:2"
    with pytest.raises(ValueError, match="differs"):
        prepare_public_branch_query(
            source, qualified, publication, root / ".git", tmp_path / "public"
        )


def test_escaping_public_symlink_is_rejected_before_any_copy(tmp_path):
    root, _, _ = repository(tmp_path)
    (root / "escape").symlink_to("..")
    git(root, "add", ".")
    git(root, "-c", "commit.gpgsign=false", "commit", "-qm", "source fixture symlink")
    head = git(root, "rev-parse", "HEAD")
    source, qualified = original_input(tmp_path)
    publication = qualified_public_push(json.dumps(event(head=head)).encode(), TARGET, URL)
    with pytest.raises(ValueError, match="symlink escapes"):
        prepare_public_branch_query(
            source, qualified, publication, root / ".git", tmp_path / "public"
        )
    assert not (tmp_path / "public").exists()


def test_recovery_cli_reads_actual_string_root_and_retains_unrecovered_denominator(
    tmp_path, monkeypatch
):
    import importlib.util
    from pathlib import Path

    from arex_skill_graph.history_census import fingerprint

    root, public, _ = repository(tmp_path)
    source, qualified = original_input(tmp_path)
    publication = qualified_public_push(json.dumps(event(head=public)).encode(), TARGET, URL)
    prior, _ = prepare_public_branch_query(
        source, qualified, publication, root / ".git", tmp_path / "prior"
    )
    content = (Path(prior.root) / "README.rst").read_bytes()
    work = [
        {
            "query_issue": TARGET.query_issue,
            "repository_id": TARGET.repository_id,
            "before_input_at": TARGET.input_available_at,
            "ref": TARGET.ref,
            "archive_url": URL,
            "locator_event_at": publication["event_created_at"],
            "source_selection_uses_gold_outcomes": False,
            "branch_evidence": [
                {
                    "path": "README.rst",
                    "line": 1,
                    "text": content.decode().splitlines()[0],
                    "file_sha256": hashlib.sha256(content).hexdigest(),
                }
            ],
        }
    ]
    queries = [{"task": prior.to_dict(), "fix_id": "fixture:repair"}]
    register = {
        "queries_sha256": fingerprint(queries),
        "query_count": 1,
        "selected_targets": 2,
        "audits": [{"query_id": TARGET.query_issue}, {"query_id": "old/project:2"}],
    }
    recovery = {
        "later_comments_and_repairs_persisted": False,
        "results": [
            {
                "query_issue": TARGET.query_issue,
                "status": "original_input_qualified",
                "input_path": str(source),
                "qualification_path": str(qualified),
            }
        ],
    }
    values = {
        "work-items": work,
        "original-queries": queries,
        "query-register": register,
        "input-recovery": recovery,
        "native-repositories": {"old/project": str(root / ".git")},
    }
    args = []
    for name, value in values.items():
        path = tmp_path / (name + ".json")
        path.write_text(json.dumps(value))
        args.extend(["--" + name, str(path)])
    output = tmp_path / "results"
    spec = importlib.util.spec_from_file_location(
        "public_branch_cli_fixture",
        Path(__file__).resolve().parents[1] / "experiments/recover_public_branch_queries.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(
        module,
        "scan_hour",
        lambda url, rows: (
            {TARGET.query_issue: [publication]},
            {"archive_url": url, "archive_scan_complete": True},
        ),
    )
    assert module.main([*args, "--output-dir", str(output)]) == 0
    result = json.loads((output / "query-register.json").read_text())
    assert result["selected_targets"] == len(result["audits"]) == 2
    assert result["query_count"] == 1
    assert {r["status"] for r in result["audits"]} == {
        "original_input_unrecovered",
        "registered_original_public_branch_query",
    }
    actual = json.loads((output / "queries.json").read_text())[0]["task"]
    assert actual["base_commit"] == public
    assert actual["public_problem"] == prior.public_problem
    assert result["new_utility_labels"] == 0


def test_archive_transport_identifies_auditor_and_counts_complete_stream(tmp_path, monkeypatch):
    import gzip
    import importlib.util
    from pathlib import Path
    from urllib.request import Request

    source = Path(__file__).resolve().parents[1] / "experiments/recover_public_branch_queries.py"
    spec = importlib.util.spec_from_file_location("public_branch_transport_test", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = json.dumps(event()).encode() + b"\n"
    compressed = gzip.compress(raw)
    requests = []

    def open_archive(request, *, timeout):
        assert isinstance(request, Request)
        assert request.full_url == URL
        assert request.get_header("User-agent") == "AREX historical-input-audit"
        assert timeout == 90
        requests.append(request)
        return io.BytesIO(compressed)

    monkeypatch.setattr(module.urllib.request, "urlopen", open_archive)
    found, audit = module.scan_hour(
        URL,
        [
            {
                "query_issue": TARGET.query_issue,
                "repository_id": TARGET.repository_id,
                "before_input_at": TARGET.input_available_at,
                "ref": TARGET.ref,
            }
        ],
    )
    assert len(requests) == 1
    assert len(found[TARGET.query_issue]) == 1
    assert audit["archive_scan_complete"] is True
    assert audit["compressed_bytes_read"] == len(compressed)
    assert audit["compressed_archive_sha256"] == hashlib.sha256(compressed).hexdigest()
    assert audit["unrelated_raw_events_persisted"] is False
