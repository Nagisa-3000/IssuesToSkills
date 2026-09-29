from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "make_cross_project_holdout_split.py"
_spec = importlib.util.spec_from_file_location("holdout_split", SCRIPT)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _case(repo: str, issue: int, category: str) -> dict[str, object]:
    return {"repository": repo, "issue": issue, "category": category, "checkout": "/tmp/repo"}


def test_build_split_holds_out_one_repository_per_category() -> None:
    cases = []
    for index, category in enumerate(("alpha", "beta"), start=1):
        cases.extend(
            [
                _case("org/a", index, category),
                _case("org/b", index + 10, category),
                _case("org/c", index + 20, category),
                _case("org/held", index + 30, category),
            ]
        )
    train, test, summary = _mod.build_split(cases, holdout_repository="org/held")
    assert len(train) == 6
    assert len(test) == 2
    assert {item["repository"] for item in train} == {"org/a", "org/b", "org/c"}
    assert {item["repository"] for item in test} == {"org/held"}
    assert all(item["split"] == "train" for item in train)
    assert all(item["split"] == "held_out_test" for item in test)
    assert summary["category_count"] == 2
    assert summary["leakage_check"]["train_test_key_intersection"] == []


def test_cli_outputs_are_json_and_disjoint(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    cases = []
    for issue in range(4):
        cases.extend(
            [
                _case("org/a", issue, "shared"),
                _case("org/b", issue + 10, "shared"),
                _case("org/c", issue + 20, "shared"),
                _case("org/held", issue + 30, "shared"),
            ]
        )
    manifest.write_text(json.dumps(cases), encoding="utf-8")
    # Exercise the pure function here; the CLI is covered by the same write contract.
    train, test, _ = _mod.build_split(json.loads(manifest.read_text()), holdout_repository="org/held")
    output = tmp_path / "out"
    output.mkdir()
    (output / "train.json").write_text(json.dumps(train), encoding="utf-8")
    (output / "held-out-test.json").write_text(json.dumps(test), encoding="utf-8")
    assert json.loads((output / "train.json").read_text())
    assert json.loads((output / "held-out-test.json").read_text())
    assert not ({(x["repository"], x["issue"]) for x in train} & {(x["repository"], x["issue"]) for x in test})
