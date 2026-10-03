from __future__ import annotations

import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = (
    ROOT
    / "data"
    / "skill-extraction"
    / "agent-core-twenty-category-extraction-v2"
    / "codex-5.6-sol-contract-v2-20261001"
    / "extraction-inventory.json"
)
VALIDATION_REPORT = INVENTORY.with_name("extraction-validation.json")
VALIDATOR_SCRIPT = (
    ROOT
    / "data"
    / "skill-extraction"
    / "packages"
    / "universal-resolution-distiller"
    / "scripts"
    / "validate_extraction_inventory.py"
)
SPEC = importlib.util.spec_from_file_location("extraction_inventory_validator", VALIDATOR_SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_twenty_category_inventory_has_complete_disjoint_splits() -> None:
    inventory = _load_object(INVENTORY)
    records = inventory["records"]
    summaries = inventory["category_summaries"]

    assert inventory["counts"] == {
        "categories": 20,
        "training_cases": 80,
        "admitted_episodes": 80,
        "manual_validation_pass": 80,
        "jsonschema_validation_pass": 80,
        "exact_table_rows": 7,
        "verified_substitutes": 21,
        "candidate_atomics": 218,
        "candidate_workflows": 83,
        "holdouts": 20,
        "holdout_leaks": 0,
    }
    assert len(records) == 80
    assert len(summaries) == 20
    assert len({record["case_id"] for record in records}) == 80
    assert {record["model"] for record in records} == {"openai/gpt-5.6-sol"}

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_category[record["category"]].append(record)

    assert set(by_category) == {summary["category"] for summary in summaries}
    for summary in summaries:
        category = summary["category"]
        category_records = by_category[category]
        training_repositories = {record["repository"] for record in category_records}
        holdout = summary["holdout"]

        assert len(category_records) == 4
        assert len(training_repositories) == 4
        assert holdout["repository"] not in training_repositories
        assert holdout["extraction_forbidden"] is True
        assert holdout["evidence_status"] == "intentionally_not_extracted"
        assert all(record["manual_validation_valid"] for record in category_records)
        assert all(record["jsonschema_valid"] for record in category_records)

    assert Counter(record["sample_kind"] for record in records) == {
        "exact_table_row": 7,
        "verified_implementation_pull_request": 52,
        "verified_substitute": 21,
    }


def test_extracted_cases_are_grounded_and_do_not_contain_holdouts() -> None:
    inventory = _load_object(INVENTORY)
    summaries = {
        summary["category"]: summary for summary in inventory["category_summaries"]
    }

    for record in inventory["records"]:
        output = ROOT / record["relative_output"]
        holdout = summaries[record["category"]]["holdout"]
        response = _load_object(output / "codex-response.json")
        validation = _load_object(output / "validation.json")

        assert validation == {"valid": True, "errors": []}
        assert response["episode"]["episode_id"] == record["episode_id"]
        assert response["evidence_units"]
        assert response["candidate_atomics"]
        assert response["candidate_workflows"]

        evidence_ids = {unit["id"] for unit in response["evidence_units"]}
        atomic_names = {atomic["name"] for atomic in response["candidate_atomics"]}
        for atomic in response["candidate_atomics"]:
            assert set(atomic["evidence_ids"]) <= evidence_ids
            semantic_action = atomic["semantic_action"]
            assert semantic_action["pre_state"]
            assert semantic_action["post_state"]
            assert semantic_action["validation"]
            assert set(semantic_action["evidence_ids"]) <= evidence_ids

        for workflow in response["candidate_workflows"]:
            assert set(workflow["atomic_names"]) <= atomic_names
            assert set(workflow["evidence_ids"]) <= evidence_ids
            graph = workflow["workflow_graph"]
            assert graph["when_to_use"]
            assert graph["anti_goals"]
            assert graph["not_applicable_when"]
            assert graph["validation_ladder"]
            assert graph["stop_conditions"]
            assert {step["action_name"] for step in graph["steps"]} <= atomic_names

        for artifact_name in (
            "prompt.txt",
            "issue-bundle.json",
            "codex-response.json",
            "validation.json",
        ):
            artifact = output / artifact_name
            assert artifact.is_file()
            artifact_text = artifact.read_text(encoding="utf-8")
            assert holdout["case_id"] not in artifact_text
            assert holdout["issue_url"] not in artifact_text


def test_distiller_validator_accepts_the_frozen_twenty_category_corpus() -> None:
    report = VALIDATOR.validate_inventory(
        INVENTORY,
        repository_root=ROOT,
        expected_categories=20,
        expected_training_per_category=4,
        expected_model="openai/gpt-5.6-sol",
    )

    assert report["valid"] is True
    assert report["errors"] == []
    assert report["counts"] == {
        "categories": 20,
        "training_cases": 80,
        "holdouts": 20,
        "candidate_atomics": 218,
        "candidate_workflows": 83,
        "holdout_leaks": 0,
    }
    assert report == _load_object(VALIDATION_REPORT)


def test_distiller_validator_rejects_a_training_holdout_repository_overlap(
    tmp_path: Path,
) -> None:
    inventory = _load_object(INVENTORY)
    first_category = inventory["category_summaries"][0]["category"]
    first_training_record = next(
        record for record in inventory["records"] if record["category"] == first_category
    )
    inventory["category_summaries"][0]["holdout"]["repository"] = first_training_record[
        "repository"
    ]
    tampered = tmp_path / "inventory.json"
    tampered.write_text(json.dumps(inventory), encoding="utf-8")

    report = VALIDATOR.validate_inventory(
        tampered,
        repository_root=ROOT,
        expected_categories=20,
        expected_training_per_category=4,
        expected_model="openai/gpt-5.6-sol",
    )

    assert report["valid"] is False
    assert any("holdout repository appears in training records" in error for error in report["errors"])


def test_frozen_json_corpus_is_valid_ir_but_not_complete_skill_extraction() -> None:
    report = VALIDATOR.validate_inventory(INVENTORY, repository_root=ROOT, require_packages=True)

    assert report["ir_validation_valid"] is True
    assert report["valid"] is False
    assert report["extraction_success"] is False
    assert report["status"] == "materialization_pending"
    assert report["materialized_skill_packages"] == 0
