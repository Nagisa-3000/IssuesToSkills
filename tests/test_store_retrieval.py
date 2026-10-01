from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import Edge, Node, NodeType, RelationType
from arex_skill_graph.store import CatalogStore


class StoreRetrievalTests(unittest.TestCase):
    def test_reverse_requires_recovers_prerequisite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                prerequisite = Node(
                    id="action:initialize",
                    node_type=NodeType.ACTION,
                    title="initialize one extension runtime per extension root",
                    summary="construct the shared runtime before registering extension tools",
                    repository="example/harness",
                )
                dependent = Node(
                    id="action:deduplicate",
                    node_type=NodeType.ACTION,
                    title="prevent duplicate extension runtimes",
                    summary="reuse the canonical runtime when loading an extension twice",
                    repository="example/harness",
                )
                with store.transaction():
                    store.upsert_node(prerequisite)
                    store.upsert_node(dependent)
                    store.upsert_edge(
                        Edge.create(
                            prerequisite.id,
                            dependent.id,
                            RelationType.REQUIRES,
                        )
                    )

                response = SkillRetriever(store).search(
                    "prevent duplicate extension runtimes",
                    top_k=10,
                    expand_hops=1,
                )
                ids = {hit.node.id for hit in response.hits}
                self.assertIn(dependent.id, ids)
                self.assertIn(prerequisite.id, ids)
                prerequisite_hit = next(
                    hit for hit in response.hits if hit.node.id == prerequisite.id
                )
                self.assertIn("prerequisite_closure", prerequisite_hit.sources)

    def test_same_level_only_keeps_graph_neighbors_out_of_peer_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                atomic = Node(
                    id="atomic:budget",
                    node_type=NodeType.ATOMIC,
                    title="derive residual capacity budget",
                    summary="compute the remaining shared capacity before compaction",
                    repository="example/harness",
                )
                workflow = Node(
                    id="workflow:compaction",
                    node_type=NodeType.WORKFLOW,
                    title="repair shared capacity compaction pressure",
                    summary="recompute the policy and validate the boundary",
                    repository="example/harness",
                )
                with store.transaction():
                    store.upsert_node(atomic)
                    store.upsert_node(workflow)
                    store.upsert_edge(Edge.create(workflow.id, atomic.id, RelationType.CONTAINS))

                response = SkillRetriever(store).search(
                    "derive residual capacity budget",
                    node_types=[NodeType.ATOMIC],
                    top_k=10,
                    expand_hops=1,
                    same_level_only=True,
                )
                self.assertTrue(response.hits)
                self.assertTrue(all(hit.node.node_type is NodeType.ATOMIC for hit in response.hits))
                self.assertIn(atomic.id, {hit.node.id for hit in response.hits})

                expanded = SkillRetriever(store).search(
                    "derive residual capacity budget",
                    node_types=[NodeType.ATOMIC],
                    top_k=10,
                    expand_hops=1,
                )
                self.assertIn(workflow.id, {hit.node.id for hit in expanded.hits})

    def test_fts_and_vector_channels_are_both_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                node = Node(
                    id="action:session",
                    node_type=NodeType.ACTION,
                    title="persist session messages exactly once",
                    summary="avoid duplicate transcript rows after compaction",
                    repository="example/harness",
                )
                with store.transaction():
                    store.upsert_node(node)
                response = SkillRetriever(store).search(
                    "duplicate session transcript after compaction"
                )
                hit = next(hit for hit in response.hits if hit.node.id == node.id)
                self.assertIn("lexical", hit.sources)
                self.assertIn("vector", hit.sources)


    def test_multilevel_search_filters_seeds_and_expands_contains_edges(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                atomic = Node(
                    id="atomic:budget",
                    node_type=NodeType.ATOMIC,
                    title="derive residual request budget",
                    summary="subtract mandatory reservations from shared capacity",
                    repository="example/harness",
                )
                workflow = Node(
                    id="workflow:repair",
                    node_type=NodeType.WORKFLOW,
                    title="repair shared-capacity pressure accounting",
                    summary="normalize reservations then recompute the pressure threshold",
                    repository="example/harness",
                )
                pattern = Node(
                    id="pattern:residual",
                    node_type=NodeType.PATTERN,
                    title="derive policies from residual capacity",
                    summary="base control policies on capacity remaining after reservations",
                    repository="example/harness",
                )
                with store.transaction():
                    for node in (atomic, workflow, pattern):
                        store.upsert_node(node)
                    store.upsert_edge(
                        Edge.create(workflow.id, atomic.id, RelationType.CONTAINS)
                    )
                    store.upsert_edge(
                        Edge.create(pattern.id, workflow.id, RelationType.CONTAINS)
                    )

                retriever = SkillRetriever(store)
                for node in (atomic, workflow, pattern):
                    response = retriever.search(
                        f"{node.title} {node.summary}",
                        node_types=[node.node_type],
                        top_k=8,
                        expand_hops=0,
                    )
                    self.assertIn(node.id, [hit.node.id for hit in response.hits])
                    self.assertTrue(
                        all(hit.node.node_type is node.node_type for hit in response.hits)
                    )

                response = retriever.search(
                    "subtract mandatory reservations from shared capacity",
                    node_types=[NodeType.ATOMIC],
                    top_k=8,
                    expand_hops=2,
                )
                seeded = [
                    hit for hit in response.hits
                    if "lexical" in hit.sources or "vector" in hit.sources
                ]
                self.assertTrue(seeded)
                self.assertTrue(
                    all(hit.node.node_type is NodeType.ATOMIC for hit in seeded)
                )
                ids = {hit.node.id for hit in response.hits}
                self.assertIn(atomic.id, ids)
                self.assertIn(workflow.id, ids)
                self.assertIn(pattern.id, ids)
                self.assertGreaterEqual(response.expanded_count, 2)
                self.assertTrue(
                    any("--contains/" in trace for hit in response.hits for trace in hit.trace)
                )

    def test_unpromoted_empty_pattern_is_not_reported_as_unresolved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                pattern = Node(
                    id="pattern:pending",
                    node_type=NodeType.PATTERN,
                    title="pending cross-repository pattern",
                    summary="awaits enough mandatory action support",
                    repository=None,
                    payload={
                        "mandatory_actions": [],
                        "promotion_status": "insufficient-structural-support",
                    },
                )
                with store.transaction():
                    store.upsert_node(pattern)

                response = SkillRetriever(store).search(
                    "pending cross-repository pattern",
                    top_k=4,
                    expand_hops=1,
                )
                self.assertIn(pattern.id, {hit.node.id for hit in response.hits})
                self.assertEqual([], response.unresolved)


if __name__ == "__main__":
    unittest.main()

