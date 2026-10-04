import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

from arex_skill_graph.action_contracts import digest

_spec = importlib.util.spec_from_file_location(
    "temporal_ranker_data_cli",
    Path(__file__).resolve().parents[1] / "experiments/build_temporal_workflow_ranker_dataset.py",
)
_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cli)


def test_plan_pool_and_exclusions_are_part_of_dataset_input_identity(tmp_path):
    paths = {}
    for name in ("queries", "references", "labels", "plans", "excluded_query_ids"):
        path = tmp_path / (name + ".json")
        path.write_text(json.dumps([name]))
        paths[name] = path
    args = SimpleNamespace(**paths)
    original = _cli.source_input_hashes(args)
    assert original == {name: digest([name]) for name in paths}
    args.plans.write_text(json.dumps(["changed frozen plan"]))
    changed = _cli.source_input_hashes(args)
    assert changed["plans"] != original["plans"]
    assert {k: v for k, v in changed.items() if k != "plans"} == {
        k: v for k, v in original.items() if k != "plans"
    }


def test_absent_optional_inputs_are_not_fingerprinted(tmp_path):
    path = tmp_path / "input.json"
    path.write_text("[]")
    result = _cli.source_input_hashes(
        SimpleNamespace(queries=path, references=path, labels=path, plans=None)
    )
    assert set(result) == {"queries", "references", "labels"}
