from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "data" / "skill-extraction" / "cases"
PACKAGE = ROOT / "data" / "skill-extraction" / "packages" / "repair-shared-capacity-pressure"


class SkillExtractionArtifactTests(unittest.TestCase):
    def test_real_case_artifacts_are_parseable_and_have_provenance(self) -> None:
        case_dirs = sorted(path for path in CASES.iterdir() if path.is_dir())
        self.assertGreaterEqual(len(case_dirs), 4)
        for case_dir in case_dirs:
            case = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
            self.assertTrue(case["case_id"])
            self.assertTrue(case["repository"]["path"])
            self.assertTrue(case["evidence_units"])
            self.assertTrue(case["case_actions"])
            workflow = case["case_workflow"]
            self.assertTrue(workflow.get("steps") or workflow.get("step_order") or workflow.get("nodes"))
            self.assertTrue((case_dir / "evidence.md").read_text(encoding="utf-8").strip())
            self.assertTrue((case_dir / "candidate-skills.md").read_text(encoding="utf-8").strip())

    def test_workflow_package_has_progressive_disclosure_contract(self) -> None:
        skill_md = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill_md.startswith("---\n"))
        self.assertIn("name: repair-shared-capacity-pressure", skill_md)
        self.assertIn("description:", skill_md)
        self.assertIn("## Workflow", skill_md)
        self.assertIn("## Validation", skill_md)
        self.assertTrue((PACKAGE / "references" / "atomic" / "derive-policy-from-residual-capacity.md").exists())
        self.assertTrue((PACKAGE / "references" / "pattern.md").exists())
        self.assertTrue((PACKAGE / "references" / "evidence" / "hermes.md").exists())
        self.assertTrue((PACKAGE / "references" / "evidence" / "deepseek.md").exists())

    def test_manifest_records_level_and_promotion_gates(self) -> None:
        manifest = json.loads(
            (ROOT / "data" / "skill-extraction" / "synthesis" / "skill-family-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        levels = {item["level"] for item in manifest["knowledge_nodes"]}
        self.assertEqual({"atomic", "workflow", "pattern"}, levels)
        self.assertIn("held-out", manifest["promotion_gates"]["pattern_validated"])
        self.assertEqual("completed", manifest["independent_extraction_runs"][0]["status"])
        self.assertEqual(4, manifest["independent_extraction_runs"][0]["cases"])

    def test_residual_family_keeps_adjacent_alignments_separate(self) -> None:
        rejected = (
            ROOT / "data" / "skill-extraction" / "synthesis" / "residual-budget-family" / "rejected-alignments.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Pi", rejected)
        self.assertIn("Aider", rejected)
        self.assertIn("not a third residual-arithmetic proof", rejected)


if __name__ == "__main__":
    unittest.main()


