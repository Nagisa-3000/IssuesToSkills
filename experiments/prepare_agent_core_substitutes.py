#!/usr/bin/env python3
"""Route already-admitted episodes into explicit agent-core category supplements."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
from typing import Any


SELECTIONS = {
    ("NousResearch/hermes-agent", 123989): {
        "target_category": "effect-control-and-isolation",
        "reason": "profile-qualified sandbox/session identity prevents cross-profile effect leakage",
    },
    ("QwenLM/qwen-code", 12683): {
        "target_category": "structured-tool-contract-integrity",
        "reason": "structured permission aggregation applies a stable restrictive decision order",
    },
    ("google-gemini/gemini-cli", 28339): {
        "target_category": "failure-recovery-and-streaming",
        "reason": "retry classification distinguishes terminal capacity exhaustion from retryable transport recovery",
    },
    ("QwenLM/qwen-code", 12047): {
        "target_category": "state-continuity-and-resume",
        "reason": "session-owned cached token state survives route adoption and resume",
    },
}


def issue_key(episode: dict[str, Any]) -> tuple[str, int]:
    metadata = episode.get("metadata") if isinstance(episode.get("metadata"), dict) else {}
    issue = metadata.get("issue")
    if issue is None:
        match = re.search(r"#(\d+)", str(episode.get("episode_id") or ""))
        issue = int(match.group(1)) if match else 0
    return str(episode.get("repository") or ""), int(issue)


def normalize(episode: dict[str, Any], selection: dict[str, str]) -> dict[str, Any]:
    result = copy.deepcopy(episode)
    metadata = result.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
        result["metadata"] = metadata
    source_metadata = metadata.get("manifest_metadata")
    source_metadata = copy.deepcopy(source_metadata) if isinstance(source_metadata, dict) else {}
    source_category = str(source_metadata.get("category") or "")
    target_category = selection["target_category"]
    source_metadata.update({
        "category": target_category,
        "substitute_for": target_category,
        "source_category": source_category,
        "provenance": "previously admitted and verified episode; not an exact row of the six-harness issue table",
        "substitute_reason": selection["reason"],
    })
    metadata["manifest_metadata"] = source_metadata
    metadata["supplement_provenance"] = {
        "kind": "explicit-category-substitute",
        "target_category": target_category,
        "source_category": source_category,
        "reason": selection["reason"],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for path in args.source:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError(f"{path} must contain a JSON array")
        for item in raw:
            if isinstance(item, dict):
                by_key.setdefault(issue_key(item), item)
    missing = sorted(set(SELECTIONS) - set(by_key))
    if missing:
        raise ValueError(f"selected episodes are missing: {missing}")
    episodes = [normalize(by_key[key], selection) for key, selection in SELECTIONS.items()]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "episodes": len(episodes), "categories": sorted({item["target_category"] for item in SELECTIONS.values()})}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
