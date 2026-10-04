"""Actual prerequisites for the next Action, separate from conditional DAG validity."""

from __future__ import annotations

from .action_contracts import CheckStatus


def action_execution_checks(action, task):
    rows = []

    def add(key, status, rationale, refs=()):
        rows.append(
            {"key": key, "status": str(status), "rationale": rationale, "evidence_refs": list(refs)}
        )

    for key in ("action:" + action.id, "owner:" + action.owner_role):
        check = task.semantic(key)
        add(key, check.status, check.rationale, check.evidence_refs)
    binding = next((b for b in task.bindings if b.role == action.owner_role), None)
    add(
        "binding",
        CheckStatus.PASS if binding else CheckStatus.UNKNOWN,
        "The current owner must be bound.",
        binding.evidence_refs if binding else (),
    )
    for pre in action.preconditions:
        add(
            "precondition:" + pre.key,
            task.condition(pre),
            "Only current observations establish execution prerequisites.",
        )
    for exclusion in action.exclusions:
        status = task.condition(exclusion)
        add(
            "exclusion:" + exclusion.key,
            {
                CheckStatus.PASS: CheckStatus.FAIL,
                CheckStatus.FAIL: CheckStatus.PASS,
                CheckStatus.UNKNOWN: CheckStatus.UNKNOWN,
            }[status],
            "An unknown exclusion cannot authorize modification.",
        )
    for port in action.inputs:
        values = [v for v in task.port_values if v.port.compatible(port)]
        if not values and port.optional:
            continue
        proofs = [
            task.semantic(f"current-connect:{v.port.name}:{action.id}:{port.name}") for v in values
        ]
        usable = [
            (v, c) for v, c in zip(values, proofs, strict=True) if c.status == CheckStatus.PASS
        ]
        add(
            "input:" + port.name,
            CheckStatus.PASS if usable else CheckStatus.UNKNOWN,
            "A planned predecessor output is not a current observed PortValue.",
            tuple(ref for v, c in usable for ref in (*v.evidence_refs, *c.evidence_refs)),
        )
    for oracle in action.oracle:
        actual = next(
            (
                o
                for o in task.oracles
                if o.action_id == action.id and o.source_oracle_id == oracle.id
            ),
            None,
        )
        add(
            "bound-oracle:" + oracle.id,
            CheckStatus.PASS if actual else CheckStatus.UNKNOWN,
            "Bind the Oracle to current public inputs.",
            actual.evidence_refs if actual else (),
        )
        proof = task.semantic(f"oracle:{action.id}:{oracle.id}")
        add("oracle:" + oracle.id, proof.status, proof.rationale, proof.evidence_refs)
    return {
        "action_id": action.id,
        "ready": all(c["status"] == "PASS" for c in rows),
        "checks": rows,
    }


def execution_frontier(plan, task):
    return [action_execution_checks(i.action, task) | {"instance_id": i.id} for i in plan.instances]


def ready_modifying_action(plan, task, action_id):
    action = next((i.action for i in plan.instances if i.action.id == action_id), None)
    if (
        action is None
        or action.kind not in {"edit", "bridge", "cleanup"}
        or not action_execution_checks(action, task)["ready"]
    ):
        return None
    return action


def declared_write_paths(action, task):
    anchors = {a.id: a for a in task.anchors}
    paths = set()
    for item in action.write_set:
        role = item.removeprefix("role:")
        binding = next((b for b in task.bindings if b.role == role), None)
        if binding:
            path = anchors[binding.anchor_id].path
            if path:
                paths.add(path)
        elif any(a.path == item for a in task.anchors):
            paths.add(item)
    return paths
