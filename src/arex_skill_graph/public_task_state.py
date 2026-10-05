"""Retain actual solver bytes and a public base identity without promoting facts."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path

from .action_contracts import digest
from .git_tree_export import exact_git_tar
from .public_snapshot import extract_public_archive, initialize_public_base
from .task_context import EvidenceAnchor
from .workspace_state import (
    copy_sealed_public_workspace,
    public_workspace_execution_sha256,
    public_workspace_sha256,
)


def public_state_destination(destination, *source_roots):
    """Require a new output outside every source being verified or copied."""
    destination = Path(destination).absolute()
    if os.path.lexists(destination):
        raise ValueError("retained public state must use a new, nonexisting directory")
    destination = destination.resolve()
    for source in source_roots:
        source = Path(source).resolve()
        if destination.is_relative_to(source) or source.is_relative_to(destination):
            raise ValueError("retained public state must not overlap its source")
    return destination


def retain_public_task_state(current, input_task, destination):
    """Export produced public state, with exactly one pinned base commit.

    This is a byte/mode handoff for independent review and subsequent Actions.
    It does not review observations or establish successful execution or repair.
    Failed solver attempts may also be retained as unreviewed evidence.
    """
    destination = public_state_destination(destination, current.root, input_task.root)
    if (current.task_id, current.repository, current.base_commit) != (
        input_task.task_id, input_task.repository, input_task.base_commit
    ):
        raise ValueError("retained state changed its authenticated input identity")
    input_task.verify()
    current.verify(verify_head=False)
    content_seal = public_workspace_sha256(current.root)
    execution_seal = public_workspace_execution_sha256(current.root)
    git = ["git", "-C", input_task.root]
    raw_commit = subprocess.check_output([*git, "cat-file", "commit", input_task.base_commit])
    tree = subprocess.check_output(
        [*git, "rev-parse", input_task.base_commit + "^{tree}"], text=True
    ).strip()
    archive = exact_git_tar(git, input_task.base_commit)
    with tempfile.TemporaryDirectory(prefix="arex-retained-base-") as scratch:
        base = Path(scratch) / "base"
        base.mkdir()
        extract_public_archive(archive, base)
        initialize_public_base(base, input_task.base_commit, raw_commit, tree)
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy_sealed_public_workspace(current.root, destination, execution_seal)
        # Import freshly generated base metadata only, never source Git history.
        shutil.move(str(base / ".git"), str(destination / ".git"))

    anchors = []
    existing_ids = {a.id for a in current.anchors}
    for kind, sha, suffix in (
        ("workspace_snapshot", content_seal, "content"),
        ("workspace_execution_snapshot", execution_seal, "execution"),
    ):
        if not any(a.kind == kind for a in current.anchors):
            anchor_id = "retained:public-state:" + suffix
            if anchor_id in existing_ids:
                raise ValueError("retained state evidence identity conflicts")
            anchors.append(EvidenceAnchor(
                anchor_id, kind,
                "Actual final public state retained for independent review; no semantic acceptance.",
                current.base_commit, sha256=sha,
            ))
    retained = replace(current, root=str(destination)).update(anchors=tuple(anchors))
    retained.verify()
    if (public_workspace_sha256(destination) != content_seal
            or public_workspace_execution_sha256(destination) != execution_seal):
        raise ValueError("retained public state changed during identity preparation")
    audit = {
        "schema": "arex-retained-public-task-state-v1",
        "task_id": current.task_id,
        "base_commit": current.base_commit,
        "root": str(destination),
        "input_task_sha256": digest(input_task.to_dict()),
        "final_task_sha256": digest(retained.to_dict()),
        "workspace_sha256": content_seal,
        "workspace_execution_sha256": execution_seal,
        "git_identity": "exactly_one_shallow_public_base_commit",
        "source_git_history_copied": False,
        "semantic_facts_promoted": [],
        "semantic_checks_promoted": [],
        "repair_success_established": False,
        "review_status": "unreviewed_state_handoff",
    }
    return retained, audit
