# Atomic: derive policy from residual capacity

## Problem

A pressure/admission threshold uses nominal capacity even though a mandatory downstream consumer reserves part of that same capacity.

## Solution paradigm

At the policy seam, identify all mandatory consumers, compute residual capacity first, and derive threshold, retention, and safety guards from that residual. The reusable invariant is more important than a repository-specific formula:

```text
policy_limit <= residual_admissible_capacity
```

A common realization is:

```text
M = W - output_reservation
P = M - headroom
T = min(nominal_policy(W), P)
```

## Inputs and outputs

Inputs: nominal capacity, mandatory reservations, headroom, policy parameters, target identity.

Outputs: immutable derived policy or an actionable configuration error.

## Preconditions

- Capacity consumers share one enforceable admission window.
- Reservations affect provider/runtime admission.
- The policy can observe the effective capacity envelope.

## Exclusions

Do not apply to independent capacity pools or advisory hints.

## Procedure

1. Normalize reservations.
2. Compute residual message capacity.
3. Compute residual pressure capacity if headroom exists.
4. Apply threshold/retention policy to the residual.
5. Validate all derived values against the residual.
6. Return an explicit error for impossible configurations.

## Validation oracle

Test a nominal threshold that is below `W` but above `W - reservation`; it must trigger based on the residual policy before provider rejection. Test absent, invalid, near-capacity, and over-capacity reservations.

## Realizations

- Hermes Agent: `623b21bf24ea3f2f2c2d90de3ae872b8a0a000c4`.
- DeepSeek Harness: PR `#4530`, especially `0fadb08...` and `555b664...`.
