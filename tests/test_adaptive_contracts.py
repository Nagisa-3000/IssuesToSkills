from dataclasses import replace
import hashlib
import json
import subprocess

import pytest

from adaptive_fixture import authored_bundle, make_fixture, CUTOFF
from arex_skill_graph.action_contracts import CheckStatus, Predicate, TemporalPolicy, Dependency
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger, BudgetExceeded
from arex_skill_graph.adaptive_guidance import index_native_package, prepare_adaptive_guidance
from arex_skill_graph.crossbind import splice_workflows, cut_workflow, substitute_action
from arex_skill_graph.guidance_renderer import GuidanceRenderer
from arex_skill_graph.pattern_contracts import publish_v4_bundle, load_native_package
from arex_skill_graph.plan_validation import validate_task_plan, TaskWorkflowPlan
from arex_skill_graph.skill_packages import hydrate_package, validate_package
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.task_context import SemanticCheck, TaskContext, ObservedFact
from arex_skill_graph.workflow_ranker import WorkflowRanker, workflow_capsule, CRITERIA
from arex_skill_graph.workflow_rewriter import bind_selection, rewrite_workflow


def ledger(**kwargs):
    return BudgetLedger(BudgetCaps(history_tokens=200000, **kwargs))


def good_plan(package, task):
    w = package.workflows[0]
    return bind_selection(task, package.pattern, w.actions, (w,))


def test_native_roundtrip_and_copied_integrity(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    assert validate_package(tmp_path / "packages/type-context-pattern") == []
    plan = good_plan(p, task)
    assert TaskWorkflowPlan.from_dict(json.loads(json.dumps(plan.to_dict()))) == plan
    report = validate_task_plan(plan, task, policy)
    assert report.status == CheckStatus.PASS, report.to_dict()
    assert report.to_dict()["behavior_verified"] is False
    assert hydrate_package({"skill_package": p.reference}, render=False)["rendered"] == ""
    result = subprocess.run(
        ["python3", str(tmp_path / "packages/type-context-pattern/scripts/verify_package.py")],
        capture_output=True,
    )
    assert result.returncode == 0
    source = tmp_path / "packages/type-context-pattern/references/actions/guard-a.md"
    source.write_text(source.read_text() + "tampered\n")
    with pytest.raises(ValueError):
        load_native_package(p.reference)


def test_predicate_description_is_not_semantic_identity():
    assert Predicate("x", True, description="A") == Predicate("x", True, description="B")


def test_duplicate_pattern_and_temporal_sources_rejected(tmp_path):
    response, sources = authored_bundle(duplicate=True)
    with pytest.raises(ValueError, match="independent"):
        publish_v4_bundle(response, sources, TemporalPolicy(CUTOFF), tmp_path / "duplicates")
    assert not list((tmp_path / "duplicates").glob("type-*"))
    response, sources = authored_bundle()
    with pytest.raises(ValueError, match="cutoff"):
        publish_v4_bundle(
            response, sources, TemporalPolicy("2019-01-01T00:00:00Z"), tmp_path / "future"
        )


def test_cut_splice_executes_public_oracle(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    left, right = p.workflows
    cut = cut_workflow(right, ["guard:b"], task)
    assert "validate:b" in cut.retained_action_ids
    result = splice_workflows(
        left, right, ["detect:a"], ["guard:b"], task, p.pattern, ledger(), policy
    )
    assert result.plans, [r.to_dict() for r in result.rejected]
    assert result.reports[0].status == "PASS"
    assert set(result.plans[0].parent_workflow_ids) == {left.id, right.id}
    rendered = GuidanceRenderer(policy, ledger()).render(result.plans[0], task)
    assert "guard:b" in rendered
    root = task.root
    before = subprocess.run(["python3", root + "/checker.py"], capture_output=True)
    assert before.returncode != 0
    from pathlib import Path

    source = Path(root) / "checker.py"
    source.write_text(source.read_text().replace("return True", "return context != 'type'"))
    after = subprocess.run(["python3", str(source)], capture_output=True)
    assert after.returncode == 0
    with pytest.raises(ValueError, match="refresh"):
        task.verify()
    changed = replace(task.anchors[-1], sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    refreshed = task.update(anchors=(changed,))
    assert not refreshed.bindings or all(
        "current:checker" not in b.evidence_refs for b in refreshed.bindings
    )


@pytest.mark.parametrize(
    "mutation, expected",
    [
        ("missing_prerequisite", "precondition"),
        ("missing_validation", "verification_closure"),
        ("cycle", "DAG"),
        ("missing_role", "pattern_role"),
        ("fake_action", "action_contract"),
        ("missing_interface", "current_or_package_evidence"),
        ("cross_language", "current_or_package_evidence"),
    ],
)
def test_invalid_compositions(tmp_path, mutation, expected):
    p, task, policy = make_fixture(tmp_path)
    plan = good_plan(p, task)
    if mutation == "missing_prerequisite":
        task = replace(
            task, facts=(*task.facts, ObservedFact("context_known", False, ("current:context",)))
        )
        plan = replace(
            plan,
            instances=tuple(i for i in plan.instances if i.action.kind != "read"),
            dependencies=tuple(d for d in plan.dependencies if "detect:" not in d.before),
        )
    elif mutation == "missing_validation":
        plan = replace(
            plan,
            instances=tuple(i for i in plan.instances if i.action.kind != "validate"),
            dependencies=tuple(d for d in plan.dependencies if "validate:" not in d.after),
        )
    elif mutation == "cycle":
        first, last = plan.instances[0], plan.instances[-1]
        plan = replace(
            plan,
            dependencies=(
                *plan.dependencies,
                Dependency(last.id, first.id, "Artificial cycle", ("evidence:a",)),
            ),
        )
    elif mutation == "missing_role":
        # Keep goals achievable but lie about the required Pattern role.
        plan = replace(
            plan,
            instances=tuple(
                replace(i, role="irrelevant") if i.action.kind == "read" else i
                for i in plan.instances
            ),
        )
    elif mutation == "fake_action":
        plan = replace(
            plan,
            instances=(
                replace(
                    plan.instances[0],
                    action=replace(plan.instances[0].action, operation="Invented operation"),
                ),
                *plan.instances[1:],
            ),
        )
    elif mutation == "missing_interface":
        task = replace(
            task, bindings=(replace(task.bindings[0], symbol="missing_symbol"), task.bindings[1])
        )
    elif mutation == "cross_language":
        task = replace(
            task, bindings=(replace(task.bindings[0], language="Rust"), task.bindings[1])
        )
    report = validate_task_plan(plan, task, policy)
    assert report.status == "FAIL", report.to_dict()
    assert any(c.code == expected and c.status == "FAIL" for c in report.checks), report.to_dict()


def test_unknown_semantics_cannot_authorize_edit(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    task = replace(task, checks=tuple(c for c in task.checks if not c.key.startswith("connect:")))
    plan = good_plan(p, task)
    report = validate_task_plan(plan, task, policy)
    assert report.mode == "probe_only"
    rendered = GuidanceRenderer(policy, ledger()).render(plan, task)
    assert "probe_only" in rendered and "Narrow the actual diagnostic" not in rendered


def test_static_runtime_port_rejected(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    plan = good_plan(p, task)
    guard = plan.instances[1]
    bad = replace(guard.action, inputs=(replace(guard.action.inputs[0], phase="runtime"),))
    plan = replace(
        plan, instances=(plan.instances[0], replace(guard, action=bad), plan.instances[2])
    )
    report = validate_task_plan(plan, task, policy)
    assert any(c.code == "port_contract" and c.status == "FAIL" for c in report.checks)


def test_real_alias_write_conflict(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    actions = (p.workflows[0].actions[1], p.workflows[1].actions[1])
    plan = bind_selection(task, None, actions, p.workflows)
    report = validate_task_plan(plan, task, policy)
    assert any(c.code == "write_conflict" and c.status == "FAIL" for c in report.checks)


def test_sourced_port_bridge_is_inserted(tmp_path):
    p, task, policy = make_fixture(tmp_path, pattern=False, bridge=True)
    from arex_skill_graph.workflow_rewriter import prerequisite_closure

    selected, changes, _ = prerequisite_closure(
        (next(a for a in p.actions if a.id == "guard:a"),), p.actions, task
    )
    assert "bridge:a" in {a.id for a in selected}
    assert "bridge-check:a" in {a.id for a in selected}
    assert any(c["operation"] == "insert_bridge" for c in changes)
    assert all(c["source_ids"] for c in changes)


class RankingReplay:
    def __init__(self, bad=False):
        self.bad = bad

    def complete(self, *, user, **kwargs):
        payload = json.loads(user)
        rows = []
        for capsule in payload["candidates"]:
            rows.append(
                {
                    "id": "invented" if self.bad else capsule["id"],
                    "mode": capsule["hard_mode"],
                    "utility": 1.0,
                    "uncertainty": 0.2,
                    "criteria_evidence": {
                        k: {
                            "rationale": "Synthetic evidence-backed replay",
                            "evidence_refs": ["current:issue"],
                        }
                        for k in CRITERIA
                    },
                    "unmet_preconditions": [],
                    "rationale": "Offline protocol fixture",
                }
            )
        return {"evaluations": rows}


def test_ranker_authority_unknown_id_and_order(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    capsules = [workflow_capsule(w, task, policy) for w in p.workflows]
    ranker = WorkflowRanker(RankingReplay())
    a = ranker.rank_workflows(task, capsules, policy, ledger())
    b = ranker.rank_workflows(task, list(reversed(capsules)), policy, ledger())
    assert a.selected_ids == b.selected_ids
    with pytest.raises(ValueError, match="unknown IDs"):
        WorkflowRanker(RankingReplay(True)).rank_workflows(task, capsules, policy, ledger())
    with pytest.raises(ValueError, match="authoritative"):
        ranker.rank_workflows(task, [replace(capsules[0], hard_mode="reject")], policy, ledger())
    assert WorkflowRanker().rank_workflows(task, capsules, policy, ledger()).decision == "abstain"


def test_native_retrieval_guidance_arms(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    with CatalogStore(tmp_path / "catalog.sqlite") as store:
        store.initialize()
        index_native_package(store, p.reference, policy.temporal)
        for arm in ("E0", "E1", "E2"):
            result = prepare_adaptive_guidance(
                task, store, policy, WorkflowRanker(RankingReplay()), ledger(), arm=arm
            )
            assert result["retrieved_ids"] and result["selected_plan"], result
            assert not result["behavior_verified"]
        with pytest.raises(ValueError, match="trained scorer"):
            prepare_adaptive_guidance(
                task, store, policy, WorkflowRanker(RankingReplay()), ledger(), arm="E3"
            )


def test_budget_and_public_input_isolation(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    context = task.to_dict()
    context["environment"] = [{"gold_patch": "blocked"}]
    with pytest.raises(ValueError, match="evaluator-only"):
        TaskContext.from_dict(context)
    budget = BudgetLedger(BudgetCaps(history_tokens=3))
    with pytest.raises(BudgetExceeded):
        budget.history("abcd", "rejected read still costs")
    assert budget.history_tokens == 4
    renderer = GuidanceRenderer(policy, ledger())
    with pytest.raises(ValueError, match="approved"):
        renderer.read_resource(p.reference["skill_id"], "SKILL.md", set())


def test_drop_satisfied_and_substitute_current_realization(tmp_path):
    from arex_skill_graph.task_context import PortValue

    p, task, policy = make_fixture(tmp_path)
    port = next(a for a in p.actions if a.id == "detect:a").outputs[0]
    port = replace(port, name="current_context")
    proof = tuple(
        SemanticCheck(
            f"current-connect:{port.name}:guard:{letter}:context",
            "PASS",
            "Observed current context has required meaning",
            ("current:context",),
            "fixture-review",
        )
        for letter in ("a", "b")
    )
    ready = task.update(
        facts=(ObservedFact("context_known", True, ("current:context",)),),
        port_values=(PortValue(port, ("current:context",)),),
        checks=proof,
    )
    rewrite = rewrite_workflow(p.pattern, ready, p.actions, ledger(), workflows=p.workflows)
    assert rewrite.candidate_dags
    assert all(
        not any(i.action.id.startswith("detect:") for i in plan.instances)
        for plan in rewrite.candidate_dags
    )
    assert any(c["operation"] == "drop_satisfied_action" for c in rewrite.candidate_dags[0].changes)
    original = good_plan(p, task)
    updated, report = substitute_action(
        original,
        "guard:a",
        next(a for a in p.actions if a.id == "guard:b"),
        task,
        p.workflows,
        policy,
    )
    assert report.status == "PASS", report.to_dict()
    assert updated.id != original.id and any(
        c["operation"] == "substitute" for c in updated.changes
    )


def test_invariant_and_cross_language_are_hard_failures(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    plan = good_plan(p, task)
    guard = plan.instances[1]
    changed = replace(guard, action=replace(guard.action, invalidates=("runtime_preserved",)))
    report = validate_task_plan(
        replace(plan, instances=(plan.instances[0], changed, plan.instances[2])), task, policy
    )
    assert any(c.code == "invariant_invalidation" and c.status == "FAIL" for c in report.checks)
    rust_root = tmp_path / "rust"
    p2, task2, policy2 = make_fixture(rust_root, language="Rust")
    report = validate_task_plan(good_plan(p2, task2), task2, policy2)
    assert any(c.code == "binding_language" and c.status == "FAIL" for c in report.checks)


def test_all_rejected_does_not_resurrect_pattern_neighbors(tmp_path):
    p, task, policy = make_fixture(tmp_path)

    class RejectAll(RankingReplay):
        def complete(self, **kwargs):
            result = super().complete(**kwargs)
            for row in result["evaluations"]:
                row["mode"] = "reject"
            return result

    with CatalogStore(tmp_path / "rejected.sqlite") as store:
        store.initialize()
        index_native_package(store, p.reference, policy.temporal)
        result = prepare_adaptive_guidance(
            task, store, policy, WorkflowRanker(RejectAll()), ledger(), arm="E2"
        )
        assert result["fallback"] and result["plans"] == [] and result["role_gap_action_hits"] == []
    # Index writes really persist across catalog connections.
    with CatalogStore(tmp_path / "rejected.sqlite") as store:
        assert store.get_node("workflow:a") is not None


def test_predicate_description_cannot_tamper_native_action(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    plan = good_plan(p, task)
    guard = plan.instances[1]
    changed = replace(
        guard.action,
        preconditions=(replace(guard.action.preconditions[0], description="Unauthorized text"),),
    )
    report = validate_task_plan(
        replace(
            plan, instances=(plan.instances[0], replace(guard, action=changed), plan.instances[2])
        ),
        task,
        policy,
    )
    assert any(c.code == "action_contract" and c.status == "FAIL" for c in report.checks)


def test_distinct_owner_aliases_share_current_write_resource(tmp_path):
    p, task, policy = make_fixture(tmp_path, alias=True)
    guards = tuple(a for a in p.actions if a.kind == "edit")
    assert guards[0].write_set != guards[1].write_set
    plan = bind_selection(task, None, guards, p.workflows)
    report = validate_task_plan(plan, task, policy)
    assert any(c.code == "write_conflict" and c.status == "FAIL" for c in report.checks)


def test_cleanup_survives_cut_and_cannot_be_dropped(tmp_path):
    p, task, policy = make_fixture(tmp_path, cleanup=True, pattern=False)
    cut = cut_workflow(p.workflows[0], ["guard:a"], task)
    assert {"cleanup:a", "cleanup-check:a", "validate:a"}.issubset(cut.retained_action_ids)
    plan = good_plan(p, task)
    assert validate_task_plan(plan, task, policy).status == "PASS"
    omitted = "instance:cleanup:a"
    bad = replace(
        plan,
        instances=tuple(i for i in plan.instances if i.id != omitted),
        dependencies=tuple(d for d in plan.dependencies if omitted not in (d.before, d.after)),
    )
    report = validate_task_plan(bad, task, policy)
    assert any(c.code == "cleanup_closure" and c.status == "FAIL" for c in report.checks)


def test_inapplicable_optional_action_can_be_omitted(tmp_path):
    p, task, policy = make_fixture(tmp_path, pattern=False, optional=True)
    task = task.update(facts=(ObservedFact("plugin_available", False, ("current:issue",)),))
    capsule = workflow_capsule(p.workflows[0], task, policy)
    assert capsule.hard_mode != "reject"
    result = rewrite_workflow(None, task, p.actions, ledger(), workflows=p.workflows)
    plan = result.candidate_dags[0]
    assert "optional:a" not in {i.action.id for i in plan.instances}
    assert validate_task_plan(plan, task, policy).status == "PASS"


def test_current_role_predicates_and_qualified_symbols(tmp_path):
    p, task, policy = make_fixture(tmp_path)
    assert (
        task.condition(Predicate("role:diagnostic_owner", True, evaluator="file_exists")) == "PASS"
    )
    assert (
        task.condition(Predicate("role:diagnostic_owner", True, evaluator="symbol_exists"))
        == "PASS"
    )
    assert (
        task.condition(Predicate("role:unknown_owner", True, evaluator="symbol_exists"))
        == "UNKNOWN"
    )
    anchor = next(a for a in task.anchors if a.path == "context.py")
    from pathlib import Path

    source = Path(task.root) / "context.py"
    source.write_text("class Scope:\n    def type_only(self):\n        return True\n")
    fresh = replace(anchor, sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    from arex_skill_graph.task_context import Binding

    current = task.update(
        anchors=(fresh,),
        bindings=(
            Binding(
                "context_owner",
                anchor.id,
                "Scope.type_only",
                "Python",
                "Scope.type_only()",
                (anchor.id,),
            ),
        ),
    )
    current.verify()


def test_oracle_commands_are_bound_to_current_task(tmp_path):
    from arex_skill_graph.task_context import CurrentOracle

    package, task, policy = make_fixture(tmp_path)
    assert TaskContext.from_dict(json.loads(json.dumps(task.to_dict()))) == task
    current = tuple(
        CurrentOracle(
            o.action_id,
            o.source_oracle_id,
            "Use current public checks",
            ("python3", "-m", "current_public_checks"),
            o.evidence_refs,
        )
        for o in task.oracles
    )
    task = replace(task, oracles=current)
    plan = good_plan(package, task)
    rendered = GuidanceRenderer(policy, ledger()).render(plan, task)
    rows = json.loads(rendered.split("\n", 1)[1].split("\n", 1)[0])["actions"]
    assert all(
        row["oracles"][0]["command"] == ["python3", "-m", "current_public_checks"] for row in rows
    )
    assert all(
        row["oracles"][0]["command"] != list(instance.action.oracle[0].command)
        for row, instance in zip(rows, plan.instances)
    )
    missing = replace(task, oracles=())
    assert validate_task_plan(plan, missing, policy).mode == "probe_only"
    assert "current_public_checks" not in GuidanceRenderer(policy, ledger()).render(plan, missing)
    key = "oracle:" + plan.instances[0].action.id + ":" + plan.instances[0].action.oracle[0].id
    failed = task.update(
        checks=(
            SemanticCheck(
                key, "FAIL", "Wrong current behavior boundary", ("current:issue",), "review"
            ),
        )
    )
    assert (
        validate_task_plan(replace(plan, context_revision=failed.revision), failed, policy).mode
        == "reject"
    )
    with pytest.raises(ValueError, match="duplicate current oracle"):
        replace(task, oracles=(*current, current[0]))
    with pytest.raises(ValueError, match="reference is not closed"):
        replace(task, oracles=(replace(current[0], evidence_refs=("historical:answer",)),))


def test_refresh_removes_stale_current_oracles(tmp_path):
    from pathlib import Path

    package, task, policy = make_fixture(tmp_path)
    anchor = next(a for a in task.anchors if a.path == "context.py")
    path = Path(task.root) / anchor.path
    path.write_text(path.read_text() + "\n# public observation refreshed\n")
    fresh = replace(anchor, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    updated = task.update(anchors=(fresh,))
    assert not any(anchor.id in o.evidence_refs for o in updated.oracles)
    assert not any(
        c.key.startswith("oracle:") and anchor.id in c.evidence_refs for c in updated.checks
    )
    plan = good_plan(package, updated)
    assert validate_task_plan(plan, updated, policy).mode == "probe_only"


def test_grounding_adapts_oracles_from_public_evidence(tmp_path):
    from arex_skill_graph.adaptive_guidance import current_grounding

    package, task, policy = make_fixture(tmp_path)

    class GroundingReplay:
        calls = []

        def complete(self, **request):
            payload = json.loads(request["user"])
            assert set(request["response_schema"]["required"]) == {
                "checks",
                "bindings",
                "facts",
                "oracles",
            }
            return {
                "checks": [
                    SemanticCheck(
                        key,
                        "PASS",
                        "Current public implementation reviewed",
                        ("current:context", "current:checker"),
                        "synthetic-review",
                    ).__dict__
                    for key in payload["expected_check_keys"]
                ],
                "bindings": [b.__dict__ for b in task.bindings],
                "facts": [],
                "oracles": [o.__dict__ for o in task.oracles],
            }

    updated = current_grounding(
        replace(task, checks=(), bindings=(), oracles=()), (package,), GroundingReplay(), ledger()
    )
    assert updated.oracles == task.oracles
    assert validate_task_plan(good_plan(package, updated), updated, policy).mode == "use"


@pytest.mark.parametrize("finished_at", [9.0, 11.0])
def test_model_deadline_restored_and_late_requests_accounted(finished_at):
    from dataclasses import dataclass
    from arex_skill_graph.adaptive_budget import BudgetedTransport

    @dataclass(frozen=True)
    class Config:
        timeout_seconds: float = 90
        retries: int = 0
        max_output_tokens: int = 100

    now = [0.0]
    budget = BudgetLedger(BudgetCaps(seconds=10), clock=lambda: now[0])
    now[0] = 5.0

    class Transport:
        config = Config()
        calls = []

        def complete(self, **request):
            assert self.config.timeout_seconds == 5.0
            now[0] = finished_at
            self.calls.append({"usage": {"total_tokens": 7}})
            return {}

    transport = Transport()
    original = transport.config
    metered = BudgetedTransport(transport, budget)
    if finished_at > 10:
        with pytest.raises(BudgetExceeded, match="wall-clock"):
            metered.complete(system="test", user="test", response_schema={})
    else:
        assert metered.complete(system="test", user="test", response_schema={}) == {}
    assert transport.config is original
    assert budget.model_calls == 1 and budget.model_tokens == 7
