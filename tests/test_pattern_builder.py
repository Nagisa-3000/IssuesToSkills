from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from arex_skill_graph.mining.pattern import PatternCandidateBuilder
from arex_skill_graph.schema import Edge, Node, NodeType, RelationType, stable_id
from arex_skill_graph.store import CatalogStore


class PatternCandidateBuilderTests(unittest.TestCase):
    def test_requires_two_repositories_and_emits_typed_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with CatalogStore(Path(directory) / "catalog.db") as store:
                store.initialize()
                workflows = []
                nodes = []
                edges = []
                for repository in ("repo-a", "repo-b"):
                    workflow = Node(
                        id=stable_id("workflow", repository),
                        node_type=NodeType.WORKFLOW,
                        title=f"{repository} provider change",
                        summary="provider adapter workflow",
                        repository=repository,
                        lifecycle="reviewed",
                        facets={"domain": "model_provider_adapter"},
                    )
                    step = Node(
                        id=stable_id("workflow_step", repository),
                        node_type=NodeType.WORKFLOW_STEP,
                        title=f"{repository} normalize",
                        summary="implement provider normalization",
                        repository=repository,
                        lifecycle="reviewed",
                        facets={"domain": "model_provider_adapter", "role": "implement"},
                    )
                    action = Node(
                        id=stable_id("action", repository),
                        node_type=NodeType.ACTION,
                        title=f"{repository} action",
                        summary="normalize provider contract",
                        repository=repository,
                        lifecycle="reviewed",
                    )
                    workflows.append(workflow)
                    nodes.extend((workflow, step, action))
                    edges.extend(
                        (
                            Edge.create(workflow.id, step.id, RelationType.HAS_STEP),
                            Edge.create(step.id, action.id, RelationType.EXECUTED_BY),
                        )
                    )
                with store.transaction():
                    store.upsert_nodes(nodes)
                    for edge in edges:
                        store.upsert_edge(edge)

                report = PatternCandidateBuilder().build_to_store(store)
                patterns = store.list_nodes(node_types=[NodeType.PATTERN])
                pattern_steps = store.list_nodes(node_types=[NodeType.PATTERN_STEP])
                predicates = store.list_nodes(node_types=[NodeType.PREDICATE])

            self.assertEqual(report.candidates_built, 1)
            self.assertEqual(report.skipped_insufficient_support, 6)
            self.assertEqual(len(patterns), 1)
            self.assertEqual(len(pattern_steps), 3)
            self.assertEqual(len(predicates), 3)
            self.assertEqual(report.workflow_support_edges, 4)
            self.assertEqual(report.workflow_step_realizations, 2)
            self.assertEqual(report.action_conformance_edges, 2)
            self.assertEqual(
                set(patterns[0].payload["supporting_repositories"]),
                {"repo-a", "repo-b"},
            )

    def test_single_repository_family_is_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with CatalogStore(Path(directory) / "catalog.db") as store:
                store.initialize()
                workflow = Node(
                    id="workflow:one",
                    node_type=NodeType.WORKFLOW,
                    title="one",
                    summary="one",
                    repository="only-repo",
                    facets={"domain": "model_provider_adapter"},
                )
                store.upsert_node(workflow)
                report = PatternCandidateBuilder().build_to_store(store)
                self.assertEqual(report.candidates_built, 0)
                self.assertEqual(store.stats()["nodes"].get("pattern", 0), 0)


if __name__ == "__main__":
    unittest.main()

