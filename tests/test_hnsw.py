from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from arex_skill_graph.hnsw import HNSWMetadataError, HNSWUnavailable
from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.store import CatalogStore


class HNSWStoreTests(unittest.TestCase):
    def _catalog(self, root: Path) -> CatalogStore:
        store = CatalogStore(root / "catalog.db")
        store.initialize()
        with store.transaction():
            for index in range(24):
                repository = "repo/a" if index % 2 == 0 else "repo/b"
                node_type = NodeType.ACTION if index % 3 else NodeType.WORKFLOW
                store.upsert_node(
                    Node(
                        id=f"node:{index:02d}",
                        node_type=node_type,
                        title=f"{repository} session compaction tool execution case {index}",
                        summary=f"persist transcript and retry provider request for case {index}",
                        repository=repository,
                    )
                )
        return store

    def test_hnsw_round_trip_matches_exact_and_supports_filters(self) -> None:
        try:
            import hnswlib  # noqa: F401
        except ImportError:
            self.skipTest("optional hnswlib is not installed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self._catalog(root) as store:
                index_path = root / "routing.hnsw"
                store.build_hnsw_index(index_path, ef_search=128)
                exact = store.search_vector(
                    "session compaction retry provider", limit=8, vector_backend="exact"
                )
                approx = store.search_vector(
                    "session compaction retry provider",
                    limit=8,
                    vector_backend="hnsw",
                    hnsw_path=index_path,
                    hnsw_ef_search=128,
                    hnsw_oversample=8,
                )
                self.assertEqual([node.id for node, _ in exact], [node.id for node, _ in approx])

                filtered = store.search_vector(
                    "session compaction retry provider",
                    repository="repo/b",
                    node_types=[NodeType.ACTION],
                    limit=20,
                    vector_backend="hnsw",
                    hnsw_path=index_path,
                    hnsw_ef_search=128,
                    hnsw_oversample=8,
                )
                self.assertTrue(filtered)
                self.assertTrue(all(node.repository == "repo/b" for node, _ in filtered))
                self.assertTrue(all(node.node_type is NodeType.ACTION for node, _ in filtered))
                self.assertEqual(
                    [node.id for node, _ in filtered],
                    sorted(node.id for node, _ in filtered),
                    "tie ordering must be deterministic",
                ) if len({score for _, score in filtered}) == 1 else None


    def test_hnsw_filtered_search_returns_only_requested_skill_level(self) -> None:
        try:
            import hnswlib  # noqa: F401
        except ImportError:
            self.skipTest("optional hnswlib is not installed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = CatalogStore(root / "catalog.db")
            store.initialize()
            try:
                with store.transaction():
                    for node_type in (
                        NodeType.ATOMIC,
                        NodeType.WORKFLOW,
                        NodeType.PATTERN,
                    ):
                        for index in range(3):
                            store.upsert_node(
                                Node(
                                    id=f"{node_type.value}:{index}",
                                    node_type=node_type,
                                    title=f"{node_type.value} residual capacity policy {index}",
                                    summary="reserve output headroom and recompute request budget",
                                    repository="repo/levels",
                                )
                            )
                index_path = root / "levels.hnsw"
                store.build_hnsw_index(index_path, ef_search=128)
                for node_type in (
                    NodeType.ATOMIC,
                    NodeType.WORKFLOW,
                    NodeType.PATTERN,
                ):
                    hits = store.search_vector(
                        "residual capacity request budget",
                        node_types=[node_type],
                        limit=8,
                        vector_backend="hnsw",
                        hnsw_path=index_path,
                        hnsw_ef_search=128,
                        hnsw_oversample=8,
                    )
                    self.assertEqual(3, len(hits))
                    self.assertTrue(
                        all(node.node_type is node_type for node, _ in hits)
                    )
            finally:
                store.close()

    def test_hnsw_rejects_stale_catalog_inventory(self) -> None:
        try:
            import hnswlib  # noqa: F401
        except ImportError:
            self.skipTest("optional hnswlib is not installed")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self._catalog(root) as store:
                index_path = root / "routing.hnsw"
                store.build_hnsw_index(index_path)
                with store.transaction():
                    store.upsert_node(
                        Node(
                            id="node:new",
                            node_type=NodeType.ACTION,
                            title="new session action",
                            summary="newly added node makes the persisted index stale",
                            repository="repo/a",
                        )
                    )
                with self.assertRaises(HNSWMetadataError):
                    store.search_vector(
                        "new session action",
                        vector_backend="hnsw",
                        hnsw_path=index_path,
                    )


if __name__ == "__main__":
    unittest.main()
