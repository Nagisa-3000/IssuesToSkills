# Evidence: Hermes compaction threshold reserves output capacity

## Scope and provenance

- Repository: `/home/chenyujia/tritonToLlvm/hermes-agent`
- Commit: `623b21bf24ea3f2f2c2d90de3ae872b8a0a000c4`
- Subject: `fix(compress): reserve output tokens in the compaction threshold (#23767, #43547)`
- Parent: `623b21bf^`
- Files read from the verified diff:
  - `agent/agent_init.py`
  - `agent/context_compressor.py`
  - `tests/agent/test_context_compressor.py`

This is one repository case. It is evidence for Case Actions and single-case Atomic candidates, not by itself a cross-repository Pattern.

## Observed failure mechanism

The old compaction threshold used the nominal `context_length * threshold_percent`. The provider charges `max_tokens` output from the same context window, so the input-side budget is smaller. The fix changes the calculation to use the effective input budget, conceptually:

```text
W = context_length
O = normalized positive max_tokens reservation
M = W - O, when M > 0
threshold = policy(M), not policy(W)
```

The small-window 85% guard is applied to the effective budget. When a reservation is absent, invalid, non-positive, or leaves no positive effective budget, the implementation preserves a safe positive fallback rather than emitting a non-positive threshold.

## Implementation evidence

1. `agent/agent_init.py` threads `agent.max_tokens` into `ContextCompressor` construction.
2. `ContextCompressor._coerce_max_tokens()` turns `None`, non-numeric, and non-positive values into no reservation; positive values become the reservation.
3. `_compute_threshold_tokens(context_length, threshold_percent, max_tokens)` derives the threshold from the effective budget and applies the small-window guard there.
4. `update_model()` retains the existing reservation when a model switch does not supply a new value and recalculates thresholds after context changes; an explicitly supplied value replaces it.
5. Tests cover no reservation, `200000 - 65536` at 50% (`67232`), small effective windows, reservation exceeding the window, invalid values, and positive-threshold/no-crash behavior.

## Case Actions

- `CA1`: diagnose a shared-capacity accounting mismatch between input pressure and downstream output reservation.
- `CA2`: normalize optional reservation inputs before arithmetic.
- `CA3`: derive a policy threshold from residual input capacity and apply all guards to that same capacity.
- `CA4`: propagate the reservation through construction and model/runtime reconfiguration.
- `CA5`: validate boundary partitions: absent/invalid/non-positive reservation, positive reservation, reservation near capacity, and reservation exceeding capacity.
- `CA6`: verify the behavior with numeric unit oracles and reconfiguration regression tests.

## What this case does not prove

- It does not prove configurable headroom separate from output reservation.
- It does not prove a full compaction workflow or a cross-repository Pattern.
- It does not justify naming a repository-specific class or function as a reusable Skill.
