from __future__ import annotations

import importlib.util
from pathlib import Path

from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.store import CatalogStore

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_materializer_preserves_workflow_action_pattern_graph(tmp_path: Path) -> None:
    builder = load_module(
        "universal_graph_for_catalog", ROOT / "experiments/build_universal_resolution_graph.py"
    )
    materializer = load_module(
        "universal_materializer", ROOT / "experiments/materialize_universal_resolution_graph.py"
    )
    manifest = {
        "cases": [
            {"repository": "org/a", "issue": 1, "category": "state", "role": "train_candidate"},
            {"repository": "org/b", "issue": 2, "category": "state", "role": "train_candidate"},
        ]
    }

    def episode(repo: str, issue: int, suffix: str) -> dict[str, object]:
        return {
            "episode_id": suffix,
            "repository": repo,
            "metadata": {
                "issue": issue,
                "candidate_atomics": [
                    {
                        "name": "reconcile state",
                        "title": "Reconcile authoritative state",
                        "description": "Reconcile authoritative state.",
                        "semantic_action": {
                            "intent": "reconcile authoritative state",
                            "module_role": "state owner",
                            "operation": "reconcile",
                            "pre_state": "derived state diverges",
                            "post_state": "derived state agrees",
                            "validation": "replay test",
                        },
                    }
                ],
                "candidate_workflows": [
                    {
                        "name": "restore and validate",
                        "title": "Restore state and validate replay",
                        "description": "Restore state then validate replay.",
                        "atomic_names": ["reconcile state"],
                        "workflow_graph": {
                            "goal": "restore authoritative state",
                            "when_to_use": ["reconstructed state diverges after a boundary"],
                            "anti_goals": ["do not replace the authoritative source"],
                            "not_applicable_when": ["no authoritative snapshot exists"],
                            "inputs": ["state snapshot"],
                            "entry_state": "derived state diverges",
                            "exit_state": "derived state agrees",
                            "steps": [
                                {
                                    "action_name": "reconcile state",
                                    "role": "reconcile",
                                    "required": True,
                                    "depends_on": [],
                                    "condition": "when state diverges",
                                    "validation": "replay test",
                                }
                            ],
                            "edges": [],
                            "validation_ladder": ["run replay test"],
                            "stop_conditions": ["stop without an authoritative snapshot"],
                            "unresolved_or_deferred": [],
                        },
                    }
                ],
            },
        }

    graph = builder.build([episode("org/a", 1, "e1"), episode("org/b", 2, "e2")], manifest)
    db = tmp_path / "catalog.sqlite"
    with CatalogStore(db) as store:
        store.initialize()
        counts = materializer.materialize(graph, store)
        assert counts["actions"] == 1
        assert counts["workflows"] == 2
        assert counts["workflow_fragments"] == 0
        assert counts["patterns"] == 1
        stats = store.stats()
        assert stats["nodes"]["action"] == 1
        assert stats["nodes"]["workflow"] == 2
        assert stats["nodes"]["pattern"] == 1
        assert stats["edges"]["has_step"] == 2
        assert stats["edges"]["executed_by"] == 2
        response = SkillRetriever(store).search(
            "reconcile state", top_k=5, seed_k=10, expand_hops=2
        )
        assert response.hits
        assert any(hit.node.node_type.value == "action" for hit in response.hits)
