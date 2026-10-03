---
name: annotated-assignment-binding-order
description: "Repair a Python static analyzer that binds an annotated assignment target before checking its initializer, suppressing an undefined-name diagnostic."
---

# Annotated assignment binding order

## Activation and exclusions

Activate when a Python static analyzer reports an undefined name for ordinary `x = x` but suppresses that diagnostic for annotated `x: int = x`.

This is a conditional, single-repair Workflow Skill, not a Pattern or a claim of cross-project verification. Before editing, establish that the current target-handling operation introduces a binding before initializer analysis.

Clarify when the reproduction, current analyzer, or semantic owner is unknown. Do not activate for unrelated annotation syntax errors, runtime annotation evaluation, or a deliberately different name-resolution policy.

## Current probes and bindings

Use [inspection](references/actions/inspect.md) to locate the current annotated-assignment visitor and public annotation regression suite. Inspect target-binding effects, annotation processing, initializer dispatch, and the reported diagnostic discrepancy. Historical paths in [the episode](references/episode.md) are not current bindings.

Create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve role aliases before checking read/write conflicts.

Each current Oracle maps an Action ID and source Oracle ID to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty command arrays in these historical contracts require current binding; they are not executable commands.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only. Hard semantic failures reject the repair. Structural PASS predicts compatibility, not repair success.

## Linked operations

1. [Inspect ordering and reproduce the discrepancy](references/actions/inspect.md).
2. If the mechanism is confirmed, [defer target handling and add a regression](references/actions/reorder.md).
3. [Validate the diagnostic and adjacent behavior](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) records dependencies. Inspection may be omitted only when fresh current observations already satisfy its output and prerequisites. The modifying Action always retains its explicit validation Action.

## Validation and stopping

Require an undefined-name diagnostic for a previously unbound `x` in `x: int = x`. Check ordinary `x = x`, a previously bound initializer name, annotation-only declarations, and existing special annotation/TypeAlias behavior where present.

Stop if early target binding is absent, moving target handling would violate required annotation semantics, owner bindings or public test commands remain unknown, or required adjacent checks fail. Refresh validation observations made stale by edits. Expected effects are not observed results.

## Authority and limits

The supplied evidence supports one historical repair. The regression is a committed assertion; historical test execution is not supplied. A contemporary qualification attests one fail-to-pass and 53 pass-to-pass cases in changed test files only, with original-base control. Whole-project regression and cross-project transfer are untested.

See [the implementation evidence](references/evidence/fix.md), [provenance](references/provenance.json), and the non-executed [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions.

During formal evaluation, keep knowledge and checkpoints frozen. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. Do not publish a current task plan as newly verified historical knowledge. After public verification and solver completion, independent hidden acceptance remains required.
