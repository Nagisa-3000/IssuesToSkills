#!/usr/bin/env python3
"""Prepare leakage-controlled agent cases from verified universal issues.

This adapter is intentionally conservative.  It emits a case only when a
holdout candidate has a concrete solution commit (from the manifest or an
evidence episode) and the local checkout can resolve it.  Unverified seed rows
are reported as blockers instead of being turned into synthetic tasks with a
made-up base or oracle.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.prepare_cross_project_holdout_cases import prepare_case


def load_cases(path: Path, role: str) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    cases = value.get("cases", []) if isinstance(value, dict) else value
    if not isinstance(cases, list):
        raise ValueError("manifest must contain a cases array")
    return [dict(item) for item in cases if str(item.get("role") or item.get("split")) == role]


def episode_refs(path: Path | None) -> dict[tuple[str, int], str]:
    if path is None:
        return {}
    values = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(values, list):
        raise ValueError("episodes must be an array")
    result: dict[tuple[str, int], str] = {}
    for episode in values:
        metadata = episode.get("metadata") or {}
        if not isinstance(metadata, dict):
            continue
        repository = str(episode.get("repository", ""))
        issue = int(metadata.get("issue", 0) or 0)
        bundle = metadata.get("github_bundle") or {}
        ref = str(bundle.get("resolved_commit") or "")
        if not ref:
            for linked in bundle.get("linked_pull_requests", []) if isinstance(bundle, dict) else []:
                pull = linked.get("pull_request", {}) if isinstance(linked, dict) else {}
                if pull.get("merged") and pull.get("merge_commit_sha"):
                    ref = str(pull["merge_commit_sha"])
                    break
        if repository and issue and ref:
            result[(repository, issue)] = ref
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--episodes", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--role", default="holdout_candidate", choices=("train_candidate", "holdout_candidate"))
    parser.add_argument("--max-test-paths", type=int, default=12)
    args = parser.parse_args()
    cases = load_cases(args.manifest, args.role)
    refs = episode_refs(args.episodes)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prepared: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    for case in cases:
        key = (str(case.get("repository", "")), int(case.get("issue", 0)))
        enriched = dict(case)
        # The HTML/PR enrichment pass records the selected merged resolution
        # as ``extraction_ref``.  It is safe for a holdout only when the PR
        # pass actually observed a merged PR; a merely referenced commit or a
        # closed/unmerged head must remain a blocker rather than becoming a
        # synthetic oracle.
        verification = case.get("verification") if isinstance(case.get("verification"), dict) else {}
        html_merged = bool(verification.get("html_merged_resolution"))
        enriched_ref = case.get("ref") or case.get("solution_ref")
        if not enriched_ref and html_merged:
            enriched_ref = case.get("extraction_ref")
        enriched["ref"] = str(enriched_ref or refs.get(key) or "")
        if not enriched["ref"]:
            blockers.append({"case_id": case.get("case_id"), "repository": key[0], "issue": key[1], "reason": "no verified solution commit"})
            continue
        try:
            prepared.append(prepare_case(enriched, output_dir=args.output_dir, max_test_paths=max(1, args.max_test_paths)))
        except Exception as exc:  # keep all blockers visible in one report
            blockers.append({"case_id": case.get("case_id"), "repository": key[0], "issue": key[1], "reason": f"{type(exc).__name__}: {exc}"})
    (args.output_dir / "case-manifest.json").write_text(json.dumps(prepared, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "schema_version": "universal-agent-case-readiness-v1",
        "role": args.role,
        "candidate_rows": len(cases),
        "prepared_cases": len(prepared),
        "blockers": blockers,
        "oracle_note": "A case with no focused visible test remains oracle-unqualified and must not enter the causal success denominator.",
    }
    (args.output_dir / "readiness-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_rows": len(cases), "prepared_cases": len(prepared), "blockers": len(blockers)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
