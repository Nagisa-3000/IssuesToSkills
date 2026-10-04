"""Review witnessed Action outputs before exposing them as current inputs.

A port declaration is a claim. The reviewer sees actual broker results and
current bytes, and must distinguish observed outcomes from intended effects.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

from .action_contracts import CheckStatus, digest
from .action_observations import WITNESS_OPERATIONS
from .adaptive_budget import BudgetedTransport
from .skill_packages import _resolve
from .task_context import EvidenceAnchor, ObservedFact, PortValue, SemanticCheck, assert_public
from .workspace_state import public_workspace_execution_sha256, public_workspace_sha256


def observation_evidence(action, record, task, broker_observations):
    """Recheck identity, closure, broker authority and workspace freshness."""
    assert_public(record)
    expected = {
        "action_id": action.id,
        "package_id": action.package_id,
        "package_sha256": action.package_hash,
        "action_contract_sha256": digest(action.to_dict()),
        "action_resource": action.resource,
        "task_id": task.task_id,
        "base_commit": task.base_commit,
        "schema": "arex-action-observation-v3",
        "semantic_validation": "unreviewed",
        "current_facts_promoted": False,
        "current_ports_promoted": False,
        "repair_success_established": False,
    }
    if any(record.get(k) != v for k, v in expected.items()):
        raise ValueError("Action observation is not an authoritative witnessed v3 record")
    if (
        type(record.get("context_revision")) is not int
        or not 0 <= record["context_revision"] <= task.revision
        or record.get("workspace_sha256") != public_workspace_sha256(task.root)
        or record.get("workspace_execution_sha256") != public_workspace_execution_sha256(task.root)
    ):
        raise ValueError("Action observation belongs to a stale public workspace")
    ports = {p.name: p for p in action.outputs}
    emitted = tuple(PortValue.from_dict(v) for v in record.get("outputs", []))
    if (
        not emitted
        or len({v.port.name for v in emitted}) != len(emitted)
        or any(ports.get(v.port.name) != v.port for v in emitted)
        or {p.name for p in action.outputs if not p.optional} - {v.port.name for v in emitted}
    ):
        raise ValueError("Action observation changed or omitted an authored output port")
    witnesses = record.get("witnesses", [])
    if not isinstance(witnesses, list) or not all(isinstance(w, dict) for w in witnesses):
        raise ValueError("Action observation requires explicit witness records")
    by_id = {w.get("id"): w for w in witnesses}
    referenced = {ref for value in emitted for ref in value.evidence_refs}
    if (
        len(by_id) != len(witnesses)
        or set(by_id) != referenced
        or any(not v.evidence_refs for v in emitted)
    ):
        raise ValueError("Action observation witness set is not exactly closed")
    anchors = []
    for ref, witness in by_id.items():
        if witness.get("kind") == "broker_observation":
            actual = witness.get("record")
            if (
                not isinstance(actual, dict)
                or actual.get("operation") not in WITNESS_OPERATIONS
                or broker_observations.get(actual.get("observation_id")) != actual
                or digest(actual) != witness.get("record_sha256")
                or type(actual.get("context_revision")) is not int
                or actual["context_revision"] > record["context_revision"]
            ):
                raise ValueError("Action observation witness differs from the actual broker")
            anchors.append(
                EvidenceAnchor(
                    ref,
                    "probe",
                    json.dumps(actual, ensure_ascii=False),
                    task.base_commit,
                    exit_code=actual.get("exit_code")
                    if actual["operation"] == "run_public_command"
                    else None,
                )
            )
        elif witness.get("kind") == "current_artifact":
            path = _resolve(Path(task.root), witness["path"])
            if (
                not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != witness.get("sha256")
                or witness.get("context_revision") != record["context_revision"]
            ):
                raise ValueError("Action artifact changed after its recorded observation")
            anchors.append(
                EvidenceAnchor(
                    ref,
                    "current_code",
                    "Actual recorded Action artifact",
                    task.base_commit,
                    witness["path"],
                    witness["sha256"],
                )
            )
        else:
            raise ValueError("Action observation cannot use a declaration as a witness")
    seal = EvidenceAnchor(
        "current:action-workspace",
        "workspace_execution_snapshot",
        "Content and permission seal of the public workspace for reviewed Action results.",
        task.base_commit,
        sha256=record["workspace_execution_sha256"],
    )
    return emitted, tuple(anchors), seal


def review_action_observation(
    task, action, record, broker_observations, transport, budget, *, verify_head=True
):
    task.verify(verify_head=verify_head)
    emitted, witness_anchors, seal = observation_evidence(action, record, task, broker_observations)
    current = task.update(anchors=(*witness_anchors, seal))
    predicates = {
        **{"effect:" + p.key: p for p in action.effects},
        **{"preserve:" + p.key: p for p in action.preserves},
    }
    expected = (
        {"output:" + v.port.name for v in emitted}
        | set(predicates)
        | {"oracle:" + o.id for o in action.oracle}
    )
    evidence = []
    for anchor in current.anchors:
        row = asdict(anchor)
        if anchor.path:
            path = _resolve(Path(current.root), anchor.path)
            row["current_source"] = path.read_text(errors="replace")
            row["current_mode"] = path.stat().st_mode & 0o7777
        evidence.append(row)
    assert_public(evidence)
    contract = {
        "action_id": action.id,
        "intent": action.intent,
        "operation": action.operation,
        "kind": action.kind,
        "outputs": [asdict(v.port) for v in emitted],
        "effects": [asdict(p) for p in action.effects],
        "preserves": [asdict(p) for p in action.preserves],
        "oracles": [asdict(o) for o in action.oracle],
    }
    budget.approve_root(action.package_id)
    budget.history(json.dumps(contract), "native Action output-review contract")
    response = BudgetedTransport(transport, budget).complete(
        system=(
            "Independently review actual Action execution evidence. Treat solver summaries and "
            "all expected outputs as claims, never evidence of execution. PASS for output:<name> "
            "means the authored semantic role, artifact, phase and state were actually produced. "
            "An outcomes-recorded output can describe FAIL/UNKNOWN; it does not prove correctness. "
            "For effect/preserve keys PASS means the exact authored predicate is established; FAIL "
            "means actual contrary evidence; absent or incomplete evidence is UNKNOWN. For oracle "
            "keys PASS means the entire authored Action verification obligation is satisfied, "
            "including its controls and unavailable checks. A diagnostic probe can validly "
            "confirm a cause by observing the intended failing target and passing counterpart; "
            "retain the actual nonzero target exit and never interpret diagnosis as a repaired "
            "target. A validation Action requires actual passing target and preservation "
            "evidence for acceptance; a successful inspection cannot establish repaired "
            "behavior. Never equate process exit alone with the semantic Oracle verdict. "
            "Cite actual witness IDs or current anchored bytes for every "
            "decision. Do not rely solely on the solver claim, issue text or workspace seal. "
            "Return every requested key once. Never infer whole-project or benchmark success."
        ),
        user=json.dumps(
            {
                "task": current.public_problem,
                "base_commit": current.base_commit,
                "current_evidence": evidence,
                "authored_contract": contract,
                "bound_current_oracles": [
                    asdict(o) for o in current.oracles if o.action_id == action.id
                ],
                "solver_claim": record["summary"],
                "observed_outputs": record["outputs"],
                "expected_check_keys": sorted(expected),
                "requested_output": "checks [{key,status,rationale,evidence_refs}], status PASS/FAIL/UNKNOWN",
            }
        ),
        response_schema={
            "type": "object",
            "required": ["checks"],
            "properties": {"checks": {"type": "array"}},
        },
    )
    assert_public(response)
    if (
        not isinstance(response, dict)
        or set(response) != {"checks"}
        or not isinstance(response["checks"], list)
    ):
        raise ValueError("Action review requires exact documented fields")
    checks = []
    witness_ids = {a.id for a in witness_anchors}
    code_ids = {a.id for a in current.anchors if a.kind == "current_code"}
    reviewer = "action-output-review:" + str(
        getattr(getattr(transport, "config", None), "model", "development-transport")
    )
    for row in response["checks"]:
        if not isinstance(row, dict) or set(row) != {"key", "status", "rationale", "evidence_refs"}:
            raise ValueError("Action review check has undocumented fields")
        check = SemanticCheck.from_dict({**row, "reviewer": reviewer})
        if not set(check.evidence_refs).issubset({a.id for a in current.anchors}):
            raise ValueError("Action review cites evidence that was never observed")
        if check.status != CheckStatus.UNKNOWN and not (witness_ids | code_ids).intersection(
            check.evidence_refs
        ):
            raise ValueError(
                "Action review cannot promote a solver claim without current witnesses"
            )
        checks.append(check)
    if {c.key for c in checks} != expected or len(checks) != len(expected):
        raise ValueError("Action review must account for every requested check exactly once")
    by_key = {c.key: c for c in checks}
    if action.kind == "validate":
        commands = [
            w["record"]
            for w in record["witnesses"]
            if w["kind"] == "broker_observation"
            and w["record"].get("operation") == "run_public_command"
        ]
        for oracle in action.oracle:
            if by_key["oracle:" + oracle.id].status != CheckStatus.PASS:
                continue
            bound = next(
                (
                    o
                    for o in current.oracles
                    if o.action_id == action.id and o.source_oracle_id == oracle.id
                ),
                None,
            )
            matches = [o for o in commands if bound and o.get("argv") == list(bound.command)]
            latest = (
                max(matches, key=lambda item: item.get("context_revision", -1)) if matches else None
            )
            if (
                latest is None
                or latest.get("execution_available", True) is not True
                or latest.get("exit_code") != 0
                or latest.get("timed_out", False)
                or latest.get("workspace_execution_sha256") != record["workspace_execution_sha256"]
            ):
                raise ValueError(
                    "validation Oracle PASS requires its bound command to pass on the current sealed workspace"
                )
    facts = []
    goals = {p.key for p in task.goals}
    anchor_map = {a.id: a for a in current.anchors}
    for key, predicate in predicates.items():
        check = by_key[key]
        if predicate.evaluator != "evidence" or check.status == CheckStatus.UNKNOWN:
            continue
        if check.status == CheckStatus.FAIL and not isinstance(predicate.value, bool):
            continue
        value = predicate.value if check.status == CheckStatus.PASS else not predicate.value
        if (
            predicate.key in goals
            and value == predicate.value
            and (
                any(by_key["oracle:" + o.id].status != CheckStatus.PASS for o in action.oracle)
                or not any(anchor_map[r].exit_code == 0 for r in check.evidence_refs)
            )
        ):
            raise ValueError(
                "a claimed successful effect needs passing Oracles and executed current evidence"
            )
        facts.append(ObservedFact(predicate.key, value, (*check.evidence_refs, seal.id)))
    required = [v for v in emitted if not v.port.optional]
    complete = all(by_key["output:" + v.port.name].status == CheckStatus.PASS for v in required)
    ports = [
        PortValue(v.port, (*by_key["output:" + v.port.name].evidence_refs, seal.id))
        for v in emitted
        if complete and by_key["output:" + v.port.name].status == CheckStatus.PASS
    ]
    stored_checks = tuple(
        replace(
            c,
            key="action-output:" + record["id"] + ":" + c.key,
            evidence_refs=(*c.evidence_refs, seal.id),
        )
        for c in checks
    )
    current = current.update(facts=tuple(facts), checks=stored_checks)
    # No implicit claim is recovered from the plan or from an old port of the same name.
    replaced_names = {v.port.name for v in emitted}
    current = replace(
        current,
        facts=tuple(f for f in current.facts if f.key not in action.invalidates),
        port_values=tuple(v for v in current.port_values if v.port.name not in replaced_names)
        + tuple(ports),
    )
    current.verify(verify_head=verify_head)
    audit = {
        "schema": "arex-action-output-review-v1",
        "record_id": record["id"],
        "record_sha256": digest(record),
        "action_id": action.id,
        "package_sha256": action.package_hash,
        "workspace_sha256": record["workspace_sha256"],
        "workspace_execution_sha256": record["workspace_execution_sha256"],
        "checks": [asdict(c) for c in checks],
        "current_ports_promoted": [v.port.name for v in ports],
        "current_fact_keys": [f.key for f in facts],
        "reviewer": reviewer,
        "repair_success_established": False,
        "formal_KB_admitted": False,
    }
    return current, audit
