#!/usr/bin/env python3
"""Admit Atomic/Workflow candidates already produced by the Codex evidence extractor.

This is a lower-cost companion to ``admit_codex_episodes.py``.  It does not
re-extract semantics from the episode: the evidence-backed candidate arrays in
each canonical episode are normalized into SkillRecords, then the normal LLM
same-level deduplication and cross-workflow Pattern extraction are applied.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.admission import BottomUpSkillAdmission, SkillCandidateRetriever
from arex_skill_graph.episodes import ChangeEpisode
from arex_skill_graph.lifecycle import LifecycleManager, SkillLevel, SkillRecord
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.store import CatalogStore


def slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text[:96] or "skill"


def load_episodes(path: Path) -> list[ChangeEpisode]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("episodes must be an array")
    return [ChangeEpisode.from_mapping(item) for item in raw]


def candidate_values(episode: ChangeEpisode, key: str) -> list[dict[str, Any]]:
    value = episode.metadata.get(key, []) if isinstance(episode.metadata, dict) else []
    return [dict(item) for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def category(episode: ChangeEpisode) -> str:
    if not isinstance(episode.metadata, dict):
        return ""
    manifest = episode.metadata.get("manifest_metadata") or {}
    return str(manifest.get("category") or manifest.get("theme") or "") if isinstance(manifest, dict) else ""


def atomic_records(episode: ChangeEpisode) -> tuple[SkillRecord, ...]:
    records: list[SkillRecord] = []
    seen: set[str] = set()
    for index, item in enumerate(candidate_values(episode, "candidate_atomics"), start=1):
        title = str(item.get("title") or item.get("name") or f"Atomic {index}").strip()
        summary = str(item.get("summary") or item.get("description") or "").strip()
        if not summary:
            continue
        base = slug(title)
        skill_id = f"{episode.episode_id}:atomic:{base}"
        suffix = 2
        while skill_id in seen:
            skill_id = f"{episode.episode_id}:atomic:{base}-{suffix}"
            suffix += 1
        seen.add(skill_id)
        evidence_ids = {f"{episode.episode_id}:{value}" for value in item.get("evidence_ids", episode.evidence_ids)}
        records.append(SkillRecord(skill_id=skill_id, level=SkillLevel.ATOMIC, title=title, summary=summary, evidence_ids=evidence_ids, preconditions=tuple(str(x) for x in item.get("preconditions", [])), exclusions=tuple(str(x) for x in item.get("exclusions", [])), failure_modes=tuple(str(x) for x in item.get("failure_modes", [])), payload={"source_episode_id": episode.episode_id, "repository": episode.repository, "category": category(episode), "candidate_source": "codex_episode_extractor"}))
    return tuple(records)


def workflow_records(episode: ChangeEpisode, atomics: Sequence[SkillRecord]) -> tuple[SkillRecord, ...]:
    by_name = {record.title: record.skill_id for record in atomics}
    records: list[SkillRecord] = []
    for index, item in enumerate(candidate_values(episode, "candidate_workflows"), start=1):
        title = str(item.get("title") or item.get("name") or f"Workflow {index}").strip()
        summary = str(item.get("summary") or item.get("description") or "").strip()
        if not summary:
            continue
        names = [str(x) for x in item.get("atomic_names", [])]
        atomic_ids = [by_name[name] for name in names if name in by_name] or [record.skill_id for record in atomics]
        evidence_ids = {f"{episode.episode_id}:{value}" for value in item.get("evidence_ids", episode.evidence_ids)}
        records.append(SkillRecord(skill_id=f"{episode.episode_id}:workflow:{slug(title)}", level=SkillLevel.WORKFLOW, title=title, summary=summary, evidence_ids=evidence_ids, payload={"atomic_ids": atomic_ids, "source_episode_id": episode.episode_id, "repository": episode.repository, "category": category(episode), "candidate_source": "codex_episode_extractor"}))
    return tuple(records)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--judge-k", type=int, default=1)
    parser.add_argument("--hnsw-path", type=Path)
    args = parser.parse_args()
    if not args.api_key:
        raise ValueError("--api-key or OPENAI_API_KEY is required")
    episodes = load_episodes(args.episodes)
    args.output.mkdir(parents=True, exist_ok=True)
    transport = OpenAICompatibleTransport(OpenAICompatibleConfig(api_key=args.api_key, base_url=args.base_url, model=args.model, timeout_seconds=240, max_output_tokens=7000, retries=2))
    governance = LLMGovernanceAdapter(transport, GovernanceContext(repository="cross-project-training-only", model=args.model, prompt_version="preextracted-candidate-admission-v1"))
    manager = LifecycleManager()
    with CatalogStore(args.output / "skill-catalog.sqlite") as store:
        store.initialize()
        admission = BottomUpSkillAdmission(manager, SkillCandidateRetriever(store), judge=governance.judge, judge_k=args.judge_k)
        episode_results, pattern_results = admission.insert_episodes(episodes, atomic_extractor=atomic_records, workflow_extractor=workflow_records, pattern_extractor=governance.extract_patterns_from_workflows)
        if args.hnsw_path:
            store.build_hnsw_index(args.hnsw_path, embedding_kind="routing", model_version="hash-v1")
        retriever = SkillRetriever(store)
        retrieval = []
        for episode in episodes:
            response = retriever.search(episode.title, top_k=8, seed_k=32, expand_hops=2, query_mode="solve", vector_backend="exact", include_inactive=False)
            retrieval.append({"episode_id": episode.episode_id, "category": category(episode), "hits": [{"id": hit.node.id, "type": hit.node.node_type.value, "title": hit.node.title, "score": hit.score, "sources": dict(hit.sources), "trace": list(hit.trace)} for hit in response.hits], "seed_count": response.seed_count, "expanded_count": response.expanded_count})
        summary = {"source": "codex_preextracted_candidates", "episodes_input": len(episodes), "episode_results": [{"episode_id": row.episode_id, "atomics": [item.resolved_id for item in row.atomics], "workflows": [item.resolved_id for item in row.workflows]} for row in episode_results], "patterns": [item.resolved_id for item in pattern_results], "nodes": len(manager.skills), "active_nodes": sum(item.status.value == "active" for item in manager.skills.values()), "relations": len(manager.relations), "dedup_proposals": len(manager.dedup_proposals), "llm_calls": len(transport.calls)}
        (args.output / "admission-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "skill-records.json").write_text(json.dumps([item.to_json() for item in manager.skills.values()], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "retrieval-evaluation.json").write_text(json.dumps(retrieval, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "transport-calls.json").write_text(json.dumps(transport.calls, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "llm-transcript.json").write_text(json.dumps(transport.transcripts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.output), **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
