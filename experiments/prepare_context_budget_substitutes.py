#!/usr/bin/env python3
"""Route previously admitted budget episodes into the context-budget supplement.

This is an explicit provenance-preserving adapter.  It never changes an
episode's before/after/diff/evidence; it only changes the routing metadata used
by the training catalog and records that the episode is a substitute rather
than an exact row from the six-harness issue table.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
from typing import Any


DEFAULT_SELECTION = {
    ("Aider-AI/aider", 1842): "request-local budget isolation is a context/resource-boundary fix",
    ("NousResearch/hermes-agent", 125235): "compression threshold default and migration govern context-window budget",
    ("QwenLM/qwen-code", 12029): "deferred tool schema preload is explicitly bounded by session context budget",
    ("google-gemini/gemini-cli", 29080): "long-session history and continuation recovery are bounded at the model boundary",
}


def issue_key(episode: dict[str, Any]) -> tuple[str, int]:
    metadata = episode.get("metadata") if isinstance(episode.get("metadata"), dict) else {}
    issue = metadata.get("issue")
    if issue is None:
        match = re.search(r"#(\d+)", str(episode.get("episode_id") or ""))
        issue = int(match.group(1)) if match else 0
    return str(episode.get("repository") or ""), int(issue)


def normalize(episode: dict[str, Any], reason: str) -> dict[str, Any]:
    result = copy.deepcopy(episode)
    metadata = result.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
        result["metadata"] = metadata
    source_metadata = metadata.get("manifest_metadata")
    source_metadata = copy.deepcopy(source_metadata) if isinstance(source_metadata, dict) else {}
    source_category = str(source_metadata.get("category") or "")
    source_metadata.update({
        "category": "context-budget-and-compaction",
        "substitute_for": "context-budget-and-compaction",
        "source_category": source_category,
        "provenance": "accepted episode from universal extraction pilot; not an exact row of the six-harness issue table",
        "substitute_reason": reason,
    })
    metadata["manifest_metadata"] = source_metadata
    metadata["supplement_provenance"] = {
        "kind": "explicit-category-substitute",
        "target_category": "context-budget-and-compaction",
        "source_category": source_category,
        "reason": reason,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.source.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("source must contain a JSON array")
    by_key = {issue_key(item): item for item in raw if isinstance(item, dict)}
    missing = sorted(set(DEFAULT_SELECTION) - set(by_key))
    if missing:
        raise ValueError(f"selected substitute episodes are missing: {missing}")
    episodes = [normalize(by_key[key], reason) for key, reason in DEFAULT_SELECTION.items()]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "episodes": len(episodes), "category": "context-budget-and-compaction"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
