---
name: repair-shared-capacity-pressure
description: Repair a pressure, compaction, admission, or retention policy when upstream work and a mandatory downstream reservation share one finite capacity. Use when a provider rejects requests before proactive pressure fires, a threshold is based on nominal capacity, or model/provider switching leaves derived budgets stale.
---

# Repair shared-capacity pressure policy

## Purpose

Keep upstream pressure and retention decisions within the capacity that remains after all mandatory downstream reservations.

This skill is a provisional workflow extracted from real Hermes Agent and DeepSeek Harness changes. It is not a repository-specific patch recipe.

## Use when

- A threshold is computed from a nominal context/window size.
- A downstream output cap, reservation, or safety headroom is charged against the same capacity.
- Provider rejection occurs before proactive compaction or pressure handling.
- Model/provider/context switching changes the capacity envelope.

## Do not use when

- Input and output use independent capacity pools.
- The reservation is merely advisory and does not affect admission.
- The defect is only request-loop timing after a terminal tool result; use the request-boundary timing skill instead.
- The defect is only incomplete token accounting for custom context entries; use complete-context accounting instead.

## Preflight

1. Identify the nominal capacity `W` and every capacity consumer.
2. Decide which consumers are mandatory under the provider/runtime contract.
3. Locate the policy-resolution seam where capacity, reservation, and model identity are available.
4. Record existing unit, integration, replay, and provider/request oracles.

## Workflow

1. Normalize optional reservations and headroom into explicit typed values.
2. Compute residual message/pressure capacity before deriving thresholds.
3. Reject or explicitly handle non-positive residual budgets.
4. Bind the resolved policy to the active runtime envelope.
5. Recompute derived budgets after model/provider/context reconfiguration.
6. Validate arithmetic boundaries, configuration composition, runtime switching, and an observable request/replay behavior.
7. Preserve the prior safe context or policy on recoverable summary failure; do not silently discard evidence.

## Decision rules

- If capacity pools are independent, stop and choose another policy family.
- If a reservation is absent, preserve the documented full-capacity compatibility behavior.
- If residual capacity is non-positive, use an explicit error or documented compatibility fallback; never let negative arithmetic flow silently.
- Derive an auxiliary summary cap from headroom only when the contract says that summary output shares that headroom. Explicit caps take precedence.
- Do not equate summary `maxTokens` with the routed request reservation without an explicit provider contract.

## Invariants

- Every derived pressure/admission limit is admissible under residual capacity.
- A changed mandatory reservation deterministically changes the derived policy.
- Active model, reservation, and capacity are reflected after runtime reconfiguration.
- Invalid boundaries produce observable errors or documented fallbacks.

## Validation

Run positive, boundary, negative/exclusion, and regression cases. At minimum verify:

- nominal threshold versus residual threshold;
- absent, zero, negative, non-integer, and over-capacity reservations;
- model/provider switching with omitted and explicit replacement values;
- provider/request or deterministic replay behavior;
- recovery when summary generation fails.

## Failure recovery

If summary generation fails and the host contract permits recovery, preserve original context and emit an observable warning. This is a separate recovery behavior, not proof that residual arithmetic is correct.

## Stopping conditions

Stop and classify the case as adjacent when the evidence only shows request timing, complete-context measurement, or summarizer input fitting without a shared-capacity reservation invariant.

## Resources

- Read `references/atomic/derive-policy-from-residual-capacity.md` for the main reusable primitive.
- Read `references/atomic/normalize-capacity-reservation-boundaries.md` before arithmetic changes.
- Read `references/atomic/replay-capacity-policy-across-reconfiguration.md` for model/provider switching.
- Read `references/pattern.md` only when choosing among variants or explaining trade-offs.
- Read `references/evidence/` before claiming cross-repository generalization.
