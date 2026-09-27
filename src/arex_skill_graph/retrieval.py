from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .schema import Node, NodeType, RelationType
from .store import CatalogStore


FORWARD_WEIGHTS: dict[RelationType, float] = {
    RelationType.DECLARES_STEP: 0.95,
    RelationType.HAS_STEP: 0.95,
    RelationType.EXECUTED_BY: 0.95,
    RelationType.REALIZES: 0.80,
    RelationType.CONFORMS_TO: 0.75,
    RelationType.INSTANTIATES: 0.75,
    RelationType.EVIDENCED_BY: 0.10,
    RelationType.SUPPORTED_BY: 0.55,
    RelationType.APPLICABLE_WHEN: 0.65,
    RelationType.VERIFIES: 0.45,
    RelationType.GROUNDS: 0.65,
    RelationType.CONTAINS: 0.90,
    RelationType.REQUIRES: 0.70,
    RelationType.ENABLES: 0.55,
    RelationType.PRECEDES: 0.45,
    RelationType.VALIDATES: 0.45,
    RelationType.REPAIRS: 0.55,
    RelationType.ALTERNATIVE_TO: 0.20,
    RelationType.SPECIALIZES: 0.70,
    RelationType.COMPOSES_WITH: 0.35,
    RelationType.REQUIRES_PATTERN: 0.70,
}

REVERSE_WEIGHTS: dict[RelationType, float] = {
    RelationType.DECLARES_STEP: 0.45,
    RelationType.HAS_STEP: 0.45,
    RelationType.EXECUTED_BY: 0.60,
    RelationType.REALIZES: 0.55,
    RelationType.CONFORMS_TO: 0.55,
    RelationType.INSTANTIATES: 0.20,
    RelationType.EVIDENCED_BY: 0.75,
    RelationType.SUPPORTED_BY: 0.20,
    RelationType.APPLICABLE_WHEN: 0.20,
    RelationType.VERIFIES: 0.90,
    RelationType.GROUNDS: 0.40,
    RelationType.CONTAINS: 0.85,
    RelationType.REQUIRES: 1.00,
    RelationType.ENABLES: 0.50,
    RelationType.PRECEDES: 0.35,
    RelationType.VALIDATES: 0.90,
    RelationType.REPAIRS: 0.65,
    RelationType.ALTERNATIVE_TO: 0.20,
    RelationType.SPECIALIZES: 0.35,
    RelationType.COMPOSES_WITH: 0.35,
    RelationType.REQUIRES_PATTERN: 0.90,
}


@dataclass(slots=True)
class SearchHit:
    node: Node
    score: float
    sources: dict[str, float] = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SearchResponse:
    query: str
    hits: list[SearchHit]
    seed_count: int
    expanded_count: int
    unresolved: list[str]


class SkillRetriever:
    def __init__(self, store: CatalogStore):
        self.store = store

    def search(
        self,
        query: str,
        *,
        node_types: Sequence[NodeType] | None = None,
        repository: str | None = None,
        top_k: int = 12,
        seed_k: int = 50,
        expand_hops: int = 2,
        query_mode: str = "solve",
        vector_backend: str = "exact",
        hnsw_path: str | None = None,
        hnsw_ef_search: int = 64,
        hnsw_oversample: int = 4,
        same_level_only: bool = False,
        include_inactive: bool = True,
    ) -> SearchResponse:
        lexical = self.store.search_lexical(
            query,
            node_types=node_types,
            repository=repository,
            limit=seed_k,
        )
        vector = self.store.search_vector(
            query,
            node_types=node_types,
            repository=repository,
            limit=seed_k,
            vector_backend=vector_backend,
            hnsw_path=hnsw_path,
            hnsw_ef_search=hnsw_ef_search,
            hnsw_oversample=hnsw_oversample,
        )
        terminal_lifecycles = {
            "quarantined", "deprecated", "retired", "merged", "superseded",
        }
        if not include_inactive:
            lexical = [(node, score) for node, score in lexical if node.lifecycle not in terminal_lifecycles]
            vector = [(node, score) for node, score in vector if node.lifecycle not in terminal_lifecycles]

        hits: dict[str, SearchHit] = {}
        self._fuse_ranked(hits, lexical, "lexical")
        self._fuse_ranked(hits, vector, "vector")

        seeds = sorted(hits.values(), key=lambda hit: hit.score, reverse=True)[:seed_k]
        expanded_ids: set[str] = set()
        frontier = [(hit.node.id, hit.score, 0) for hit in seeds]
        best_frontier_score = {node_id: score for node_id, score, _ in frontier}

        while frontier:
            node_id, current_score, hop = frontier.pop(0)
            if hop >= expand_hops:
                continue
            for edge, neighbor, direction in self.store.neighbors(node_id):
                if not include_inactive and neighbor.lifecycle in terminal_lifecycles:
                    continue
                relation_weight = (
                    FORWARD_WEIGHTS[edge.relation]
                    if direction == "out"
                    else REVERSE_WEIGHTS[edge.relation]
                )
                if query_mode == "solve" and neighbor.node_type in {
                    NodeType.COMMIT,
                    NodeType.HUNK,
                }:
                    relation_weight *= 0.10
                expansion_score = (
                    current_score
                    * relation_weight
                    * edge.weight
                    * edge.confidence
                    * (0.72 ** (hop + 1))
                )
                if expansion_score <= 0:
                    continue
                hit = hits.get(neighbor.id)
                trace = (
                    f"{node_id} --{edge.relation.value}/{direction}--> {neighbor.id}"
                )
                if hit is None:
                    hit = SearchHit(node=neighbor, score=expansion_score)
                    hits[neighbor.id] = hit
                else:
                    hit.score += expansion_score
                hit.sources["graph"] = hit.sources.get("graph", 0.0) + expansion_score
                if trace not in hit.trace:
                    hit.trace.append(trace)
                expanded_ids.add(neighbor.id)
                if expansion_score > best_frontier_score.get(neighbor.id, 0.0):
                    best_frontier_score[neighbor.id] = expansion_score
                    frontier.append((neighbor.id, expansion_score, hop + 1))

        unresolved = self._apply_closures(hits, query_mode=query_mode)
        ranked = sorted(
            hits.values(),
            key=lambda hit: (
                self._type_priority(hit.node.node_type, query_mode),
                hit.score,
                hit.node.confidence,
            ),
            reverse=True,
        )
        # Admission and same-level deduplication must never send cross-level
        # graph neighbors to the LLM judge as peers. Cross-level expansion is
        # still performed above and remains available to callers that need an
        # execution/audit context; this flag only controls returned peers.
        if same_level_only and node_types is not None:
            allowed_types = set(node_types)
            ranked = [hit for hit in ranked if hit.node.node_type in allowed_types]
        return SearchResponse(
            query=query,
            hits=ranked[:top_k],
            seed_count=len(seeds),
            expanded_count=len(expanded_ids),
            unresolved=unresolved,
        )

    @staticmethod
    def _fuse_ranked(
        hits: dict[str, SearchHit],
        ranked: Sequence[tuple[Node, float]],
        source: str,
        *,
        rrf_constant: int = 60,
    ) -> None:
        for rank, (node, raw_score) in enumerate(ranked, start=1):
            contribution = 1.0 / (rrf_constant + rank)
            hit = hits.setdefault(node.id, SearchHit(node=node, score=0.0))
            hit.score += contribution
            hit.sources[source] = contribution
            hit.sources[f"{source}_raw"] = raw_score

    def _apply_closures(
        self,
        hits: dict[str, SearchHit],
        *,
        query_mode: str,
    ) -> list[str]:
        unresolved: list[str] = []
        selected = sorted(hits.values(), key=lambda hit: hit.score, reverse=True)[:20]

        for hit in list(selected):
            if hit.node.node_type is NodeType.ACTION:
                self._add_incoming_closure(
                    hits,
                    hit,
                    relations=(RelationType.REQUIRES,),
                    source="prerequisite_closure",
                )
                self._add_incoming_closure(
                    hits,
                    hit,
                    relations=(RelationType.VALIDATES,),
                    source="validation_closure",
                )
            elif hit.node.node_type is NodeType.PATTERN:
                step_neighbors = self.store.neighbors(
                    hit.node.id,
                    relations=(RelationType.DECLARES_STEP,),
                    direction="out",
                )
                if not step_neighbors:
                    unresolved.append(f"pattern {hit.node.id} has no declared steps")
                for edge, step, _ in step_neighbors:
                    step_hit = hits.setdefault(
                        step.id,
                        SearchHit(
                            node=step,
                            score=hit.score * edge.weight * edge.confidence * 0.8,
                        ),
                    )
                    step_hit.sources["mandatory_step_closure"] = step_hit.score
                    actions = self.store.neighbors(
                        step.id,
                        relations=(RelationType.CONFORMS_TO,),
                        direction="in",
                    )
                    if not actions:
                        unresolved.append(
                            f"mandatory pattern step {step.id} has no conforming action"
                        )
                    for action_edge, action, _ in actions[:5]:
                        action_score = (
                            step_hit.score
                            * action_edge.weight
                            * action_edge.confidence
                            * 0.75
                        )
                        action_hit = hits.setdefault(
                            action.id, SearchHit(node=action, score=action_score)
                        )
                        action_hit.sources["mandatory_step_action"] = action_score

        if query_mode == "solve":
            unresolved = sorted(set(unresolved))
        return unresolved

    def _add_incoming_closure(
        self,
        hits: dict[str, SearchHit],
        target_hit: SearchHit,
        *,
        relations: Sequence[RelationType],
        source: str,
    ) -> None:
        for edge, node, _ in self.store.neighbors(
            target_hit.node.id, relations=relations, direction="in"
        ):
            score = target_hit.score * edge.weight * edge.confidence * 0.85
            hit = hits.setdefault(node.id, SearchHit(node=node, score=score))
            hit.sources[source] = hit.sources.get(source, 0.0) + score
            hit.trace.append(
                f"{node.id} --{edge.relation.value}--> {target_hit.node.id}"
            )

    @staticmethod
    def _type_priority(node_type: NodeType, query_mode: str) -> int:
        if query_mode == "audit":
            return {
                NodeType.COMMIT: 4,
                NodeType.HUNK: 4,
                NodeType.WORKFLOW: 3,
                NodeType.ACTION: 2,
            }.get(node_type, 1)
        return {
            NodeType.PATTERN: 5,
            NodeType.WORKFLOW: 4,
            NodeType.ATOMIC: 3,
            NodeType.PATTERN_STEP: 2,
            NodeType.ACTION: 2,
            NodeType.WORKFLOW_STEP: 2,
            NodeType.VALIDATION: 2,
            NodeType.PREDICATE: 1,
            NodeType.BINDING: 1,
            NodeType.COMMIT: 0,
            NodeType.HUNK: 0,
        }.get(node_type, 1)



