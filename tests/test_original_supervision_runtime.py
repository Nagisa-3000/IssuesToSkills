"""Solver runtime and frozen-pool checks for original-query supervision."""

import pytest
from adaptive_fixture import make_fixture
from test_historical_plan_pool import _prepared_study

from arex_skill_graph.adaptive_budget import BudgetLedger
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.historical_plan_pool import load_prepared_plan_study
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.workflow_ranker import WorkflowRanker


def test_original_runtime_mismatch_stops_before_any_model_call(tmp_path):
    _package, task, policy = make_fixture(tmp_path)
    state = {"closed": False, "preflight": False, "model_calls": 0}

    class Tools:
        runtime_sha256 = "a" * 64
        isolation = "synthetic-unit-runtime"

        def preflight(self):
            state["preflight"] = True

        def close(self):
            state["closed"] = True

    class Transport:
        def complete(self, **kwargs):
            state["model_calls"] += 1
            raise AssertionError("a mismatched runtime cannot reach the model")

    with CatalogStore(tmp_path / "runtime-guard-catalog.sqlite") as store:
        store.initialize()
        solver = AdaptiveSolver(
            Transport(),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(),
            arm="B0",
            tools_factory=lambda *_: Tools(),
            required_runtime_sha256="b" * 64,
        )
        with pytest.raises(ValueError, match="runtime mismatch before model"):
            solver.run(task, use_frozen_selection=True)
    assert state == {"closed": True, "preflight": True, "model_calls": 0}


@pytest.mark.parametrize("field", ["evaluation_route", "original_supervision_registry_sha256"])
def test_prepared_candidates_cannot_mix_original_and_native_parent_authority(tmp_path, field):
    package, task, policy = make_fixture(tmp_path)
    directory, expected, _ = _prepared_study(tmp_path, package, task, policy)
    expected[field] = "changed-original-authority"
    with pytest.raises(ValueError, match=field):
        load_prepared_plan_study(directory, expected)
