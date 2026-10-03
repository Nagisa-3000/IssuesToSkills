---
name: assignment-expression-outer-scope
description: "Conditionally repair false undefined-name diagnostics caused by binding assignment-expression targets inside comprehension scopes instead of their enclosing scope."
---

# Assignment-expression outer-scope binding

## Activation

Use this Workflow when a Python static analyzer reports an undefined assignment-expression target after a generator expression or comprehension, and current public inspection confirms that the target was incorrectly bound inside a comprehension scope.

Before editing, establish that:

- The syntax is an assignment expression (`:=`), not an ordinary comprehension iteration target.
- The analyzer and validation runtime support that syntax.
- Current binding classification and insertion owners are located.
- The relevant scope chain contains identifiable comprehension scopes.
- The public diagnostic and code inspection support this specific ownership mismatch.

Clarify an undefined-name report without its reproduction, syntax version, or scope context. Do not activate for genuinely undefined names, runtime unbound-variable errors, ordinary iteration-variable leakage, or unrelated name-resolution failures.

This evidence does not establish comprehensive handling of class-body restrictions, `global`, `nonlocal`, or evaluation-order edge cases. Do not cross a real function boundary when routing the binding.

## Operations and current probes

1. [Probe binding ownership](references/actions/probe.md): inspect current public code and reproduce the diagnostic without editing source.
2. [Repair classification and routing](references/actions/repair.md): distinguish assignment-expression bindings; route only those bindings past contiguous comprehension scopes; add single and nested regression assertions.
3. [Validate the repair](references/actions/validate.md): execute current-bound public target checks and adjacent scope checks; review preserved bookkeeping.

The [historical Workflow](references/workflow.md) records the supported mechanism. The [episode](references/episode.md) records historical paths and symbols; these are not automatic current bindings.

## Current execution requirements

Construct a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Match all Port dimensions, not merely artifact types or similar names.

Each current Oracle binding maps `action_id` and `source_oracle_id` to a public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render current-bound commands before execution. Empty command arrays in these historical contracts are not executable command authorizations.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only; hard failures reject the plan. Structural PASS predicts compatibility, not successful repair. After edits, refresh stale validation observations. Expected effects in Action contracts must not be reported as observed results without current checks.

## Preservation and stop conditions

Preserve ordinary assignment ownership, comprehension iteration-variable isolation, and unrelated binding bookkeeping. Stop if owners cannot be safely identified, the public mismatch is absent, routing would cross a function boundary, or adjacent checks fail. A version-skipped target check is insufficient validation.

Run public checks, report their actual scope and outcomes, and stop the solver before any independent hidden acceptance. Hidden acceptance is not guidance. Do not publish current task plans as newly verified historical knowledge during formal evaluation.

## Evidence and limits

This is a single-repair Workflow, not a Pattern or a cross-project template. All four supplied evidence entries are packaged in the [episode](references/episode.md). Historical regression evidence records assertions at the merged commit, not a supplied execution transcript.

The later qualification attestation reports two fail-to-pass and 123 pass-to-pass checks using changed test files and an original-base control. Whole-project regression and cross-project transfer are untested. That attestation is contemporary provenance, not pre-cutoff learned content; see [provenance](references/provenance.json).

Formal knowledge and checkpoints remain frozen. Time-reconstructed catalogs exclude the current query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before its input time.

Evaluation definitions remain unexecuted: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json).
