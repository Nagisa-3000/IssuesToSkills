from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "adjudicate_universal_resolution_graph.py"
SPEC = importlib.util.spec_from_file_location("graph_adjudication", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_offline_adjudication_is_explicitly_deferred(tmp_path: Path) -> None:
    graph = {
        "actions": [
            {"id": "a1", "category": "state", "operation": "reconcile", "intent": "restore state"},
            {"id": "a2", "category": "state", "operation": "reconcile", "intent": "reconcile state"},
        ],
        "workflows": [{"id": "w1", "repository": "org/a", "steps": []}],
        "patterns": [{"id": "p1", "supporting_workflows": ["w1"]}],
    }
    source = tmp_path / "graph.json"
    output = tmp_path / "judgment.json"
    source.write_text(json.dumps(graph), encoding="utf-8")
    # Exercise the bounded decision helper without making a network call.
    status, result, error = MODULE.bounded_call(None, system="test", payload={}, schema={})
    assert status == "deferred_no_api_key"
    assert result is None
    assert error is None

