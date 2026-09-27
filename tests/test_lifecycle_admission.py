from __future__ import annotations

import json
import tempfile
import unittest
from jsonschema import Draft202012Validator
from pathlib import Path

from arex_skill_graph.admission import BottomUpSkillAdmission, SkillCandidateRetriever
from arex_skill_graph.lifecycle import (
    DedupDecision,
    DedupProposal,
    FailureIncident,
    FailureKind,
    LifecycleManager,
    LifecyclePolicy,
    SkillLevel,
    SkillRecord,
    SkillStatus,
    UsageEvent,
    UsageResult,
)
from arex_skill_graph.store import CatalogStore


def skill(skill_id: str, level: SkillLevel, title: str, summary: str, **kwargs: object) -> SkillRecord:
    return SkillRecord(skill_id=skill_id, level=level, title=title, summary=summary, **kwargs)



class LifecycleSchemaTests(unittest.TestCase):
    def test_lifecycle_schema_is_valid_draft_2020_12(self) -> None:
        path = Path(__file__).resolve().parents[1] / "schemas" / "skill-lifecycle-v1.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
class LifecycleTests(unittest.TestCase):
    def test_exact_duplicate_aliases_without_deleting_evidence(self) -> None:
        manager = LifecycleManager()
        old = skill("atomic:old", SkillLevel.ATOMIC, "Residual capacity", "Subtract reservation before policy")
        new = skill(
            "atomic:new",
            SkillLevel.ATOMIC,
            "Reserve output first",
            "Subtract output reservation before policy",
            evidence_ids={"evidence:new"},
        )
        manager.add_candidate(old)
        manager.add_candidate(new)
        result = manager.apply_dedup(
            DedupProposal(
                "atomic:new",
                "atomic:old",
                DedupDecision.EXACT_DUPLICATE,
                0.98,
                "same residual-capacity invariant and same boundary",
            )
        )
        self.assertIs(result, old)
        self.assertEqual(SkillStatus.MERGED, new.status)
        self.assertIn("atomic:new", old.aliases)
        self.assertIn("evidence:new", old.evidence_ids)

    def test_merge_creates_version_and_preserves_old_nodes(self) -> None:
        manager = LifecycleManager()
        left = skill("workflow:left", SkillLevel.WORKFLOW, "Repair budget", "Normalize then recompute")
        right = skill("workflow:right", SkillLevel.WORKFLOW, "Repair capacity", "Normalize then recompute")
        manager.add_candidate(left)
        manager.add_candidate(right)
        merged = manager.apply_dedup(
            DedupProposal(
                "workflow:right",
                "workflow:left",
                DedupDecision.MERGEABLE,
                0.96,
                "same control flow, complementary evidence",
            )
        )
        assert merged is not None
        self.assertEqual("workflow:left@v2", merged.skill_id)
        self.assertEqual(SkillStatus.SUPERSEDED, left.status)
        self.assertEqual(SkillStatus.SUPERSEDED, right.status)
        self.assertEqual({"workflow:left", "workflow:right"}, merged.merged_from)

    def test_independent_logic_failures_quarantine_and_revalidate_parent(self) -> None:
        manager = LifecycleManager(LifecyclePolicy(quarantine_after_independent_failures=3))
        atomic = skill("atomic:a", SkillLevel.ATOMIC, "A", "A")
        workflow = skill("workflow:w", SkillLevel.WORKFLOW, "W", "W")
        manager.add_candidate(atomic)
        manager.add_candidate(workflow)
        manager.attach_parent("atomic:a", "workflow:w")
        for index in range(3):
            decision = manager.report_incident(
                FailureIncident(
                    f"incident:{index}",
                    "atomic:a",
                    f"task:{index}",
                    FailureKind.SKILL_LOGIC,
                    f"context:{index}",
                    severity="high",
                )
            )
        self.assertTrue(decision.review_required)
        self.assertEqual(SkillStatus.CANDIDATE, decision.current_status)
        self.assertEqual(("workflow:w",), decision.parent_ids_needing_revalidation)
        manager.apply_llm_lifecycle_decision("atomic:a", status=SkillStatus.QUARANTINED, rationale="LLM found the residual-capacity method invalid across three independent cases")
        self.assertEqual(SkillStatus.QUARANTINED, atomic.status)

    def test_non_logic_failure_does_not_quarantine(self) -> None:
        manager = LifecycleManager()
        atomic = skill("atomic:a", SkillLevel.ATOMIC, "A", "A")
        manager.add_candidate(atomic)
        manager.record_usage(
            UsageEvent(
                "usage:1",
                "atomic:a",
                1,
                "task:1",
                UsageResult.FAILURE,
                FailureKind.RETRIEVAL,
                "context:1",
            )
        )
        self.assertEqual(SkillStatus.CANDIDATE, manager.health("atomic:a").current_status)


class BottomUpAdmissionTests(unittest.TestCase):
    def test_bm25_and_embedding_retrieve_only_same_level_then_llm_orders_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with CatalogStore(Path(tmp) / "catalog.sqlite") as store:
                store.initialize()
                manager = LifecycleManager()
                retriever = SkillCandidateRetriever(store)
                existing_atomic = skill(
                    "atomic:existing",
                    SkillLevel.ATOMIC,
                    "Residual capacity reservation",
                    "Subtract mandatory output headroom before pressure policy",
                )
                existing_workflow = skill(
                    "workflow:existing",
                    SkillLevel.WORKFLOW,
                    "Residual capacity workflow",
                    "Normalize reservation and recompute pressure policy",
                )
                manager.add_candidate(existing_atomic)
                manager.add_candidate(existing_workflow)
                retriever.index(existing_atomic)
                retriever.index(existing_workflow)
                new_atomic = skill(
                    "atomic:new",
                    SkillLevel.ATOMIC,
                    "Output reservation capacity",
                    "Subtract mandatory output headroom before pressure policy",
                )
                candidates = retriever.find(new_atomic, limit=10)
                self.assertEqual(("atomic:existing",), tuple(item.skill_id for item in candidates))

                calls: list[str] = []

                def judge(candidate: SkillRecord, peer: SkillRecord) -> DedupProposal:
                    calls.append(candidate.level.value)
                    if candidate.level is SkillLevel.ATOMIC:
                        return DedupProposal(candidate.skill_id, peer.skill_id, DedupDecision.EXACT_DUPLICATE, 0.99, "same mechanism")
                    return DedupProposal(candidate.skill_id, peer.skill_id, DedupDecision.NO_MATCH, 0.20, "distinct")

                def workflow_extractor(resolved: SkillRecord):
                    calls.append("extract-workflow")
                    yield skill(
                        "workflow:new",
                        SkillLevel.WORKFLOW,
                        "Repair shared capacity",
                        "Normalize, recompute, and validate",
                        payload={"atomic_ids": [resolved.skill_id]},
                    )

                def pattern_extractor(resolved: SkillRecord):
                    calls.append("extract-pattern")
                    yield skill(
                        "pattern:new",
                        SkillLevel.PATTERN,
                        "Residual budget invariant",
                        "Reserve downstream capacity before upstream policy",
                        payload={"workflow_ids": [resolved.skill_id]},
                    )

                result = BottomUpSkillAdmission(manager, retriever, judge=judge).insert_atomic(
                    new_atomic,
                    workflow_extractor=workflow_extractor,
                    pattern_extractor=pattern_extractor,
                )
                self.assertEqual("atomic:existing", result.atomic.resolved_id)
                self.assertEqual(("workflow:new",), tuple(item.resolved_id for item in result.workflows))
                self.assertEqual(("pattern:new",), tuple(item.resolved_id for item in result.patterns))
                self.assertEqual(["atomic", "extract-workflow", "workflow", "extract-pattern"], calls)
                self.assertIn("workflow:new", manager.get("atomic:existing").parent_ids)
                self.assertIn("pattern:new", manager.get("workflow:new").parent_ids)


if __name__ == "__main__":
    unittest.main()






