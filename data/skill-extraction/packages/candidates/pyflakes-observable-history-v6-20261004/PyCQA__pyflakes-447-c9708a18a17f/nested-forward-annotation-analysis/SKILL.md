---
name: nested-forward-annotation-analysis
description: "Repair Python static-analysis traversal when imported names used inside nested quoted type annotations are missed, while preserving Literal string values and deferred-analysis behavior."
---

# Nested forward-annotation analysis

This conditional Workflow Skill addresses a Python AST-based analyzer that visits outer annotations but ignores quoted type expressions nested inside them. Its historical example is an unused-import warning for `Optional['Queue[int]']`.

## Activation

Activate when public evidence shows all of the following:

- An imported name is used inside a quoted type expression nested within an annotation.
- The analyzer reports that import as unused, or otherwise misses that annotation reference.
- The current implementation has identifiable annotation traversal, string-node dispatch, scope resolution, and deferred-analysis owners.

Clarify when the report provides only an unused-import warning without its annotation or a public reproduction.

Do not activate for ordinary runtime strings, genuine unused imports, runtime type evaluation failures, or a non-Python analyzer without a separately supported realization.

## Current probes and binding

Start with [the read-only probe](references/actions/probe.md). Locate semantic owners in the current checkout rather than copying historical file paths. Capture the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Each current Oracle must bind its Action ID and source Oracle ID to a public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Historical implementation and test snippets are evidence, not authorization to execute historical commands.

Use PASS/FAIL/UNKNOWN checks. Unknown prerequisites permit investigation only; failed applicability checks reject this workflow. A structurally compatible plan predicts compatibility, not repair success.

## Operations

1. [Probe annotation and deferred traversal](references/actions/probe.md).
2. [Edit context-aware quoted-annotation traversal](references/actions/edit.md), only after the current semantic owners and failure mechanism are established.
3. [Validate the candidate through public probes and repository tests](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records these dependencies. Current plans may omit already satisfied operations, but every modifying operation retains public validation.

## Required behavior

Interpret nested strings as annotation expressions only within annotation traversal, excluding strings under recognized `typing.Literal` or `typing_extensions.Literal`. Restore temporary traversal flags even on exceptions. Preserve scope-aware name resolution, ordinary runtime strings, existing overload handling, and analysis-phase integrity.

The historical repair recognized imported bare typing names through bindings, and qualified attributes with the literal module names `typing` and `typing_extensions`. It does not establish support for arbitrary module aliases.

## Validation and stopping

Validate the original public reproduction and these adjacent cases:

- Partially quoted parameter and return annotations.
- A quoted outer annotation containing an inner quoted annotation.
- Postponed annotations where supported.
- Single and multiple string values in recognized `Literal` expressions.
- Existing overload behavior, including qualified `typing_extensions.overload`.
- Ordinary runtime strings and supported string AST representations.

Refresh validation observations after edits. Stop if semantic ownership cannot be established, nested-string interpretation would alter unrelated runtime strings, current typing recognition differs materially from the supported mechanism, or public validation fails. Do not treat missing execution evidence as success.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and the packaged evidence cards:

- [Original title](references/evidence/title.md)
- [Original report](references/evidence/body.md)
- [Merged implementation](references/evidence/fix.md)
- [Regression assertions](references/evidence/regression.md)

This is one verified historical repair, not a cross-project Pattern. Historical regression assertions are recorded as assertions present at the commit; the supplied evidence does not establish their historical execution. A later qualification attestation reports changed-test-file checks only, with four fail-to-pass and 25 pass-to-pass cases. Whole-project regression and cross-project transfer are untested. That attestation is not pre-cutoff learned content.

The packaged [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions and remain `not_executed`. During formal evaluation, keep knowledge and checkpoints frozen, do not publish current task plans as historical knowledge, and obtain independent hidden acceptance only after the solver stops. Time-reconstructed catalogs must exclude the current issue, fix, cluster, aliases, copies, and sources unavailable before query time.
