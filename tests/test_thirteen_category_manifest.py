from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "experiments" / "manifests" / "agent-core-thirteen-category-extraction-v2"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_thirteen_categories_have_four_cross_repository_training_cases() -> None:
    manifests = sorted(MANIFEST_ROOT.glob("[0-9][0-9]-*.json"))

    assert len(manifests) == 13
    for path in manifests:
        manifest = _load(path)
        category = re.sub(r"^\d\d-", "", path.stem)
        cases = manifest["cases"]
        assert manifest["category"] == category
        assert isinstance(cases, list)
        assert len(cases) == 4
        assert len({case["repository"] for case in cases}) == 4
        for case in cases:
            assert case["category"] == category
            assert case["role"] == "train_candidate"
            assert case["evidence_status"] == "ready_for_codex_extraction"
            assert case["ref"] == case["extraction_ref"]
            assert len(case["ref"]) == 40
            assert case["provenance"]["classification"] == "direct_implementation_artifact"


def test_holdouts_are_repository_disjoint_and_absent_from_extraction_inputs() -> None:
    holdouts = _load(MANIFEST_ROOT / "holdouts.json")["cases"]
    manifests = {
        re.sub(r"^\d\d-", "", path.stem): path
        for path in MANIFEST_ROOT.glob("[0-9][0-9]-*.json")
    }

    assert isinstance(holdouts, list)
    assert len(holdouts) == 13
    assert {case["category"] for case in holdouts} == set(manifests)
    for holdout in holdouts:
        assert holdout["extraction_forbidden"] is True
        assert holdout["evidence_status"] == "intentionally_not_extracted"
        path = manifests[holdout["category"]]
        manifest = _load(path)
        train_repositories = {case["repository"] for case in manifest["cases"]}
        assert holdout["repository"] not in train_repositories
        extraction_input = path.read_text(encoding="utf-8")
        assert holdout["issue_url"] not in extraction_input


def test_combined_training_manifest_matches_category_manifests() -> None:
    category_cases = []
    for path in sorted(MANIFEST_ROOT.glob("[0-9][0-9]-*.json")):
        category_cases.extend(_load(path)["cases"])
    combined = _load(MANIFEST_ROOT / "train-all.json")
    combined_cases = combined["cases"]

    assert combined["counts"] == {"categories": 13, "total": 52}
    assert len(combined_cases) == 52
    assert {case["case_id"] for case in combined_cases} == {
        case["case_id"] for case in category_cases
    }
    assert len({case["case_id"] for case in combined_cases}) == 52
    assert len({case["ref"] for case in combined_cases}) == 52
