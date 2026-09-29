#!/usr/bin/env python3
"""Canonicalize one raw Codex response after independent response validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.run_codex_issue_episode_extraction import canonical_episode, validate_response


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--case-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    response = json.loads(args.response.read_text(encoding="utf-8"))
    valid, errors = validate_response(response)
    validation = {"valid": valid, "errors": errors, "response": str(args.response)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    validation_path = args.output.with_name(args.output.stem + "-validation.json")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not valid:
        raise ValueError("raw Codex response failed validation: " + "; ".join(errors))

    document = json.loads(args.case_manifest.read_text(encoding="utf-8"))
    cases = document.get("cases", []) if isinstance(document, dict) else document
    if not isinstance(cases, list) or len(cases) != 1:
        raise ValueError("case manifest must contain exactly one case")
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    episode = canonical_episode(response, bundle, dict(cases[0]))
    episode.setdefault("metadata", {})["raw_codex_response"] = str(args.response)
    episode["metadata"]["response_validation"] = validation
    args.output.write_text(json.dumps([episode], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "valid": True,
        "episode_id": episode["episode_id"],
        "repository": episode["repository"],
        "issue": episode["metadata"]["issue"],
        "evidence_units": len(response["evidence_units"]),
        "candidate_atomics": len(response["candidate_atomics"]),
        "candidate_workflows": len(response["candidate_workflows"]),
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
