---
name: direct-export-binding-guard
description: "Repair Python static-analyzer export binding that mistakes indirect module-level __all__ targets for direct assignments; gate specialized dispatch by immediate AST parent and validate ordinary import diagnostics."
---

# Direct export binding guard

## Activation

Activate when public evidence shows a Python static analyzer crashing or misclassifying module-level `__all__` reached through an indirect assignment target, and specialized export handling appears to receive a target container instead of an assignment statement.

A characteristic symptom is an attribute error involving `.value` on an AST tuple after processing `__all__, = ...`. The semantic defect—not a repository name—is the activation identity.

Clarify when the reproduction, traceback, pinned checkout, or immediate-parent relationship is unknown. Do not activate for runtime unpacking errors, unrelated undefined-name diagnostics, or an incompatible AST interface. Do not interpret the original reporter's suggestion to flag invalid input as the historical repair requirement.

## Current probes and bindings

Build a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners:

- `export-binding-dispatch`: the classifier choosing specialized export handling;
- `export-binding-constructor`: the consumer expecting an assignment value;
- `export-binding-tests`: public export/import diagnostic tests.

[Inspect the boundary](references/actions/inspect.md) before editing. Confirm that parent links denote the immediate syntactic parent and that indirect targets can use ordinary binding classification. UNKNOWN prerequisites permit probes only; FAIL rejects the proposed repair.

Historical paths are recorded in [the episode](references/episode.md), not silently bound to the current checkout.

## Operations

Follow the semantic dependencies in the canonical [Workflow](references/workflow.md):

1. [Inspect the boundary](references/actions/inspect.md).
2. [Guard specialized dispatch](references/actions/guard.md).
3. [Add regression coverage](references/actions/regression.md).
4. [Validate the final candidate](references/actions/validate.md).

Match all Port dimensions when connecting operations. Current plans may omit already-satisfied edits, but each performed modifying Action must retain its explicit validation Action. No bridge to another AST model is supplied.

## Validation and stopping

Bind every Oracle to a public current instruction, argv command, and evidence references. Record the mapping from `action_id/source_oracle_id`; its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution. Historical commands remain evidence, not execution authorization.

Require public checks supporting:

- no internal exception for the original indirect-target reproduction;
- an unused-import diagnostic for the indirect `__all__` regression;
- preservation of established direct module-export behavior;
- preservation of ordinary unused-import behavior in relevant adjacent tests.

Refresh validation observations after edits. Keep behavior assurances separate from observation freshness. Structural PASS predicts compatibility, not repair success. Stop if the immediate-parent contract differs, fallback behavior cannot be preserved, a public check fails, or validation cannot be bound. Record unavailable checks as UNKNOWN.

After the solver stops, obtain independent hidden acceptance through the evaluation host; hidden tests and gold-derived commands must not enter this guidance.

## Scope and evidence

This is a single-source Workflow, not a Pattern or cross-project template. The [episode and evidence](references/episode.md#evidence) distinguish reported failure, merged implementation, and committed regression assertions. No historical test-run log is supplied.

The later qualification reports one fail-to-pass and 131 pass-to-pass cases in changed test files with original-base control. Whole-project regression and cross-project transfer are untested. That 2026 attestation is provenance, not backdated pre-cutoff knowledge; see [provenance](references/provenance.json).

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`. No executable oracle is included.

Current task plans are not newly verified historical knowledge. Keep formal catalogs and checkpoints frozen; time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
