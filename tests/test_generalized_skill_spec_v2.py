from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "generalized-skill-family-v2.schema.json"


class GeneralizedSkillSpecV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.defs = cls.schema["$defs"]

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_instance_and_knowledge_planes_are_separate(self) -> None:
        required = set(self.schema["required"])
        self.assertTrue(
            {
                "evidence_units",
                "case_actions",
                "case_workflows",
                "atomic_skills",
                "workflow_skills",
                "patterns",
                "bindings",
            }.issubset(required)
        )

    def test_atomic_is_a_problem_solution_primitive_not_a_patch(self) -> None:
        required = set(self.defs["atomicSkill"]["required"])
        self.assertTrue(
            {
                "problem_signature",
                "problem_mechanism",
                "preconditions",
                "exclusions",
                "required_inputs",
                "produced_outputs",
                "solution_principle",
                "procedure",
                "preserved_invariants",
                "validation_oracles",
                "counterexamples",
                "realizations",
            }.issubset(required)
        )

    def test_workflow_steps_have_state_and_control_flow_contracts(self) -> None:
        required = set(self.defs["workflowStep"]["required"])
        self.assertTrue(
            {
                "kind",
                "semantic_goal",
                "requires",
                "uses_atomic_skill_ids",
                "produces",
                "guard",
                "on_success",
                "on_failure",
                "validation",
            }.issubset(required)
        )

    def test_agent_skill_package_uses_progressive_disclosure(self) -> None:
        package = self.defs["agentSkillPackage"]
        self.assertEqual(64, package["properties"]["name"]["maxLength"])
        self.assertEqual(1024, package["properties"]["description"]["maxLength"])
        self.assertGreaterEqual(package["properties"]["evals"]["minItems"], 3)
        self.assertIn("resources", package["required"])
        self.assertIn("skill_md_sections", package["required"])


if __name__ == "__main__":
    unittest.main()
