"""Auxiliary roles are current binding obligations, including native contracts."""

import hashlib
import json
import re
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from adaptive_fixture import CUTOFF, authored_bundle, make_fixture

from arex_skill_graph.action_contracts import ActionContract, Predicate, TemporalPolicy
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_guidance import current_grounding
from arex_skill_graph.execution_frontier import action_execution_checks, declared_write_paths
from arex_skill_graph.pattern_contracts import publish_v4_bundle
from arex_skill_graph.plan_validation import ResourcePolicy, validate_task_plan
from arex_skill_graph.task_context import Binding, ObservedFact, PortValue, SemanticCheck
from arex_skill_graph.workflow_ranker import workflow_capsule
from arex_skill_graph.workflow_rewriter import bind_selection

ROLE = "function-node-family"
FENCE = chr(96) * 3
CONTRACT = FENCE + r"arex-contract-v4\n(.*?)\n" + FENCE


def fixture(tmp_path):
    _original, task, _policy = make_fixture(tmp_path, pattern=False)
    response, sources = authored_bundle(pattern=False)

    def augment(match):
        row = json.loads(match[1])
        if row["id"] == "guard:a":
            row["read_set"] = ["role:" + ROLE]
            row["write_set"].append("role:" + ROLE)
            row["preconditions"].append(asdict(Predicate("role:" + ROLE, True, "symbol_exists")))
        return FENCE + "arex-contract-v4\n" + json.dumps(row, indent=2) + "\n" + FENCE

    response = re.sub(CONTRACT, augment, response, flags=re.S)
    (package,) = publish_v4_bundle(
        response, sources, TemporalPolicy(CUTOFF), tmp_path / "augmented"
    )
    policy = ResourcePolicy(TemporalPolicy(CUTOFF), (package.reference,))
    guard = next(a for a in package.actions if a.id == "guard:a")
    probe = next(a for a in package.actions if a.id == "detect:a")
    binding = Binding(
        ROLE, "current:context", "type_only", "Python", "type_only(context)", ("current:context",)
    )
    task = task.update(
        bindings=(binding,),
        facts=(ObservedFact("context_known", True, ("current:context",)),),
        checks=(
            SemanticCheck(
                "owner:" + ROLE,
                "PASS",
                "Synthetic auxiliary implementation reviewed",
                ("current:context",),
                "fixture-review",
            ),
            SemanticCheck(
                "current-connect:context:guard:a:context",
                "PASS",
                "Actual fixture port connection reviewed",
                ("current:context",),
                "fixture-review",
            ),
        ),
        port_values=(PortValue(probe.outputs[0], ("current:context",)),),
    )
    task.verify()
    return package, task, policy, guard


def test_real_overload_contract_declares_auxiliary_node_and_test_roles():
    root = Path(__file__).resolve().parents[1]
    directory = (
        root
        / "data/skill-extraction/packages/candidates/pyflakes-mechanism-history-v4-20261004/b8f8b3836dbeb26b4ee62590/async-ast-classification-extension/references/actions"
    )
    rows = []
    for path in directory.glob("*.md"):
        match = re.search(CONTRACT, path.read_text(), re.S)
        if match:
            action = ActionContract.from_dict(json.loads(match[1]))
            if action.id.endswith((":overload-inspect", ":overload-edit", ":overload-validate")):
                rows.append(action)
    assert len(rows) == 3
    for action in rows:
        assert set(action.required_binding_roles) == {
            "overload-recognition",
            ROLE,
            "overload-regression-tests",
        }
        assert ROLE != action.owner_role


def test_binding_role_derivation_is_deterministic_and_distinguishes_facts(tmp_path):
    _p, _task, _policy, action = fixture(tmp_path)
    action = replace(
        action,
        read_set=("literal.py", "role:z", "role:a", "role:z"),
        write_set=("role:a",),
        preconditions=(
            Predicate("role:fact", True),
            Predicate("role:absent", False, "file_exists"),
        ),
        preserves=(Predicate("role:preserved", True, "symbol_exists"),),
        exclusions=(Predicate("role:excluded", True, "file_exists"),),
        effects=(Predicate("role:future", True, "file_exists"),),
    )
    assert action.required_binding_roles == (
        action.owner_role,
        "a",
        "absent",
        "excluded",
        "preserved",
        "z",
    )
    assert "required_binding_roles" not in action.to_dict()
    with pytest.raises(ValueError, match="binding role"):
        replace(action, read_set=("role:",)).required_binding_roles


def test_complete_auxiliary_binding_reaches_all_four_gates(tmp_path):
    package, task, policy, guard = fixture(tmp_path)
    workflow = package.workflows[0]
    plan = bind_selection(
        task, None, tuple(a for a in workflow.actions if a.kind != "read"), (workflow,)
    )
    instance = next(i for i in plan.instances if i.action.id == guard.id)
    assert {b.role for b in instance.bindings} == set(guard.required_binding_roles)
    assert validate_task_plan(plan, task, policy).mode == "use"
    assert workflow_capsule(workflow, task, policy).hard_mode == "use"
    assert action_execution_checks(guard, task)["ready"]
    assert declared_write_paths(guard, task) == {"checker.py", "context.py"}


@pytest.mark.parametrize(
    "mutation, mode",
    [
        ("missing_binding", "probe_only"),
        ("missing_review", "probe_only"),
        ("contrary_review", "reject"),
        ("wrong_language", "reject"),
    ],
)
def test_auxiliary_binding_cannot_be_bypassed_by_primary_owner(tmp_path, mutation, mode):
    package, task, policy, guard = fixture(tmp_path)
    if mutation == "missing_binding":
        task = replace(task, bindings=tuple(b for b in task.bindings if b.role != ROLE))
    elif mutation == "missing_review":
        task = replace(task, checks=tuple(c for c in task.checks if c.key != "owner:" + ROLE))
    elif mutation == "contrary_review":
        task = task.update(
            checks=(
                SemanticCheck(
                    "owner:" + ROLE,
                    "FAIL",
                    "Fixture contradicts this boundary",
                    ("current:context",),
                    "fixture-review",
                ),
            )
        )
    else:
        task = replace(
            task,
            bindings=tuple(
                replace(b, language="JavaScript") if b.role == ROLE else b for b in task.bindings
            ),
        )
    workflow = package.workflows[0]
    plan = bind_selection(
        task, None, tuple(a for a in workflow.actions if a.kind != "read"), (workflow,)
    )
    assert validate_task_plan(plan, task, policy).mode == mode
    assert workflow_capsule(workflow, task, policy).hard_mode == mode
    assert not action_execution_checks(guard, task)["ready"]
    assert task.semantic("owner:" + guard.owner_role).status == "PASS"


def test_instance_must_carry_current_auxiliary_binding(tmp_path):
    package, task, policy, guard = fixture(tmp_path)
    workflow = package.workflows[0]
    plan = bind_selection(
        task, None, tuple(a for a in workflow.actions if a.kind != "read"), (workflow,)
    )
    plan = replace(
        plan,
        instances=tuple(
            replace(i, bindings=tuple(b for b in i.bindings if b.role != ROLE))
            if i.action.id == guard.id
            else i
            for i in plan.instances
        ),
    )
    report = validate_task_plan(plan, task, policy)
    assert report.mode == "probe_only"
    assert any(
        c.code == "current_binding"
        and c.subject.endswith(":role:" + ROLE)
        and c.status == "UNKNOWN"
        for c in report.checks
    )


def test_refresh_invalidates_auxiliary_binding_and_review(tmp_path):
    package, task, policy, guard = fixture(tmp_path)
    anchor = next(a for a in task.anchors if a.id == "current:context")
    path = Path(task.root) / anchor.path
    path.write_text(path.read_text() + "\n# changed public implementation\n")
    task = task.update(
        anchors=(replace(anchor, sha256=hashlib.sha256(path.read_bytes()).hexdigest()),)
    )
    task.verify()
    assert not any(b.role == ROLE for b in task.bindings)
    assert task.semantic("owner:" + ROLE).status == "UNKNOWN"
    assert not action_execution_checks(guard, task)["ready"]
    assert workflow_capsule(package.workflows[0], task, policy).hard_mode == "probe_only"


@pytest.mark.parametrize("invented", [False, True])
def test_grounding_requests_auxiliary_roles_and_rejects_undeclared_roles(tmp_path, invented):
    package, task, _policy, guard = fixture(tmp_path)

    class GroundingFixture:
        calls = []

        def complete(self, **request):
            payload = json.loads(request["user"])
            assert "owner:" + ROLE in payload["expected_check_keys"]
            schema = request["response_schema"]
            assert schema["additionalProperties"] is False
            checks = schema["properties"]["checks"]
            assert checks["minItems"] == checks["maxItems"] == len(payload["expected_check_keys"])
            assert checks["items"]["properties"]["key"]["enum"] == payload["expected_check_keys"]
            assert checks["items"]["additionalProperties"] is False
            capsule = next(a for a in payload["actions"] if a["id"] == guard.id)
            assert set(capsule["required_binding_roles"]) == set(guard.required_binding_roles)
            assert capsule["read_set"] == ["role:" + ROLE]
            assert "role:" + ROLE in capsule["write_set"]
            bindings = [asdict(b) for b in task.bindings]
            if invented:
                bindings.append({**bindings[-1], "role": "undeclared-owner"})
            reply = {
                "checks": [
                    asdict(
                        SemanticCheck(
                            k,
                            "PASS",
                            "Synthetic current evidence review",
                            ("current:context", "current:checker"),
                            "fixture-review",
                        )
                    )
                    for k in payload["expected_check_keys"]
                ],
                "bindings": bindings,
                "facts": [],
                "oracles": [asdict(o) for o in task.oracles],
            }
            if not invented:
                import copy
                from jsonschema import Draft202012Validator

                normalized = json.loads(json.dumps(reply))
                validator = Draft202012Validator(schema)
                validator.validate(normalized)
                nested = copy.deepcopy(normalized)
                nested["oracles"][0]["command"] = [nested["oracles"][0]["command"]]
                assert not validator.is_valid(nested)
                extra = copy.deepcopy(normalized)
                extra["checks"].append(
                    {**extra["checks"][0], "key": "future-post-edit-observation"}
                )
                assert not validator.is_valid(extra)
                rogue = copy.deepcopy(normalized)
                rogue["bindings"][0]["role"] = "undeclared-owner"
                assert not validator.is_valid(rogue)
                combined = copy.deepcopy(normalized)
                combined["bindings"][0]["symbol"] = "PY35_PLUS; is_typing_overload"
                assert not validator.is_valid(combined)
            return reply

    public = replace(task, checks=(), bindings=(), oracles=())
    ledger = BudgetLedger(BudgetCaps(history_tokens=200000))
    if invented:
        with pytest.raises(ValueError, match="non-candidate binding role"):
            current_grounding(public, (package,), GroundingFixture(), ledger)
    else:
        current = current_grounding(public, (package,), GroundingFixture(), ledger)
        assert any(b.role == ROLE for b in current.bindings)
        assert current.semantic("owner:" + ROLE).status == "PASS"
        assert action_execution_checks(guard, current)["ready"]


def test_auxiliary_write_alias_still_requires_dependency_with_reading_probe(tmp_path):
    package, task, policy, _guard = fixture(tmp_path)
    workflow = package.workflows[0]
    plan = bind_selection(task, None, workflow.actions, (workflow,))
    report = validate_task_plan(plan, task, policy)
    assert report.mode == "reject"
    assert any(c.code == "write_conflict" and c.status == "FAIL" for c in report.checks)


@pytest.mark.parametrize(
    "symbol",
    [
        "PY35_PLUS",
        "node_api",
        "overload_marker",
        "CAPABILITY",
        "LEFT",
        "RIGHT",
        "Policy.KINDS",
        "checker.Policy.KINDS",
    ],
)
def test_module_constants_aliases_and_class_attributes_can_be_bound(tmp_path, symbol):
    _package, task, _policy = make_fixture(tmp_path, pattern=False)
    anchor = next(a for a in task.anchors if a.id == "current:checker")
    path = Path(task.root) / anchor.path
    path.write_text(
        path.read_text()
        + "\nimport ast as node_api\nfrom typing import overload as overload_marker\nPY35_PLUS = True\nCAPABILITY: bool = True\nLEFT, RIGHT = (1, 2)\nclass Policy:\n    KINDS = (node_api.FunctionDef,)\n"
    )
    task = task.update(
        anchors=(replace(anchor, sha256=hashlib.sha256(path.read_bytes()).hexdigest()),)
    )
    binding = Binding(
        "module-symbol", anchor.id, symbol, "Python", "Current declared Python object", (anchor.id,)
    )
    task = replace(task, bindings=(binding,), checks=())
    task.verify()
    assert task.semantic("owner:module-symbol").status == "UNKNOWN"


@pytest.mark.parametrize(
    "symbol", ["FunctionDef", "IMPORTED_BUT_UNBOUND", "STRING_ONLY", "MISSING_OBJECT"]
)
def test_references_and_string_literals_do_not_invent_declared_bindings(tmp_path, symbol):
    _package, task, _policy = make_fixture(tmp_path, pattern=False)
    anchor = next(a for a in task.anchors if a.id == "current:checker")
    path = Path(task.root) / anchor.path
    path.write_text(
        path.read_text()
        + "\nimport ast\nKINDS = (ast.FunctionDef,)\nTEXT = 'STRING_ONLY'\nfrom typing import overload as real_alias\ndef unresolved():\n    return IMPORTED_BUT_UNBOUND\n"
    )
    task = task.update(
        anchors=(replace(anchor, sha256=hashlib.sha256(path.read_bytes()).hexdigest()),)
    )
    binding = Binding(
        "module-symbol", anchor.id, symbol, "Python", "Claimed declared object", (anchor.id,)
    )
    task = replace(task, bindings=(binding,), checks=())
    with pytest.raises(ValueError, match="bound Python symbol does not exist"):
        task.verify()
