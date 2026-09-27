from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from arex_skill_graph.multilevel_validation import validate_semantics


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "multilevel-skill-family-v1.schema.json"
TEMPLATE_PATH = (
    ROOT
    / "data"
    / "skill-extraction"
    / "templates"
    / "multilevel-skill-family-v1.template.json"
)


class MultiLevelSkillSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def schema_errors(self, value: dict) -> list:
        return list(self.validator.iter_errors(value))

    def test_schema_is_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.schema)

    def test_template_passes_structural_and_semantic_validation(self) -> None:
        self.assertEqual([], self.schema_errors(self.template))
        report = validate_semantics(self.template)
        self.assertEqual([], report.errors)

    def test_invalid_epistemic_status_is_rejected(self) -> None:
        bundle = deepcopy(self.template)
        bundle["task_family"]["definition"]["epistemic_status"] = "assumed"
        self.assertTrue(self.schema_errors(bundle))

    def test_pattern_with_one_supporting_workflow_is_rejected(self) -> None:
        bundle = deepcopy(self.template)
        bundle["patterns"][0]["supporting_workflow_ids"] = ["workflow:harness-a-budget"]
        self.assertTrue(self.schema_errors(bundle))

    def test_dangling_evidence_is_rejected_semantically(self) -> None:
        bundle = deepcopy(self.template)
        bundle["atomic_skills"][0]["evidence_ids"].append("evidence:missing")
        report = validate_semantics(bundle)
        self.assertIn("dangling_evidence", {issue.code for issue in report.errors})

    def test_workflow_ordering_cycle_is_rejected_semantically(self) -> None:
        bundle = deepcopy(self.template)
        workflow = bundle["workflows"][0]
        first = workflow["steps"][0]
        second = deepcopy(first)
        second["id"] = "step:harness-a-budget-validate"
        workflow["steps"].append(second)
        workflow["edges"] = [
            {
                "id": "workflow_edge:a-before-b",
                "source_step_id": first["id"],
                "target_step_id": second["id"],
                "relation": "precedes",
            },
            {
                "id": "workflow_edge:b-before-a",
                "source_step_id": second["id"],
                "target_step_id": first["id"],
                "relation": "precedes",
            },
        ]
        report = validate_semantics(bundle)
        self.assertIn("ordering_cycle", {issue.code for issue in report.errors})

    def test_validated_pattern_without_held_out_result_is_rejected(self) -> None:
        bundle = deepcopy(self.template)
        bundle["patterns"][0]["lifecycle"] = "validated"
        self.assertTrue(self.schema_errors(bundle))
        report = validate_semantics(bundle)
        self.assertIn("invalid_validated_pattern", {issue.code for issue in report.errors})

    def test_quality_overall_cannot_hide_weakest_dimension(self) -> None:
        bundle = deepcopy(self.template)
        bundle["patterns"][0]["quality"]["overall"] = 0.99
        report = validate_semantics(bundle)
        self.assertIn("inflated_confidence", {issue.code for issue in report.errors})


if __name__ == "__main__":
    unittest.main()
