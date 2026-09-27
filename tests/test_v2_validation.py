from __future__ import annotations

import json
from pathlib import Path
import unittest

from arex_skill_graph.v2_validation import validate_v2_bundle

ROOT = Path(__file__).resolve().parents[1]


class V2BundleValidationTests(unittest.TestCase):
    def test_curated_bundle_is_schema_and_reference_valid(self) -> None:
        bundle_path = ROOT / "data" / "skill-extraction" / "synthesis" / "residual-budget-family" / "bundle.json"
        schema_path = ROOT / "schemas" / "generalized-skill-family-v2.schema.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        report = validate_v2_bundle(bundle, schema)
        self.assertTrue(report.valid, report.errors)
        self.assertGreaterEqual(len(report.warnings), 1)
        self.assertTrue(any(w["code"] == "transfer_not_run" for w in report.warnings))
        self.assertEqual("candidate", bundle["patterns"][0]["lifecycle"])
        self.assertTrue(bundle["extraction"]["llm_semantic_reading_required"])

    def test_validator_rejects_dangling_tree_edge_without_semantic_inference(self) -> None:
        bundle_path = ROOT / "data" / "skill-extraction" / "synthesis" / "residual-budget-family" / "bundle.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        bundle["relations"].append({
            "id": "relation:bad",
            "source_id": "atomic:missing",
            "target_id": "workflow:reserve-output-before-pressure-policy",
            "relation": "part_of",
            "confidence": 1.0,
            "rationale": "test",
            "evidence_ids": [],
        })
        report = validate_v2_bundle(bundle)
        self.assertFalse(report.valid)
        self.assertTrue(any(e["code"] == "dangling_relation" for e in report.errors))


if __name__ == "__main__":
    unittest.main()
