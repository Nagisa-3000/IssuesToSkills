from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from arex_skill_graph.lifecycle import LifecycleManager, SkillLevel, SkillRecord, SkillStatus
from arex_skill_graph.store import CatalogStore
from experiments.run_closed_loop_feedback import (
    build_parser,
    run_experiment,
    skill_record_from_json,
)


class ClosedLoopFeedbackScriptTests(unittest.TestCase):
    def test_restores_record_and_runs_offline_feedback_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db = root / "skill-catalog.sqlite"
            output = root / "evidence"
            manager = LifecycleManager()
            manager.add_candidate(SkillRecord(
                skill_id="atomic:reserve-headroom",
                level=SkillLevel.ATOMIC,
                title="Reserve downstream headroom",
                summary="subtract mandatory output reservations before applying a policy",
                status=SkillStatus.ACTIVE,
                evidence_ids={"issue:1", "test:1"},
            ))
            with CatalogStore(db) as store:
                store.initialize()
                store.persist_lifecycle_manager(manager)

            args = build_parser().parse_args([
                "--db", str(db),
                "--output", str(output),
                "--offline",
            ])
            evidence = run_experiment(args)

            self.assertEqual(1, evidence["restored"]["records"])
            self.assertIsNotNone(evidence["retrieval_and_use"]["success"]["usage_event"])
            self.assertEqual("success", evidence["retrieval_and_use"]["success"]["usage_event"]["result"])
            self.assertEqual("failure", evidence["retrieval_and_use"]["failure"]["usage_event"]["result"])
            self.assertIsNotNone(evidence["feedback"]["revision_id"])
            self.assertEqual("active", evidence["feedback"]["resulting_status"])
            self.assertEqual(3, len(evidence["llm"]["calls"]))
            self.assertEqual(2, len(evidence["runtime_persistence"]["usage_events"]))
            self.assertEqual(1, len(evidence["runtime_persistence"]["failure_incidents"]))
            self.assertTrue((output / "closed-loop-evidence.json").exists())

            persisted = json.loads((output / "closed-loop-evidence.json").read_text())
            self.assertNotIn("api_key", json.dumps(persisted))

    def test_skill_record_loader_preserves_lifecycle_fields(self) -> None:
        record = skill_record_from_json({
            "skill_id": "atomic:x",
            "level": "atomic",
            "title": "X",
            "summary": "Y",
            "status": "quarantined",
            "parent_ids": ["workflow:w"],
            "usage": {
                "attempts": 2,
                "failures": 1,
                "failure_by_kind": {"skill_logic_failure": 1},
                "independent_failure_contexts": ["ctx:1"],
            },
        })
        self.assertEqual(SkillStatus.QUARANTINED, record.status)
        self.assertEqual({"workflow:w"}, record.parent_ids)
        self.assertEqual(1, record.usage.failure_by_kind["skill_logic_failure"])
        self.assertEqual({"ctx:1"}, record.usage.independent_failure_contexts)


if __name__ == "__main__":
    unittest.main()
