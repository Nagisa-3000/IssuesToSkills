# Candidate Atomic Skills — Hermes compaction/context pressure

These are **ordinary reusable Skills**, not commit summaries. Each is intentionally small: one recurring problem mechanism and one transferable solution protocol. A Case Action is the historical action; an Atomic Skill is the generalized protocol proposed after comparing the four cases.

## A1 — `derive-policy-from-residual-capacity`

**Small problem.** A pressure/admission/retention policy is computed from a nominal capacity, while a downstream output, safety reserve, or other mandatory consumer occupies the same capacity pool.

**Mechanism.** Nominal capacity is not admissible input capacity. If the policy runs on the nominal value, pressure can fire after the provider has already rejected/truncated the request, or retention can leave no compressible middle.

**Protocol.**
1. Identify the actual shared capacity pool and every mandatory reservation.
2. Normalize reservation values at the boundary.
3. Compute `residual = nominal_capacity - mandatory_reservations`.
4. Apply threshold/floor/headroom policy to `residual`, not to the nominal value.
5. Define explicit behavior for `residual <= 0` and for required atomic units that may overrun a soft budget.
6. Recompute when the active model/provider/window changes.

**Inputs.** Nominal context/window capacity; reservation(s); configured ratio/floor/cap; active runtime envelope.

**Outputs.** Derived pressure/admission/retention budget plus a reason explaining which term bound it.

**Preconditions.** The upstream policy and downstream reservation truly share a capacity pool; reservation affects provider admission or correctness.

**Postconditions/invariants.** `policy_limit <= residual_admissible_capacity` except explicitly documented required atomic groups; a positive/safe result is installed for degenerate inputs.

**Failure modes.** Double-subtracting a reservation; treating advisory metadata as hard reservation; applying a cap to explicit user intent; ignoring model/provider switch; hiding an impossible configuration.

**Behavioral oracle.** Numeric boundary partitions and end-to-end pressure behavior: the upstream guard fires before capacity exhaustion, and a small-window transcript leaves a real reclaimable middle.

**Realizations.** `CA-623-1/3`, `CA-4252-1/2`, `CA-B780-1/2`, and the shared relation between `CA-AF0-2` and active runtime derivation.

**Exclusions.** Not a generic “optimize tokens” rule; not applicable when input/output capacity is independent.

**Promotion.** Strongest candidate; supported by three direct capacity cases in one repository. Still provisional for cross-repository transfer.

## A2 — `normalize-capacity-reservation-boundaries`

**Small problem.** Optional or provider-derived capacity inputs arrive as `None`, zero, negative, non-integer, mock, or over-capacity values and contaminate policy arithmetic.

**Mechanism.** Boundary values are semantically ambiguous; arithmetic then crashes or installs an unreachable/non-positive threshold.

**Protocol.** Convert at the boundary into a small internal domain: `positive integer reservation` or `no reservation`; retain a separate explicit branch for reservation >= capacity; never let arbitrary objects reach arithmetic.

**Inputs/outputs.** Input: raw optional reservation. Output: normalized reservation/no-reservation plus an explicit degenerate-state decision.

**Invariants.** The arithmetic core receives stable typed values; no malformed input can cause a non-positive installed threshold or an unhandled exception.

**Oracle.** `None`, `0`, negative, string, `MagicMock`, valid positive integer, and reservation >= capacity are all tested.

**Realization.** `CA-623-2/5` in `623b21...`; only one direct Hermes case so this remains candidate, not a cross-case Pattern.

## A3 — `cap-implicit-pressure-before-capacity-exhaustion`

**Small problem.** A minimum floor or fixed retained-tail floor protects ordinary windows but becomes a disproportionate share of a small active window.

**Mechanism.** A floor is useful in absolute units but unsafe when it binds near the total capacity; equality-only guards miss near-degenerate values.

**Protocol.** Distinguish the term that bound the policy; cap only an implicit floor/optional budget as a fraction of active capacity; preserve explicit user intent; allow explicitly required atomic groups to overrun a soft ceiling.

**Inputs/outputs.** Input: active capacity, floor, explicit policy, required groups. Output: bounded pressure/retention budget and binding-reason metadata.

**Invariants.** The implicit budget leaves room for downstream work; explicit high settings are not silently rewritten; required anchors remain intact.

**Oracles.** Hermes 65536/70000/100000/372000 threshold partitions and 8K/16K/32K/128K tail partitions plus the tool-heavy end-to-end case.

**Realizations.** `CA-4252-2/3`, `CA-B780-2/3/4`.

**Promotion.** Candidate with two independent mechanisms in the same family, but “threshold floor” and “retained tail” are different policies; do not merge their implementation details into one formula.

## A4 — `centralize-derived-policy-at-a-pure-seam`

**Small problem.** Preview/warning and state-installation paths duplicate derived policy arithmetic and drift after future changes.

**Mechanism.** Two callers with supposedly identical inputs can present different thresholds; users see a warning that does not match the threshold installed.

**Protocol.** Put all pure derivation for a given input envelope in one function; have preview project from it and installation consume the same result; keep genuinely runtime-specific adjustments outside the pure seam.

**Inputs/outputs.** Input: model/provider/context/config/reservation. Output: base policy, effective policy, derived threshold, and binding reason.

**Invariant.** Previewed and installed values are equal for the same envelope; runtime-only caps remain explicitly separate.

**Oracle.** Switch-guard test quotes the cap only when it binds; preview equals `update_model` result; presentation does not claim a non-binding cap.

**Realization.** `CA-AF0-1/2/3/4`.

**Promotion.** Candidate, because it is a reusable implementation pattern, but not itself evidence of residual-budget arithmetic.

## A5 — `replay-policy-input-across-runtime-reconfiguration`

**Small problem.** A derived pressure policy is correct at construction but stale after model/provider/context/reconfiguration changes.

**Protocol.** Store semantic policy inputs, define preserve-vs-replace behavior, rederive all dependent values at the reconfiguration seam, and test both preview and installation paths.

**Realizations.** `CA-623-4` and `CA-AF0-3/4`; partial evidence only in this Hermes run.

**Exclusions.** Do not use when only presentation changes or when the runtime envelope is immutable.

## Atomic boundary decisions

- `derive-policy-from-residual-capacity` is not the same as `centralize-derived-policy-at-a-pure-seam`: the first is a capacity invariant; the second is a single-source-of-truth implementation technique.
- `scale-optional-retention-to-active-capacity` is represented by A3 rather than promoted as a separate top-level Skill because the current evidence has one retained-tail case.
- `preserve-atomic-required-context-groups` is a useful sub-protocol of A3, not yet an independent Skill: only one direct realization was found.
