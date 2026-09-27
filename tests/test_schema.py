from __future__ import annotations

import unittest

from arex_skill_graph.schema import (
    Edge,
    NodeType,
    RelationType,
    validate_endpoint,
)


class SchemaTests(unittest.TestCase):
    def test_mvp_has_no_conflict_relation(self) -> None:
        self.assertNotIn("conflicts_with", {relation.value for relation in RelationType})

    def test_action_requires_action_is_valid(self) -> None:
        edge = Edge.create("a", "b", RelationType.REQUIRES)
        validate_endpoint(edge, NodeType.ACTION, NodeType.ACTION)

    def test_invalid_cross_level_endpoint_is_rejected(self) -> None:
        edge = Edge.create("a", "b", RelationType.DECLARES_STEP)
        with self.assertRaisesRegex(ValueError, "invalid endpoints"):
            validate_endpoint(edge, NodeType.ACTION, NodeType.COMMIT)


if __name__ == "__main__":
    unittest.main()

