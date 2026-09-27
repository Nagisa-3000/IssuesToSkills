# Generalized Atomic Skills: residual-budget family

Status: `reviewed` for the two direct mechanisms below after Hermes + DeepSeek comparison; `provisional` for narrower extensions. These are graph knowledge nodes. They can be projected into `references/atomic/*.md`, but not every node should become a top-level discoverable package.

## AT1 — derive-policy-from-residual-capacity

### Problem
A policy threshold or admission gate is derived from nominal capacity even though a mandatory downstream consumer reserves part of that same capacity.

### Solution paradigm
At the policy-resolution seam, identify the shared capacity and all mandatory reservations; compute residual capacity first; derive threshold, retention, and safety guards from the residual; reject or explicitly handle degenerate residual states.

### Abstract contract

```text
Inputs:  W, R[0..n], policy parameters, guard parameters
Output:  derived policy P
Invariant: every policy limit is admissible under W - sum(R)
```

For the two direct realizations:

```text
M = W - output_reservation
P = M - headroom                 # when headroom exists
T = min(nominal_policy(W), P)
```

The formula is not a mandatory implementation recipe; the invariant is. A system may use another policy function if the resulting policy never authorizes work beyond the residual admissible capacity.

### Preconditions

- Capacity consumers share one enforceable admission window.
- Reservations are semantically mandatory or provider-enforced.
- The policy can observe the effective capacity envelope.

### Exclusions

- Separate or independently enforced capacity pools.
- Advisory hints that do not affect admission.
- A threshold unrelated to the shared capacity.

### Invariants and oracles

- Derived pressure/admission never exceeds the residual budget.
- Changing a mandatory reservation changes the derived policy deterministically.
- Nominal-only and residual cases differ at the expected boundary.
- Invalid residual budget has an explicit error/fallback, never an accidental negative threshold.

### Realizations

- Hermes: `623b21bf24ea3f2f2c2d90de3ae872b8a0a000c4`, `agent/context_compressor.py`, tests in `tests/agent/test_context_compressor.py`.
- DeepSeek: PR #4530 merge `bc45bd821a63619c39a4cf0686d94743093cd990`, especially `0fadb08...` and `555b664...`, with unit and replay oracles.

### Delivery

Default: `references/atomic/derive-policy-from-residual-capacity.md`; normally invoked by a Workflow Skill rather than exposed as a standalone top-level package.

## AT2 — normalize-capacity-reservation-boundaries

### Problem
Optional, malformed, or provider-derived capacity values reach arithmetic without a stable semantic representation.

### Solution paradigm
Normalize values at the boundary into a typed positive reservation or explicit absence; validate sign, integer-ness, and compatibility before policy derivation.

### Invariants
No malformed value can cause arithmetic failure or silently authorize an unsafe policy. `None`/absence semantics are explicit and stable.

### Oracle
Partition tests for absent, zero, negative, non-integer, positive, and over-capacity values.

### Realizations
Hermes coercion tests; DeepSeek resolver and boundary tests.

## AT3 — replay-capacity-policy-across-reconfiguration

### Problem
A capacity-aware policy is correct at construction but stale after model/provider/context switching.

### Solution paradigm
Make the active policy inputs part of runtime state; define preserve-vs-replace semantics; recompute all derived values after reconfiguration; route every execution path through the resolved policy seam.

### Invariants
Active model, active reservation, and active capacity are reflected in all thresholds and downstream budgets. Omitted replacement parameters preserve state; explicit replacements update it.

### Realizations
Hermes `update_model()` behavior; DeepSeek routed policy and explicit reservation seam; Pi per-model compaction settings propagated across manual/automatic/overflow/model-switch paths.

## AT4 — derive-auxiliary-output-cap-from-headroom *(provisional)*

Only when the same policy explicitly defines headroom as the budget for an auxiliary summary operation: default the auxiliary cap from resolved headroom, preserve explicit overrides, and reject zero-cap inheritance. This is direct in DeepSeek, not shown in Hermes/Pi/Aider.

## AT5 — place-pressure-check-at-next-request-boundary *(provisional, separate family)*

Before issuing a real next provider request, check pressure; do not compact after a terminal tool result. Direct Pi realization. This is a timing/scheduling Atomic, not residual-capacity arithmetic.

## AT6 — account-for-all-context-visible-artifacts *(provisional, separate family)*

Use the canonical context-visible representation for budget measurement and cut-point selection. Direct Pi realization; neighboring support in Aider. Do not infer output-reservation semantics from it.
