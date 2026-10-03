#!/usr/bin/env python3
"""Replay a small package->SQLite->retrieval->context->synthetic-oracle experiment.

The current session supplies the recorded applicability decision and repair.
Replay uses no model endpoint, new agent session, original holdout, or credentials.
This is a smoke experiment, not an independent measure of agent improvement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from materialize_universal_resolution_graph import materialize

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.skill_packages import hydrate_package, validate_package
from arex_skill_graph.store import CatalogStore


def oracle(functional: Path, filename: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(functional / "test_endpoint_options.py"),
            "--module",
            str(functional / filename),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    report = json.loads(result.stdout)
    report["exit_code"] = result.returncode
    return report


def run(pilot: Path, selected_skill_id: str) -> dict:
    graph = json.loads((pilot / "training-graph.json").read_text(encoding="utf-8"))
    packages = []
    for workflow in graph["workflows"]:
        hydrated = hydrate_package(workflow)
        packages.append({key: value for key, value in hydrated.items() if key != "rendered"})
        assert not validate_package(Path(hydrated["package_path"]))
        verifier = subprocess.run(
            [sys.executable, str(Path(hydrated["package_path"]) / "scripts/verify_package.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        if verifier.returncode:
            raise ValueError("standalone package verifier failed")
    query = "Safely route custom endpoints through a multi-provider SDK boundary"
    with (
        tempfile.TemporaryDirectory(prefix="arex-package-smoke-") as temporary,
        CatalogStore(Path(temporary) / "catalog.sqlite") as store,
    ):
        store.initialize()
        counts = materialize(graph, store)
        hits = SkillRetriever(store).search(query, top_k=4, require_skill_package=True).hits
        selected = next(hit for hit in hits if hit.node.id == selected_skill_id)
        context = hydrate_package({**selected.node.payload, "id": selected.node.id})
        retrieval = [
            {
                "skill_id": hit.node.id,
                "title": hit.node.title,
                "sources": sorted(hit.sources),
                "trace": list(hit.trace),
            }
            for hit in hits
        ]
    before = oracle(pilot / "functional", "endpoint_before.py")
    after = oracle(pilot / "functional", "endpoint_after.py")
    if before["success"] or not after["success"]:
        raise ValueError(
            "synthetic functional oracle did not distinguish broken and repaired clients"
        )
    identifiers = set()
    manifests = [
        ROOT / "experiments/manifests" / category / "holdouts.json"
        for category in (
            "agent-core-seven-category-extraction-v2",
            "agent-core-thirteen-category-extraction-v2",
        )
    ]
    holdout_count = 0
    for path in manifests:
        raw = json.loads(path.read_text(encoding="utf-8"))
        cases = raw.get("cases", []) if isinstance(raw, dict) else raw
        holdout_count += len(cases)
        for case in cases:
            identifiers.update(
                str(case[field]) for field in ("case_id", "issue_url") if case.get(field)
            )
    leaked_files = []
    for package in packages:
        for path in Path(package["package_path"]).rglob("*"):
            if path.is_file() and any(
                value in path.read_text(encoding="utf-8") for value in identifiers
            ):
                leaked_files.append(str(path.relative_to(ROOT)))
    if leaked_files:
        raise ValueError("holdout identifier leaked into package content")
    return {
        "schema_version": "skill-package-smoke-v1",
        "scope": "two-training-workflow-package-smoke",
        "compiler_packages": len(packages),
        "package_validation_pass": len(packages),
        "hydrated_action_count": sum(len(package["hydrated_action_ids"]) for package in packages),
        "packages": packages,
        "catalog_materialized": counts,
        "retrieval": retrieval,
        "selected_skill_id": selected_skill_id,
        "context_sha256": hashlib.sha256(context["rendered"].encode()).hexdigest(),
        "context_characters": len(context["rendered"]),
        "applicability": {
            "decision": "applicable",
            "judged_by": "current Codex session; recorded decision replay",
            "rationale": "The synthetic task has competing endpoint sources, declared provider modes, "
            "a constructor observation seam, and the same resolve/guard/adapt boundary.",
            "negative_probes": [
                {
                    "task": "A single-provider SDK already owns endpoint resolution.",
                    "decision": "not_applicable",
                },
                {
                    "task": "The SDK constructor cannot be observed and no oracle is available.",
                    "decision": "defer",
                },
            ],
        },
        "functional": {
            "before": before,
            "after_current_session_skill_guided_repair": after,
            "kind": "synthetic constructor-boundary oracle",
            "independent_agent_benchmark": False,
        },
        "holdout": {
            "metadata_records_audited": holdout_count,
            "identifier_leaks": len(leaked_files),
            "solution_loaded": False,
            "used_for_skill_generation": False,
        },
        "promoted_packages": 0,
        "pattern_packages": 0,
        "activation_eval_suites": "definitions validated; no independent behavioral activation run",
        "limitations": [
            "No causal no-skill/guided comparison was run.",
            "The source repositories' original tests and live SDKs were not executed.",
            "Legacy Pattern package migration and corpus-scale backfill were outside this small experiment.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pilot",
        type=Path,
        default=ROOT / "data/skill-extraction/package-materialization-pilot-v1",
    )
    parser.add_argument("--skill-id", default="workflow:a1416952c048b7d5")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run(args.pilot, args.skill_id)
    output = args.output or args.pilot / "pilot-report.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "report": str(output),
                "packages": report["compiler_packages"],
                "before_passed": report["functional"]["before"]["passed"],
                "after_passed": report["functional"]["after_current_session_skill_guided_repair"][
                    "passed"
                ],
                "holdout_leaks": report["holdout"]["identifier_leaks"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
