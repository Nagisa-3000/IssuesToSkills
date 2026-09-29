#!/usr/bin/env python3
"""Merge admitted episode arrays from independently audited Codex runs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def episode_key(episode: dict[str, Any]) -> tuple[str, int, str]:
    metadata = episode.get("metadata") or {}
    repository = str(episode.get("repository") or metadata.get("repository") or "")
    issue = int(metadata.get("issue") or 0)
    return repository, issue, str(episode.get("episode_id") or "")


def parse_case_key(value: str) -> tuple[str, int]:
    repository, separator, issue = value.rpartition("#")
    if not separator or not repository or not issue.isdigit():
        raise argparse.ArgumentTypeError(f"case key must look like OWNER/REPO#ISSUE, got {value!r}")
    return repository, int(issue)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exclude", type=parse_case_key, action="append", default=[])
    args = parser.parse_args()

    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    excluded = set(args.exclude)
    sources: list[str] = []
    for path in args.episodes:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError(f"{path} must contain a JSON array")
        sources.append(str(path))
        for episode in raw:
            if not isinstance(episode, dict):
                continue
            repository, issue, _ = episode_key(episode)
            key = (repository, issue)
            if key in excluded:
                continue
            if key in seen:
                raise ValueError(f"duplicate repository/issue episode: {repository}#{issue}")
            seen.add(key)
            merged.append(episode)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"episodes": len(merged), "sources": sources, "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
