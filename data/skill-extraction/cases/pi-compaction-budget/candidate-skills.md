# Candidate Atomics: Pi compaction budget

## P1 — resolve-model-specific-policy-with-fallback

**Small problem.** A runtime supports multiple models/providers, but compaction settings differ by model and must fall back predictably.

**Solution paradigm.** Resolve policy by the most specific stable model identity, validate both base and override settings, and expose one resolved policy object to every compaction entry point.

**Inputs:** base settings, provider/model identity, optional exact override.
**Outputs:** validated `reserveTokens`, `keepRecentTokens`, and precedence metadata.
**Invariants:** invalid base settings are not hidden by a valid override; model switching changes policy only according to explicit precedence.
**Oracle:** exact-match, fallback, invalid-value, and model-switch tests.
**Exclusions:** deriving a residual capacity formula; provider-specific billing semantics.

## P2 — replay-policy-across-runtime-reconfiguration

**Small problem.** A policy is resolved once but later model switches, overflow recovery, or extension preparation use stale settings.

**Solution paradigm.** Centralize resolution and route all execution paths through the same resolved policy seam.

**Invariant:** manual, automatic, overflow, extension-visible, and switched-model paths observe the same active policy.
**Oracle:** cross-entry-point equivalence tests.

## P3 — place-pressure-check-at-next-request-boundary

**Small problem.** Automatic compaction runs after a tool result even when no further assistant request will occur, or runs too late before the next provider request.

**Solution paradigm.** Trigger pressure evaluation only when the loop is about to start a real next model request; skip it for terminal tool outcomes.

**Invariant:** no unnecessary compaction after termination; no provider request starts while the active context violates the threshold.
**Oracle:** tests with queued steering, terminating tool results, and post-tool continuation.

## P4 — account-for-all-context-visible-artifacts

**Small problem.** Budget measurement ignores custom/session entries that are visible to the model.

**Solution paradigm.** Define one canonical conversion from session entries to context messages and use it for token accounting and cut-point selection.

**Invariant:** every context-visible artifact contributes to the same budget calculation.
**Oracle:** custom-message tests change retained budget and cut points as expected.

## Candidate-to-case mapping

- `CA1 -> P1`
- `CA2 -> P2`
- `CA3 -> P3`
- `CA4 -> P4`
- `CA5 -> validation support only`

Pi does not promote a residual-budget Pattern by itself.
