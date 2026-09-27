# Promotion decision — Hermes compaction/context-pressure run

## Decision

### Atomic Skills

| Candidate | Decision | Evidence basis | Limitation |
|---|---|---|---|
| `derive-policy-from-residual-capacity` | **provisional candidate; eligible for internal retrieval** | Direct residual-capacity arithmetic in `623b...`; implicit-floor/active-capacity cases in `4252...` and `b780...` | All evidence is from Hermes; cross-harness transfer and held-out success are not measured here |
| `normalize-capacity-reservation-boundaries` | **candidate, not promoted** | Concrete coercion and malformed-input tests in `623b...` | One direct realization |
| `cap-implicit-pressure-before-capacity-exhaustion` | **provisional candidate** | Two distinct policy surfaces: threshold floor (`4252...`) and retained tail (`b780...`) share the binding-term/soft-envelope mechanism | Do not collapse the two formulas or claim one exact 85%/20% constant is universal |
| `centralize-derived-policy-at-a-pure-seam` | **candidate, not promoted as family Pattern** | `_derive_trigger` and switch-guard oracle in `af0...` | One direct realization; implementation technique rather than capacity law |
| `replay-policy-input-across-runtime-reconfiguration` | **candidate, not promoted** | construction/update_model in `623b...`; shared derivation/install in `af0...` | The selected evidence does not include a separate provider-switch behavioral run |

### Workflow Skill

`repair-capacity-aware-compaction-pressure` is **provisional within Hermes**. Four cases exercise different branches of one diagnostic DAG, and the workflow has explicit stop conditions and behavior-level oracles. It should not yet be presented as a validated cross-repository workflow or exported as a default top-level agent Skill without transfer evaluation.

### Pattern

Propose only the following **provisional Pattern**:

> **Effective Capacity Envelope for Pressure Policies.** When an upstream pressure/retention decision and downstream output/safety/required-context material share a finite capacity, derive the policy from the admissible residual envelope; cap implicit floors/optional retention before exhaustion; preserve explicit intent and required atomic groups; recompute at runtime policy boundaries; validate both numeric partitions and behavior before the provider boundary.

Support:

- `623b...`: mandatory output reservation changes effective input budget.
- `4252...`: implicit minimum floor is unsafe near a small capacity and must be bounded without overriding explicit intent.
- `b780...`: fixed optional retained tail is unsafe on small capacity; the soft ceiling must follow active capacity while preserving atomic groups.
- `af0...`: duplicate derivation can make a preview violate the installed envelope; a pure seam maintains consistency.

**Status: provisional, not promoted.** The evidence is four semantically related changes in one harness. A Pattern promotion gate requires at least one independent harness (or a held-out Hermes task) to realize the causal mechanism with matching invariants and an evaluation showing transfer; this run does not claim that result.

## Rejected alignments

The following Hermes history was considered but not merged into this Pattern/Workflow because the mechanism is different:

- stale compression generation / watermark fixes (`2492193...`, `40051...`, `3f7e...`): concurrency ownership and publication race;
- summary provider overload/refusal (`af93...`, `f6f7...`, `42545...`): failure classification/recovery;
- truncated-summary backoff (`801e...`): cooldown scheduling;
- oversized-turn splitting (`cc4bb...`, `d32f...`): structural turn preservation;
- display-only token-estimate change (`444066...`): accounting semantics, not the selected capacity-envelope policy.

This rejection is important: similar words such as “compression”, “token”, and “context” are not sufficient for alignment.

## Verification record

- Output files written only in `data/skill-extraction/agent-runs/hermes/`.
- No existing `data/skill-extraction/cases/` or `data/skill-extraction/synthesis/` files were edited by this run.
- `cases.json` was parsed successfully with PowerShell `ConvertFrom-Json`; it contains four cases and all required case fields.
- Source repository cleanliness must be checked after extraction; no source changes are intended.
- Attempted `python3 -m pytest tests/agent/test_context_compressor.py -q --disable-warnings --maxfail=1` in Hermes; it could not start because `/usr/bin/python3` has no `pytest` module. This is recorded as an unavailable test runner, not a pass.

