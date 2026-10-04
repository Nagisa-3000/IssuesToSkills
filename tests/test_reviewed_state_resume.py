"""Sealed Action continuation controls; synthetic cases do not prove repair utility."""
import hashlib
import importlib.util
import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_runner import snapshot_base
from arex_skill_graph.task_context import EvidenceAnchor
from arex_skill_graph.workspace_state import (
    copy_sealed_public_workspace,
    public_workspace_execution_sha256,
)


def changed_state(tmp_path, *, seal=True):
    _package, task, _policy = make_fixture(tmp_path)
    path = Path(task.root, "checker.py")
    path.write_text(path.read_text().replace("return True", "return context == 'runtime'"))
    anchor = next(a for a in task.anchors if a.path == "checker.py")
    task = task.update(anchors=(replace(anchor, sha256=hashlib.sha256(path.read_bytes()).hexdigest()),))
    if seal:
        task = task.update(anchors=(EvidenceAnchor(
            "reviewed:post-edit", "workspace_execution_snapshot", "Synthetic accepted current state",
            task.base_commit, sha256=public_workspace_execution_sha256(task.root),
        ),))
    task.verify()
    return task


def test_explicit_continuation_transfers_the_exact_changed_public_state(tmp_path):
    task = changed_state(tmp_path)
    copied = snapshot_base(task, tmp_path / "continuation", resume_reviewed_state=True)
    assert Path(copied.root, "checker.py").read_bytes() == Path(task.root, "checker.py").read_bytes()
    assert public_workspace_execution_sha256(copied.root) == public_workspace_execution_sha256(task.root)
    assert copied.base_commit == task.base_commit
    assert not Path(copied.root, ".git").exists()
    copied.verify(verify_head=False)
    # Default benchmark bootstrap continues to demand the pinned base.
    with pytest.raises(ValueError, match="content differs from the pinned base archive"):
        snapshot_base(task, tmp_path / "default")


def test_continuation_preserves_reviewed_public_new_files_and_modes(tmp_path):
    task = changed_state(tmp_path)
    Path(task.root, "public-records").mkdir()
    Path(task.root, "public-records/observed.txt").write_text("Actual public record\n")
    Path(task.root, "checker.py").chmod(0o640)
    old = next(a for a in task.anchors if a.kind == "workspace_execution_snapshot")
    task = task.update(anchors=(replace(old, sha256=public_workspace_execution_sha256(task.root)),))
    copied = snapshot_base(task, tmp_path / "continuation", resume_reviewed_state=True)
    assert Path(copied.root, "public-records/observed.txt").read_text() == "Actual public record\n"
    assert Path(copied.root, "checker.py").stat().st_mode & 0o7777 == 0o640
    assert public_workspace_execution_sha256(copied.root) == public_workspace_execution_sha256(task.root)


def test_continuation_requires_an_execution_seal(tmp_path):
    task = changed_state(tmp_path, seal=False)
    with pytest.raises(ValueError, match="requires one consistent execution seal"):
        snapshot_base(task, tmp_path / "continuation", resume_reviewed_state=True)
    assert not (tmp_path / "continuation").exists()


def test_stale_seal_cannot_be_used_to_continue(tmp_path):
    task = changed_state(tmp_path)
    Path(task.root, "unexpected.txt").write_text("Unreviewed public change\n")
    with pytest.raises(ValueError, match="stale"):
        snapshot_base(task, tmp_path / "continuation", resume_reviewed_state=True)
    assert not (tmp_path / "continuation").exists()


def test_copy_rejects_external_links_without_exporting_their_content(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("Restricted outside content\n")
    (source / "escape").symlink_to(outside)
    with pytest.raises(ValueError, match="escapes its content seal"):
        copy_sealed_public_workspace(source, tmp_path / "copy", "0" * 64)
    assert not (tmp_path / "copy").exists()


def test_bootstrap_failure_preserves_real_call_metadata_and_redacts_the_error(tmp_path, monkeypatch):
    from arex_skill_graph.llm_http import OpenAICompatibleConfig

    spec = importlib.util.spec_from_file_location(
        "native_resume_exercise_cli", Path(__file__).resolve().parents[1] / "experiments/eval_native_action_observation.py",
    )
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    package, task, _policy = make_fixture(tmp_path)
    refs, task_path = tmp_path / "refs.json", tmp_path / "task.json"
    refs.write_text(json.dumps([package.reference]))
    task_path.write_text(json.dumps(task.to_dict()))
    secret = "fixture-private-value"
    transport = SimpleNamespace(
        config=OpenAICompatibleConfig(secret, "https://example.invalid/v1", "fixture"),
        calls=[{"successful": True, "usage": {"total_tokens": 17}}],
        transcripts=[{"response": {"fixture": "retained"}}],
    )
    monkeypatch.setattr(cli, "transport_from_args", lambda _args: transport)

    class FailingSolver:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            raise ValueError("fixture bootstrap " + secret)

    monkeypatch.setattr(cli, "AdaptiveSolver", FailingSolver)
    output = tmp_path / "output"
    assert cli.main([
        "--references", str(refs), "--task-context", str(task_path), "--output-dir", str(output),
        "--action-id", package.actions[0].id, "--cutoff", "2024-01-01T00:00:00Z",
        "--dependency-root", str(tmp_path), "--model", "fixture", "--base-url", "https://example.invalid/v1",
    ]) == 1
    failure = json.loads((output / "exercise-failure.json").read_text())
    assert failure["model_calls"] == 1 and failure["trajectory_not_returned"]
    assert failure["actual_action_records"] is None
    assert secret not in (output / "exercise-failure.json").read_text()
    assert json.loads((output / "calls.json").read_text()) == transport.calls
    assert json.loads((output / "model-transcripts.json").read_text()) == transport.transcripts
    assert not (output / "trajectory.json").exists()
