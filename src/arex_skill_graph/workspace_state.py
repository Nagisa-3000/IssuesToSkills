"""Public content and execution-state seals, excluding repository history."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def public_workspace_entries(root):
    root = Path(root).resolve()
    entries, size = {".": {"kind": "directory", "mode": root.stat().st_mode & 0o7777}}, 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if ".git" in Path(relative).parts:
            continue
        if path.is_symlink():
            target = path.readlink()
            if target.is_absolute() or not path.resolve().is_relative_to(root):
                raise ValueError("public workspace link escapes its content seal")
            entries[relative] = {"kind": "link", "target": str(target)}
        elif path.is_file():
            length = path.stat().st_size
            size += length
            if length > 16 * 1024**2 or size > 512 * 1024**2:
                raise ValueError("public workspace exceeds content-seal limits")
            entries[relative] = {
                "kind": "file",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "mode": path.stat().st_mode & 0o7777,
            }
        elif path.is_dir():
            entries[relative] = {"kind": "directory", "mode": path.stat().st_mode & 0o7777}
        else:
            raise ValueError("public workspace contains an unsupported file")
    return entries


def _sha256(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def public_workspace_sha256(root):
    # Preserve the original v2 content-seal definition for archived receipts.
    files = {}
    for name, entry in public_workspace_entries(root).items():
        if entry["kind"] == "link":
            files[name] = {"link": entry["target"]}
        elif entry["kind"] == "file":
            files[name] = entry["sha256"]
    return _sha256(files)


def public_workspace_execution_sha256(root):
    return _sha256(
        {
            "schema": "arex-public-workspace-execution-state-v1",
            "entries": public_workspace_entries(root),
        }
    )


def copy_verified_workspace_modes(source, destination):
    """Carry reviewed modes only across an identical, history-free base archive."""
    before = public_workspace_entries(source)
    after = public_workspace_entries(destination)

    def content(entries):
        return {
            name: {k: v for k, v in entry.items() if k != "mode"} for name, entry in entries.items()
        }

    if content(before) != content(after):
        raise ValueError("reviewed workspace content differs from the pinned base archive")
    destination = Path(destination)
    for name in sorted(before, key=lambda name: (name != ".", name.count("/")), reverse=True):
        if "mode" in before[name]:
            (destination / name).chmod(before[name]["mode"])
