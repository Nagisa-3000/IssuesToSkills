---
name: variadic-docname-compatibility
description: "Repair false missing or differing parameter-documentation diagnostics caused by supported bare or escaped spellings of Python variadic parameter names."
---

# Variadic documentation-name compatibility

## Activation

Activate when a Python documentation checker falsely reports a documented `*args` or `**kwargs` parameter as missing or different because its documentation uses a supported bare name or escaped asterisk notation.

Examples include paired diagnostics for `*args` missing and `args` differing, or a supported escaped parameter name failing extraction.

Clarify when the signature, documentation style, plugin configuration, diagnostic producer, or current code is unknown.

Do not activate for:

- Genuinely omitted parameter documentation.
- Unrelated misspellings or extra documented names.
- A Python string-literal backslash warning alone.
- A Sphinx rendering warning alone.
- An unsupported documentation grammar or another language without separately supported semantics.

## Current probes

Use [Inspect](references/actions/inspect.md) to distinguish parser extraction failure from signature-name comparison failure. Locate current semantic owners; historical paths in the [episode](references/episode.md) are not current bindings.

The current TaskContext must contain the public issue, pinned base, hashed code anchors, observed diagnostics and parsed names, style/configuration checks, real owner bindings, observed PortValues, and current Oracle bindings.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only. Hard semantic failures reject the plan. Matching predicate names alone does not prove applicability.

## Operations

The [Workflow](references/workflow.md) connects:

1. [Inspect](references/actions/inspect.md): locate the mismatch and bind current owners.
2. [Repair](references/actions/repair.md): implement supported extraction and conditional bare-name equivalence; add public regressions.
3. [Validate](references/actions/validate.md): execute target cases and adjacent controls.

Apply only portions supported by current observations. Do not impose one style's grammar on another, strip arbitrary punctuation, suppress diagnostics globally, or change type-documentation requirements as a substitute for repairing name handling.

Every modifying Action retains its validate Action. Refresh stale observations after edits.

## Validation and stopping

Before execution, render each current Oracle's public instruction and argv command. Bind it by Action ID and source Oracle ID, recording its check under `oracle:<action_id>:<source_oracle_id>`. Historical commands are evidence, not executable authority for a current checkout.

Validate that supported bare names document variadic parameters, supported escapes leave no name artifacts, genuine omissions remain missing, unrelated names remain differing, and ordinary parameters and exemptions survive. Keep Python string-literal warning behavior separate.

Stop before editing if style or owner bindings remain ambiguous. Stop if the behavior is already correct, a negative control regresses, or a required public oracle cannot be bound. A structural PASS predicts compatibility, not repair success. Report success only after actual current public checks; independent hidden acceptance occurs after the solver stops and never supplies guidance.

## Evidence and limits

This is a single-source Workflow, not a Pattern or cross-project abstraction. See [original report](references/evidence/body.md), [implementation](references/evidence/fix.md), [committed assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical CI execution is unknown. Later independent qualification used original-base controls and selected documentation tests: original base passed 11, base with added regression assertions failed three and passed eight, and historical fixed code passed 11. Qualification is changed-test-only; whole-project correctness and cross-project transfer remain untested. It does not execute the authored [functional cases](evals/functional-cases.json).

Formal evaluation knowledge and checkpoints stay frozen. Earlier-time admission excludes the task's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before the query input time.
