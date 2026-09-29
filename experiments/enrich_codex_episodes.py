#!/usr/bin/env python3
"""Attach non-semantic manifest metadata to extracted Codex episodes.

The Codex extractor intentionally records only evidence-backed episode content.
This utility joins category/split metadata by repository+issue for evaluation
bookkeeping; it does not invent skills or alter evidence claims.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def enrich(episodes: list[dict[str, Any]], manifest: list[dict[str, Any]], *, split: str | None = None) -> list[dict[str, Any]]:
    by_key = {(str(item["repository"]), int(item["issue"])): item for item in manifest}
    result: list[dict[str, Any]] = []
    for episode in episodes:
        value = dict(episode)
        metadata = dict(value.get("metadata") or {})
        key = (str(value.get("repository")), int(metadata.get("issue", 0)))
        source = by_key.get(key)
        if source is None:
            raise ValueError(f"no manifest case for episode {key}")
        metadata["manifest_metadata"] = {
            field: source[field]
            for field in ("category", "theme", "module_families", "file_sample", "quality", "split", "split_group", "held_out_repository")
            if field in source
        }
        value["metadata"] = metadata
        if "category" in source:
            value["category"] = source["category"]
        if "theme" in source:
            value["theme"] = source["theme"]
        if split is not None:
            value["split"] = split
        result.append(value)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split")
    args = parser.parse_args()
    episodes = json.loads(args.episodes.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if isinstance(manifest, dict) and isinstance(manifest.get("cases"), list):
        manifest = manifest["cases"]
    if not isinstance(episodes, list) or not isinstance(manifest, list):
        raise ValueError("episodes and manifest must be JSON arrays")
    output = enrich(episodes, manifest, split=args.split)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"episodes": len(output), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
