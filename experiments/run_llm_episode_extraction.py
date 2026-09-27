#!/usr/bin/env python3
"""Run the real episode -> Atomic -> Workflow -> Pattern pilot.

This runner intentionally treats the prepared case files as evidence-bearing
ChangeEpisodes. It does not claim to have a checkout of the source repositories
when only evidence.md/case.json are present. The raw LLM transcript contains
prompts and JSON responses but never the API key.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.admission import BottomUpSkillAdmission, SkillCandidateRetriever
from arex_skill_graph.episodes import ChangeEpisode
from arex_skill_graph.lifecycle import DedupProposal, LifecycleManager, SkillLevel, SkillRecord, DedupDecision
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import OpenAICompatibleConfig, OpenAICompatibleTransport
from arex_skill_graph.store import CatalogStore


def load_case(case_dir: Path) -> tuple[dict, ChangeEpisode]:
    case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    evidence = (case_dir / "evidence.md").read_text(encoding="utf-8")
    candidates = (case_dir / "candidate-skills.md").read_text(encoding="utf-8") if (case_dir / "candidate-skills.md").exists() else ""
    repo = case.get("repository", {})
    evidence_units = case.get("evidence_units", [])
    evidence_ids = tuple(str(item.get("id")) for item in evidence_units if item.get("id"))
    call_sites = tuple(
        str(item.get("claim", "")) for item in evidence_units
        if item.get("kind") in {"call_site", "call-site"}
    )
    tests = tuple(
        str(item.get("claim", "")) for item in evidence_units
        if "test" in str(item.get("kind", "")).lower()
    )
    episode = ChangeEpisode(
        episode_id=str(case["case_id"]),
        repository=str(repo.get("name", case["case_id"])),
        revision=str(case.get("git_provenance", {}).get("merge_commit") or ",".join(case.get("git_provenance", {}).get("commits", [])) or case.get("extracted_at", "unknown")),
        title=str(case.get("case_workflow", {}).get("goal", case["case_id"])),
        before="The prepared artifact does not include a separately captured before snapshot; use the pre-change claims and provenance in the evidence below.",
        after="The prepared artifact does not include a separately captured after snapshot; use the post-change mechanisms and validation claims in the evidence below.",
        diff=evidence,
        call_sites=call_sites,
        tests=tests,
        evidence_ids=evidence_ids,
        metadata={
            "case": case,
            "candidate_skills_markdown": candidates,
            "evidence_markdown": evidence,
            "evidence_only": True,
            "source_checkout_present": False,
        },
    )
    return case, episode


def namespace_records(records: Iterable[SkillRecord], namespace: str) -> tuple[SkillRecord, ...]:
    """Make provider-generated IDs collision-safe without making semantic decisions."""
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--base-url", default="https://llm.rvnpu.cn/v1")
    parser.add_argument("--model", default="openai/gpt-5.6-sol")
    parser.add_argument("--cases", nargs="*", default=[])
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "skill-extraction" / "llm-runs" / "pilot-20260927")
    args = parser.parse_args()

    case_root = ROOT / "data" / "skill-extraction" / "cases"
    selected = args.cases or [p.name for p in sorted(case_root.iterdir()) if p.is_dir()]
    loaded = [load_case(case_root / name) for name in selected]
    cases = [item[0] for item in loaded]
    episodes = [item[1] for item in loaded]
    args.output.mkdir(parents=True, exist_ok=True)

    transport = OpenAICompatibleTransport(OpenAICompatibleConfig(
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        timeout_seconds=240,
        max_output_tokens=7000,
        retries=2,
    ))
    adapters = {
        episode.episode_id: LLMGovernanceAdapter(
            transport,
            GovernanceContext(
                repository=episode.repository,
                model=args.model,
                prompt_version="episode-skill-extraction-v1",
            ),
        )
        for episode in episodes
    }
    global_adapter = LLMGovernanceAdapter(
        transport,
        GovernanceContext(repository="multi-repository-harness-family", model=args.model, prompt_version="episode-skill-extraction-v1"),
    )

    def atomic_extractor(episode: ChangeEpisode) -> Sequence[SkillRecord]:
        return namespace_records(
            adapters[episode.episode_id].extract_atomics_from_episode(episode),
            episode.episode_id,
        )

    def workflow_extractor(episode: ChangeEpisode, atomics: Sequence[SkillRecord]) -> Sequence[SkillRecord]:
        return namespace_records(
            adapters[episode.episode_id].extract_workflows_from_episode(episode, atomics),
            episode.episode_id,
        )

    def pattern_extractor(workflows: Sequence[SkillRecord]) -> Sequence[SkillRecord]:
        return global_adapter.extract_patterns_from_workflows(workflows)

    def judge(candidate: SkillRecord, peer: SkillRecord) -> DedupProposal:
        return global_adapter.judge(candidate, peer)

    db_path = args.output / "skill-catalog.sqlite"
    with CatalogStore(db_path) as store:
        store.initialize()
        manager = LifecycleManager()
        admission = BottomUpSkillAdmission(manager, SkillCandidateRetriever(store), judge=judge, judge_k=5)
        episode_results, pattern_results = admission.insert_episodes(
            episodes,
            atomic_extractor=atomic_extractor,
            workflow_extractor=workflow_extractor,
            pattern_extractor=pattern_extractor,
        )
        graph = {
            "nodes": len(manager.skills),
            "active_nodes": sum(item.status.value == "active" for item in manager.skills.values()),
            "relations": len(manager.relations),
            "dedup_proposals": len(manager.dedup_proposals),
            "episodes": [
                {
                    "episode_id": item.episode_id,
                    "atomics": [result.__dict__ if hasattr(result, "__dict__") else result.submitted_id for result in item.atomics],
                    "workflows": [result.resolved_id for result in item.workflows],
                }
                for item in episode_results
            ],
            "patterns": [result.resolved_id for result in pattern_results],
        }
    (args.output / "graph-summary.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (args.output / "episodes.json").write_text(json.dumps([episode.to_json() for episode in episodes], ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (args.output / "case-manifest.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (args.output / "transport-calls.json").write_text(json.dumps(transport.calls, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    (args.output / "llm-transcript.json").write_text(json.dumps(transport.transcripts, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "calls": len(transport.calls), **graph}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
