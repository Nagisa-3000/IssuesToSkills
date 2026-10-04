"""Rollback command changes outside a ready Action's current bound write set."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from .action_contracts import contained_resource
from .workspace_state import public_workspace_entries


def run_scoped_command(checkout, allowed_write_paths, invoke):
    checkout = Path(checkout).resolve()
    allowed = {contained_resource(p) for p in allowed_write_paths}
    before = public_workspace_entries(checkout)
    if any(".git" in p.relative_to(checkout).parts for p in checkout.rglob("*")):
        raise ValueError("scoped public commands cannot receive repository history")

    def permitted(name):
        return name in allowed or (
            name not in before
            and after.get(name, {}).get("kind") == "directory"
            and any(p.startswith(name + "/") for p in allowed)
        )

    with tempfile.TemporaryDirectory(prefix="arex-scoped-command-", dir=checkout.parent) as temp:
        temporary = Path(temp)
        backup = temporary / "before"
        shutil.copytree(checkout, backup, symlinks=True)

        def restore():
            rejected = temporary / "rejected"
            checkout.rename(rejected)
            try:
                backup.rename(checkout)
            except BaseException:
                rejected.rename(checkout)
                raise

        try:
            result = dict(invoke())
            try:
                after = public_workspace_entries(checkout)
                changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
                forbidden = sorted(p for p in changed if not permitted(p))
                invalid = any(".git" in p.relative_to(checkout).parts for p in checkout.rglob("*"))
            except (ValueError, OSError):
                changed, forbidden, invalid = set(), [], True
        except BaseException:
            restore()
            raise
        if forbidden or invalid:
            restore()
            result.update(
                process_exit_code=result.get("exit_code"),
                exit_code=125,
                workspace_adopted=False,
                workspace_rollback=True,
                write_scope_accepted=False,
                out_of_scope_paths=forbidden,
                denied="Command workspace changes exceeded the Action's current bound write set; the complete public workspace was restored.",
            )
        else:
            result.update(
                write_scope_accepted=True,
                bound_write_paths=sorted(allowed),
                workspace_changed_paths=sorted(changed),
            )
        return result
