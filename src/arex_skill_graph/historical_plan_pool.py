"""Freeze authoritative original, rewritten and composed Plan candidates for supervision."""

from __future__ import annotations

from .action_contracts import digest
from .crossbind import bind_and_compose
from .plan_validation import validate_task_plan
from .workflow_rewriter import bind_selection, rewrite_workflow


def freeze_plan_candidates(task, resource_policy, workflow_ids, budget, *, pattern_id=None):
    """Use only public context and existing contracts; never label unrun plans failures."""
    task.verify(verify_head=resource_policy.verify_head)
    workflow_ids = tuple(workflow_ids)
    if (
        len(set(workflow_ids)) != len(workflow_ids)
        or len(workflow_ids) > budget.caps.parent_workflows
    ):
        raise ValueError("frozen Plan pool exceeds unique parent Workflow cap")
    packages = resource_policy.load()
    by_id = {w.id: w for p in packages for w in p.workflows}
    if any(wid not in by_id for wid in workflow_ids):
        raise ValueError("frozen Plan pool names an unauthoritative Workflow")
    workflows = tuple(by_id[wid] for wid in workflow_ids)
    patterns = {p.pattern.id: p.pattern for p in packages if p.pattern}
    if pattern_id is not None and pattern_id not in patterns:
        raise ValueError("frozen Plan pool names an unauthoritative Pattern")
    pattern = patterns.get(pattern_id)
    if pattern and not set(workflow_ids).issubset(pattern.supporting_workflow_ids):
        raise ValueError("Pattern lacks independent support for the selected parents")
    candidates = {}
    rejected = []

    def add(plan, derivation):
        if plan.id in candidates:
            row = candidates[plan.id]
            # IDs describe execution structure; audit changes may differ.
            first = {k: v for k, v in row["plan"].items() if k != "changes"}
            current = {k: v for k, v in plan.to_dict().items() if k != "changes"}
            if first != current:
                raise ValueError("ambiguous frozen Plan identity")
            if derivation not in row["derivations"]:
                row["derivations"].append(derivation)
            return
        report = validate_task_plan(plan, task, resource_policy)
        candidates[plan.id] = {
            "plan": plan.to_dict(),
            "validation": report.to_dict(),
            "derivations": [derivation],
            "failure_label_created": False,
        }

    for workflow in workflows:
        add(bind_selection(task, None, workflow.actions, (workflow,)), "original")
        rewritten = rewrite_workflow(pattern, task, workflow.actions, budget, workflows=(workflow,))
        for plan in rewritten.candidate_dags:
            add(plan, "single_workflow_rewrite")
    if len(workflows) == 2:
        pool = tuple({a.id: a for w in workflows for a in w.actions}.values())
        result = bind_and_compose(
            task, pattern, workflows, pool, budget, resource_policy=resource_policy
        )
        for plan in result.plans:
            add(plan, "crossbind_generation")
        rejected = [r.to_dict() for r in result.rejected]
    payload = {
        "schema": "historical-frozen-plan-pool-v1",
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "context_revision": task.revision,
        "public_task_sha256": digest(task.to_dict()),
        "catalog_cutoff": resource_policy.temporal.cutoff,
        "source_package_hashes": {
            p.reference["skill_id"]: p.reference["package_sha256"] for p in packages
        },
        "parent_workflow_ids": list(workflow_ids),
        "pattern_id": pattern_id,
        "candidates": [candidates[k] for k in sorted(candidates)],
        "rejected_compositions": rejected,
        "unrun_candidates_are_failure_labels": False,
        "behavior_verified": False,
    }
    payload["candidate_pool_sha256"] = digest(payload)
    return payload
