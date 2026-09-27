from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Iterable


class NodeType(StrEnum):
    # Abstract skill levels are first-class catalog nodes.
    ATOMIC = "atomic"
    PATTERN = "pattern"
    PATTERN_STEP = "pattern_step"
    WORKFLOW = "workflow"
    WORKFLOW_STEP = "workflow_step"
    ACTION = "action"
    COMMIT = "commit"
    HUNK = "hunk"
    PREDICATE = "predicate"
    VALIDATION = "validation"
    BINDING = "binding"


class RelationType(StrEnum):
    # Cross-level structure.
    DECLARES_STEP = "declares_step"
    INSTANTIATES = "instantiates"
    HAS_STEP = "has_step"
    REALIZES = "realizes"
    EXECUTED_BY = "executed_by"
    CONFORMS_TO = "conforms_to"
    EVIDENCED_BY = "evidenced_by"
    SUPPORTED_BY = "supported_by"
    APPLICABLE_WHEN = "applicable_when"
    VERIFIES = "verifies"
    GROUNDS = "grounds"
    # Explicit hierarchy projection for the abstract skill tree.
    # Pattern contains Workflows; Workflow contains Atomics.
    CONTAINS = "contains"

    # Positive, retrieval-useful same-level relations.
    REQUIRES = "requires"
    ENABLES = "enables"
    PRECEDES = "precedes"
    VALIDATES = "validates"
    REPAIRS = "repairs"
    ALTERNATIVE_TO = "alternative_to"
    SPECIALIZES = "specializes"
    COMPOSES_WITH = "composes_with"
    REQUIRES_PATTERN = "requires_pattern"


Endpoint = tuple[frozenset[NodeType], frozenset[NodeType]]


ENDPOINTS: dict[RelationType, Endpoint] = {
    RelationType.DECLARES_STEP: (
        frozenset({NodeType.PATTERN}),
        frozenset({NodeType.PATTERN_STEP}),
    ),
    RelationType.INSTANTIATES: (
        frozenset({NodeType.WORKFLOW}),
        frozenset({NodeType.PATTERN}),
    ),
    RelationType.HAS_STEP: (
        frozenset({NodeType.WORKFLOW}),
        frozenset({NodeType.WORKFLOW_STEP}),
    ),
    RelationType.REALIZES: (
        frozenset({NodeType.WORKFLOW_STEP}),
        frozenset({NodeType.PATTERN_STEP}),
    ),
    RelationType.EXECUTED_BY: (
        frozenset({NodeType.WORKFLOW_STEP}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.CONFORMS_TO: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.PATTERN_STEP}),
    ),
    RelationType.EVIDENCED_BY: (
        frozenset({NodeType.ACTION, NodeType.WORKFLOW_STEP}),
        frozenset({NodeType.COMMIT, NodeType.HUNK}),
    ),
    RelationType.SUPPORTED_BY: (
        frozenset({NodeType.PATTERN}),
        frozenset({NodeType.WORKFLOW}),
    ),
    RelationType.APPLICABLE_WHEN: (
        frozenset(
            {
                NodeType.PATTERN,
                NodeType.PATTERN_STEP,
                NodeType.WORKFLOW_STEP,
                NodeType.ACTION,
            }
        ),
        frozenset({NodeType.PREDICATE}),
    ),
    RelationType.VERIFIES: (
        frozenset({NodeType.VALIDATION}),
        frozenset({NodeType.ACTION, NodeType.WORKFLOW, NodeType.PATTERN}),
    ),
    RelationType.GROUNDS: (
        frozenset({NodeType.BINDING}),
        frozenset({NodeType.PATTERN_STEP, NodeType.ACTION}),
    ),
    RelationType.CONTAINS: (
        frozenset({NodeType.PATTERN, NodeType.WORKFLOW}),
        frozenset({NodeType.WORKFLOW, NodeType.ATOMIC}),
    ),
    RelationType.REQUIRES: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.ENABLES: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.PRECEDES: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.VALIDATES: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.REPAIRS: (
        frozenset({NodeType.ACTION}),
        frozenset({NodeType.ACTION}),
    ),
    RelationType.ALTERNATIVE_TO: (
        frozenset({NodeType.ACTION, NodeType.PATTERN}),
        frozenset({NodeType.ACTION, NodeType.PATTERN}),
    ),
    RelationType.SPECIALIZES: (
        frozenset({NodeType.PATTERN}),
        frozenset({NodeType.PATTERN}),
    ),
    RelationType.COMPOSES_WITH: (
        frozenset({NodeType.PATTERN}),
        frozenset({NodeType.PATTERN}),
    ),
    RelationType.REQUIRES_PATTERN: (
        frozenset({NodeType.PATTERN}),
        frozenset({NodeType.PATTERN}),
    ),
}


SYMMETRIC_RELATIONS = frozenset(
    {
        RelationType.ALTERNATIVE_TO,
        RelationType.COMPOSES_WITH,
    }
)


def stable_id(namespace: str, *parts: str) -> str:
    normalized = "\x1f".join(part.strip() for part in parts)
    digest = sha256(normalized.encode("utf-8")).hexdigest()[:24]
    return f"{namespace}:{digest}"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


@dataclass(slots=True)
class Node:
    id: str
    node_type: NodeType
    title: str
    summary: str
    repository: str | None = None
    version: str = "1"
    lifecycle: str = "provisional"
    confidence: float = 1.0
    facets: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)

    def searchable_text(self) -> str:
        facet_text = " ".join(_flatten_text(self.facets))
        payload_terms = self.payload.get("routing_terms", [])
        return " ".join(
            part
            for part in (
                self.title,
                self.summary,
                facet_text,
                " ".join(str(term) for term in payload_terms),
            )
            if part
        )


@dataclass(slots=True)
class Edge:
    id: str
    source_id: str
    target_id: str
    relation: RelationType
    weight: float = 1.0
    confidence: float = 1.0
    evidence_ids: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    condition: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        source_id: str,
        target_id: str,
        relation: RelationType,
        *,
        weight: float = 1.0,
        confidence: float = 1.0,
        evidence_ids: Iterable[str] = (),
        provenance: dict[str, Any] | None = None,
        condition: dict[str, Any] | None = None,
    ) -> "Edge":
        return cls(
            id=stable_id("edge", source_id, relation.value, target_id),
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight,
            confidence=confidence,
            evidence_ids=tuple(evidence_ids),
            provenance=provenance or {},
            condition=condition or {},
        )


def validate_endpoint(edge: Edge, source_type: NodeType, target_type: NodeType) -> None:
    source_types, target_types = ENDPOINTS[edge.relation]
    if source_type not in source_types or target_type not in target_types:
        raise ValueError(
            f"invalid endpoints for {edge.relation.value}: "
            f"{source_type.value} -> {target_type.value}"
        )
    if edge.relation in SYMMETRIC_RELATIONS and source_type != target_type:
        raise ValueError(
            f"symmetric relation {edge.relation.value} requires matching node types"
        )
    if not 0.0 <= edge.confidence <= 1.0:
        raise ValueError("edge confidence must be in [0, 1]")
    if edge.weight < 0:
        raise ValueError("edge weight must be non-negative")


def _flatten_text(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, dict):
        result: list[str] = []
        for key, item in value.items():
            result.append(str(key))
            result.extend(_flatten_text(item))
        return result
    if isinstance(value, (list, tuple, set, frozenset)):
        result = []
        for item in value:
            result.extend(_flatten_text(item))
        return result
    return [str(value)]







