# Workflow Skill: repair shared-capacity pressure policy

Status: `provisional generalized Workflow`, composed from two direct repositories and explicit adjacent-case boundaries.

## Purpose

Repair a pressure, compaction, admission, or retention policy when upstream work and a mandatory downstream reservation share one finite capacity.

## Trigger cues

- Provider/request rejection happens before proactive pressure or compaction fires.
- Threshold is computed from nominal window/capacity while an output cap or other reservation consumes the same window.
- Model/provider switching changes capacity but derived policy remains unchanged.
- Headroom exists but is not applied consistently to pressure or auxiliary output.

## Inputs

- capacity envelope and its source;
- all mandatory reservations and headroom;
- policy parameters;
- model/provider/runtime reconfiguration paths;
- existing boundary and behavioral tests.

## Conditional DAG

```text
S0 Identify shared-capacity consumers
  -> S1 Normalize reservation and headroom boundaries
  -> S2 Compute residual policy budgets
  -> S3 Validate degenerate states
  -> S4 Bind policy inputs to the active runtime envelope
  -> S5 Recompute on model/provider/context reconfiguration
  -> S6 Validate numeric and behavioral oracles
  -> S7 Inspect failure/recovery behavior
```

### Decisions

- If capacity pools are independent: stop; use a different policy family.
- If reservation is advisory rather than enforced: do not apply AT1 as a hard invariant.
- If residual capacity is non-positive: reject or use the host's explicitly documented compatibility fallback; never silently continue with negative arithmetic.
- If auxiliary summary output shares the defined headroom: optionally invoke AT4; otherwise keep the caps independent.
- If the defect is timing after tool execution rather than capacity arithmetic: branch to AT5, not AT1.
- If measured tokens omit context-visible artifacts: branch to AT6.

## Validation ladder

1. Numeric unit boundaries.
2. Policy-loader/configuration composition.
3. Runtime/model-switch regression.
4. Provider/request or deterministic replay oracle.
5. Failure and recovery behavior.

## Recovery

- Preserve the prior safe policy when new configuration is incomplete.
- Emit a target-specific actionable error for impossible residual budgets.
- Preserve original context when summary generation fails; recovery is separate from threshold derivation.

## Stop conditions

- Do not claim success from formula tests alone if the provider envelope is not exercised.
- Do not promote a Workflow or Pattern from one repository.
- Do not merge adjacent timing/accounting mechanisms into this Workflow without causal evidence.

## Package projection

This Workflow is the top-level `SKILL.md` candidate. AT1–AT3 live in `references/atomic/`; AT4–AT6 remain optional references. Evidence and case realizations live in `references/evidence/` or the Graph-of-Skills store.
