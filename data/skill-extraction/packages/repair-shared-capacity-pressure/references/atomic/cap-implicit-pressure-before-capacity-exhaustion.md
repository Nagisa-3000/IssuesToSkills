# Atomic: cap implicit pressure before capacity exhaustion

## Problem

An implicit minimum floor, optional retained tail, or soft ceiling becomes the binding term on a small active capacity and leaves too little room for the next admissible request. A fixed universal constant is not the reusable knowledge.

## Solution paradigm

1. Identify which term is actually binding.
2. Apply a safety cap only to implicit/default terms.
3. Preserve explicit user intent when it is an explicit policy parameter.
4. Preserve required atomic context groups even if they exceed a soft ceiling.
5. Validate near-minimum, below-cap-floor, and explicit-high regimes.

## Invariant

Implicit/default policy must leave an admissible remainder for required downstream work; explicit user policy is not silently rewritten.

## Realization

Hermes commits `4252aecc2ed88dc69e9b0f60af796612f1feeada` and `b7803a1763558f3125834282cf17810ab2b4aa73`.

This is currently a Hermes-only provisional candidate. Do not generalize the observed 85% or 20% constants as universal.
