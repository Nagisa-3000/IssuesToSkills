"""Small current-run command results stay visible without synthetic reader events."""

import copy
import json
from dataclasses import replace
from pathlib import Path

from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_budget import BudgetLedger
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.public_evidence import read_public_evidence, solver_evidence_working_set
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import CurrentOracle
from arex_skill_graph.workflow_ranker import WorkflowRanker


def test_small_commands_survive_later_requests_without_reads_or_fact_promotion(tmp_path):
    package, task, policy = make_fixture(tmp_path)
    action = package.workflows[0].actions[-1]
    command = ["python3", "-V"]
    task = replace(
        task,
        oracles=(
            CurrentOracle(
                action.id, action.oracle[0].id, "Control", tuple(command), ("current:issue",)
            ),
        ),
    )
    original = Path(task.root, "checker.py").read_text()
    outputs = [
        "failed control: " + "x" * 800 + "MIDDLE_FAILURE" + "y" * 800,
        "resource audit: " + "a" * 800 + "MIDDLE_AUDIT" + "b" * 800,
    ]
    executions = []

    class Tools:
        isolation = "test-only-small-command-view"
        runtime_sha256 = "test-only"

        def __init__(self, *_args):
            pass

        def preflight(self):
            pass

        def close(self):
            pass

        def run(self, argv, **_options):
            executions.append(argv)
            assert len(executions) <= 2
            return {
                "argv": argv,
                "output": outputs[len(executions) - 1],
                "exit_code": 1 if len(executions) == 1 else 0,
            }

    class Transport:
        def __init__(self):
            self.frames = []

        def complete(self, **kwargs):
            frame = json.loads(kwargs["user"])
            self.frames.append(frame)
            n = len(self.frames)
            pages = frame["evidence_working_set"]["pages"]
            assert all("FAKE_PRIOR" not in p["content"] for p in pages)
            assert not frame["current_run"]["recorded_actions"]
            if n == 1:
                assert not pages
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": command},
                    "rationale": "Actual failed control",
                }
            expected = outputs[:1] if n == 2 else outputs
            assert [p["content"] for p in pages] == expected
            assert all(p["projection_kind"] == "current_run_broker_output" for p in pages)
            assert all(p["operation"] == "run_public_command" for p in pages)
            assert frame["evidence_working_set"]["omitted_read_count"] == 0
            assert frame["evidence_working_set"]["omitted_broker_output_count"] == 0
            oracle = frame["current_run"]["oracle_executions"][0]
            assert oracle["status"] == ("stale_workspace" if n == 6 else "failed_process")
            status = "stale_workspace" if n == 6 else "matches_current_workspace"
            assert all(p["source_workspace_status"] == status for p in pages)
            assert pages[0]["exit_code"] == 1
            for observation in frame["observations"]:
                if observation.get("observation_id") in {p["observation_id"] for p in pages}:
                    assert "output_excerpt" not in observation
                    assert observation["output_location"].startswith("evidence_working_set.pages")
            if n == 2:
                return {
                    "operation": "run_public_command",
                    "arguments": {"argv": ["python3", "-c", "print('audit')"]},
                    "rationale": "Separate resource audit",
                }
            if n in {3, 4}:
                return {
                    "operation": "read_file",
                    "arguments": {"path": "checker.py"},
                    "rationale": "Inspect current source",
                }
            if n == 5:
                return {
                    "operation": "write_file",
                    "arguments": {"path": "checker.py", "content": original + "\n# edit\n"},
                    "rationale": "Change workspace",
                }
            return {
                "operation": "finish",
                "arguments": {},
                "rationale": "End without success claim",
            }

    transport = Transport()
    initial = (
        {
            "operation": "run_public_command",
            "observation_id": "public:observation:99",
            "output": "FAKE_PRIOR_COMMAND",
            "exit_code": 0,
        },
        {
            "operation": "read_public_evidence",
            "observation_id": "public:observation:100",
            "content": "FAKE_PRIOR_READER",
        },
    )
    with CatalogStore(tmp_path / "small-commands.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            transport,
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(),
            arm="B0",
            tools_factory=Tools,
        ).run(
            task,
            use_frozen_selection=True,
            recordable_actions=(action,),
            initial_observations=initial,
        )
    assert result["solver_ended"] and not result["failure"]
    assert len(transport.frames) == 6 and len(executions) == 2
    assert not result["action_observations"] and result["validated_resolved"] is None
    actual = result["public_observations"][len(initial) :]
    assert sum(o["operation"] == "run_public_command" for o in actual) == 2
    assert not any(o["operation"] == "read_public_evidence" for o in actual)
    assert result["budget"]["caps"]["model_tokens"] == 300000


def test_mixed_window_orders_by_actual_sequence_and_deduplicates_exact_full_read(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    records = {}
    for n in (2, 10):
        identity = f"public:observation:{n}"
        records[identity] = {
            "operation": "run_public_command",
            "observation_id": identity,
            "output": f"output-{n}",
            "exit_code": 1,
            "workspace_execution_sha256": "current",
        }
    read = read_public_evidence(
        task, records, {"evidence_id": "public:observation:2", "field": "output"}
    )
    read["observation_id"] = "public:observation:11"
    reads = {read["observation_id"]: read}
    before = copy.deepcopy((task.to_dict(), records, reads))
    view = solver_evidence_working_set(task, records, reads, workspace_execution_sha256="current")
    assert [p["content"] for p in view["pages"]] == ["output-10", "output-2"]
    assert view["pages"][-1]["projection_kind"] == "explicit_evidence_read"
    assert view["deduplicated_page_count"] == 1
    assert view["omitted_read_count"] == 0 and view["omitted_broker_output_count"] == 1
    assert (task.to_dict(), records, reads) == before
    records["public:observation:2"]["output"] = "changed stored record"
    changed = solver_evidence_working_set(
        task, records, reads, workspace_execution_sha256="current"
    )
    assert changed["pages"][-1]["source_record_status"] == "changed_or_unavailable"
    assert len(changed["pages"]) == 3


def test_small_output_window_never_expands_limits_or_projects_untrusted_identity(tmp_path):
    _, task, _ = make_fixture(tmp_path)
    records = {}
    for n in range(12):
        identity = f"public:observation:{n}"
        records[identity] = {
            "operation": "run_public_command",
            "observation_id": identity,
            "output": str(n) + "x" * 1999,
            "exit_code": n % 2,
        }
    records["public:observation:20"] = {
        "operation": "run_public_command",
        "observation_id": "public:observation:20",
        "output": "large" * 1000,
        "exit_code": 0,
    }
    records["public:observation:21"] = {
        "operation": "run_public_command",
        "observation_id": "public:observation:999",
        "output": "UNTRUSTED_IDENTITY",
        "exit_code": 0,
    }
    records["public:observation:22"] = {
        "operation": "read_file",
        "observation_id": "public:observation:22",
        "content": "NOT_A_COMMAND",
    }
    before = copy.deepcopy(records)
    view = solver_evidence_working_set(task, records, {}, workspace_execution_sha256="current")
    assert view["pages"] and len(view["pages"]) <= 8
    assert sum(len(p["content"]) for p in view["pages"]) <= 12000
    assert all(len(p["content"]) <= 4000 for p in view["pages"])
    assert view["pages"][-1]["observation_id"] == "public:observation:11"
    assert view["omitted_read_count"] == 0 and view["omitted_broker_output_count"] > 0
    assert all(p["source_workspace_status"] == "not_established" for p in view["pages"])
    assert all(
        "UNTRUSTED" not in p["content"] and "NOT_A_COMMAND" not in p["content"]
        for p in view["pages"]
    )
    assert records == before
