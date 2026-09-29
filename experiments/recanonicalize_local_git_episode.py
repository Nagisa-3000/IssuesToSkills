#!/usr/bin/env python3
"""Rebuild one canonical episode with a truthful local-git evidence bundle.

This is used when a closed issue is resolved by a commit reference rather than
by a merged pull request.  It keeps the strict admission gate intact: the
episode must still have a pinned commit, qualifying evidence, and semantic
Action/Workflow candidates.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.run_codex_issue_episode_extraction import (  # noqa: E402
    canonical_episode,
    local_issue_bundle,
    validate_response,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = document.get("cases", []) if isinstance(document, dict) else document
    if not isinstance(cases, list) or len(cases) != 1:
        raise ValueError("manifest must contain exactly one case")
    case = dict(cases[0])
    response = json.loads(args.response.read_text(encoding="utf-8"))
    valid, errors = validate_response(response)
    if not valid:
        raise ValueError("raw response failed validation: " + "; ".join(errors))
    bundle = local_issue_bundle(case)
    episode = canonical_episode(response, bundle, case)
    episode.setdefault("metadata", {})["raw_codex_response"] = str(args.response)
    episode["metadata"]["response_validation"] = {"valid": valid, "errors": errors}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps([episode], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "episode_id": episode["episode_id"],
        "repository": episode["repository"],
        "issue": episode["metadata"]["issue"],
        "resolved_commit": bundle["resolved_commit"],
        "evidence_units": len(response["evidence_units"]),
        "candidate_atomics": len(response["candidate_atomics"]),
        "candidate_workflows": len(response["candidate_workflows"]),
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
