"""Bounded, Pattern-constrained action selection; historical files stay immutable."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .action_contracts import ActionContract, CheckStatus, Dependency, WorkflowContract
from .adaptive_budget import BudgetLedger
from .pattern_contracts import PatternContract
from .plan_validation import ActionInstance, InputLink, TaskWorkflowPlan, plan_id
from .task_context import TaskContext


@dataclass(frozen=True)
class RewriteResult:
    candidate_dags: tuple[TaskWorkflowPlan, ...]
    unmet_effects: tuple[str, ...]
    probe_obligations: tuple[str, ...]
    rejection_reasons: tuple[str, ...]


def bind_selection(
    task: TaskContext,
    pattern: PatternContract | None,
    actions: tuple[ActionContract, ...],
    workflows: tuple[WorkflowContract, ...],
    *,
    changes=(),
) -> TaskWorkflowPlan:
    selected_ids = {a.id for a in actions}
    parents = tuple(w.id for w in workflows if any(a.id in selected_ids for a in w.actions))
    instances = tuple(
        ActionInstance(
            "instance:" + a.id,
            a,
            tuple(b for b in task.bindings if b.role == a.owner_role),
            a.semantic_role,
            "Bind current objects; execute only after actual preconditions/oracles hold.",
        )
        for a in actions
    )
    by_action = {i.action.id: i for i in instances}
    dependencies = {}
    links = []

    def edge(before, after, reason, evidence):
        if before == after:
            return
        dependencies[(before, after)] = Dependency(before, after, reason, tuple(evidence))

    for consumer in instances:
        a = consumer.action
        for port in a.inputs:
            current = next((v for v in task.port_values if v.port.compatible(port)), None)
            if current:
                links.append(
                    InputLink(
                        consumer.id,
                        port.name,
                        current_port=current.port.name,
                        evidence_refs=current.evidence_refs,
                    )
                )
                continue
            possible = [
                (i, p)
                for i in instances
                if i.id != consumer.id
                for p in i.action.outputs
                if p.compatible(port)
            ]
            possible.sort(
                key=lambda pair: (
                    task.semantic(f"connect:{pair[0].action.id}:{a.id}:{port.name}").status
                    != CheckStatus.PASS,
                    pair[0].action.id,
                    pair[1].name,
                )
            )
            if possible:
                producer, output = possible[0]
                proof = task.semantic(f"connect:{producer.action.id}:{a.id}:{port.name}")
                refs = proof.evidence_refs or (*producer.action.evidence_refs, *a.evidence_refs)
                links.append(
                    InputLink(consumer.id, port.name, producer.id, output.name, evidence_refs=refs)
                )
                edge(
                    producer.id,
                    consumer.id,
                    "Current input/output contract requires this producer.",
                    refs,
                )
        for pre in a.preconditions:
            if task.condition(pre) == CheckStatus.PASS:
                continue
            providers = [i for i in instances if i.id != consumer.id and pre in i.action.effects]
            if len(providers) == 1:
                provider = providers[0]
                edge(
                    provider.id,
                    consumer.id,
                    "Current prerequisite is established by this action.",
                    (*provider.action.evidence_refs, *a.evidence_refs),
                )
        if a.kind == "cleanup":
            for aid in a.cleanup_for:
                if aid in by_action:
                    edge(
                        by_action[aid].id,
                        consumer.id,
                        "Restore/clean up the selected operation.",
                        a.evidence_refs,
                    )
        if a.kind == "validate":
            for aid in a.validation_for:
                if aid in by_action:
                    edge(
                        by_action[aid].id,
                        consumer.id,
                        "Verify the actual modified state.",
                        a.evidence_refs,
                    )
    # Historical order is inherited only with a current semantic justification.
    for workflow in workflows:
        for old in workflow.dependencies:
            if old.before in by_action and old.after in by_action:
                proof = task.semantic(f"dependency:{old.before}:{old.after}")
                if proof.status == CheckStatus.PASS:
                    edge(
                        by_action[old.before].id,
                        by_action[old.after].id,
                        "Current semantic dependency: " + proof.rationale,
                        proof.evidence_refs,
                    )
    if pattern:
        for constraint in pattern.partial_order:
            for left in instances:
                for right in instances:
                    if left.role == constraint.before and right.role == constraint.after:
                        edge(left.id, right.id, constraint.reason, constraint.evidence_refs)
    required = tuple(dict.fromkeys((*task.goals, *(pattern.required_effects if pattern else ()))))
    invariants = tuple(
        dict.fromkeys(
            (
                *[p for a in actions for p in a.preserves],
                *[p for w in workflows if w.id in parents for p in w.invariants],
                *(pattern.invariants if pattern else ()),
            )
        )
    )
    return TaskWorkflowPlan(
        plan_id(
            task,
            selected_ids,
            parents,
            pattern=pattern,
            dependencies=tuple(dependencies.values()),
            links=tuple(links),
        ),
        task.task_id,
        task.base_commit,
        task.revision,
        instances,
        tuple(dependencies.values()),
        tuple(links),
        required,
        invariants,
        parents,
        pattern,
        tuple(changes),
    )


def prerequisite_closure(selected, action_pool, task, *, mechanism=None):
    """Insert only sourced suppliers, including genuine port conversion Bridges."""
    pool = {a.id: a for a in action_pool}
    expanded = {a.id: a for a in selected}
    changes, obligations = [], set()
    changed = True
    while changed:
        changed = False
        for action in tuple(expanded.values()):
            additions = [
                a
                for a in pool.values()
                if action.id in a.validation_for or action.id in a.cleanup_for
            ]
            for pre in action.preconditions:
                if task.condition(pre) == CheckStatus.PASS or any(
                    pre in a.effects for a in expanded.values() if a.id != action.id
                ):
                    continue
                candidates = [a for a in pool.values() if a.id != action.id and pre in a.effects]
                candidates = [
                    a
                    for a in candidates
                    if task.semantic("action:" + a.id).status != CheckStatus.FAIL
                ]
                if mechanism:
                    candidates = [a for a in candidates if a.mechanism == mechanism]
                if len(candidates) == 1:
                    additions.extend(candidates)
                else:
                    obligations.add("prerequisite:" + action.id + ":" + pre.key)
            for port in action.inputs:
                if port.optional or any(v.port.compatible(port) for v in task.port_values):
                    continue
                if any(
                    p.compatible(port)
                    for a in expanded.values()
                    if a.id != action.id
                    for p in a.outputs
                ):
                    continue
                candidates = [
                    a
                    for a in pool.values()
                    if a.id != action.id
                    and any(p.compatible(port) for p in a.outputs)
                    and task.semantic("action:" + a.id).status != CheckStatus.FAIL
                ]
                if mechanism:
                    candidates = [a for a in candidates if a.mechanism == mechanism]
                confirmed = [
                    a
                    for a in candidates
                    if task.semantic(f"connect:{a.id}:{action.id}:{port.name}").status
                    == CheckStatus.PASS
                ]
                if confirmed:
                    additions.append(min(confirmed, key=lambda a: (a.estimated_cost, a.id)))
                elif len(candidates) == 1:
                    additions.append(candidates[0])
                else:
                    obligations.add("port:" + action.id + ":" + port.name)
            for addition in additions:
                if addition.id not in expanded:
                    expanded[addition.id] = addition
                    changes.append(
                        {
                            "operation": "insert_bridge"
                            if addition.kind == "bridge"
                            else "insert_prerequisite_or_validation",
                            "action_id": addition.id,
                            "consumer": action.id,
                            "source_ids": addition.source_ids,
                            "evidence_refs": addition.evidence_refs,
                            "reason": "Native input/effect or verification closure requires this sourced Action.",
                        }
                    )
                    changed = True
    return tuple(expanded.values()), tuple(changes), tuple(sorted(obligations))


def rewrite_workflow(
    pattern: PatternContract | None,
    task_context: TaskContext,
    action_pool,
    budget: BudgetLedger,
    *,
    workflows=(),
) -> RewriteResult:
    budget.check_time()
    workflows = tuple(workflows)
    pool = {a.id: a for a in action_pool}
    reasons, unmet, probes = [], [], []
    candidates = []
    if pattern is None:
        for workflow in workflows[: budget.caps.workflow_candidates]:
            actions = []
            changes = []
            removed = set()
            for action in workflow.actions:
                inapplicable = (
                    task_context.semantic("action:" + action.id).status == CheckStatus.FAIL
                    or any(
                        task_context.condition(p) == CheckStatus.FAIL for p in action.preconditions
                    )
                    or any(task_context.condition(p) == CheckStatus.PASS for p in action.exclusions)
                )
                if action.id in workflow.optional_action_ids and inapplicable:
                    removed.add(action.id)
                    changes.append(
                        {
                            "operation": "drop_inapplicable_optional",
                            "action_id": action.id,
                            "reason": "The authored optional branch contradicts current evidence.",
                        }
                    )
                    continue
                # An observed effect can remove an action only when it has no outstanding downstream role.
                satisfied = bool(action.effects) and all(
                    task_context.condition(e) == CheckStatus.PASS for e in action.effects
                )
                used = any(
                    action.id in b.cleanup_for
                    or any(p.compatible(q) for p in action.outputs for q in b.inputs)
                    for b in workflow.actions
                    if b.id != action.id
                )
                if satisfied and not used and action.kind != "validate":
                    changes.append(
                        {
                            "operation": "drop_satisfied_action",
                            "action_id": action.id,
                            "reason": "All required effects already have current evidence.",
                        }
                    )
                else:
                    actions.append(action)
            actions = [
                a
                for a in actions
                if not (
                    a.kind == "validate"
                    and a.validation_for
                    and set(a.validation_for).issubset(removed)
                )
            ]
            if actions:
                candidates.append(
                    bind_selection(task_context, None, tuple(actions), (workflow,), changes=changes)
                )
        return RewriteResult(tuple(candidates), (), (), ())
    if task_context.semantic("pattern:" + pattern.id).status == CheckStatus.FAIL:
        return RewriteResult((), (), (), ("Current evidence rejects this Pattern.",))
    for condition in pattern.applicability:
        status = task_context.condition(condition)
        if status == CheckStatus.FAIL:
            reasons.append("Pattern prerequisite false: " + condition.key)
        elif status == CheckStatus.UNKNOWN:
            probes.append(condition.key)
    for exclusion in pattern.exclusions:
        if task_context.condition(exclusion) == CheckStatus.PASS:
            reasons.append("Pattern exclusion holds: " + exclusion.key)
    if reasons:
        return RewriteResult((), (), tuple(probes), tuple(reasons))
    beams = [((), ())]
    for role in pattern.roles:
        if role.effects and all(
            task_context.condition(e) == CheckStatus.PASS for e in role.effects
        ):
            beams = [
                (
                    selected,
                    (
                        *changes,
                        {
                            "operation": "drop_satisfied_action",
                            "role": role.id,
                            "reason": "Required role effects already observed.",
                        },
                    ),
                )
                for selected, changes in beams
            ]
            continue
        choices = [
            pool[x]
            for x in role.alternatives
            if x in pool and task_context.semantic("action:" + x).status != CheckStatus.FAIL
        ]
        choices.sort(
            key=lambda a: (
                task_context.semantic("action:" + a.id).status != CheckStatus.PASS,
                a.estimated_cost,
                a.id,
            )
        )
        if not choices and role.required:
            unmet.extend(p.key for p in role.effects)
            return RewriteResult(
                (),
                tuple(unmet),
                tuple(probes),
                ("Required role has no eligible realization: " + role.id,),
            )
        if not role.required:
            choices.append(None)
        next_beams = []
        for (selected, changes), action in product(beams, choices):
            if action is None:
                next_beams.append(
                    (
                        selected,
                        (
                            *changes,
                            {
                                "operation": "skip_optional",
                                "role": role.id,
                                "reason": "Optional branch omitted.",
                            },
                        ),
                    )
                )
            elif action not in selected:
                next_beams.append(
                    (
                        (*selected, action),
                        (
                            *changes,
                            {
                                "operation": "select_realization",
                                "role": role.id,
                                "action_id": action.id,
                                "reason": "Evidenced Pattern alternative.",
                            },
                        ),
                    )
                )
        beams = next_beams[: budget.caps.beam_width]
    for selected, changes in beams:
        closed, inserted, missing = prerequisite_closure(
            selected, pool.values(), task_context, mechanism=pattern.mechanism
        )
        expanded = {a.id: a for a in closed}
        changes = (*changes, *inserted)
        probes.extend(missing)
        if expanded:
            plans = bind_selection(
                task_context, pattern, tuple(expanded.values()), workflows, changes=changes
            )
            if len(plans.parent_workflow_ids) <= budget.caps.parent_workflows:
                candidates.append(plans)
            else:
                reasons.append("Selection exceeds parent Workflow cap.")
    return RewriteResult(
        tuple(candidates[: budget.caps.composed_plans]), tuple(unmet), tuple(probes), tuple(reasons)
    )
