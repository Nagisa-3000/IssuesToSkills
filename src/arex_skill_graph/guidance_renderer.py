"""Progressive resource loading for approved temporary plans."""

from __future__ import annotations

import json
from pathlib import Path

from .action_contracts import CheckStatus
from .execution_frontier import execution_frontier
from .plan_validation import topological, validate_task_plan
from .skill_packages import _resolve


class GuidanceRenderer:
    def __init__(self, policy, budget):
        self.policy, self.budget = policy, budget
        self.reads = []

    def read_resource(self, package_id, relative, allowed_roots):
        if package_id not in allowed_roots:
            raise ValueError("resource is not part of the approved current plan")
        self.budget.approve_root(package_id)
        packages = {p.reference["skill_id"]: p for p in self.policy.load()}
        if package_id not in packages:
            raise ValueError("unknown resource root")
        package = packages[package_id]
        if relative not in {
            "SKILL.md",
            "references/workflow.md",
            "references/provenance.json",
        } and not relative.startswith("references/"):
            raise ValueError("only approved guidance resources may be read")
        path = _resolve(Path(package.root), relative)
        manifest = json.loads((Path(package.root) / "manifest.json").read_text())
        if relative not in manifest["files"]:
            raise ValueError("unmanifested resource")
        content = path.read_text()
        self.budget.history(content, "approved resource " + relative)
        self.reads.append(
            {
                "package_id": package_id,
                "resource": relative,
                "package_hash": package.reference["package_sha256"],
            }
        )
        return content

    def render(self, plan, task):
        report = validate_task_plan(plan, task, self.policy)
        if report.status == CheckStatus.FAIL:
            raise ValueError("rejected plan cannot provide guidance")
        for pid in sorted(plan.package_ids):
            self.budget.approve_root(pid)
        if report.mode == "probe_only":
            obligations = [c for c in report.checks if c.status == CheckStatus.UNKNOWN]
            rendered = (
                "Current plan is probe_only. Establish the following facts before any modifying action:\n"
                + "\n".join(f"- {c.subject}: {c.rationale}" for c in obligations)
                + "\nRefresh TaskContext and revalidate. This text does not authorize the proposed edits."
            )
            self.budget.history(rendered, "probe obligations from historical plan")
            return rendered
        order = topological([i.id for i in plan.instances], plan.dependencies)
        by_id = {i.id: i for i in plan.instances}
        rows = []
        for iid in order:
            instance = by_id[iid]
            a = instance.action
            rows.append(
                {
                    "instance": iid,
                    "skill": a.package_id,
                    "package_hash": a.package_hash,
                    "action": a.id,
                    "current_binding": [b.__dict__ for b in instance.bindings],
                    "current_evidence": list(
                        dict.fromkeys(e for b in instance.bindings for e in b.evidence_refs)
                    ),
                    "operation": a.operation,
                    "role": instance.role,
                    "preconditions": [p.__dict__ for p in a.preconditions],
                    "preserves": [p.__dict__ for p in a.preserves],
                    "oracles": [o.__dict__ for o in task.oracles if o.action_id == a.id],
                    "resource": a.resource,
                    "adaptation": instance.adaptation,
                }
            )
        # Full SKILL/Action cards remain available through read_resource; no automatic historical replay.
        rendered = (
            "Current task plan (expected effects, not verified execution):\n"
            + json.dumps(
                {
                    "plan_id": plan.id,
                    "actions": rows,
                    "execution_frontier": execution_frontier(plan, task),
                    "changes": plan.changes,
                    "stop_conditions": plan.stop_conditions,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\nBefore each action check actual input/output evidence. Historical Workflow is an example; "
            "request only the approved resource needed for this action. Stop and replan on a failed oracle."
        )
        self.budget.history(rendered, "rendered Action guidance and source references")
        return rendered
