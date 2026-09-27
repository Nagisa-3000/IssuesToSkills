"""Cost-controlled, bottom-up skill admission.

Candidate generation is intentionally non-semantic: FTS5/BM25, exact vectors,
and optional HNSW only retrieve same-level peers.  A caller-supplied LLM judge
is the sole semantic adjudicator.  Episode admission extracts Atomic skills
from code evidence, then extracts Workflows once from the complete episode and
all resolved Atomics, and finally extracts Patterns once from the resolved
Workflows.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

from .episodes import ChangeEpisode
from .lifecycle import (
    DedupDecision,
    DedupProposal,
    LifecycleManager,
    SkillLevel,
    SkillRecord,
    SkillStatus,
)
from .schema import Node, NodeType
from .store import CatalogStore


LEVEL_NODE_TYPES: dict[SkillLevel, NodeType] = {
    SkillLevel.ATOMIC: NodeType.ATOMIC,
    SkillLevel.WORKFLOW: NodeType.WORKFLOW,
    SkillLevel.PATTERN: NodeType.PATTERN,
}


@dataclass(frozen=True, slots=True)
class SimilarityCandidate:
    skill_id: str
    level: SkillLevel
    score: float
    channels: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    submitted_id: str
    resolved_id: str
    level: SkillLevel
    decision: DedupDecision | None
    candidate_ids: tuple[str, ...]
    changed: bool
    parent_ids_needing_revalidation: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class BottomUpResult:
    atomic: AdmissionResult
    workflows: tuple[AdmissionResult, ...]
    patterns: tuple[AdmissionResult, ...]


@dataclass(frozen=True, slots=True)
class EpisodeAdmissionResult:
    """Audit-friendly result for one complete ChangeEpisode."""

    episode_id: str
    atomics: tuple[AdmissionResult, ...]
    workflows: tuple[AdmissionResult, ...]
    patterns: tuple[AdmissionResult, ...]


DedupJudge = Callable[[SkillRecord, SkillRecord], DedupProposal]
WorkflowExtractor = Callable[[SkillRecord], Iterable[SkillRecord]]
PatternExtractor = Callable[[SkillRecord], Iterable[SkillRecord]]
EpisodeAtomicExtractor = Callable[[ChangeEpisode], Iterable[SkillRecord]]
EpisodeWorkflowExtractor = Callable[[ChangeEpisode, Sequence[SkillRecord]], Iterable[SkillRecord]]
EpisodePatternExtractor = Callable[[Sequence[SkillRecord]], Iterable[SkillRecord]]


class SkillCandidateRetriever:
    """Retrieve likely same-level peers before spending an LLM call.

    BM25 and vector/HNSW scores are used for candidate generation only.  No
    similarity threshold here means "duplicate"; the LLM must decide that.
    """

    def __init__(self, store: CatalogStore):
        self.store = store

    def index(self, skill: SkillRecord, *, embed: bool = True) -> None:
        node = Node(
            id=skill.skill_id,
            node_type=LEVEL_NODE_TYPES[skill.level],
            title=skill.title,
            summary=skill.summary,
            version=str(skill.version),
            lifecycle=skill.status.value,
            confidence=1.0,
            facets={
                "level": skill.level.value,
                "preconditions": list(skill.preconditions),
                "exclusions": list(skill.exclusions),
                "failure_modes": list(skill.failure_modes),
            },
            payload={
                "skill_level": skill.level.value,
                "skill_status": skill.status.value,
                "canonical_id": skill.canonical_id,
                "routing_terms": [
                    skill.level.value,
                    *skill.preconditions,
                    *skill.exclusions,
                    *skill.failure_modes,
                ],
            },
        )
        self.store.upsert_node(node, embed=embed)
        self.store.connection.commit()

    def find(
        self,
        skill: SkillRecord,
        *,
        limit: int = 12,
        lexical_k: int | None = None,
        vector_k: int | None = None,
        vector_backend: str = "exact",
        hnsw_path: str | None = None,
        ef_search: int = 64,
        oversample: int = 4,
    ) -> list[SimilarityCandidate]:
        if limit <= 0:
            return []
        lexical_k = lexical_k or max(limit * 4, 20)
        vector_k = vector_k or max(limit * 4, 20)
        node_type = LEVEL_NODE_TYPES[skill.level]
        query = " ".join(
            [skill.title, skill.summary, *skill.preconditions, *skill.exclusions, *skill.failure_modes]
        )
        lexical = self.store.search_lexical(query, node_types=[node_type], limit=lexical_k)
        vector = self.store.search_vector(
            query,
            node_types=[node_type],
            limit=vector_k,
            vector_backend=vector_backend,
            hnsw_path=hnsw_path,
            hnsw_ef_search=ef_search,
            hnsw_oversample=oversample,
        )
        fused: dict[str, SimilarityCandidate] = {}
        for channel, hits in (("bm25", lexical), ("embedding", vector)):
            for rank, (node, raw_score) in enumerate(hits, start=1):
                if node.id == skill.skill_id:
                    continue
                if node.payload.get("skill_level") != skill.level.value:
                    continue
                if node.lifecycle in {
                    SkillStatus.RETIRED.value,
                    SkillStatus.MERGED.value,
                    SkillStatus.SUPERSEDED.value,
                }:
                    continue
                rrf = 1.0 / (60.0 + rank)
                old = fused.get(node.id)
                if old is None:
                    fused[node.id] = SimilarityCandidate(
                        skill_id=node.id,
                        level=skill.level,
                        score=rrf,
                        channels={channel: float(raw_score)},
                    )
                else:
                    old.channels[channel] = float(raw_score)
                    fused[node.id] = SimilarityCandidate(
                        skill_id=old.skill_id,
                        level=old.level,
                        score=old.score + rrf,
                        channels=old.channels,
                    )
        return sorted(fused.values(), key=lambda item: (-item.score, item.skill_id))[:limit]


class BottomUpSkillAdmission:
    """Insert/update the tree from leaves upward.

    The episode API is the production path. Its extractors are LLM-backed in
    production and receive the full evidence boundary. Local code only does
    candidate retrieval, lifecycle bookkeeping, and structural tree routing.
    """

    def __init__(
        self,
        manager: LifecycleManager,
        retriever: SkillCandidateRetriever,
        *,
        judge: DedupJudge,
        judge_k: int = 5,
    ) -> None:
        if judge_k <= 0:
            raise ValueError("judge_k must be positive")
        self.manager = manager
        self.retriever = retriever
        self.judge = judge
        self.judge_k = judge_k

    def _admit(self, skill: SkillRecord) -> AdmissionResult:
        self.manager.add_candidate(skill)
        self.retriever.index(skill)
        candidates = self.retriever.find(skill, limit=self.judge_k)
        proposals: list[DedupProposal] = []
        for candidate in candidates:
            peer = self.manager.skills.get(candidate.skill_id)
            if peer is None:
                continue
            proposal = self.judge(skill, peer)
            proposals.append(proposal)
            if proposal.decision in {DedupDecision.EXACT_DUPLICATE, DedupDecision.MERGEABLE}:
                resolved = self.manager.apply_dedup(proposal)
                if resolved is None:
                    break
                if resolved.status is SkillStatus.CANDIDATE:
                    resolved.status = SkillStatus.ACTIVE
                    resolved.touch()
                self.retriever.index(resolved)
                return AdmissionResult(
                    submitted_id=skill.skill_id,
                    resolved_id=resolved.skill_id,
                    level=skill.level,
                    decision=proposal.decision,
                    candidate_ids=tuple(item.skill_id for item in candidates),
                    changed=True,
                    parent_ids_needing_revalidation=tuple(sorted(resolved.parent_ids)),
                )
            self.manager.apply_dedup(proposal)
        skill.status = SkillStatus.ACTIVE
        skill.touch()
        self.retriever.index(skill)
        return AdmissionResult(
            submitted_id=skill.skill_id,
            resolved_id=skill.skill_id,
            level=skill.level,
            decision=proposals[-1].decision if proposals else None,
            candidate_ids=tuple(item.skill_id for item in candidates),
            changed=True,
        )

    @staticmethod
    def _unique_resolved(results: Iterable[AdmissionResult]) -> tuple[AdmissionResult, ...]:
        unique: dict[str, AdmissionResult] = {}
        for result in results:
            unique.setdefault(result.resolved_id, result)
        return tuple(unique.values())

    def _attach_children(
        self,
        *,
        parent: SkillRecord,
        ids: Iterable[str] | None,
        fallback_ids: Iterable[str],
    ) -> None:
        child_ids = (
            tuple(str(item) for item in ids)
            if ids is not None
            else tuple(str(item) for item in fallback_ids)
        )
        for child_id in child_ids:
            if child_id in self.manager.skills:
                self.manager.attach_parent(child_id, parent.skill_id)

    def insert_episode(
        self,
        episode: ChangeEpisode,
        *,
        atomic_extractor: EpisodeAtomicExtractor,
        workflow_extractor: EpisodeWorkflowExtractor,
        pattern_extractor: EpisodePatternExtractor,
    ) -> EpisodeAdmissionResult:
        """Admit one complete ChangeEpisode in strict bottom-up order.

        Atomics are extracted first; Workflows are extracted exactly once from
        the complete episode and all resolved Atomics; Patterns are extracted
        exactly once from all resolved Workflows. No upper-level node is
        manufactured from a single lower-level node.
        """
        atomic_results = self._unique_resolved(
            self._admit(candidate) for candidate in atomic_extractor(episode)
        )
        resolved_atomics = tuple(self.manager.get(item.resolved_id) for item in atomic_results)

        workflow_candidates = tuple(workflow_extractor(episode, resolved_atomics))
        workflow_results = self._unique_resolved(
            self._admit(candidate) for candidate in workflow_candidates
        )
        resolved_workflows = tuple(self.manager.get(item.resolved_id) for item in workflow_results)
        atomic_ids = tuple(item.skill_id for item in resolved_atomics)
        for workflow in resolved_workflows:
            self._attach_children(
                parent=workflow,
                ids=workflow.payload.get("atomic_ids", ()),
                fallback_ids=atomic_ids,
            )

        pattern_candidates = tuple(pattern_extractor(resolved_workflows)) if resolved_workflows else ()
        pattern_results = self._unique_resolved(
            self._admit(candidate) for candidate in pattern_candidates
        )
        resolved_patterns = tuple(self.manager.get(item.resolved_id) for item in pattern_results)
        workflow_ids = tuple(item.skill_id for item in resolved_workflows)
        for pattern in resolved_patterns:
            self._attach_children(
                parent=pattern,
                ids=pattern.payload.get("workflow_ids", ()),
                fallback_ids=workflow_ids,
            )

        self.retriever.store.persist_lifecycle_manager(self.manager)
        return EpisodeAdmissionResult(
            episode_id=episode.episode_id,
            atomics=atomic_results,
            workflows=workflow_results,
            patterns=pattern_results,
        )

    def insert_episodes(
        self,
        episodes: Sequence[ChangeEpisode],
        *,
        atomic_extractor: EpisodeAtomicExtractor,
        workflow_extractor: EpisodeWorkflowExtractor,
        pattern_extractor: EpisodePatternExtractor,
    ) -> tuple[tuple[EpisodeAdmissionResult, ...], tuple[AdmissionResult, ...]]:
        """Admit a batch and abstract Patterns across all episode Workflows.

        This is the preferred path when several Harness issues have already
        been grouped as a potentially related family: every episode supplies
        its own Atomic and Workflow evidence, while Pattern extraction sees
        the complete cross-episode Workflow set exactly once.
        """
        episode_results: list[EpisodeAdmissionResult] = []
        all_workflows: list[SkillRecord] = []
        for episode in episodes:
            atomic_results = self._unique_resolved(
                self._admit(candidate) for candidate in atomic_extractor(episode)
            )
            resolved_atomics = tuple(self.manager.get(item.resolved_id) for item in atomic_results)
            workflow_candidates = tuple(workflow_extractor(episode, resolved_atomics))
            workflow_results = self._unique_resolved(
                self._admit(candidate) for candidate in workflow_candidates
            )
            resolved_workflows = tuple(self.manager.get(item.resolved_id) for item in workflow_results)
            atomic_ids = tuple(item.skill_id for item in resolved_atomics)
            for workflow in resolved_workflows:
                self._attach_children(
                    parent=workflow,
                    ids=workflow.payload.get("atomic_ids", ()),
                    fallback_ids=atomic_ids,
                )
            all_workflows.extend(resolved_workflows)
            episode_results.append(
                EpisodeAdmissionResult(
                    episode_id=episode.episode_id,
                    atomics=atomic_results,
                    workflows=workflow_results,
                    patterns=(),
                )
            )

        pattern_results = self._unique_resolved(
            self._admit(candidate) for candidate in pattern_extractor(tuple(all_workflows))
        ) if all_workflows else ()
        resolved_patterns = tuple(self.manager.get(item.resolved_id) for item in pattern_results)
        workflow_ids = tuple(item.skill_id for item in all_workflows)
        for pattern in resolved_patterns:
            self._attach_children(
                parent=pattern,
                ids=pattern.payload.get("workflow_ids", ()),
                fallback_ids=workflow_ids,
            )
        self.retriever.store.persist_lifecycle_manager(self.manager)
        return tuple(episode_results), pattern_results
    def insert_atomic(
        self,
        atomic: SkillRecord,
        *,
        workflow_extractor: WorkflowExtractor,
        pattern_extractor: PatternExtractor,
    ) -> BottomUpResult:
        """Legacy single-leaf adapter; new code should use ``insert_episode``."""
        atomic_result = self._admit(atomic)
        resolved_atomic = self.manager.get(atomic_result.resolved_id)
        workflow_results: list[AdmissionResult] = []
        pattern_results: list[AdmissionResult] = []
        for workflow in workflow_extractor(resolved_atomic):
            workflow_result = self._admit(workflow)
            resolved_workflow = self.manager.get(workflow_result.resolved_id)
            self._attach_children(
                parent=resolved_workflow,
                ids=resolved_workflow.payload.get("atomic_ids", ()),
                fallback_ids=(resolved_atomic.skill_id,),
            )
            workflow_results.append(workflow_result)
            for pattern in pattern_extractor(resolved_workflow):
                pattern_result = self._admit(pattern)
                resolved_pattern = self.manager.get(pattern_result.resolved_id)
                self._attach_children(
                    parent=resolved_pattern,
                    ids=resolved_pattern.payload.get("workflow_ids", ()),
                    fallback_ids=(resolved_workflow.skill_id,),
                )
                pattern_results.append(pattern_result)
        self.retriever.store.persist_lifecycle_manager(self.manager)
        return BottomUpResult(
            atomic=atomic_result,
            workflows=tuple(workflow_results),
            patterns=tuple(pattern_results),
        )


