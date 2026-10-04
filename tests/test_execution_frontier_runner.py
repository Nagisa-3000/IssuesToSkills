"""Broker gating fixtures do not claim operating-system isolation."""

from pathlib import Path
from typing import ClassVar

from adaptive_fixture import make_fixture

from arex_skill_graph.action_contracts import Dependency
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import ReplayTransport
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.plan_validation import (
    ActionInstance,
    InputLink,
    TaskWorkflowPlan,
    validate_task_plan,
)
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import ObservedFact, PortValue, SemanticCheck
from arex_skill_graph.workflow_ranker import WorkflowRanker


class RecordingTools:
    isolation = "test-only-recording-fixture"
    runtime_sha256 = "test-only"
    calls: ClassVar[list] = []

    def __init__(self, root, _budget):
        self.root = Path(root)

    def preflight(self):
        pass

    def close(self):
        pass

    def run(self, argv, *, readonly_workspace=False, **_options):
        self.calls.append({"argv": argv, "readonly_workspace": readonly_workspace})
        if not readonly_workspace:
            (self.root / "checker.py").write_text("unauthorized = True\n")
        return {
            "argv": argv,
            "exit_code": 1 if readonly_workspace else 0,
            "output": "Fixture records the broker's write authorization flag.",
        }


def plan_for(package, task):
    workflow = package.workflows[0]
    names = {"detect:a": "probe", "guard:a": "edit", "validate:a": "validate"}
    return TaskWorkflowPlan(
        "plan:execution-frontier",
        task.task_id,
        task.base_commit,
        task.revision,
        tuple(
            ActionInstance(
                names[a.id],
                a,
                tuple(b for b in task.bindings if b.role == a.owner_role),
                a.semantic_role,
                "Bind the actual synthetic owner",
            )
            for a in workflow.actions
        ),
        (
            Dependency("probe", "edit", "Context required", ("current:context",)),
            Dependency("edit", "validate", "Validate the actual edit", ("current:checker",)),
        ),
        (
            InputLink(
                "edit",
                "context",
                producer="probe",
                output_port="context",
                evidence_refs=("current:context",),
            ),
        ),
        workflow.required_effects,
        workflow.invariants,
        (workflow.id,),
    )


def solver_result(tmp_path, task, policy, plan, steps):
    with CatalogStore(tmp_path / "catalog.sqlite") as store:
        store.initialize()
        return AdaptiveSolver(
            ReplayTransport(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=RecordingTools,
        ).run(task, use_frozen_selection=True, initial_plan=plan)


def test_conditional_plan_pass_does_not_authorize_an_edit_from_predicted_ports(tmp_path):
    package, task, policy = make_fixture(tmp_path, pattern=False)
    plan = plan_for(package, task)
    assert validate_task_plan(plan, task, policy).mode == "use"
    RecordingTools.calls = []
    result = solver_result(
        tmp_path,
        task,
        policy,
        plan,
        [
            {
                "operation": "write_file",
                "arguments": {
                    "action_id": "guard:a",
                    "path": "checker.py",
                    "content": "unauthorized = True\n",
                },
                "rationale": "Attempt guided edit before observing the planned predecessor.",
            },
            {
                "operation": "run_public_command",
                "arguments": {
                    "action_id": "guard:a",
                    "argv": ["python3", "-c", "attempt modification"],
                },
                "rationale": "Command route cannot bypass the actual input gate.",
            },
            {"operation": "finish", "arguments": {}, "rationale": "End rejection fixture."},
        ],
    )
    assert result["solver_ended"] and not result["failure"]
    assert not result["patch"]
    assert "actual ready Action" in result["public_observations"][0]["denied"]
    assert RecordingTools.calls[0]["readonly_workspace"]


def test_guided_edit_requires_fresh_review_or_explicit_fallback_after_code_changes(tmp_path):
    package, task, policy = make_fixture(tmp_path, pattern=False)
    port = next(a for a in package.actions if a.id == "detect:a").outputs[0]
    task = task.update(
        facts=(ObservedFact("context_known", True, ("current:context",)),),
        port_values=(PortValue(port, ("current:context",)),),
        checks=(
            SemanticCheck(
                "current-connect:context:guard:a:context",
                "PASS",
                "Synthetic current-port review",
                ("current:context",),
                "fixture-review",
            ),
        ),
    )
    plan = plan_for(package, task)
    original = Path(task.root, "checker.py").read_text()
    fixed = original.replace("return True", "return context != 'type'")
    result = solver_result(
        tmp_path,
        task,
        policy,
        plan,
        [
            {
                "operation": "write_file",
                "arguments": {"action_id": "guard:a", "path": "checker.py", "content": fixed},
                "rationale": "The current input and owner have been reviewed.",
            },
            {
                "operation": "write_file",
                "arguments": {"path": "extra.py", "content": "unreviewed = True\n"},
                "rationale": "An invalidated plan cannot silently authorize further changes.",
            },
            {
                "operation": "drop_guidance",
                "arguments": {},
                "rationale": "Explicitly continue as an ordinary solver from current observations.",
            },
            {
                "operation": "write_file",
                "arguments": {"path": "extra.py", "content": "fallback = True\n"},
                "rationale": "Authorized ordinary solving after explicit fallback.",
            },
            {"operation": "finish", "arguments": {}, "rationale": "End fixture."},
        ],
    )
    assert result["solver_ended"] and not result["failure"]
    assert "previous guided edit" in result["public_observations"][1]["denied"]
    assert any(o["operation"] == "drop_guidance" for o in result["public_observations"])
    assert "fallback = True" in result["patch"]
    assert "unreviewed = True" not in result["patch"]
    assert Path(task.root, "checker.py").read_text() == original


def test_strict_functional_catalog_cannot_edit_from_unknown_inputs(tmp_path):
    package, task, policy = make_fixture(tmp_path, pattern=False)
    action = next(a for a in package.actions if a.id == "guard:a")
    RecordingTools.calls = []
    steps = [
        {
            "operation": "write_file",
            "arguments": {
                "action_id": action.id,
                "path": "checker.py",
                "content": "unauthorized = True\n",
            },
            "rationale": "Try a modifying Action with no current input port.",
        },
        {
            "operation": "run_public_command",
            "arguments": {
                "action_id": action.id,
                "argv": ["python3", "-c", "attempt modification"],
            },
            "rationale": "The command path must enforce the same prerequisite gate.",
        },
        {"operation": "finish", "arguments": {}, "rationale": "End strict fixture."},
    ]
    with CatalogStore(tmp_path / "strict.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            ReplayTransport(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            tools_factory=RecordingTools,
        ).run(
            task,
            use_frozen_selection=True,
            recordable_actions=(action,),
            enforce_catalog_prerequisites=True,
        )
    assert result["solver_ended"] and not result["failure"]
    assert not result["patch"]
    assert result["strict_functional_action_catalog"]
    assert "actual current prerequisites" in result["public_observations"][0]["denied"]
    assert RecordingTools.calls[0]["readonly_workspace"]
