# Candidate Atomics: Hermes compaction reservation

These are candidates extracted from one case. They remain `candidate` until compared with independent realizations.

## A1 — derive-policy-from-residual-capacity

**Small problem.** A policy threshold is computed from nominal shared capacity even though a downstream stage reserves part of that capacity.

**Solution paradigm.** Identify every capacity consumer, compute the residual budget at the policy seam, and apply the policy and its safety guards to the residual budget. Do not merely lower the final threshold after computing from the nominal value.

**Inputs:** nominal capacity `W`, downstream reservation `O`, policy parameters, safety guard.
**Output:** threshold and any derived retain/pressure budgets.
**Preconditions:** both consumers are charged against the same capacity; reservation semantics are known.
**Exclusions:** independent capacities; a reservation that is not enforced by the provider/runtime.
**Invariant:** policy threshold must not authorize more upstream work than the residual capacity can support.
**Oracle:** boundary tests where the nominal threshold is below `W` but above `W-O`; threshold changes exactly when `O` changes; no non-positive result.
**Failure modes:** silently clamping invalid reservation; applying the guard to `W` instead of `W-O`; mixing units.

## A2 — normalize-optional-capacity-reservation

**Small problem.** Optional or malformed reservation values reach arithmetic and cause crashes or unsafe thresholds.

**Solution paradigm.** Normalize at the boundary into either a positive integer reservation or an explicit “no reservation” state, then keep downstream arithmetic typed and deterministic.

**Inputs:** `None`, numeric, string-like, mocked, zero, and negative values.
**Output:** `positive integer | no reservation`.
**Invariant:** invalid input cannot make the policy arithmetic throw or produce a non-positive threshold.
**Exclusions:** semantic validation of provider-specific maximums beyond the local policy contract.
**Oracle:** partitioned input tests and no-crash assertions.

## A3 — replay-policy-parameter-across-reconfiguration

**Small problem.** A capacity policy is correct at construction but becomes stale after model/provider/context switching.

**Solution paradigm.** Make the policy parameter part of the runtime state, define explicit “preserve” versus “replace” semantics, and recompute all derived budgets after reconfiguration.

**Inputs:** current policy state, new model/context, optional replacement reservation.
**Output:** recalibrated threshold and derived budgets.
**Invariant:** the active model and active reservation are reflected in every derived budget.
**Exclusions:** configuration precedence across multiple independent user scopes unless specified by the host system.
**Oracle:** switch tests with omitted and explicit replacement values.

## A4 — validate-shared-capacity-boundaries

**Small problem.** Degenerate residual budgets are allowed to flow into normal policy logic.

**Solution paradigm.** Partition boundary states and choose an explicit policy: reject impossible configurations, or use a documented safe fallback only where the runtime contract requires compatibility.

This candidate is a validation companion to A1, not a second threshold algorithm.

## Candidate-to-case mapping

- `CA1 -> A1`
- `CA2 -> A2`
- `CA3 -> A1`
- `CA4 -> A3`
- `CA5 -> A4`
- `CA6 -> A1, A2, A3, A4` (validation only)

No candidate is promoted to a generalized Pattern from this case alone.
