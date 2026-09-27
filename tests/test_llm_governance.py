from __future__ import annotations

import unittest

from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.lifecycle import DedupDecision, SkillLevel, SkillRecord


class FakeTransport:
    def __init__(self):
        self.calls = []

    def complete(self, *, system, user, response_schema):
        self.calls.append((system, user, response_schema))
        if '"operation": "deduplicate"' in user:
            return {"decision": "related_but_distinct", "confidence": 0.8, "rationale": "different preconditions", "evidence_ids": ["diff:1"]}
        if 'extract_workflow' in user:
            return {"skills": [{"skill_id": "workflow:1", "title": "Compose capacity repair", "summary": "Reserve and recompute", "evidence_ids": ["diff:1"]}]}
        return {"failure_class": "applicability", "root_cause": "missing precondition", "recommended_status": "suspect"}


class LLMGovernanceAdapterTests(unittest.TestCase):
    def test_semantic_decision_and_extraction_are_provider_responses(self):
        transport = FakeTransport()
        adapter = LLMGovernanceAdapter(transport, GovernanceContext(model="test-model"))
        atomic = SkillRecord("atomic:1", SkillLevel.ATOMIC, "Reserve", "Reserve output headroom")
        peer = SkillRecord("atomic:2", SkillLevel.ATOMIC, "Reserve", "Reserve output headroom")
        proposal = adapter.judge(atomic, peer)
        self.assertIs(DedupDecision.RELATED_BUT_DISTINCT, proposal.decision)
        workflows = adapter.extract(SkillLevel.WORKFLOW, atomic)
        self.assertEqual("workflow:1", workflows[0].skill_id)
        self.assertEqual(("atomic:1",), tuple(workflows[0].payload["atomic_ids"]))
        self.assertEqual(2, len(transport.calls))


if __name__ == "__main__":
    unittest.main()
