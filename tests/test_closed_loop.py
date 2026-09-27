from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from arex_skill_graph.admission import SkillCandidateRetriever
from arex_skill_graph.closed_loop import ClosedLoopEngine
from arex_skill_graph.lifecycle import (
    FailureKind,
    LifecycleManager,
    SkillLevel,
    SkillRecord,
    SkillStatus,
    UsageResult,
)
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.store import CatalogStore


class FakeTransport:
    def __init__(self, selected: str | None, review: dict) -> None:
        self.selected = selected
        self.review = review
        self.calls: list[str] = []

    def complete(self, *, system: str, user: str, response_schema):
        payload = json.loads(user)
        operation = payload["operation"]
        self.calls.append(operation)
        if operation == "judge_retrieval_use":
            return {
                "selected_skill_id": self.selected,
                "applicable": self.selected is not None,
                "confidence": 0.97,
                "rationale": "candidate matches the required operation and preconditions",
                "missing_preconditions": [],
            }
        if operation == "failure_review":
            return self.review
        raise AssertionError(operation)


def active_atomic(skill_id: str = "atomic:reserve") -> SkillRecord:
    return SkillRecord(
        skill_id=skill_id,
        level=SkillLevel.ATOMIC,
        title="Reserve residual capacity",
        summary="Subtract the downstream reservation before applying the policy",
        status=SkillStatus.ACTIVE,
        evidence_ids={"issue:1", "test:1"},
        preconditions=("residual capacity is available",),
    )


class ClosedLoopTests(unittest.TestCase):
    def _engine(self, root: Path, transport: FakeTransport, *, hnsw: bool = False):
        store = CatalogStore(root / "catalog.sqlite")
        store.initialize()
        manager = LifecycleManager()
        record = active_atomic()
        manager.add_candidate(record)
        candidate_index = SkillCandidateRetriever(store)
        candidate_index.index(record)
        store.persist_lifecycle_manager(manager)
        engine = ClosedLoopEngine(
            manager,
            SkillRetriever(store),
            LLMGovernanceAdapter(
                transport,
                GovernanceContext(repository="repo", model="fake", prompt_version="test"),
            ),
            candidate_index=candidate_index,
            store=store,
            hnsw_path=str(root / "routing.hnsw") if hnsw else None,
        )
        return store, manager, engine

    def test_judge_can_only_use_returned_active_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transport = FakeTransport("atomic:reserve", {"recommended_status": "active", "root_cause": "none"})
            store, manager, engine = self._engine(root, transport)
            with store:
                outcome = engine.use(
                    "subtract reservation before residual capacity policy",
                    task_id="task:success",
                )
                self.assertEqual("atomic:reserve", outcome.selected_skill_id)
                self.assertIsNotNone(outcome.usage_event)
                self.assertEqual(1, manager.get("atomic:reserve").usage.successes)
                self.assertEqual(["judge_retrieval_use"], transport.calls)

    def test_failure_feedback_creates_revision_detaches_old_projection_and_rebuilds_hnsw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transport = FakeTransport(
                "atomic:reserve",
                {
                    "failure_class": "stale_skill",
                    "root_cause": "the provider usage shape changed",
                    "recommended_status": "active",
                    "revision": {
                        "title": "Reserve residual capacity with canonical usage",
                        "summary": "Normalize provider usage before applying the reservation policy",
                        "payload": {"updated_by": "failure-review"},
                    },
                },
            )
            store, manager, engine = self._engine(root, transport, hnsw=True)
            workflow = SkillRecord(
                "workflow:reserve",
                SkillLevel.WORKFLOW,
                "Reserve before policy",
                "Reserve, normalize, then apply policy",
                status=SkillStatus.ACTIVE,
            )
            manager.add_candidate(workflow)
            manager.attach_parent("atomic:reserve", "workflow:reserve")
            candidate_index = SkillCandidateRetriever(store)
            candidate_index.index(workflow)
            with store:
                store.persist_lifecycle_manager(manager)
                outcome = engine.use(
                    "subtract reservation before residual capacity policy",
                    task_id="task:failure",
                    result=UsageResult.FAILURE,
                    failure_kind=FailureKind.SKILL_LOGIC,
                    independent_context_id="context:one",
                )
                feedback = engine.report_failure(outcome, evidence_ids=("incident:e1",))
                self.assertEqual("atomic:reserve@v2", feedback.revision_id)
                self.assertEqual(SkillStatus.SUPERSEDED, manager.get("atomic:reserve").status)
                revision = manager.get("atomic:reserve@v2")
                self.assertEqual(SkillStatus.ACTIVE, revision.status)
                self.assertEqual({"workflow:reserve"}, manager.get("atomic:reserve").parent_ids)
                self.assertEqual({"workflow:reserve"}, revision.parent_ids)
                self.assertTrue((root / "routing.hnsw").exists())
                self.assertEqual(1, manager.get("atomic:reserve").usage.failures)
                self.assertEqual(1, len(manager.incidents))
                edges = store.connection.execute(
                    "SELECT source_id, target_id FROM edges WHERE relation = 'contains'"
                ).fetchall()
                self.assertIn(("workflow:reserve", "atomic:reserve@v2"), [(r[0], r[1]) for r in edges])
                self.assertNotIn(("workflow:reserve", "atomic:reserve"), [(r[0], r[1]) for r in edges])
                self.assertEqual("superseded", store.get_node("atomic:reserve").lifecycle)
                self.assertEqual("active", store.get_node("atomic:reserve@v2").lifecycle)

    def test_incident_after_failure_usage_is_not_double_counted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transport = FakeTransport(
                "atomic:reserve",
                {
                    "failure_class": "skill_logic_failure",
                    "root_cause": "bad invariant",
                    "recommended_status": "quarantined",
                    "revision": None,
                },
            )
            store, manager, engine = self._engine(root, transport)
            with store:
                outcome = engine.use(
                    "subtract reservation before residual capacity policy",
                    task_id="task:double",
                    result=UsageResult.FAILURE,
                    failure_kind=FailureKind.SKILL_LOGIC,
                    independent_context_id="context:one",
                )
                engine.report_failure(outcome, incident_id="incident:double", review=True)
                self.assertEqual(1, manager.get("atomic:reserve").usage.failures)
                self.assertEqual(1, manager.get("atomic:reserve").usage.failure_by_kind[FailureKind.SKILL_LOGIC.value])
                self.assertEqual(SkillStatus.QUARANTINED, manager.get("atomic:reserve").status)
                self.assertEqual(set(), manager.get("atomic:reserve").parent_ids)


if __name__ == "__main__":
    unittest.main()
