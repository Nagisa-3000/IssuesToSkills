import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

import pytest

from arex_skill_graph.published_history_query import prepare_published_query


def packet(tmp_path, extra=None):
    opened = {
        "query_issue": "example/repo:7",
        "event_id": "event-7",
        "repository_id": 77,
        "raw_event_sha256": "a" * 64,
        "event_type": "IssuesEvent",
        "event_created_at": "2020-06-05T19:22:59Z",
        "input": {
            "number": 7,
            "title": "Supported names fragment",
            "body": "Public reproduction only.",
            "created_at": "2020-06-05T19:22:58Z",
            "updated_at": "2020-06-05T19:22:58Z",
        },
    }
    ip = tmp_path / "input.json"
    ip.write_text(json.dumps(opened))
    qualified = {
        "schema": "historical-query-original-opened-input-qualification-v1",
        "public_event_verified": True,
        "query_text_as_of_input_time_verified": True,
        "repair_tests_patch_and_later_comments_supplied": False,
        "input_artifact_sha256": hashlib.sha256(ip.read_bytes()).hexdigest(),
        "canonical_repository": "example/repo",
        "input_available_at": opened["event_created_at"],
        "original_body_version_at": opened["input"]["created_at"],
        **{k: opened[k] for k in ["query_issue", "event_id", "repository_id", "raw_event_sha256"]},
    }
    qp = tmp_path / "qualification.json"
    qp.write_text(json.dumps(qualified))
    archive = io.BytesIO()
    files = {"package-1.0/example.py": b"print('published')\n", **(extra or {})}
    with tarfile.open(fileobj=archive, mode="w:gz") as stream:
        for name, content in files.items():
            entry = tarfile.TarInfo(name)
            entry.size = len(content)
            entry.mode = 0o644
            stream.addfile(entry, io.BytesIO(content))
    ap = tmp_path / "package-1.0.tar.gz"
    ap.write_bytes(archive.getvalue())
    metadata = {
        "name": "package",
        "version": "1.0",
        "urls": [
            {
                "filename": ap.name,
                "url": "https://files.pythonhosted.org/packages/public/package-1.0.tar.gz",
                "packagetype": "sdist",
                "upload_time_iso_8601": "2020-04-27T10:04:19Z",
                "size": ap.stat().st_size,
                "digests": {"sha256": hashlib.sha256(ap.read_bytes()).hexdigest()},
            }
        ],
    }
    mp = tmp_path / "metadata.json"
    mp.write_text(json.dumps(metadata))
    return [ip, qp, mp, ap, tmp_path / "replay"]


def edit(path, change):
    value = json.loads(path.read_text())
    change(value)
    path.write_text(json.dumps(value))


def test_original_body_and_published_bytes_are_the_only_replay_inputs(tmp_path):
    args = packet(tmp_path)
    task, audit = prepare_published_query(*args)
    assert task.public_problem == "Supported names fragment\n\nPublic reproduction only."
    assert task.input_available_at == "2020-06-05T19:22:59Z"
    assert task.environment == ()
    assert audit["published_file_count"] == audit["published_index_artifacts_verified"] == 1
    assert audit["later_comments_repairs_and_git_tag_contents_imported"] is False
    assert audit["formal_SWE_query"] is False
    at = subprocess.check_output(
        ["git", "-C", task.root, "show", "-s", "--format=%cI", "HEAD"], text=True
    ).strip()
    assert at > task.input_available_at
    assert audit["synthetic_commit_is_not_a_historical_publication_event"]


@pytest.mark.parametrize("at", ["2020-06-05T19:22:59Z", "2021-03-28T19:41:52Z"])
def test_release_at_or_after_original_input_cannot_qualify_a_base(tmp_path, at):
    args = packet(tmp_path)
    edit(args[2], lambda x: x["urls"][0].update(upload_time_iso_8601=at))
    with pytest.raises(ValueError, match="strictly before"):
        prepare_published_query(*args)
    assert not args[-1].exists()


def test_changed_original_input_is_rejected_before_export(tmp_path):
    args = packet(tmp_path)
    edit(args[0], lambda x: x["input"].update(body="Later modified report"))
    with pytest.raises(ValueError, match="qualification is missing or changed"):
        prepare_published_query(*args)
    assert not args[-1].exists()


def test_archive_bytes_must_match_exact_registry_identity(tmp_path):
    args = packet(tmp_path)
    args[3].write_bytes(args[3].read_bytes() + b"extra")
    with pytest.raises(ValueError, match="archive bytes differ"):
        prepare_published_query(*args)
    assert not args[-1].exists()


def test_later_body_version_is_not_an_original_opened_input(tmp_path):
    args = packet(tmp_path)
    edit(args[0], lambda x: x["input"].update(updated_at="2020-06-06T00:00:00Z"))
    edit(
        args[1],
        lambda x: x.update(input_artifact_sha256=hashlib.sha256(args[0].read_bytes()).hexdigest()),
    )
    with pytest.raises(ValueError, match="chronology or identity"):
        prepare_published_query(*args)


def test_unaccepted_original_input_receipt_cannot_qualify_a_query(tmp_path):
    args = packet(tmp_path)
    edit(args[1], lambda x: x.update(public_event_verified=False))
    with pytest.raises(ValueError, match="qualification is missing or changed"):
        prepare_published_query(*args)


def test_existing_replay_is_preserved(tmp_path):
    args = packet(tmp_path)
    args[-1].mkdir()
    marker = args[-1] / "user-work.txt"
    marker.write_text("preserve")
    with pytest.raises(ValueError, match="preserve existing replay"):
        prepare_published_query(*args)
    assert marker.read_text() == "preserve"


def test_archive_cannot_import_git_history(tmp_path):
    args = packet(tmp_path, {"package-1.0/.git/config": b"untrusted history"})
    with pytest.raises(ValueError, match="Git history"):
        prepare_published_query(*args)


def test_crlf_source_survives_git_attribute_normalization(tmp_path):
    raw = b"first = 1\r\nsecond = 2\r\n"
    args = packet(
        tmp_path, {"package-1.0/.gitattributes": b"*.py text eol=lf\n", "package-1.0/crlf.py": raw}
    )
    task, audit = prepare_published_query(*args)
    actual = subprocess.check_output(["git", "-C", task.root, "show", "HEAD:crlf.py"])
    assert actual == raw == (Path(task.root) / "crlf.py").read_bytes()
    assert audit["published_file_sha256"]["crlf.py"] == hashlib.sha256(raw).hexdigest()


def test_explicit_observed_environment_is_preserved_without_claiming_original_binary(tmp_path):
    args = packet(tmp_path)
    observed = ("Python 3.8.3; later isolated verification runtime",)
    task, audit = prepare_published_query(*args, environment=observed)
    assert task.environment == observed
    assert audit["runtime_environment"] == list(observed)
    assert audit["runtime_environment_inferred_from_repository"] is False
    assert audit["original_reported_environment_is_not_claimed_as_observed"] is True


def test_cli_exports_a_reusable_task_and_audit(tmp_path):
    import importlib.util

    script = Path(__file__).resolve().parents[1] / "experiments/prepare_published_history_query.py"
    spec = importlib.util.spec_from_file_location("published_query_cli", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = packet(tmp_path)
    out = tmp_path / "cli-preparation"
    flags = [
        item
        for name, value in zip(
            ("input", "qualification", "metadata", "archive", "output-dir"), (*args[:4], out)
        )
        for item in ("--" + name, str(value))
    ]
    assert module.main(flags) == 0
    exported = json.loads((out / "task.json").read_text())
    assert exported["environment"] == []
    assert exported["task_id"] == "example/repo:7"
    audit = json.loads((out / "audit.json").read_text())
    assert audit["published_index_artifacts_verified"] == 1
    with pytest.raises(ValueError, match="preserve existing query"):
        module.main(flags)
