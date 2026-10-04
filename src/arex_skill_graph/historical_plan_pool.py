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


def verify_frozen_plan_pool(payload, task, resource_policy, budget):
    """Check a saved public pool without retrieving, rewriting, or composing again."""
    task.verify(verify_head=resource_policy.verify_head)
    if payload.get("schema") != "historical-frozen-plan-pool-v1":
        raise ValueError("unsupported frozen Plan pool schema")
    if payload.get("candidate_pool_sha256") != digest(
        {key: value for key, value in payload.items() if key != "candidate_pool_sha256"}
    ):
        raise ValueError("frozen Plan pool digest mismatch")
    expected = {
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "context_revision": task.revision,
        "public_task_sha256": digest(task.to_dict()),
        "catalog_cutoff": resource_policy.temporal.cutoff,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        raise ValueError("frozen Plan pool current public task or time boundary changed")
    packages = resource_policy.load()
    source_hashes = {
        package.reference["skill_id"]: package.reference["package_sha256"] for package in packages
    }
    if payload.get("source_package_hashes") != source_hashes:
        raise ValueError("frozen Plan pool source catalog changed")
    workflows = {workflow.id: workflow for package in packages for workflow in package.workflows}
    parents = payload.get("parent_workflow_ids", [])
    if (
        len(set(parents)) != len(parents)
        or len(parents) > budget.caps.parent_workflows
        or any(parent not in workflows for parent in parents)
    ):
        raise ValueError("frozen Plan pool has invalid or excessive parents")
    patterns = {package.pattern.id: package.pattern for package in packages if package.pattern}
    pattern_id = payload.get("pattern_id")
    if pattern_id is not None and (
        pattern_id not in patterns
        or not set(parents).issubset(patterns[pattern_id].supporting_workflow_ids)
    ):
        raise ValueError("frozen Plan pool Pattern has no authoritative parent support")
    if (
        payload.get("behavior_verified") is not False
        or payload.get("unrun_candidates_are_failure_labels") is not False
    ):
        raise ValueError("frozen candidate preparation cannot establish behavior or failure labels")
    plans = []
    from .plan_validation import TaskWorkflowPlan

    for candidate in payload.get("candidates", []):
        plan = TaskWorkflowPlan.from_dict(candidate["plan"])
        if (
            plan.task_id != task.task_id
            or plan.base_commit != task.base_commit
            or plan.context_revision != task.revision
            or not set(plan.parent_workflow_ids).issubset(parents)
            or len(plan.parent_workflow_ids) > budget.caps.parent_workflows
            or (plan.pattern is not None and plan.pattern.id != pattern_id)
            or candidate.get("failure_label_created") is not False
        ):
            raise ValueError("frozen candidate identity or authority differs from its pool")
        plans.append(plan)
    if len({plan.id for plan in plans}) != len(plans):
        raise ValueError("frozen Plan pool contains duplicate candidate identities")
    # Current validation remains the execution gate. Saved PASS/UNKNOWN reports
    # are provenance, not authorization; run_branch validates before solving.
    return tuple(plans)


def load_prepared_plan_study(directory, expected_identity):
    """Load and cross-check prepared artifacts; never regenerate a candidate."""
    import hashlib
    import json
    from pathlib import Path

    directory = Path(directory).resolve()
    names = (
        "study-identity.json",
        "plan-pools.json",
        "plans.json",
        "controlled-schedule.json",
        "candidate-coverage.json",
    )
    documents, hashes = {}, {}
    for name in names:
        contents = (directory / name).read_bytes()
        documents[name] = json.loads(contents)
        hashes[name] = hashlib.sha256(contents).hexdigest()
    source_identity = documents["study-identity.json"]
    for key in (
        "queries_sha256",
        "references_sha256",
        "training_cutoff",
        "main_cutoff",
        "seed",
        "encoder",
    ):
        if source_identity.get(key) != expected_identity.get(key):
            raise ValueError("prepared study identity changed: " + key)
    if (
        source_identity.get("candidate_kind") not in {"plan", "both"}
        or source_identity.get("candidate_generation_frozen") is not True
        or source_identity.get("development_population") is not True
    ):
        raise ValueError("prepared study does not contain frozen development Plan candidates")
    pools = documents["plan-pools.json"]
    coverage = documents["candidate-coverage.json"]
    if (
        len({row["query_id"] for row in coverage}) != len(coverage)
        or {row["query_id"] for row in coverage} != set(pools)
        or any(row.get("unrun_candidates_are_failure_labels") is not False for row in coverage)
    ):
        raise ValueError("prepared coverage does not retain every query exactly once")
    projections = {
        query_id: [candidate["plan"] for candidate in pool["candidates"]]
        for query_id, pool in pools.items()
    }
    if documents["plans.json"] != projections:
        raise ValueError("prepared Plan projections differ from frozen pools")
    if any(
        row.get("candidate_kind") not in {"baseline", "workflow", "plan"}
        for row in documents["controlled-schedule.json"]
    ):
        raise ValueError("prepared schedule contains an unknown candidate kind")
    schedule = [
        row
        for row in documents["controlled-schedule.json"]
        if row["candidate_kind"] in {"baseline", "plan"}
    ]
    identities, paths = set(), set()
    for row in schedule:
        relative = Path(row["relative_output"])
        identity = (row["query_id"], row["candidate_kind"], row["candidate_id"])
        if (
            row["query_id"] not in pools
            or identity in identities
            or str(relative) in paths
            or relative.is_absolute()
            or not relative.parts
            or any(part in {".", ".."} for part in relative.parts)
            or not 0 < row["sampling_probability"] <= 1
            or (row["candidate_kind"] == "baseline" and row["candidate_id"] is not None)
        ):
            raise ValueError("prepared schedule has an invalid, duplicate, or unsafe branch")
        identities.add(identity)
        paths.add(str(relative))
    expected_branches = {(query_id, "baseline", None) for query_id in pools} | {
        (query_id, "plan", candidate["plan"]["id"])
        for query_id, pool in pools.items()
        for candidate in pool["candidates"]
    }
    if identities != expected_branches:
        raise ValueError("prepared schedule omits or invents frozen Plan candidates")
    return {
        "plan_pools": pools,
        "coverage": coverage,
        "schedule": schedule,
        "lineage": {
            "schema": "prepared-plan-study-lineage-v1",
            "source_artifact_sha256": hashes,
            "source_study_identity": source_identity,
            "candidate_generation_reexecuted": False,
            "embedding_batches": 0,
        },
    }
