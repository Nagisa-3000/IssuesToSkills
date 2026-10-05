"""Extract Git base archives while preserving contained repository symlinks."""

from __future__ import annotations

import io
import re
import subprocess
import tarfile
from pathlib import Path

from .skill_packages import _resolve


def _public_member_filter(member, destination):
    filtered = tarfile.data_filter(member, destination)
    if filtered is not None and member.issym():
        root = Path(destination).resolve()
        path = _resolve(root, member.name)
        target = Path(member.linkname)
        if target.is_absolute() or not (path.parent / target).resolve().is_relative_to(root):
            raise ValueError("public archive symlink escapes its repository")
        # data_filter normalizes linkname on recent Python versions. Git stores
        # the original target bytes, including meaningful trailing separators.
        return filtered.replace(linkname=member.linkname)
    return filtered


def extract_public_archive(raw, destination):
    destination = Path(destination).resolve()
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        for member in archive.getmembers():
            if (
                not (member.isfile() or member.isdir() or member.issym())
                or ".git" in Path(member.name).parts
            ):
                raise ValueError("public archive contains Git history or unsupported special files")
            path = _resolve(destination, member.name)
            if member.issym():
                target = Path(member.linkname)
                if target.is_absolute() or not (path.parent / target).resolve().is_relative_to(
                    destination
                ):
                    raise ValueError("public archive symlink escapes its repository")
        archive.extractall(destination, filter=_public_member_filter)
    # Recheck resolved chains after extraction, including links through links.
    for path in destination.rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(destination):
            raise ValueError("public archive symlink chain escapes its repository")


def initialize_public_base(checkout, base_commit, raw_commit, tree_id):
    """Import exactly one commit and its already-exported tree into a shallow repo."""
    checkout = Path(checkout)
    if not re.fullmatch(r"[0-9a-f]{40}", base_commit) or not re.fullmatch(r"[0-9a-f]{40}", tree_id):
        raise ValueError("public Git base and tree must be pinned")
    git = ["git", "-C", str(checkout)]
    subprocess.run(["git", "init", "-q", str(checkout)], check=True, capture_output=True)
    subprocess.run(
        [*git, "-c", "core.autocrlf=false", "add", "--force", "--all"],
        check=True,
        capture_output=True,
    )
    actual_tree = subprocess.check_output([*git, "write-tree"], text=True).strip()
    if actual_tree != tree_id:
        raise ValueError("public archive content/modes differ from the pinned Git tree")
    actual_commit = (
        subprocess.check_output(
            [*git, "hash-object", "-t", "commit", "-w", "--stdin"], input=raw_commit
        )
        .decode()
        .strip()
    )
    if actual_commit != base_commit:
        raise ValueError("exported public commit identity changed")
    (checkout / ".git/shallow").write_text(base_commit + "\n")
    subprocess.run(
        [*git, "update-ref", "refs/heads/public-base", base_commit], check=True, capture_output=True
    )
    subprocess.run(
        [*git, "symbolic-ref", "HEAD", "refs/heads/public-base"], check=True, capture_output=True
    )
    if subprocess.check_output([*git, "status", "--porcelain"], text=True).strip():
        raise ValueError("prepared public base is not clean")
