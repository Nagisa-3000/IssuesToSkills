"""Attribute candidate assignment, fallback and observed Actions without claiming execution."""

from __future__ import annotations

import re

from .action_contracts import digest
from .task_context import assert_public

ASSIGNED_POLICY = "assigned_candidate_policy"
ATTRIBUTION_SCHEMA = "controlled-guidance-attribution-v1"
DISPOSITIONS = {"no_explicit_fallback", "explicit_fallback", "unknown"}


def controlled_guidance_attribution(run):
    """Recompute public trajectory attribution; exposure is never proof of plan execution.

    Older receipts lack per-request state. Their successful explicit fallback can
    still be identified, while active-plan request counts remain unknown.
    """
    requests = run.get("requests", [])
    observations = run.get("public_observations", [])
    contexts = run.get("guidance_request_contexts")
    usage = run.get("guidance_usage", [])
    if not all(isinstance(row, dict) for row in [*requests, *observations, *usage]):
        raise ValueError("invalid public guidance trajectory")
    complete = contexts is not None
    if complete:
        if not isinstance(contexts, list) or len(contexts) != len(requests):
            raise ValueError("incomplete per-request guidance context")
        for index, row in enumerate(contexts):
            if (
                not isinstance(row, dict)
                or row.get("request_index") != index
                or type(row.get("pending_guidance_refresh")) is not bool
                or not isinstance(row.get("parent_workflow_ids"), list)
                or row.get("authorization_mode") not in {None, "use", "probe_only", "reject"}
                or (row.get("plan_id") is None) != (row.get("authorization_mode") is None)
            ):
                raise ValueError("invalid per-request guidance context")
    drops = [i for i, row in enumerate(requests) if row.get("operation") == "drop_guidance"]
    receipts = [
        row
        for row in observations
        if row.get("operation") == "drop_guidance"
        and "fallback_reason" in row
        and not row.get("denied")
        and not row.get("protocol_error")
    ]
    if complete:
        receipt_indices = [row.get("request_index") for row in receipts]
        confirmed = (
            len(set(receipt_indices)) == len(receipt_indices)
            and set(receipt_indices) == set(drops)
            and all(type(i) is int for i in receipt_indices)
        )
    else:
        confirmed = len(receipts) == len(drops)
    disposition = (
        "unknown" if not confirmed else "explicit_fallback" if drops else "no_explicit_fallback"
    )
    action_records = [
        row
        for row in observations
        if row.get("operation") == "record_action_observation" and row.get("record")
    ]
    unassigned_records = (
        sum(
            contexts[row["request_index"]]["plan_id"] is None
            for row in action_records
            if type(row.get("request_index")) is int and 0 <= row["request_index"] < len(contexts)
        )
        if complete
        and all(
            type(row.get("request_index")) is int and 0 <= row["request_index"] < len(contexts)
            for row in action_records
        )
        else None
    )
    source = {
        "requests": requests,
        "public_observations": observations,
        "guidance_usage": usage,
        "guidance_request_contexts": contexts,
        "action_observations": run.get("action_observations", []),
    }
    assert_public(source)
    return {
        "schema": ATTRIBUTION_SCHEMA,
        "utility_target": ASSIGNED_POLICY if usage else "baseline_policy",
        "guidance_disposition": disposition,
        "per_request_contexts_complete": complete,
        "request_count": len(requests),
        "active_plan_request_count": sum(row["plan_id"] is not None for row in contexts)
        if complete
        else None,
        "suspended_request_count": sum(row["pending_guidance_refresh"] for row in contexts)
        if complete
        else None,
        "unguided_request_count": sum(
            row["plan_id"] is None and not row["pending_guidance_refresh"] for row in contexts
        )
        if complete
        else None,
        "explicit_drop_request_indices": drops,
        "confirmed_drop_observation_ids": [row.get("observation_id") for row in receipts],
        "action_observation_count": len(run.get("action_observations", [])),
        "action_records_without_active_plan": unassigned_records,
        "plan_execution_established": False,
        "source_trace_sha256": digest(source),
    }


def attributed_execution_label(label):
    """An assignment outcome can train utility, never semantic applicability."""
    return (
        label.get("label_source") == "execution"
        and label.get("execution_scope") == ASSIGNED_POLICY
        and label.get("guidance_disposition") in DISPOSITIONS
        and isinstance(label.get("guidance_attribution_sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", label["guidance_attribution_sha256"]) is not None
    )
