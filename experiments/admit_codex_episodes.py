#!/usr/bin/env python3
"""Admit canonical episodes produced by the server Codex extraction runner.

This is the second, cost-visible stage: only episodes already admitted by the
strict extraction validator use package-derived Actions and Workflows, followed
by semantic adjudication. --legacy-json-reextract explicitly retains the old
semantic extraction experiment.
It never reads prepared evidence.md/case.json fixtures.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Iterable, Sequence
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from admit_preextracted_candidates import atomic_records, workflow_records

from arex_skill_graph.admission import BottomUpSkillAdmission, SkillCandidateRetriever
from arex_skill_graph.episodes import ChangeEpisode
from arex_skill_graph.lifecycle import LifecycleManager, SkillRecord
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.store import CatalogStore


def namespace_records(records: Iterable[SkillRecord], namespace: str) -> tuple[SkillRecord, ...]:
    values = tuple(records)
    old_to_new = {item.skill_id: f"{namespace}:{item.skill_id}" for item in values}
    result: list[SkillRecord] = []
    for item in values:
        payload = dict(item.payload)
        for key in ("atomic_ids", "workflow_ids"):
            if key in payload:
                payload[key] = [old_to_new.get(str(value), str(value)) for value in payload[key]]
        result.append(replace(item, skill_id=old_to_new[item.skill_id], payload=payload))
    return tuple(result)


def load_episodes(path: Path) -> tuple[ChangeEpisode, ...]:
    values = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(values, list):
        raise TypeError("episodes file must contain an array")
    return tuple(ChangeEpisode.from_mapping(item) for item in values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--legacy-json-reextract", action="store_true",
                        help="explicitly repeat historical semantic JSON extraction calls")
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--judge-k", type=int, default=5)
    parser.add_argument("--hnsw-path", type=Path)
    parser.add_argument("--query", action="append", default=[], help="retrieval evaluation query; repeatable")
    args = parser.parse_args()
    episodes = load_episodes(args.episodes)
    args.output.mkdir(parents=True, exist_ok=True)
    db_path = args.output / "skill-catalog.sqlite"
    transport = OpenAICompatibleTransport(OpenAICompatibleConfig(
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        timeout_seconds=240,
        max_output_tokens=7000,
        retries=2,
    ))
    manager = LifecycleManager()
    with CatalogStore(db_path) as store:
        store.initialize()
        retriever = SkillCandidateRetriever(store)
        governance = LLMGovernanceAdapter(
            transport,
            GovernanceContext(
                repository="codex-github-issue-pilot",
                model=args.model,
                prompt_version="codex-episode-admission-v1",
            ),
        )
        admission = BottomUpSkillAdmission(
            manager,
            retriever,
            judge=governance.judge,
            judge_k=args.judge_k,
        )

        def extract_atomics(episode: ChangeEpisode) -> tuple[SkillRecord, ...]:
            if not args.legacy_json_reextract:
                return atomic_records(episode)
            return namespace_records(governance.extract_atomics_from_episode(episode), episode.episode_id)

        def extract_workflows(
            episode: ChangeEpisode, atomics: Sequence[SkillRecord]
        ) -> tuple[SkillRecord, ...]:
            if not args.legacy_json_reextract:
                return workflow_records(episode, atomics)
            return namespace_records(
                governance.extract_workflows_from_episode(episode, atomics), episode.episode_id
            )

        def extract_patterns(workflows: Sequence[SkillRecord]) -> tuple[SkillRecord, ...]:
            return namespace_records(governance.extract_patterns_from_workflows(workflows), "pattern")

        episode_results, pattern_results = admission.insert_episodes(
            episodes,
            atomic_extractor=extract_atomics,
            workflow_extractor=extract_workflows,
            pattern_extractor=extract_patterns,
        )
        if args.hnsw_path:
            store.build_hnsw_index(
                args.hnsw_path,
                embedding_kind="routing",
                model_version="hash-v1",
            )

        queries = args.query or [episode.title for episode in episodes]
        retrieval_results: list[dict] = []
        searcher = SkillRetriever(store)
        for query in queries:
            response = searcher.search(
                query,
                top_k=10,
                seed_k=50,
                expand_hops=2,
                query_mode="solve",
                vector_backend="exact",
            )
            retrieval_results.append({
                "query": query,
                "hits": [
                    {
                        "skill_id": hit.node.id,
                        "node_type": hit.node.node_type.value,
                        "score": hit.score,
                        "sources": dict(hit.sources),
                        "trace": list(hit.trace),
                    }
                    for hit in response.hits
                ],
            })

        summary = {
            "source": "server_codex_cli_canonical_episodes",
            "episodes_input": len(episodes),
            "episode_results": [
                {
                    "episode_id": item.episode_id,
                    "atomics": [result.resolved_id for result in item.atomics],
                    "workflows": [result.resolved_id for result in item.workflows],
                }
                for item in episode_results
            ],
            "patterns": [result.resolved_id for result in pattern_results],
            "nodes": len(manager.skills),
            "active_nodes": sum(skill.status.value == "active" for skill in manager.skills.values()),
            "relations": len(manager.relations),
            "dedup_proposals": len(manager.dedup_proposals),
            "retrieval_queries": len(retrieval_results),
            "llm_calls": len(transport.calls),
        }
        (args.output / "admission-summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (args.output / "retrieval-evaluation.json").write_text(
            json.dumps(retrieval_results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (args.output / "episodes-used.json").write_text(
            json.dumps([episode.to_json() for episode in episodes], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (args.output / "transport-calls.json").write_text(
            json.dumps(transport.calls, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (args.output / "llm-transcript.json").write_text(
            json.dumps(transport.transcripts, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps({"output": str(args.output), **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
