#!/usr/bin/env python3
"""Run npm/pnpm through the local Node runtime used by holdout evaluation.

The evaluation workspaces live in WSL, while this host exposes Node through a
Windows installation.  Keeping this adapter outside the synthetic worktree
lets the same case command work for both environments without copying a host
``node_modules`` tree into the agent snapshot.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


def _windows_path(path: Path) -> str:
    try:
        return subprocess.run(["wslpath", "-w", str(path)], text=True, capture_output=True, check=True).stdout.strip() or str(path)
    except (OSError, subprocess.CalledProcessError):
        return str(path)


def _node() -> tuple[str, bool]:
    configured = os.environ.get("HOLDOUT_NODE")
    candidates = [Path(configured)] if configured else []
    candidates += [
        Path("/usr/bin/node"),
        Path("/mnt/c/Users/W/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"),
        Path("/mnt/e/Node/node.exe"),
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return str(candidate), candidate.suffix.lower() == ".exe"
    found = shutil.which("node")
    if found:
        return found, Path(found).suffix.lower() == ".exe"
    raise SystemExit("holdout Node runtime not found")


def _cli(tool: str, windows: bool) -> str:
    if tool == "npm":
        candidates = [Path("/mnt/e/Node/node_modules/npm/bin/npm-cli.js"), Path("/mnt/c/Users/W/AppData/Roaming/npm/node_modules/npm/bin/npm-cli.js")]
    elif tool == "pnpm":
        candidates = [Path("/mnt/c/Users/W/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pnpm/bin/pnpm.mjs")]
    else:
        raise SystemExit(f"unsupported node tool: {tool}")
    for candidate in candidates:
        if candidate.exists():
            return _windows_path(candidate) if windows else str(candidate)
    raise SystemExit(f"{tool} CLI not found")


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: run_holdout_node_tool.py npm|pnpm [args ...]")
    tool = sys.argv[1]
    node, windows = _node()
    command = [node, _cli(tool, windows), *sys.argv[2:]]
    return subprocess.run(command, cwd=os.getcwd(), env=os.environ.copy()).returncode


if __name__ == "__main__":
    raise SystemExit(main())
