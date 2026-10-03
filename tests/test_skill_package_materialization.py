from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from arex_skill_graph.retrieval import SearchHit, SkillRetriever
from arex_skill_graph.schema import Node, NodeType
from arex_skill_graph.skill_packages import (
    compile_workflow_graph,
    extraction_completion,
    hydrate_package,
    validate_package,
)
from arex_skill_graph.store import CatalogStore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from build_universal_resolution_graph import build
from materialize_universal_resolution_graph import materialize
from run_codex_issue_episode_extraction import canonical_episode, finalize_extraction

SOURCE = ROOT / "data/skill-extraction/agent-core-seven-category-extraction-v2"
CASE_DIR = (
    SOURCE
    / "codex-5.6-sol-contract-v2-20261001/01-provider-interface-adaptation/google-gemini__gemini-cli__25357"
)


def source():
    response = json.loads((CASE_DIR / "codex-response.json").read_text())
    manifest = json.loads(
        (
            ROOT / "experiments/manifests/agent-core-seven-category-extraction-v2/train-all.json"
        ).read_text()
    )
    cases = manifest["cases"] if isinstance(manifest, dict) else manifest
    case = next(
        row
        for row in cases
        if row["repository"] == "google-gemini/gemini-cli" and row["issue"] == 25357
    )
    return response, case


def projection():
    response, case = source()
    episode = canonical_episode(response, {}, case)
    graph = build([episode], {"cases": [case]})
    return graph, [episode]


def compile_one(tmp_path):
    graph, episodes = projection()
    report = compile_workflow_graph(graph, episodes, tmp_path / "packages")
    assert report["extraction_success"], report["failures"]
    root = Path(report["packages"][0]["package_path"])
    return graph, episodes, report, root


def test_json_only_is_not_completed_extraction():
    assert extraction_completion(True, [], 1) == {
        "status": "materialization_pending",
        "admitted": False,
        "extraction_success": False,
        "skill_materialized": False,
        "materialized_skill_packages": 0,
    }


def test_claimed_json_package_flags_do_not_bypass_real_file_validation(tmp_path):
    fake = {
        "skill_id": "workflow:fake",
        "source_workflow_id": "workflow:fake",
        "source_episode_ids": ["episode:fake"],
        "package_path": str(tmp_path / "absent"),
        "package_sha256": "0" * 64,
        "package_version": 1,
        "package_status": "candidate",
        "status": "package_validated",
        "package_validation": "passed",
    }
    result = extraction_completion(True, [fake], 1)
    assert result["extraction_success"] is False
    assert result["materialized_skill_packages"] == 0


def test_v3_schema_requires_explicit_skill_guidance_and_v2_remains_migratable():
    from jsonschema import Draft202012Validator

    response, _ = source()
    validator = Draft202012Validator(
        json.loads((ROOT / "schemas/codex-change-episode-v3.schema.json").read_text())
    )
    assert list(validator.iter_errors(response))
    response["candidate_workflows"][0]["skill_contract"] = {
        "name": "adapt-provider-endpoint-contract",
        "description": "Route provider-specific endpoint overrides when caller and environment sources compete.",
        "applicability_probes": [
            "Does the client-construction boundary know the declared provider?"
        ],
        "failure_modes": ["No constructor observation seam is available."],
        "known_limitations": ["The training checkout's tests were inspected but not executed."],
    }
    validator.validate(response)


def test_runner_finalization_requires_and_returns_a_real_package(tmp_path):
    response, case = source()
    completion, episode = finalize_extraction(response, {}, case, tmp_path / "packages")
    assert completion["admitted"] is True
    assert completion["status"] == "admitted_candidate"
    assert episode["metadata"]["extraction_completion"]["skill_materialized"] is True
    assert all(validate_package(Path(row["package_path"])) == [] for row in completion["packages"])
    response["candidate_workflows"][0]["workflow_graph"]["steps"][0]["validation"] = ""
    rejected, episode = finalize_extraction(response, {}, case, tmp_path / "rejected")
    assert not rejected["extraction_success"] and episode is None
    assert not (tmp_path / "rejected").exists()


def test_packages_are_idempotent_and_refuse_manual_overwrites(tmp_path):
    graph, episodes, first, root = compile_one(tmp_path)
    original = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    again = compile_workflow_graph(graph, episodes, tmp_path / "packages")
    assert first["packages"] == again["packages"]
    assert original == {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    }
    skill = root / "SKILL.md"
    changed = skill.read_text() + "\nManual clarification.\n"
    skill.write_text(changed)
    failed = compile_workflow_graph(graph, episodes, tmp_path / "packages")
    assert not failed["admitted"]
    assert "refusing to overwrite" in failed["failures"][0]["reason"]
    assert skill.read_text() == changed


def test_check_does_not_create_files(tmp_path):
    graph, episodes = projection()
    report = compile_workflow_graph(graph, episodes, tmp_path / "packages", check=True)
    assert not report["extraction_success"]
    assert not (tmp_path / "packages").exists()
    assert report["failures"][0]["status"] == "would_create"


def test_copied_package_is_self_contained_and_hydrates_actual_guidance(tmp_path):
    graph, _, report, root = compile_one(tmp_path)
    relocated = tmp_path / "other-machine" / root.name
    shutil.copytree(root, relocated)
    assert validate_package(relocated) == []
    verified = subprocess.run(
        [sys.executable, str(relocated / "scripts/verify_package.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert verified.returncode == 0, verified.stderr
    payload = copy.deepcopy(graph["workflows"][0])
    payload["skill_package"]["package_path"] = str(relocated)
    hydrated = hydrate_package(payload)
    assert (relocated / "SKILL.md").read_text() in hydrated["rendered"]
    assert len(hydrated["hydrated_action_ids"]) == 3
    assert hydrated["package_sha256"] == report["packages"][0]["package_sha256"]
    provenance = json.loads((relocated / "references/provenance.json").read_text())
    assert provenance["holdout_used"] is False
    assert provenance["package"]["status"] == "candidate"
    evidence = {row["id"] for row in provenance["evidence"]}
    assert all(set(row["evidence_ids"]).issubset(evidence) for row in provenance["actions"])


def test_graph_admission_cannot_succeed_with_json_only_or_modified_package(tmp_path):
    graph, episodes = projection()
    graph["extraction_policy"]["skill_package_required"] = True
    with CatalogStore(tmp_path / "catalog.sqlite") as store:
        store.initialize()
        with pytest.raises(ValueError, match="structured_only"):
            materialize(graph, store)
        assert not store.get_node(graph["workflows"][0]["id"])
        report = compile_workflow_graph(graph, episodes, tmp_path / "packages")
        materialize(graph, store)
        node = store.get_node(graph["workflows"][0]["id"])
        assert node.payload["skill_package"] == report["packages"][0]
        store.upsert_node(
            Node(
                "workflow:ir",
                NodeType.WORKFLOW,
                "provider endpoint",
                "provider endpoint configuration",
                payload={"goal": "JSON only"},
            ),
            embed=True,
        )
        hits = (
            SkillRetriever(store)
            .search("provider endpoint configuration", require_skill_package=True)
            .hits
        )
        assert [hit.node.id for hit in hits] == [node.id]
        root = Path(report["packages"][0]["package_path"])
        (root / "SKILL.md").write_text("corrupt")
        assert (
            not SkillRetriever(store).search("provider endpoint", require_skill_package=True).hits
        )


def test_holdout_cannot_be_materialized(tmp_path):
    response, case = source()
    case["role"] = "holdout_candidate"
    case["extraction_forbidden"] = True
    with pytest.raises(ValueError, match="holdout"):
        finalize_extraction(response, {}, case, tmp_path / "packages")
    assert not (tmp_path / "packages").exists()


def test_dangling_atomic_and_cyclic_dependencies_cannot_be_silently_repaired(tmp_path):
    response, case = source()
    response["candidate_workflows"][0]["workflow_graph"]["steps"][0]["action_name"] = "unknown"
    episode = canonical_episode(response, {}, case)
    with pytest.raises(ValueError, match="unknown Action"):
        build([episode], {"cases": [case]})
    graph, episodes = projection()
    steps = graph["workflows"][0]["steps"]
    steps[0]["depends_on"] = [steps[-1]["action_name"]]
    report = compile_workflow_graph(graph, episodes, tmp_path / "packages")
    assert not report["admitted"]
    assert "cycle" in report["failures"][0]["reason"]


def test_missing_atomic_evidence_and_forged_graph_hash_are_rejected(tmp_path):
    graph, episodes = projection()
    episodes[0]["metadata"]["codex_response"]["candidate_atomics"][0]["semantic_action"][
        "evidence_ids"
    ] = ["missing"]
    assert not compile_workflow_graph(graph, episodes, tmp_path / "missing")["admitted"]
    graph, _, _, _ = compile_one(tmp_path)
    graph["workflows"][0]["skill_package"]["package_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash disagree"):
        hydrate_package(graph["workflows"][0])


def test_deferred_record_cannot_supply_a_package_to_serving_or_guidance(tmp_path):
    graph, _, _, _ = compile_one(tmp_path)
    workflow = graph["workflows"][0]
    workflow["promotion_status"] = "deferred_by_semantic_judge"
    with pytest.raises(ValueError, match="deferred"):
        hydrate_package(workflow)
    from run_cross_project_holdout_agent_eval import _split_guidance_hits

    node = Node(
        workflow["id"],
        NodeType.WORKFLOW,
        workflow["title"],
        workflow["description"],
        payload=workflow,
    )
    eligible, excluded = _split_guidance_hits([SearchHit(node, 1.0)], require_packages=True)
    assert not eligible and len(excluded) == 1


def test_revised_workflow_cannot_serve_a_stale_package(tmp_path):
    graph, _, _, _ = compile_one(tmp_path)
    workflow = graph["workflows"][0]
    workflow["when_to_use"] = ["A different owner boundary and mechanism applies."]
    with pytest.raises(ValueError, match="stale package"):
        hydrate_package(workflow)


def test_applicability_judge_receives_skill_md_and_explicit_actions(tmp_path):
    from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter

    graph, _, _, root = compile_one(tmp_path)
    workflow = graph["workflows"][0]

    class CapturingTransport:
        def complete(self, *, system, user, response_schema):
            candidates = json.loads(user)["payload"]["candidates"]
            context = candidates[0]["skill_package_context"]
            assert (root / "SKILL.md").read_text() in context["rendered"]
            assert len(context["hydrated_action_ids"]) == 3
            return {
                "applicable": True,
                "selected_skill_id": workflow["id"],
                "confidence": 0.9,
                "rationale": "Matching constructor-boundary contract.",
            }

    node = Node(
        workflow["id"],
        NodeType.WORKFLOW,
        workflow["title"],
        workflow["description"],
        payload=workflow,
    )
    judge = LLMGovernanceAdapter(
        CapturingTransport(), GovernanceContext(repository="synthetic", model="test")
    )
    assert (
        judge.judge_retrieval_use("provider endpoint", [SearchHit(node, 1.0)])["applicable"] is True
    )
