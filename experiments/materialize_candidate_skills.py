#!/usr/bin/env python3
"""Compile selected, validated training responses into real candidate Skill Packages.

No LLM call or holdout solution is needed. --check compares the deterministic
projection without writing packages. The original extraction corpus is immutable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from build_universal_resolution_graph import build
from run_codex_issue_episode_extraction import canonical_episode, validate_response

from arex_skill_graph.skill_packages import PACKAGE_ROOT, compile_workflow_graph


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", type=Path, action="append", required=True)
    parser.add_argument("--manifest", type=Path, required=True, help="training allowlist")
    parser.add_argument("--packages-root", type=Path, default=PACKAGE_ROOT / "candidates/workflows")
    parser.add_argument("--output", type=Path, help="new experiment artifacts directory")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    raw = json.loads(args.manifest.read_text(encoding="utf-8"))
    cases = raw.get("cases", []) if isinstance(raw, dict) else raw
    by_key = {(row["repository"], int(row["issue"])): row for row in cases}
    episodes = []
    sources = []
    selected_cases = []
    for case_dir in args.case_dir:
        raw_bundle = json.loads((case_dir / "issue-bundle.json").read_text(encoding="utf-8"))
        key = (raw_bundle["repository"], int(raw_bundle["issue_number"]))
        case = by_key[key]
        if (case.get("role") or case.get("split")) != "train_candidate" or case.get(
            "extraction_forbidden"
        ):
            raise ValueError("case is not allowlisted for training extraction")
        validation = json.loads((case_dir / "validation.json").read_text(encoding="utf-8"))
        response = json.loads((case_dir / "codex-response.json").read_text(encoding="utf-8"))
        valid, errors = validate_response(response)
        if validation.get("valid") is not True or not valid:
            raise ValueError(f"source response failed validation: {errors}")
        # Copy only public provenance, never issue bodies, credentials, command logs,
        # provider configuration, or transcripts into the experiment artifacts.
        bundle = {
            field: raw_bundle[field]
            for field in (
                "source",
                "repository",
                "issue_number",
                "resolved_commit",
                "parent_commit",
            )
            if field in raw_bundle
        }
        episode = canonical_episode(response, bundle, case)
        if bundle.get("resolved_commit"):
            episode["revision"] = bundle["resolved_commit"]
        episodes.append(episode)
        selected_cases.append(case)
        source = (case_dir / "codex-response.json").resolve()
        sources.append(
            str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source)
        )
    graph = build(episodes, {"cases": selected_cases})
    report = compile_workflow_graph(graph, episodes, args.packages_root, check=args.check)
    report["source_responses"] = sources
    report["training_episode_count"] = len(episodes)
    report["holdout_solution_loaded"] = False
    report["pattern_packages"] = 0
    report["pattern_policy"] = "structural Pattern IR is not a usable or promoted Skill"
    if args.output and not args.check:
        artifacts = {
            "package-materialization.json": report,
            "training-graph.json": graph,
            "training-episodes.json": episodes,
        }
        expected = {
            name: json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            for name, value in artifacts.items()
        }
        for name, content in expected.items():
            path = args.output / name
            if path.exists() and path.read_text(encoding="utf-8") != content:
                raise ValueError("experiment artifact differs; choose a new output directory")
        args.output.mkdir(parents=True, exist_ok=True)
        for name, content in expected.items():
            (args.output / name).write_text(content, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["extraction_success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
