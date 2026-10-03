#!/usr/bin/env python3
"""Replay the frozen real direct extraction through indexes and context hydration.

This needs no model or credentials. It verifies delivery, portability and
retrieval, not functional repair or transfer on an unseen task.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from build_universal_resolution_graph import build
from materialize_universal_resolution_graph import materialize

from arex_skill_graph.direct_skill_extraction import parse_bundle, validate_graph_packages
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.skill_packages import hydrate_package, validate_package
from arex_skill_graph.store import CatalogStore

PILOT = ROOT / "data/skill-extraction/direct-skill-pilot-20261003"


def run(output: Path) -> dict:
    extraction = PILOT / "extraction-staged/01-provider-interface-adaptation"
    manifest = json.loads((PILOT / "staged-manifest.json").read_text())
    episodes = json.loads((extraction / "episodes.json").read_text())
    raw_path = extraction / "google-gemini__gemini-cli__25357/codex-response.skill.md"
    authored, deferred = parse_bundle(raw_path.read_bytes().decode("utf-8"))
    if deferred or len(episodes) != 1:
        raise ValueError("frozen pilot must contain one successful direct extraction")
    if any(key.startswith("candidate_") for key in episodes[0]["metadata"]):
        raise ValueError("direct extraction unexpectedly depends on candidate JSON")
    graph = build(episodes, manifest)
    admission = validate_graph_packages(graph, episodes)
    if not admission["extraction_success"]:
        raise ValueError("frozen package admission failed")
    preserved, portable, snapshots = 0, [], {}
    for reference in admission["packages"]:
        hydrated = hydrate_package({"id": reference["skill_id"], "skill_package": reference})
        root = Path(hydrated["package_path"])
        for relative, text in authored[root.name].items():
            if (root / relative).read_bytes() != text.encode("utf-8"):
                raise ValueError("model-authored file was rewritten")
            preserved += 1
        snapshots.update({path: path.read_bytes() for path in root.rglob("*") if path.is_file()})
        with tempfile.TemporaryDirectory(prefix="arex-portable-skill-") as temporary:
            copied = Path(temporary) / root.name
            shutil.copytree(root, copied)
            if validate_package(copied):
                raise ValueError("copied standalone package is invalid")
            result = subprocess.run(
                [sys.executable, str(copied / "scripts/verify_package.py")],
                capture_output=True,
                text=True,
                check=True,
            )
            relocated = {**reference, "package_path": str(copied)}
            loaded = hydrate_package({"id": relocated["skill_id"], "skill_package": relocated})
            portable.append(
                {
                    "skill_id": loaded["skill_id"],
                    "package_sha256": loaded["package_sha256"],
                    "standalone_verifier": result.stdout.strip(),
                    "hydrated_actions": len(loaded["hydrated_action_ids"]),
                    "context_characters": len(loaded["rendered"]),
                }
            )
    output.mkdir(parents=True, exist_ok=True)
    with CatalogStore(output / "catalog.sqlite") as store:
        store.initialize()
        counts = materialize(graph, store)
        index = output / "catalog.hnsw"
        store.build_hnsw_index(index)
        retrieval = {}
        query = "provider SDK endpoint override authentication route and default mode"
        for backend in ("exact", "hnsw"):
            response = SkillRetriever(store).search(
                query,
                vector_backend=backend,
                hnsw_path=str(index),
                require_skill_package=True,
                include_inactive=False,
            )
            ids = [hit.node.id for hit in response.hits]
            if set(ids) != {row["skill_id"] for row in admission["packages"]}:
                raise ValueError("retrieval did not return the package-backed Workflow")
            for hit in response.hits:
                hydrate_package(hit.node.payload)
            retrieval[backend] = {
                "skill_ids": ids,
                "seed_count": response.seed_count,
                "expanded_count": response.expanded_count,
            }
    if any(path.read_bytes() != before for path, before in snapshots.items()):
        raise ValueError("index rebuilding modified authoritative Skill files")
    report = {
        "schema_version": "direct-skill-smoke-v1",
        "fresh_model_extraction": False,
        "replays_frozen_real_extraction": True,
        "model": "openai/gpt-6.1-sol",
        "source_ref": episodes[0]["revision"],
        "materialized_skill_packages": len(admission["packages"]),
        "authored_files_preserved_verbatim": preserved,
        "index_rebuild_preserves_skill_files": True,
        "materialized": counts,
        "portable_packages": portable,
        "retrieval": retrieval,
        "functional_evals_executed": False,
        "holdout_solution_loaded": False,
        "scope": "real Skill file delivery, structural admission, portability and retrieval; no repair-rate claim",
    }
    (output / "verification-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PILOT / "verification")
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
