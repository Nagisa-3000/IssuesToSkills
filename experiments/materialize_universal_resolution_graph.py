#!/usr/bin/env python3
"""Materialize the universal ChangeAction -> Workflow -> Pattern graph.

``build_universal_resolution_graph.py`` intentionally emits a JSON graph so
that structural review and LLM adjudication remain separate from persistence.
This script is the catalog boundary: it turns the reviewed graph projection
into the existing AREX SQLite schema, creates authoritative hash embeddings,
and optionally builds the rebuildable HNSW cache.

The materializer never imports holdout records.  The graph builder has already
rejected them, and this second boundary checks the graph policy again before
writing anything.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.schema import Edge, Node, NodeType, RelationType, stable_id
from arex_skill_graph.store import CatalogStore

RELATIONS = {
    "requires": RelationType.REQUIRES,
    "enables": RelationType.ENABLES,
    "precedes": RelationType.PRECEDES,
    "validates": RelationType.VALIDATES,
    "repairs": RelationType.REPAIRS,
}


def text(value: Any) -> str:
    return str(value or "").strip()


def node_from_action(action: dict[str, Any]) -> Node:
    action_id = text(action.get("id"))
    category = text(action.get("category"))
    return Node(
        id=action_id,
        node_type=NodeType.ACTION,
        title=text(action.get("intent") or action.get("source_name") or action_id),
        summary=text(action.get("description") or action.get("intent")),
        repository=None,
        lifecycle="provisional",
        confidence=1.0 if action.get("grounded_semantics") else 0.35,
        facets={
            "problem_class": category,
            "module_role": text(action.get("module_role")),
            "operation": text(action.get("operation")),
            "grounded_semantics": bool(action.get("grounded_semantics")),
        },
        payload=dict(action),
        provenance={"source": "universal-resolution-graph", "stage": "materialize"},
    )


def node_from_workflow(workflow: dict[str, Any]) -> Node:
    workflow_id = text(workflow.get("id"))
    category = text(workflow.get("category"))
    return Node(
        id=workflow_id,
        node_type=NodeType.WORKFLOW,
        title=text(workflow.get("name") or workflow_id),
        summary=text(workflow.get("description") or workflow.get("goal")),
        repository=text(workflow.get("repository")) or None,
        lifecycle="provisional",
        confidence=0.8,
        facets={
            "problem_class": category,
            "entry_state": text(workflow.get("entry_state")),
            "exit_state": text(workflow.get("exit_state")),
        },
        payload=dict(workflow),
        provenance={"source": "universal-resolution-graph", "stage": "materialize"},
    )


def node_from_pattern(pattern: dict[str, Any]) -> Node:
    pattern_id = text(pattern.get("id"))
    category = text(pattern.get("category"))
    return Node(
        id=pattern_id,
        node_type=NodeType.PATTERN,
        title=text(pattern.get("title") or pattern.get("intent") or pattern_id),
        summary=text(pattern.get("summary") or pattern.get("intent")),
        lifecycle="provisional",
        confidence=float(pattern.get("confidence") or 0.0),
        facets={
            "problem_class": category,
            "promotion_status": text(pattern.get("promotion_status")),
        },
        payload=dict(pattern),
        provenance={"source": "universal-resolution-graph", "stage": "materialize"},
    )


def node_from_workflow_fragment(fragment: dict[str, Any]) -> Node:
    fragment_id = text(fragment.get("id"))
    roles = [text(value) for value in fragment.get("segment_roles", []) if text(value)]
    title = "Workflow fragment: " + " -> ".join(roles)
    return Node(
        id=fragment_id,
        node_type=NodeType.WORKFLOW,
        title=title or fragment_id,
        summary=text(fragment.get("interpretation")) or "Reusable role skeleton over repository-specific Actions.",
        repository=None,
        lifecycle="provisional",
        confidence=0.55,
        facets={
            "problem_class": "universal-workflow-skeleton",
            "workflow_kind": "role-skeleton",
            "reuse_scope": text(fragment.get("reuse_scope")),
            "supporting_categories": fragment.get("supporting_categories", []),
            "supporting_repositories": fragment.get("supporting_repositories", []),
        },
        payload=dict(fragment),
        provenance={"source": "action-factorization-audit", "stage": "materialize-workflow-fragment"},
    )


def materialize(graph: dict[str, Any], store: CatalogStore) -> dict[str, int]:
    policy = graph.get("extraction_policy") or {}
    if policy.get("holdout_refused") is not True:
        raise ValueError("graph must declare holdout_refused=true")
    action_rows = [dict(item) for item in graph.get("actions", []) if isinstance(item, dict)]
    workflow_rows = [dict(item) for item in graph.get("workflows", []) if isinstance(item, dict)]
    fragment_rows = [dict(item) for item in graph.get("workflow_fragments", []) if isinstance(item, dict)]
    pattern_rows = [dict(item) for item in graph.get("patterns", []) if isinstance(item, dict)]

    nodes: list[Node] = []
    nodes.extend(node_from_action(row) for row in action_rows if text(row.get("id")))
    nodes.extend(node_from_workflow(row) for row in workflow_rows if text(row.get("id")))
    nodes.extend(node_from_workflow_fragment(row) for row in fragment_rows if text(row.get("id")))
    nodes.extend(node_from_pattern(row) for row in pattern_rows if text(row.get("id")))

    with store.transaction():
        store.upsert_nodes(nodes, embed=True)

        # A Workflow step is a first-class bridge node.  This keeps the
        # schema-valid relation chain Workflow -> WorkflowStep -> Action while
        # preserving the partial-order edge type between actions.
        workflow_steps_by_action: dict[tuple[str, str], list[Node]] = {}
        for workflow in workflow_rows:
            workflow_id = text(workflow.get("id"))
            steps = [item for item in workflow.get("steps", []) if isinstance(item, dict)]
            step_nodes: dict[str, Node] = {}
            for step in steps:
                step_id = stable_id("workflow-step", workflow_id, text(step.get("step_id")))
                action_id = text(step.get("action_id"))
                step_node = Node(
                    id=step_id,
                    node_type=NodeType.WORKFLOW_STEP,
                    title=text(step.get("role") or step_id),
                    summary=f"{text(step.get('role') or 'implement')} {action_id}".strip(),
                    repository=text(workflow.get("repository")) or None,
                    lifecycle="provisional",
                    confidence=0.8,
                    facets={"problem_class": text(workflow.get("category"))},
                    payload={"workflow_id": workflow_id, "action_id": action_id, **step},
                    provenance={"source": "universal-resolution-graph", "stage": "materialize"},
                )
                store.upsert_node(step_node, embed=True)
                step_nodes[text(step.get("step_id"))] = step_node
                store.upsert_edge(Edge.create(workflow_id, step_id, RelationType.HAS_STEP, confidence=0.8))
                if action_id and store.get_node(action_id) is not None:
                    store.upsert_edge(Edge.create(step_id, action_id, RelationType.EXECUTED_BY, confidence=0.8))
                    workflow_steps_by_action.setdefault((workflow_id, action_id), []).append(
                        step_node
                    )

            for edge in workflow.get("edges", []):
                if not isinstance(edge, dict):
                    continue
                source_step = step_nodes.get(text(edge.get("from")))
                target_step = step_nodes.get(text(edge.get("to")))
                relation = RELATIONS.get(text(edge.get("type")), RelationType.REQUIRES)
                if source_step is None or target_step is None:
                    continue
                source_action = text(source_step.payload.get("action_id"))
                target_action = text(target_step.payload.get("action_id"))
                if source_action and target_action and store.get_node(source_action) and store.get_node(target_action):
                    store.upsert_edge(Edge.create(source_action, target_action, relation, confidence=0.75))

        for pattern in pattern_rows:
            pattern_id = text(pattern.get("id"))
            category = text(pattern.get("category"))
            template_rows = [
                dict(item)
                for item in pattern.get("action_template", [])
                if isinstance(item, dict)
            ]
            realization_rows = [
                dict(item)
                for item in pattern.get("workflow_realizations", [])
                if isinstance(item, dict)
            ]
            if template_rows:
                bindings_by_role: dict[str, set[tuple[str, str]]] = {}
                for realization in realization_rows:
                    workflow_id = text(realization.get("workflow_id"))
                    for binding in realization.get("role_bindings", []):
                        if not isinstance(binding, dict):
                            continue
                        role_id = text(binding.get("role_id"))
                        for action_id in binding.get("action_ids", []):
                            if role_id and text(action_id):
                                bindings_by_role.setdefault(role_id, set()).add(
                                    (workflow_id, text(action_id))
                                )

                for index, template in enumerate(template_rows, start=1):
                    role_id = text(template.get("role_id")) or f"role-{index}"
                    step_id = stable_id("pattern-step", pattern_id, role_id)
                    bindings = sorted(bindings_by_role.get(role_id, set()))
                    bound_action_ids = sorted({action_id for _workflow_id, action_id in bindings})
                    step = Node(
                        id=step_id,
                        node_type=NodeType.PATTERN_STEP,
                        title=text(template.get("title")) or f"{category} role {index}",
                        summary=text(template.get("purpose")) or f"Pattern role {role_id}",
                        lifecycle="provisional",
                        confidence=float(pattern.get("confidence") or 0.5),
                        facets={
                            "problem_class": category,
                            "role_id": role_id,
                            "required": bool(template.get("required")),
                        },
                        payload={
                            "pattern_id": pattern_id,
                            **template,
                            "role_id": role_id,
                            "bound_action_ids": bound_action_ids,
                        },
                        provenance={
                            "source": "universal-resolution-graph",
                            "stage": "materialize-semantic-pattern-role",
                        },
                    )
                    store.upsert_node(step, embed=True)
                    store.upsert_edge(
                        Edge.create(
                            pattern_id,
                            step_id,
                            RelationType.DECLARES_STEP,
                            confidence=step.confidence,
                        )
                    )
                    for workflow_id, action_id in bindings:
                        if store.get_node(action_id) is not None:
                            store.upsert_edge(
                                Edge.create(
                                    action_id,
                                    step_id,
                                    RelationType.CONFORMS_TO,
                                    confidence=step.confidence,
                                )
                            )
                        for workflow_step in workflow_steps_by_action.get(
                            (workflow_id, action_id), []
                        ):
                            store.upsert_edge(
                                Edge.create(
                                    workflow_step.id,
                                    step_id,
                                    RelationType.REALIZES,
                                    confidence=step.confidence,
                                )
                            )
            else:
                action_ids = [
                    text(value)
                    for value in list(pattern.get("mandatory_actions", []))
                    + list(pattern.get("optional_actions", []))
                    if text(value)
                ]
                for index, action_id in enumerate(dict.fromkeys(action_ids), start=1):
                    if store.get_node(action_id) is None:
                        continue
                    step_id = stable_id("pattern-step", pattern_id, action_id)
                    step = Node(
                        id=step_id,
                        node_type=NodeType.PATTERN_STEP,
                        title=f"{category} step {index}",
                        summary=f"Pattern step for {action_id}",
                        lifecycle="provisional",
                        confidence=0.5,
                        facets={"problem_class": category},
                        payload={
                            "pattern_id": pattern_id,
                            "action_id": action_id,
                            "optional": action_id in pattern.get("optional_actions", []),
                        },
                        provenance={
                            "source": "universal-resolution-graph",
                            "stage": "materialize",
                        },
                    )
                    store.upsert_node(step, embed=True)
                    store.upsert_edge(
                        Edge.create(
                            pattern_id,
                            step_id,
                            RelationType.DECLARES_STEP,
                            confidence=0.5,
                        )
                    )
                    store.upsert_edge(
                        Edge.create(
                            action_id,
                            step_id,
                            RelationType.CONFORMS_TO,
                            confidence=0.5,
                        )
                    )

            for workflow_id in pattern.get("supporting_workflows", []):
                workflow_id = text(workflow_id)
                if store.get_node(workflow_id) is not None:
                    store.upsert_edge(Edge.create(pattern_id, workflow_id, RelationType.SUPPORTED_BY, confidence=0.5))
                    store.upsert_edge(
                        Edge.create(
                            workflow_id,
                            pattern_id,
                            RelationType.INSTANTIATES,
                            confidence=0.5,
                        )
                    )

    stats = store.stats()
    node_counts = stats.get("nodes", {})
    return {
        "actions": len(action_rows),
        "workflows": len(workflow_rows),
        "workflow_fragments": len(fragment_rows),
        "patterns": len(pattern_rows),
        "nodes": sum(int(value) for value in node_counts.values()) if isinstance(node_counts, dict) else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--hnsw", type=Path)
    args = parser.parse_args()

    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    if not isinstance(graph, dict):
        raise TypeError("graph must be an object")
    args.db.parent.mkdir(parents=True, exist_ok=True)
    with CatalogStore(args.db) as store:
        store.initialize()
        counts = materialize(graph, store)
        hnsw_status = "not_requested"
        if args.hnsw:
            try:
                store.build_hnsw_index(args.hnsw)
                hnsw_status = "built"
            except Exception as exc:  # noqa: BLE001 - optional dependency is environment-specific
                hnsw_status = f"unavailable: {type(exc).__name__}: {exc}"
        payload = {"db": str(args.db), "hnsw": str(args.hnsw) if args.hnsw else None, "hnsw_status": hnsw_status, "counts": counts, "stats": store.stats()}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
