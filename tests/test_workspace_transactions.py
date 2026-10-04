import os

import pytest

from arex_skill_graph.workspace_state import public_workspace_execution_sha256
from arex_skill_graph.workspace_transactions import run_scoped_command


def command(operation):
    def invoke():
        operation()
        return {"argv": ["fixture"], "exit_code": 0, "output": "Actual command result"}

    return invoke


def test_multi_file_command_retains_only_declared_changes(tmp_path):
    (tmp_path / "a.py").write_text("before")
    (tmp_path / "b.py").write_text("before")

    def edit():
        (tmp_path / "a.py").write_text("after a")
        (tmp_path / "b.py").write_text("after b")

    result = run_scoped_command(tmp_path, {"a.py", "b.py"}, command(edit))
    assert result["exit_code"] == 0 and result["write_scope_accepted"]
    assert result["workspace_changed_paths"] == ["a.py", "b.py"]
    assert (tmp_path / "a.py").read_text() == "after a"


@pytest.mark.parametrize(
    "outside", ["create", "delete", "content", "mode", "git", "escaped_link", "root_mode"]
)
def test_out_of_scope_change_rolls_back_entire_command(tmp_path, outside):
    (tmp_path / "allowed.py").write_text("original")
    other = tmp_path / "other.sh"
    other.write_text("#!/bin/sh\nexit 0\n")
    other.chmod(0o755)
    before = public_workspace_execution_sha256(tmp_path)

    def edit():
        (tmp_path / "allowed.py").write_text("unaccepted")
        if outside == "create":
            (tmp_path / "extra.py").write_text("new")
        elif outside == "delete":
            other.unlink()
        elif outside == "content":
            other.write_text("changed")
        elif outside == "mode":
            other.chmod(0o644)
        elif outside == "git":
            (tmp_path / ".git").mkdir()
        elif outside == "root_mode":
            tmp_path.chmod(0o755 if tmp_path.stat().st_mode & 0o7777 != 0o755 else 0o700)
        else:
            os.symlink("/etc/passwd", tmp_path / "escaped")

    result = run_scoped_command(tmp_path, {"allowed.py"}, command(edit))
    assert result["exit_code"] == 125 and result["process_exit_code"] == 0
    assert result["workspace_rollback"] and not result["write_scope_accepted"]
    assert public_workspace_execution_sha256(tmp_path) == before


def test_failing_command_keeps_its_valid_in_scope_edits(tmp_path):
    (tmp_path / "a.py").write_text("before")

    def edit():
        (tmp_path / "a.py").write_text("retained")
        return {"argv": ["fixture"], "exit_code": 1, "output": "Check failed"}

    result = run_scoped_command(tmp_path, {"a.py"}, edit)
    assert result["exit_code"] == 1 and result["write_scope_accepted"]
    assert (tmp_path / "a.py").read_text() == "retained"


def test_launcher_exception_restores_partial_edits(tmp_path):
    (tmp_path / "a.py").write_text("before")

    def edit():
        (tmp_path / "a.py").write_text("partial")
        raise RuntimeError("launcher failed")

    with pytest.raises(RuntimeError, match="launcher failed"):
        run_scoped_command(tmp_path, {"a.py"}, edit)
    assert (tmp_path / "a.py").read_text() == "before"


def test_new_parent_directory_can_support_a_declared_file(tmp_path):
    def edit():
        (tmp_path / "nested").mkdir()
        (tmp_path / "nested/a.py").write_text("allowed")

    result = run_scoped_command(tmp_path, {"nested/a.py"}, command(edit))
    assert result["write_scope_accepted"]
    assert result["workspace_changed_paths"] == ["nested", "nested/a.py"]


def test_existing_parent_permissions_are_outside_a_file_write_set(tmp_path):
    parent = tmp_path / "nested"
    parent.mkdir(mode=0o755)
    (parent / "a.py").write_text("original")
    before = public_workspace_execution_sha256(tmp_path)

    def edit():
        (parent / "a.py").write_text("rejected")
        parent.chmod(0o700)

    result = run_scoped_command(tmp_path, {"nested/a.py"}, command(edit))
    assert result["exit_code"] == 125
    assert result["out_of_scope_paths"] == ["nested"]
    assert public_workspace_execution_sha256(tmp_path) == before
