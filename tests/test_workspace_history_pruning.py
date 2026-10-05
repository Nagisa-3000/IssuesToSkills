"""Archived public seals remain byte-identical while Git history is never traversed."""

import os
from pathlib import Path

import pytest

import arex_skill_graph.workspace_state as state


@pytest.fixture
def public_vector(tmp_path):
    tmp_path.chmod(0o755)
    directory = tmp_path / "src"
    directory.mkdir()
    directory.chmod(0o750)
    checker = directory / "checker.py"
    checker.write_bytes(b"public code\n")
    checker.chmod(0o640)
    probe = tmp_path / "probe.py"
    probe.write_bytes(b"public probe\n")
    probe.chmod(0o755)
    (tmp_path / "link.py").symlink_to("src/checker.py")
    for root in (tmp_path, directory):
        history = root / ".git"
        history.mkdir()
        (history / "private").write_bytes(b"ignored Git history")
    return tmp_path


@pytest.mark.skipif(os.name != "posix", reason="frozen vector includes POSIX modes and symlinks")
def test_archived_content_and_execution_seals_are_unchanged(public_vector):
    # These hashes were captured with the pre-optimization implementation.
    assert state.public_workspace_sha256(public_vector) == (
        "8501b2155ac282b594e194ffe7591f9cd44b926d6b43a06225ea4dd06b3444fc"
    )
    assert state.public_workspace_execution_sha256(public_vector) == (
        "df53a9062b78bc910e0031d2993b55272d0b421d34cb3f9233309302ae00ce06"
    )


def test_history_directories_are_pruned_before_scanning(public_vector, monkeypatch):
    original = os.scandir
    visited = []

    def guarded(path):
        path = Path(path)
        if ".git" in path.parts:
            raise AssertionError("Git history was visited while sealing public inputs")
        visited.append(path.relative_to(public_vector).as_posix())
        return original(path)

    monkeypatch.setattr(state.os, "scandir", guarded)
    entries = state.public_workspace_entries(public_vector)
    assert set(entries) == {".", "src", "src/checker.py", "probe.py", "link.py"}
    assert set(visited) == {".", "src"}


def test_changing_historical_objects_cannot_change_public_seals(public_vector):
    before = (
        state.public_workspace_sha256(public_vector),
        state.public_workspace_execution_sha256(public_vector),
    )
    (public_vector / ".git/private").write_bytes(b"different historical objects")
    (public_vector / "src/.git/private").write_bytes(b"different nested historical objects")
    after = (
        state.public_workspace_sha256(public_vector),
        state.public_workspace_execution_sha256(public_vector),
    )
    assert before == after


@pytest.mark.skipif(os.name != "posix", reason="execution seal includes POSIX modes")
def test_public_permission_changes_remain_visible_without_changing_content(public_vector):
    content = state.public_workspace_sha256(public_vector)
    execution = state.public_workspace_execution_sha256(public_vector)
    (public_vector / "src/checker.py").chmod(0o750)
    assert state.public_workspace_sha256(public_vector) == content
    assert state.public_workspace_execution_sha256(public_vector) != execution


def test_unreadable_public_directory_cannot_produce_a_partial_seal(public_vector, monkeypatch):
    original = os.scandir

    def unavailable(path):
        if Path(path) == public_vector / "src":
            raise PermissionError("controlled unavailable public directory")
        return original(path)

    monkeypatch.setattr(state.os, "scandir", unavailable)
    with pytest.raises(PermissionError, match="unavailable public"):
        state.public_workspace_execution_sha256(public_vector)


def test_public_link_escape_is_still_rejected(public_vector):
    (public_vector / "link.py").unlink()
    (public_vector / "link.py").symlink_to("../outside.py")
    with pytest.raises(ValueError, match="escapes"):
        state.public_workspace_sha256(public_vector)
