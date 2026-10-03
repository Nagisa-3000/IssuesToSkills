"""Current binding and bounded cross-Workflow cut/splice composition."""

from __future__ import annotations

from dataclasses import dataclass

from .action_contracts import CheckStatus
from .adaptive_budget import BudgetLedger
from .plan_validation import (
    ResourcePolicy,
    TaskWorkflowPlan,
    PlanValidationReport,
    validate_task_plan,
)
from .workflow_rewriter import bind_selection, rewrite_workflow, prerequisite_closure


@dataclass(frozen=True)
class CutBoundary:
    retained_action_ids: tuple[str, ...]
    removed_action_ids: tuple[str, ...]
    boundary_effects: tuple[dict, ...]
    obligations: tuple[str, ...]


def cut_workflow(workflow, keep_ids, task) -> CutBoundary:
    """Cut a DAG by selected effects, preserving prerequisite and verification closure."""
    keep = set(keep_ids)
    actions = {a.id: a for a in workflow.actions}
    if not keep.issubset(actions):
        raise ValueError("cut references unknown Action")
    selected, _, obligations = prerequisite_closure(
        tuple(actions[x] for x in keep), actions.values(), task
    )
    keep = {a.id for a in selected}
    # Keep an inherited prerequisite only when its current semantic dependency is evidenced.
    changed = True
    while changed:
        changed = False
        for edge in workflow.dependencies:
            if (
                edge.after in keep
                and edge.before not in keep
                and task.semantic(f"dependency:{edge.before}:{edge.after}").status
                == CheckStatus.PASS
            ):
                keep.add(edge.before)
                changed = True
        selected, _, more = prerequisite_closure(
            tuple(actions[x] for x in keep), actions.values(), task
        )
        new = {a.id for a in selected}
        changed |= new != keep
        keep = new
        obligations = (*obligations, *more)
    return CutBoundary(
        tuple(sorted(keep)),
        tuple(sorted(set(actions) - keep)),
        tuple(
            {"key": e.key, "value": e.value, "action_id": aid}
            for aid in sorted(keep)
            for e in actions[aid].effects
        ),
        tuple(sorted(set(obligations))),
    )


@dataclass(frozen=True)
class CrossBindResult:
    plans: tuple[TaskWorkflowPlan, ...]
    reports: tuple[PlanValidationReport, ...]
    rejected: tuple[PlanValidationReport, ...]
    boundaries: tuple[CutBoundary, ...]
    unmet_effects: tuple[str, ...]
    probe_obligations: tuple[str, ...]


def bind_and_compose(
    task_context,
    pattern,
    workflows,
    action_pool,
    budget: BudgetLedger,
    *,
    resource_policy: ResourcePolicy,
) -> CrossBindResult:
    if len(workflows) > budget.caps.parent_workflows:
        raise ValueError("CrossBind parent count exceeds configured cap")
    budget.check_time()
    rewrite = rewrite_workflow(pattern, task_context, action_pool, budget, workflows=workflows)
    plans, reports, rejected, boundaries = [], [], [], []
    seen = set()
    # Include original currently-bound parents; composition cannot silently replace every fallback.
    originals = [
        bind_selection(
            task_context,
            None,
            w.actions,
            (w,),
            changes=(
                {
                    "operation": "retain_original",
                    "workflow_id": w.id,
                    "reason": "Keep original as a current-bound comparator.",
                },
            ),
        )
        for w in workflows
    ]
    composed = []
    if pattern is None and len(workflows) > 1:
        seeds = [a for a in action_pool if any(e in a.effects for e in task_context.goals)]
        if seeds:
            selected, inserted, _ = prerequisite_closure(seeds, action_pool, task_context)
            composed.append(
                bind_selection(task_context, None, selected, tuple(workflows), changes=inserted)
            )
    for plan in [*rewrite.candidate_dags, *composed, *originals]:
        if plan.id in seen:
            continue
        seen.add(plan.id)
        report = validate_task_plan(plan, task_context, resource_policy)
        if report.status == CheckStatus.FAIL:
            rejected.append(report)
            continue
        if len(plans) >= budget.caps.composed_plans:
            break
        plans.append(plan)
        reports.append(report)
        for workflow in workflows:
            keep = {
                i.action.id
                for i in plan.instances
                if i.action.id in {a.id for a in workflow.actions}
            }
            if keep:
                boundaries.append(cut_workflow(workflow, keep, task_context))
    return CrossBindResult(
        tuple(plans),
        tuple(reports),
        tuple(rejected),
        tuple(boundaries),
        rewrite.unmet_effects,
        rewrite.probe_obligations,
    )


def splice_workflows(left, right, left_keep, right_keep, task, pattern, budget, resource_policy):
    """Explicit cut/splice entrypoint with immutable parents and validation reports."""
    budget.check_time()
    if budget.caps.parent_workflows < 2:
        raise ValueError("splice requires two authorized parent workflows")
    pool = {a.id: a for w in (left, right) for a in w.actions}
    if not set(left_keep).issubset({a.id for a in left.actions}) or not set(right_keep).issubset(
        {a.id for a in right.actions}
    ):
        raise ValueError("splice cut references unknown parent Action")
    selected = tuple(pool[x] for x in dict.fromkeys((*left_keep, *right_keep)))
    # Close prerequisites jointly: one side may establish the other side's state.
    selected, inserted, obligations = prerequisite_closure(
        selected, pool.values(), task, mechanism=pattern.mechanism if pattern else None
    )
    selected_ids = {a.id for a in selected}
    cuts = tuple(
        CutBoundary(
            tuple(a.id for a in w.actions if a.id in selected_ids),
            tuple(a.id for a in w.actions if a.id not in selected_ids),
            tuple(
                {"key": e.key, "value": e.value, "action_id": a.id}
                for a in w.actions
                if a.id in selected_ids
                for e in a.effects
            ),
            obligations,
        )
        for w in (left, right)
    )
    plan = bind_selection(
        task,
        pattern,
        selected,
        (left, right),
        changes=(
            *inserted,
            *tuple(
                {
                    "operation": "truncate_splice",
                    "workflow_id": w.id,
                    "retained": c.retained_action_ids,
                    "removed": c.removed_action_ids,
                    "boundary_state": c.boundary_effects,
                    "reason": "Current prerequisites and verification closure define this cut.",
                }
                for w, c in zip((left, right), cuts)
            ),
        ),
    )
    report = validate_task_plan(plan, task, resource_policy)
    return CrossBindResult(
        (plan,) if report.status != CheckStatus.FAIL else (),
        (report,) if report.status != CheckStatus.FAIL else (),
        (report,) if report.status == CheckStatus.FAIL else (),
        cuts,
        (),
        tuple(dict.fromkeys((*obligations, *(x for c in cuts for x in c.obligations)))),
    )


def substitute_action(plan, old_action_id, replacement, task, workflows, resource_policy):
    """Replace an operation and re-derive all current dependencies and obligations."""
    if old_action_id not in {i.action.id for i in plan.instances}:
        raise ValueError("substitution target is absent")
    selected = tuple(
        replacement if i.action.id == old_action_id else i.action for i in plan.instances
    )
    selected, inserted, _ = prerequisite_closure(
        selected, [a for w in workflows for a in w.actions], task
    )
    updated = bind_selection(
        task,
        plan.pattern,
        selected,
        tuple(workflows),
        changes=(
            *plan.changes,
            *inserted,
            {
                "operation": "substitute",
                "removed": old_action_id,
                "inserted": replacement.id,
                "reason": "Alternative must satisfy current bindings/effects and verification.",
            },
        ),
    )
    return updated, validate_task_plan(updated, task, resource_policy)
