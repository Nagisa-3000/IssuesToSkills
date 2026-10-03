#!/usr/bin/env python3
"""Build one training-only Action -> Workflow -> Pattern catalog.

The extractor and LLM admission stages remain separate.  This command is the
post-admission system boundary: it combines canonical episodes from multiple
categories, rejects holdout episodes through the manifest gate, builds the
structural graph, audits Action reuse/granularity, and materializes one SQLite
plus optional HNSW retrieval environment.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(ROOT / "src"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GRAPH = load_module("agent_core_graph_builder", EXPERIMENTS / "build_universal_resolution_graph.py")
MATERIALIZER = load_module("agent_core_graph_materializer", EXPERIMENTS / "materialize_universal_resolution_graph.py")
FACTOR = load_module("agent_core_factorization_audit", EXPERIMENTS / "audit_action_factorization.py")


def load_json_array(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"{path} must contain a JSON array of canonical episodes")
    return [dict(item) for item in raw if isinstance(item, dict)]


def issue_key(episode: dict[str, Any]) -> tuple[str, int]:
    metadata = episode.get("metadata") if isinstance(episode.get("metadata"), dict) else {}
    issue = metadata.get("issue")
    if issue is None:
        episode_id = str(episode.get("episode_id") or "")
        import re
        match = re.search(r"#(\d+)", episode_id)
        issue = int(match.group(1)) if match else 0
    return str(episode.get("repository") or ""), int(issue)


def training_only(episodes: list[dict[str, Any]], manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cases = manifest.get("cases", []) if isinstance(manifest, dict) else []
    roles = {(str(item.get("repository")), int(item.get("issue"))): str(item.get("role") or item.get("split") or "") for item in cases if isinstance(item, dict) and item.get("issue") is not None}
    accepted: list[dict[str, Any]] = []
    refused: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for episode in episodes:
        key = issue_key(episode)
        role = roles.get(key, "")
        if role != "train_candidate":
            refused.append({"episode_id": episode.get("episode_id"), "key": key, "reason": "episode is not a train_candidate in the manifest"})
            continue
        if key in seen:
            refused.append({"episode_id": episode.get("episode_id"), "key": key, "reason": "duplicate training episode key"})
            continue
        seen.add(key)
        accepted.append(episode)
    return accepted, refused


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--episodes", type=Path, nargs="+", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-pattern-support", type=int, default=2)
    parser.add_argument("--build-hnsw", action="store_true")
    parser.add_argument("--allow-structured-ir", action="store_true",
                        help="audit historical graph IR; does not produce serving Skills")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be an object")
    input_episodes: list[dict[str, Any]] = []
    for path in args.episodes:
        input_episodes.extend(load_json_array(path))
    episodes, refused = training_only(input_episodes, manifest)
    graph = GRAPH.build(episodes, manifest, min_pattern_support=max(2, args.min_pattern_support))
    graph["rejected"].extend(refused)
    graph["summary"]["preflight_refused"] = len(refused)
    graph["summary"]["episodes_used"] = len(episodes)
    package_report = {"status": "structured_only", "materialized_skill_packages": 0}
    if not args.allow_structured_ir:
        from arex_skill_graph.skill_packages import PACKAGE_ROOT, compile_workflow_graph

        package_report = compile_workflow_graph(graph, episodes, PACKAGE_ROOT / "candidates/workflows")
        if not package_report["extraction_success"]:
            raise ValueError(f"catalog Skill admission failed: {package_report['failures']}")
    audit = FACTOR.audit(graph)
    fragments = []
    for index, row in enumerate(audit.get("workflow_role_segments", [])):
        fragment = dict(row)
        fragment["id"] = f"workflow-fragment:{index + 1:03d}:" + "->".join(str(role) for role in row.get("segment_roles", []))
        fragment["node_type"] = "workflow_fragment"
        fragments.append(fragment)
    graph["workflow_fragments"] = fragments

    args.output_dir.mkdir(parents=True, exist_ok=True)
    graph_path = args.output_dir / "training-graph.json"
    audit_path = args.output_dir / "action-factorization-audit.json"
    episodes_path = args.output_dir / "training-episodes.json"
    db_path = args.output_dir / "catalog.sqlite"
    hnsw_path = args.output_dir / "catalog.hnsw"
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit["workflow_fragment_ids"] = [fragment["id"] for fragment in fragments]
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    episodes_path.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from arex_skill_graph.store import CatalogStore

    with CatalogStore(db_path) as store:
        store.initialize()
        counts = MATERIALIZER.materialize(graph, store)
        hnsw_status = "not-requested"
        if args.build_hnsw:
            try:
                store.build_hnsw_index(hnsw_path)
                hnsw_status = "built"
            except Exception as exc:  # optional dependency is environment-specific
                hnsw_status = f"unavailable: {type(exc).__name__}: {exc}"
        stats = store.stats()

    report = {
        "schema_version": "agent-core-catalog-build-v1",
        "manifest": str(args.manifest),
        "episode_sources": [str(path) for path in args.episodes],
        "training_only": True,
        "skill_packages": package_report,
        "holdout_loaded": False,
        "input_episodes": len(input_episodes),
        "training_episodes": len(episodes),
        "preflight_refused": len(refused),
        "graph_summary": graph.get("summary", {}),
        "factorization_summary": audit.get("summary", {}),
        "materialized": counts,
        "catalog": {"sqlite": str(db_path), "hnsw": str(hnsw_path) if args.build_hnsw else None, "hnsw_status": hnsw_status, "stats": stats},
        "artifacts": {"graph": str(graph_path), "factorization_audit": str(audit_path), "training_episodes": str(episodes_path)},
    }
    (args.output_dir / "catalog-build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
