from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from arex_skill_graph.lifecycle import (
    DedupDecision, DedupProposal, FailureIncident, FailureKind,
    LifecycleManager, SkillLevel, SkillRecord, UsageEvent, UsageResult,
)
from arex_skill_graph.store import CatalogStore


class PersistentLifecycleTests(unittest.TestCase):
    def test_registry_and_audit_events_survive_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.sqlite"
            manager = LifecycleManager()
            atomic = SkillRecord("atomic:persist", SkillLevel.ATOMIC, "Reserve headroom", "Keep downstream output capacity reserved")
            peer = SkillRecord("atomic:peer", SkillLevel.ATOMIC, "Reserve output", "Keep downstream output capacity reserved")
            manager.add_candidate(atomic)
            manager.add_candidate(peer)
            manager.apply_dedup(DedupProposal(
                atomic.skill_id, peer.skill_id, DedupDecision.RELATED_BUT_DISTINCT,
                0.81, "LLM found related mechanisms but different applicability", evidence_ids=("commit:c1",)
            ))
            manager.record_usage(UsageEvent("usage:persist", atomic.skill_id, 1, "task:1", UsageResult.FAILURE, FailureKind.SKILL_LOGIC, "ctx:1"))
            manager.report_incident(FailureIncident("incident:persist", atomic.skill_id, "task:1", FailureKind.SKILL_LOGIC, "ctx:1", evidence_ids=("test:t1",)))
            with CatalogStore(path) as store:
                store.initialize()
                store.persist_lifecycle_manager(manager)
                self.assertEqual(2, len(store.load_skill_json()))
                self.assertEqual(1, store.connection.execute("SELECT COUNT(*) FROM skill_dedup_proposals").fetchone()[0])
                self.assertEqual(1, store.connection.execute("SELECT COUNT(*) FROM skill_usage_events").fetchone()[0])
                self.assertEqual(1, store.connection.execute("SELECT COUNT(*) FROM skill_failure_incidents").fetchone()[0])
            with CatalogStore(path) as reopened:
                reopened.initialize()
                loaded = reopened.load_skill_json()
                self.assertEqual(2, len(loaded))
                by_id = {item["skill_id"]: item for item in loaded}
                self.assertEqual(2, by_id["atomic:persist"]["usage"]["failure_by_kind"].get("skill_logic_failure", 0))


if __name__ == "__main__":
    unittest.main()


