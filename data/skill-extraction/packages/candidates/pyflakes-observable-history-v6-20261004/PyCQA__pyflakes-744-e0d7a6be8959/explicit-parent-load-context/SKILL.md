---
name: explicit-parent-load-context
description: "Repair Python AST analysis crashes when early name-load dispatch needs parent context before traversal has attached parent metadata, and the caller already owns the correct parent."
---

# Explicit parent context for early load analysis

Canonical Skill/Workflow ID: `workflow:verified-history:73c1883f7ed05d43025127fa`.

## Activation and exclusions

Activate when current public evidence establishes that:

- A Python AST analyzer dispatches load analysis for an augmented-assignment target before ordinary traversal initializes its parent metadata.
- Load analysis reads that metadata for a parent-sensitive semantic check.
- The dispatching caller already has the correct parent node available.

Probe or clarify when the missing-parent traceback is known but initialization order or parent semantics are unknown. Do not activate merely because an input contains `print`.

Exclude parser rejection before analysis, unrelated missing attributes, non-Python interfaces, and cases where the caller cannot supply the semantically correct parent. This single-source Workflow does not establish a general cross-project Pattern.

## Current probes and bindings

Establish a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Resolve these semantic owners in the current checkout:

- `load-analysis-owner`: load-analysis interface and parent-sensitive branch;
- `early-load-dispatch-owner`: early augmented-assignment load dispatch;
- `ordinary-load-dispatch-owner`: ordinary name-load dispatch;
- `regression-test-owner`: public analyzer regression tests.

[Inspect dispatch and parent lifecycle](references/actions/inspect.md) before editing. Existence predicates use boolean values and role-based keys; the role must resolve to a current symbol or file. Existence alone does not establish semantic compatibility.

UNKNOWN prerequisites authorize probes only. Hard semantic failures reject the repair. Current bindings resolve aliases before read/write conflict checks.

## Operations

1. [Inspect dispatch and parent lifecycle](references/actions/inspect.md).
2. [Pass explicit parent context and add regression coverage](references/actions/repair.md).
3. [Validate public behavior and adjacent diagnostics](references/actions/validate.md).

The [Workflow](references/workflow.md) supplies dependencies and invariants. The [Episode](references/episode.md) separates historical facts from reusable operations.

The supported edit makes parent context an explicit load-analysis argument. Ordinary dispatch continues using its traversal-aware parent lookup; early augmented-assignment dispatch passes its enclosing assignment directly. Preserve the builtin-sensitive print diagnostic and the existing value-then-target traversal order.

## Validation and stop conditions

Bind each source Oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty historical command arrays do not authorize guessed commands.

Check the public reproductions `print *= -1` and `print += 1`, the added regression, adjacent ordinary-load and incompatible-print tests, and every changed-interface caller. Refresh `public-validation-observed` after edits.

Accept only when required current checks are PASS. A validation record may contain failures; its existence is not repair success. Stop on unresolved callers, incorrect parent semantics, failed regressions, or unavailable public validation. Structural PASS predicts compatibility, not success. Independent hidden acceptance occurs after the solver stops and does not supply public repair guidance.

## Evidence and limits

The historical evidence contains a reported crash, a merged interface change, and a regression assertion available at that commit. It supplies no historical test execution transcript.

The later qualification attestation reports one fail-to-pass and 126 pass-to-pass results in changed test files with original-base control. Whole-project regression and cross-project transfer remain untested. This contemporary attestation is recorded in [provenance](references/provenance.json), not backdated as pre-cutoff knowledge.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are unexecuted definitions. During formal evaluation, keep knowledge and checkpoints frozen; never publish a current task plan as newly verified history. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
