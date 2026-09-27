# Alignment decision: Pi versus residual-budget family

## Decision

`partial_alignment`, not `same_pattern`.

## Supporting overlap

Pi makes capacity-policy parameters explicit, model-specific, validated, and replayed across runtime reconfiguration. That is causally compatible with the generalized Atomic `replay-policy-parameter-across-reconfiguration`.

## Blocking difference

The verified Pi commits establish per-model reserve/keep settings and context accounting, but the reviewed evidence does not establish that the pressure threshold is computed as `nominal capacity - downstream output reservation` in the same semantic seam as Hermes and DeepSeek. The request-boundary timing fix and complete-context accounting solve different failure mechanisms.

## Promotion consequence

Pi can support a cross-case Atomic about policy propagation. It should not be used as a third proof point for `Residual-Budget Invariant for Shared-Capacity Pipelines` until a specific implementation path and oracle demonstrate the same invariant.
