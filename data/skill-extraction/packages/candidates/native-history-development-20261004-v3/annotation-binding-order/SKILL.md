---
name: annotation-binding-order
description: "Repair premature target binding in a Python static analyzer's annotated-assignment handler when it suppresses an undefined-name diagnostic in the initializer."
---

# Annotation binding order

## Conditional activation

Activate when current public observations establish both:

1. In comparable isolated scopes with no preceding binding, `x = x` reports an undefined name but `x: int = x` does not.
2. The annotated-assignment handler introduces the target binding before analyzing the initializer.

This is a focused Workflow supported by one historical bug cluster and fix. It is not a Pattern or evidence of cross-project transfer.

Clarify or probe if the isolated reproduction, scope, pinned checkout, or handler inspection is missing. Do not activate for malformed annotation syntax, runtime Python evaluation changes, or annotations alone. Reject the mechanism if target registration already follows initializer analysis or a preceding binding explains the diagnostic.

## Current probes and bindings

Create a current TaskContext recording the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Locate current semantic owners for annotated-assignment analysis, target registration, annotation and optional initializer analysis, specialized initializer dispatch, and annotation-diagnostic tests. Historical paths appear in [the episode](references/episode.md), not as automatic current bindings.

Compare isolated ordinary and annotated self-reference probes. Inspect the full current handler before editing. Unknown prerequisites authorize probes only; hard incompatibilities reject the plan. Port bindings must agree on semantic_role, artifact_kind, language, scope, phase, and state.

## Linked operations

- [Inspect symptom and mechanism](references/actions/inspect.md).
- [Delay target registration](references/actions/reorder.md).
- [Add or confirm the regression](references/actions/regression.md).
- [Validate both modifying Actions](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records supported semantic dependencies, not a recorded chronology of developer actions. Current DAGs may omit already satisfied operations only with current evidence for their outputs and prerequisites. Every edit retains explicit validation.

## Validation and stopping

Bind each oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render current bound commands before execution. Empty source command arrays are placeholders for current binding, not executable authorization.

Require actual evidence that:

- The unbound annotated initializer now reports undefined name.
- The ordinary-assignment control retains that diagnostic.
- The isolated regression and relevant annotation suite pass.
- Annotation processing, optional initializer handling, and specialized value dispatch remain intact.

Review annotation-only and previously bound-name cases using applicable current public tests or probes. These are preservation checks, not universally established semantics from the single historical reproduction.

Record PASS, FAIL, or UNKNOWN, actual outputs, and checkout identity. Refresh facts invalidated by edits. Stop on failed preservation, unresolved bindings, unavailable required oracles, or a different causal mechanism. Structural plan PASS predicts compatibility, not repair success. Obtain independent hidden acceptance after solver work stops; hidden checks do not enter public guidance.

## Limits and provenance

Historical test evidence consists of an assertion available at the merged commit; no historical test-run output was supplied. The contemporary qualification reports one fail-to-pass and 53 pass-to-pass cases in changed test files with an original-base control. Whole-project regression and cross-project transfer are untested.

The qualification remains a separately timestamped provenance attestation, not backdated learned content. Package eval definitions are **not_executed**. See [episode and evidence](references/episode.md), [provenance](references/provenance.json), and [functional definitions](evals/functional-cases.json).

Keep formal knowledge and checkpoints frozen. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and every source unavailable before query input time. Never publish a current task plan as newly verified historical knowledge.
