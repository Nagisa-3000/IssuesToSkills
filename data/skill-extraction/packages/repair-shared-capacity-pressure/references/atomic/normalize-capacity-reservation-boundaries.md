# Atomic: normalize capacity reservation boundaries

Normalize absent, malformed, zero, negative, and provider-derived reservation values into an explicit positive integer reservation or a documented no-reservation state before arithmetic.

## Invariant

Malformed input cannot crash policy arithmetic or silently authorize an unsafe threshold.

## Oracle

Partition tests for `None`, zero, negative, non-integer, positive, and reservation-at/over-capacity values.
