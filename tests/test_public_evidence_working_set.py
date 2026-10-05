"""Regression for loss of already-read evidence across later tool requests."""

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_budget import BudgetLedger
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.public_evidence import read_public_evidence
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import CurrentOracle
from arex_skill_graph.workflow_ranker import WorkflowRanker


def test_grouped_selection_retains_failed_case_and_does_not_mutate_evidence(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    payload = {
        "padding": "irrelevant" * 3000,
        "cases": [{"status": "FAIL"}],
        "stderr": "",
        "exception": None,
    }
    output = json.dumps(payload)
    records = {"public:observation:0": {"observation_id": "public:observation:0", "output": output}}
    before = copy.deepcopy((task.to_dict(), records))
    read = read_public_evidence(
        task,
        records,
        {
            "evidence_id": "public:observation:0",
            "field": "output",
            "json_pointers": ["/cases", "/stderr", "/exception"],
        },
    )
    assert json.loads(read["content"]) == {
        "/cases": payload["cases"],
        "/stderr": "",
        "/exception": None,
    }
    assert read["field_sha256"] == hashlib.sha256(output.encode()).hexdigest()
    assert len(read["content"]) <= 4000 and read["next_offset"] is None
    assert "not fresh execution" in read["assurance"]
    assert (task.to_dict(), records) == before


@pytest.mark.parametrize(
    "selectors",
    [
        {"json_pointers": []},
        {"json_pointers": ["/cases"] * 2},
        {"json_pointers": ["/cases"] * 17},
        {"json_pointers": "/cases"},
        {"json_pointers": [False]},
        {"json_pointers": ["/cases", "/missing"]},
        {"json_pointers": ["/bad~2escape"]},
        {"json_pointers": ["/cases"], "json_pointer": "/cases"},
    ],
)
def test_group_selection_fails_closed_without_partial_success(tmp_path, selectors):
    _, task, _ = make_fixture(tmp_path)
    records = {
        "public:observation:0": {"observation_id": "public:observation:0", "output": '{"cases":[]}'}
    }
    before = copy.deepcopy(records)
    with pytest.raises(ValueError):
        read_public_evidence(
            task, records, {"evidence_id": "public:observation:0", "field": "output", **selectors}
        )
    assert records == before


def test_solver_keeps_read_failure_through_other_tools_and_marks_it_stale_after_edit(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[-1]
    command = ["python3", "-V"]
    task = replace(
        task,
        oracles=(
            CurrentOracle(
                action.id,
                action.oracle[0].id,
                "Control",
                tuple(command),
                ("current:issue",),
            ),
        ),
    )
    original = Path(task.root, "checker.py").read_text()
    failed_case = {"status": "FAIL", "detail": "x" * 900 + "MIDDLE_BAD_STATE" + "y" * 900}
    payload = {"padding": "noise" * 2000, "cases": [failed_case], "stderr": "", "exception": None}

    class Tools:
        isolation = "test-only-evidence-working-set"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            self.executions = 0

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **_options):
            self.executions += 1
            assert self.executions <= 2
            if self.executions == 1:
                assert argv == command
                return {"argv": argv, "output": json.dumps(payload), "exit_code": 1}
            return {"argv": argv, "output": "supplemental observed", "exit_code": 0}

    class Transport:
        def __init__(self):
            self.frames = []

        def complete(self, **kwargs):
            frame = json.loads(kwargs["user"])
            self.frames.append(frame)
            n = len(self.frames)
            budget = frame["budget"]
            assert budget["remaining"]["model_tokens"] + budget["used"]["model_tokens"] == 300000
            assert "events" not in budget
            assert not any(
                "FAKE_PRIOR_READER_PAGE" in p["content"]
                for p in frame["evidence_working_set"]["pages"]
            )
            if n == 1:
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": command},
                    "rationale": "Control",
                }
            oracle = frame["current_run"]["oracle_executions"][0]
            witness = oracle["latest_observation_id"]
            if n == 2:
                assert oracle["status"] == "failed_process"
                index = frame["observations"][-1]["output_json_index"]
                assert "cases" in index["keys"]
                return {
                    "operation": "read_public_evidence",
                    "arguments": {
                        "evidence_id": witness,
                        "field": "output",
                        "json_pointers": ["/cases", "/stderr", "/exception"],
                    },
                    "rationale": "Inspect failed domain result once",
                }
            page = next(
                p
                for p in frame["evidence_working_set"]["pages"]
                if p["projection_kind"] == "explicit_evidence_read"
            )
            assert json.loads(page["content"])["/cases"] == [failed_case]
            assert "PUBLIC TEXT EXCERPT" not in page["content"]
            assert not frame["current_run"]["recorded_actions"]
            if n < 6:
                assert page["source_workspace_status"] == "matches_current_workspace"
                assert oracle["status"] == "failed_process"
            if n == 3:
                return {
                    "operation": "read_file",
                    "arguments": {"path": "checker.py"},
                    "rationale": "Inspect current source",
                }
            if n == 4:
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": ["python3", "-c", "print('supplemental')"]},
                    "rationale": "Other obligation",
                }
            if n == 5:
                return {
                    "operation": "write_file",
                    "arguments": {"path": "checker.py", "content": original + "\n# current edit\n"},
                    "rationale": "Change current workspace",
                }
            assert page["source_workspace_status"] == "stale_workspace"
            assert oracle["status"] == "stale_workspace"
            return {
                "operation": "finish",
                "arguments": {},
                "rationale": "End without success claim",
            }

    transport = Transport()
    ledger = BudgetLedger()
    with CatalogStore(tmp_path / "working-set.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport, WorkflowRanker(), store, policy, ledger, arm="B0", tools_factory=Tools
        ).run(
            task,
            use_frozen_selection=True,
            recordable_actions=(action,),
            initial_observations=(
                {
                    "operation": "read_public_evidence",
                    "observation_id": "public:observation:99",
                    "content": "FAKE_PRIOR_READER_PAGE",
                    "evidence_id": "current:issue",
                },
            ),
        )
    assert result["solver_ended"] and not result["failure"]
    assert len(transport.frames) == 6
    assert not result["action_observations"] and result["validated_resolved"] is None
    assert sum(o["operation"] == "run_public_command" for o in result["public_observations"]) == 2
    assert (
        len([o for o in result["public_observations"] if o["operation"] == "read_public_evidence"])
        == 2
    )
    assert transport.frames[1]["budget"]["used"]["model_tokens"] > 0
    assert result["budget"]["caps"]["model_tokens"] == 300000


def test_working_set_eviction_is_bounded_and_preserves_full_sealed_reads(tmp_path):
    from arex_skill_graph.public_evidence import solver_evidence_working_set

    _, task, _ = make_fixture(tmp_path)
    records = {
        "public:observation:0": {"observation_id": "public:observation:0", "output": "a" * 24000}
    }
    reads = {}
    for n in range(6):
        read = read_public_evidence(
            task,
            records,
            {"evidence_id": "public:observation:0", "field": "output", "offset": n * 4000},
        )
        read["observation_id"] = f"public:observation:{n + 1}"
        reads[read["observation_id"]] = read
    before = copy.deepcopy((task.to_dict(), records, reads))
    view = solver_evidence_working_set(task, records, reads, workspace_execution_sha256="current")
    assert sum(len(p["content"]) for p in view["pages"]) <= 12000
    assert view["omitted_read_count"] > 0
    assert view["pages"][-1]["offset"] == 20000
    assert all(p["source_workspace_status"] == "not_established" for p in view["pages"])
    assert (task.to_dict(), records, reads) == before


def test_grouped_selection_has_one_total_page_limit_for_large_values(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    payload = {"left": "x" * 5000, "right": "汉" * 5000}
    records = {
        "public:observation:0": {
            "observation_id": "public:observation:0",
            "output": json.dumps(payload, ensure_ascii=False),
        }
    }
    pages, offset = [], 0
    while True:
        page = read_public_evidence(
            task,
            records,
            {
                "evidence_id": "public:observation:0",
                "field": "output",
                "json_pointers": ["/left", "/right"],
                "offset": offset,
            },
        )
        assert len(page["content"]) <= 4000
        pages.append(page["content"])
        if page["next_offset"] is None:
            break
        offset = page["next_offset"]
    assert json.loads("".join(pages)) == {"/left": payload["left"], "/right": payload["right"]}
