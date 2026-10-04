"""Content seals of the public workspace, excluding repository history."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def public_workspace_sha256(root):
    root = Path(root).resolve()
    files, size = {}, 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if ".git" in Path(relative).parts:
            continue
        if path.is_symlink():
            target = path.readlink()
            if target.is_absolute() or not path.resolve().is_relative_to(root):
                raise ValueError("public workspace link escapes its content seal")
            files[relative] = {"link": str(target)}
        elif path.is_file():
            length = path.stat().st_size
            size += length
            if length > 16 * 1024**2 or size > 512 * 1024**2:
                raise ValueError("public workspace exceeds content-seal limits")
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise ValueError("public workspace contains an unsupported file")
    return hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
