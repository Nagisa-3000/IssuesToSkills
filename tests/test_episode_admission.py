from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from arex_skill_graph.admission import BottomUpSkillAdmission, SkillCandidateRetriever
from arex_skill_graph.episodes import ChangeEpisode
from arex_skill_graph.lifecycle import DedupProposal, SkillLevel, SkillRecord, DedupDecision, LifecycleManager
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.store import CatalogStore


class EpisodeAdmissionTests(unittest.TestCase):
    def test_workflow_and_pattern_are_episode_level_and_tree_is_structural(self) -> None:
        episode = ChangeEpisode(
            episode_id="episode:budget",
            repository="repo",
            revision="r1",
            title="Reserve shared capacity",
            before="old implementation",
            after="new implementation",
            diff="- nominal window\n+ residual window",
            call_sites=("compressor()",),
            tests=("test_residual_capacity",),
            evidence_ids=("diff:1", "test:1"),
        )
        calls: list[str] = []

        def atomics(value: ChangeEpisode):
            calls.append("atomic")
            self.assertIs(value, episode)
            return (
                SkillRecord("atomic:derive", SkillLevel.ATOMIC, "Derive residual", "Derive residual capacity", evidence_ids={"diff:1"}),
                SkillRecord("atomic:validate", SkillLevel.ATOMIC, "Validate boundary", "Validate capacity boundary", evidence_ids={"test:1"}),
            )

        def workflows(value: ChangeEpisode, resolved_atomics):
            calls.append("workflow")
            self.assertIs(value, episode)
            self.assertEqual(("atomic:derive", "atomic:validate"), tuple(x.skill_id for x in resolved_atomics))
            return (
                SkillRecord("workflow:reserve", SkillLevel.WORKFLOW, "Reserve before pressure", "Reserve capacity then derive threshold", payload={"atomic_ids": ["atomic:derive", "atomic:validate"]}),
                SkillRecord("workflow:replay", SkillLevel.WORKFLOW, "Replay on reconfiguration", "Replay the policy after model changes", payload={"atomic_ids": ["atomic:derive"]}),
            )

        def patterns(resolved_workflows):
            calls.append("pattern")
            self.assertEqual(("workflow:reserve", "workflow:replay"), tuple(x.skill_id for x in resolved_workflows))
            return (
                SkillRecord("pattern:shared-budget", SkillLevel.PATTERN, "Shared-capacity budget", "Apply residual capacity accounting across workflows", payload={"workflow_ids": [x.skill_id for x in resolved_workflows]}),
            )

        def judge(candidate, peer):
            return DedupProposal(candidate.skill_id, peer.skill_id, DedupDecision.RELATED_BUT_DISTINCT, 0.8, "distinct")

        with tempfile.TemporaryDirectory() as tmp:
            with CatalogStore(Path(tmp) / "catalog.sqlite") as store:
                store.initialize()
                manager = LifecycleManager()
                admission = BottomUpSkillAdmission(manager, SkillCandidateRetriever(store), judge=judge)
                result = admission.insert_episode(
                    episode,
                    atomic_extractor=atomics,
                    workflow_extractor=workflows,
                    pattern_extractor=patterns,
                )
                edge_rows = store.connection.execute(
                    "SELECT source_id, relation, target_id FROM edges ORDER BY source_id, target_id"
                ).fetchall()
                self.assertEqual(
                    {
                        ("workflow:reserve", "contains", "atomic:derive"),
                        ("workflow:reserve", "contains", "atomic:validate"),
                        ("workflow:replay", "contains", "atomic:derive"),
                        ("pattern:shared-budget", "contains", "workflow:reserve"),
                        ("pattern:shared-budget", "contains", "workflow:replay"),
                    },
                    {(row["source_id"], row["relation"], row["target_id"]) for row in edge_rows},
                )
        self.assertEqual(["atomic", "workflow", "pattern"], calls)
        self.assertEqual(("atomic:derive", "atomic:validate"), tuple(x.resolved_id for x in result.atomics))
        self.assertEqual(("workflow:reserve", "workflow:replay"), tuple(x.resolved_id for x in result.workflows))
        self.assertEqual(("pattern:shared-budget",), tuple(x.resolved_id for x in result.patterns))
        self.assertEqual({"pattern:shared-budget"}, manager.skills["workflow:reserve"].parent_ids)
        self.assertEqual({"workflow:reserve"}, manager.skills["atomic:validate"].parent_ids)
        self.assertEqual({"workflow:reserve", "workflow:replay"}, manager.skills["atomic:derive"].parent_ids)


    def test_pattern_attaches_only_explicitly_supported_workflows(self) -> None:
        episode = ChangeEpisode("episode:subset", "repo", "r1", "Subset support")

        with tempfile.TemporaryDirectory() as tmp:
            with CatalogStore(Path(tmp) / "catalog.sqlite") as store:
                store.initialize()
                manager = LifecycleManager()
                admission = BottomUpSkillAdmission(
                    manager,
                    SkillCandidateRetriever(store),
                    judge=lambda candidate, peer: DedupProposal(
                        candidate.skill_id,
                        peer.skill_id,
                        DedupDecision.RELATED_BUT_DISTINCT,
                        0.8,
                        "distinct",
                    ),
                )
                admission.insert_episode(
                    episode,
                    atomic_extractor=lambda _: (
                        SkillRecord("atomic:one", SkillLevel.ATOMIC, "One", "One"),
                    ),
                    workflow_extractor=lambda *_: (
                        SkillRecord(
                            "workflow:supported",
                            SkillLevel.WORKFLOW,
                            "Supported",
                            "Supported",
                            payload={"atomic_ids": ["atomic:one"]},
                        ),
                        SkillRecord(
                            "workflow:excluded",
                            SkillLevel.WORKFLOW,
                            "Excluded",
                            "Excluded",
                            payload={"atomic_ids": ["atomic:one"]},
                        ),
                    ),
                    pattern_extractor=lambda _: (
                        SkillRecord(
                            "pattern:subset",
                            SkillLevel.PATTERN,
                            "Subset",
                            "Only one workflow is governed as supporting evidence",
                            payload={"workflow_ids": ["workflow:supported"]},
                        ),
                    ),
                )
                rows = store.connection.execute(
                    "SELECT source_id, target_id FROM edges "
                    "WHERE relation = 'contains' AND source_id = 'pattern:subset'"
                ).fetchall()
                self.assertEqual(
                    [("pattern:subset", "workflow:supported")],
                    [(row["source_id"], row["target_id"]) for row in rows],
                )
                self.assertEqual(
                    {"pattern:subset"}, manager.skills["workflow:supported"].parent_ids
                )
                self.assertEqual(
                    set(), manager.skills["workflow:excluded"].parent_ids
                )

    def test_empty_workflows_does_not_manufacture_pattern(self) -> None:
        episode = ChangeEpisode("episode:empty", "repo", "r1", "No workflow")
        pattern_called = False

        def pattern(_):
            nonlocal pattern_called
            pattern_called = True
            return ()

        with tempfile.TemporaryDirectory() as tmp:
            with CatalogStore(Path(tmp) / "catalog.sqlite") as store:
                store.initialize()
                manager = LifecycleManager()
                result = BottomUpSkillAdmission(manager, SkillCandidateRetriever(store), judge=lambda *_: None).insert_episode(
                    episode,
                    atomic_extractor=lambda _: (SkillRecord("atomic:one", SkillLevel.ATOMIC, "One", "One"),),
                    workflow_extractor=lambda *_: (),
                    pattern_extractor=pattern,
                )
        self.assertFalse(pattern_called)  # no upper-level extraction without workflows
        self.assertEqual((), result.patterns)


class EpisodePromptTests(unittest.TestCase):
    def test_explicit_episode_prompts_carry_code_context_and_all_lower_level_nodes(self) -> None:
        class Transport:
            def __init__(self):
                self.users = []

            def complete(self, *, system, user, response_schema):
                self.users.append(json.loads(user))
                return {"skills": []}

        transport = Transport()
        adapter = LLMGovernanceAdapter(transport, GovernanceContext(repository="repo"))
        episode = ChangeEpisode("ep", "repo", "r", "title", before="B", after="A", diff="D", call_sites=("C",), tests=("T",))
        atomics = adapter.extract_atomics_from_episode(episode)
        workflows = adapter.extract_workflows_from_episode(episode, (SkillRecord("a", SkillLevel.ATOMIC, "a", "a"),))
        patterns = adapter.extract_patterns_from_workflows((SkillRecord("w", SkillLevel.WORKFLOW, "w", "w"),))
        self.assertEqual((), atomics)
        self.assertEqual((), workflows)
        self.assertEqual((), patterns)
        self.assertEqual("B", transport.users[0]["payload"]["before"])
        self.assertEqual("A", transport.users[1]["payload"]["after"])
        self.assertEqual("D", transport.users[1]["payload"]["diff"])
        self.assertEqual(["a"], [x["skill_id"] for x in transport.users[1]["payload"]["atomic_candidates"]])
        self.assertEqual(["w"], [x["skill_id"] for x in transport.users[2]["payload"]["workflow_candidates"]])


    def test_pattern_supported_by_is_normalized_without_fallback_expansion(self) -> None:
        class Transport:
            def complete(self, *, system, user, response_schema):
                return {
                    "skills": [
                        {
                            "skill_id": "pattern:residual",
                            "title": "Residual capacity",
                            "summary": "Derive policies from residual capacity",
                            "supported_by": ["workflow:deepseek", "workflow:hermes"],
                        }
                    ]
                }

        adapter = LLMGovernanceAdapter(Transport())
        workflows = (
            SkillRecord("workflow:aider", SkillLevel.WORKFLOW, "Aider", "Aider"),
            SkillRecord("workflow:deepseek", SkillLevel.WORKFLOW, "DeepSeek", "DeepSeek", evidence_ids={"EU-DEEPSEEK"}),
            SkillRecord("workflow:hermes", SkillLevel.WORKFLOW, "Hermes", "Hermes", evidence_ids={"EU-HERMES"}),
            SkillRecord("workflow:pi", SkillLevel.WORKFLOW, "Pi", "Pi"),
        )
        patterns = adapter.extract_patterns_from_workflows(workflows)
        self.assertEqual(1, len(patterns))
        self.assertEqual(
            ["workflow:deepseek", "workflow:hermes"],
            patterns[0].payload["workflow_ids"],
        )
        self.assertEqual({"EU-DEEPSEEK", "EU-HERMES"}, patterns[0].evidence_ids)


if __name__ == "__main__":
    unittest.main()


