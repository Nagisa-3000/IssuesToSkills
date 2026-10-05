"""Exact public state handoff controls; these fixtures establish no SWE utility."""

import hashlib
import json
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_budget import BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.adaptive_runner import AdaptiveSolver, snapshot_base
from arex_skill_graph.public_task_state import retain_public_task_state
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.workflow_ranker import WorkflowRanker
from arex_skill_graph.workspace_state import public_workspace_entries
from test_action_observation_runner import FixtureTools


def changed_scratch(tmp_path):
    _package, source, policy = make_fixture(tmp_path)
    current = snapshot_base(source, tmp_path / "scratch")
    owner = Path(current.root, "checker.py")
    owner.write_text(owner.read_text().replace("return True", "return context == 'runtime'"))
    owner.chmod(0o640)
    Path(current.root, "observed.txt").write_text("Actual public observation\n")
    Path(current.root, "local-link").symlink_to("checker.py")
    anchor = next(a for a in current.anchors if a.path == "checker.py")
    current = current.update(anchors=(
        replace(anchor, sha256=hashlib.sha256(owner.read_bytes()).hexdigest()),
    ))
    current.verify(verify_head=False)
    return source, current, policy


def git(root, *args, **kwargs):
    return subprocess.check_output(["git", "-C", str(root), *args], **kwargs)


def test_retains_actual_modified_files_modes_links_and_only_pinned_base(tmp_path):
    source, current, _policy = changed_scratch(tmp_path)
    (retained, audit) = retain_public_task_state(current, source, tmp_path / "retained")
    assert public_workspace_entries(retained.root) == public_workspace_entries(current.root)
    assert retained.base_commit == source.base_commit
    assert retained.facts == current.facts
    assert retained.checks == current.checks
    assert retained.bindings == current.bindings
    assert retained.port_values == current.port_values
    assert retained.oracles == current.oracles
    assert not audit["semantic_facts_promoted"]
    assert not audit["semantic_checks_promoted"]
    assert not audit["repair_success_established"]
    assert git(retained.root, "rev-parse", "HEAD", text=True).strip() == source.base_commit
    assert git(retained.root, "rev-list", "--count", "HEAD", text=True).strip() == "1"
    assert not git(retained.root, "remote", text=True).strip()
    assert "checker.py" in git(retained.root, "diff", "--name-only", text=True)
    # A downstream Action receives the produced bytes rather than the historical base.
    resumed = snapshot_base(retained, tmp_path / "next-action", resume_reviewed_state=True)
    assert public_workspace_entries(resumed.root) == public_workspace_entries(current.root)
    TaskContext.from_dict(json.loads(json.dumps(retained.to_dict()))).verify()


def test_retention_never_imports_future_or_untracked_source_content(tmp_path):
    source, current, _policy = changed_scratch(tmp_path)
    (Path(source.root) / "future.txt").write_text("Future fixture content\n")
    git(source.root, "add", "--all")
    git(source.root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Future fixture")
    future = git(source.root, "rev-parse", "HEAD", text=True).strip()
    git(source.root, "checkout", "--detach", source.base_commit)
    (Path(source.root) / "untracked-source.txt").write_text("Excluded source file\n")
    retained, _audit = retain_public_task_state(current, source, tmp_path / "retained")
    assert not Path(retained.root, "future.txt").exists()
    assert not Path(retained.root, "untracked-source.txt").exists()
    missing = subprocess.run(
        ["git", "-C", retained.root, "cat-file", "-e", future], capture_output=True
    )
    assert missing.returncode != 0


@pytest.mark.parametrize("destination", ["existing", "dangling", "nested", "ancestor"])
def test_retention_rejects_overwrite_and_source_overlap(tmp_path, destination):
    source, current, _policy = changed_scratch(tmp_path)
    if destination == "existing":
        target = tmp_path / "existing"
        target.mkdir()
        (target / "keep.txt").write_text("Preserve this state\n")
    elif destination == "dangling":
        target = tmp_path / "dangling"
        target.symlink_to(tmp_path / "absent")
    elif destination == "nested":
        target = Path(current.root) / "retained"
    else:
        target = tmp_path
    before = public_workspace_entries(current.root)
    with pytest.raises(ValueError, match="nonexisting|overlap"):
        retain_public_task_state(current, source, target)
    assert public_workspace_entries(current.root) == before
    if destination == "existing":
        assert (target / "keep.txt").read_text() == "Preserve this state\n"


def test_retention_rejects_stale_current_state_without_creating_output(tmp_path):
    source, current, _policy = changed_scratch(tmp_path)
    Path(current.root, "checker.py").write_text("Changed without renewed anchor\n")
    with pytest.raises(ValueError, match="changed"):
        retain_public_task_state(current, source, tmp_path / "retained")
    assert not (tmp_path / "retained").exists()


def test_runner_retains_final_actual_task_after_termination_and_default_is_unchanged(tmp_path):
    _package, task, policy = make_fixture(tmp_path)
    original = Path(task.root, "checker.py").read_text()
    modified = original.replace("return True", "return context == 'runtime'")
    steps = [
        {"operation": "write_file", "arguments": {"path": "checker.py", "content": modified},
         "rationale": "Actual synthetic repair for handoff protocol."},
        {"operation": "finish", "arguments": {}, "rationale": "End fixture."},
    ]
    with CatalogStore(tmp_path / "store.sqlite") as store:
        store.initialize()
        solver = AdaptiveSolver(ReplayTransport(steps), WorkflowRanker(), store, policy,
                                BudgetLedger(), arm="B0", tools_factory=FixtureTools)
        result = solver.run(task, retain_public_state_dir=tmp_path / "retained")
        assert result["solver_ended"] and not result["failure"]
        retained = TaskContext.from_dict(result["final_public_task"])
        retained.verify()
        assert Path(retained.root, "checker.py").read_text() == modified
        assert Path(task.root, "checker.py").read_text() == original
        assert not result["public_state_retention"]["repair_success_established"]
        default = AdaptiveSolver(
            ReplayTransport([steps[-1]]), WorkflowRanker(), store, policy, BudgetLedger(),
            arm="B0", tools_factory=FixtureTools,
        ).run(task)
    assert "final_public_task" not in default
    assert "public_state_retention" not in default
