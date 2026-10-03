---
name: return-annotation-scope
description: "Repair a Python static analyzer that incorrectly revisits a function return annotation inside the function-body scope, causing class-bound annotation names to be reported undefined."
---

# Return annotation scope

## Activation

Use this Workflow when a Python static analyzer reports an undefined name in a method's return annotation even though the name is bound in the enclosing class, and current inspection suggests that function-child traversal revisits the return annotation after entering the function-body scope.

The historical reproduction uses a class-level `TypeVar`, but the activation identity is the scope/traversal defect, not a repository name or the presence of `TypeVar` alone.

**Clarify or probe first** when the diagnostic location, annotation-processing phase, or scope owner is unknown. Unknown prerequisites authorize inspection, not editing.

**Do not activate** for a genuinely missing annotation name, runtime annotation evaluation failures, unrelated type-checker inference problems, or a different annotation-resolution model without evidence of the duplicate inner-scope visit. Do not suppress undefined-name reporting globally or make body-local variables visible to return annotations.

## Current probes and bindings

Before applying the historical mechanism:

1. Locate the current semantic owner of function-definition child traversal and its scope-entry operation.
2. Trace how return annotations are processed before and after entering function scope.
3. Establish whether the current traversal would revisit the return annotation in the wrong scope.
4. Locate the public annotation regression suite and its test runner.
5. Bind both regression scenarios to the current checkout.

Historical file paths are documented only in [the episode](references/episode.md). They are not current bindings.

A current TaskContext should record the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render and run those bound commands; no historical command here authorizes execution against an uninspected checkout.

## Operations

- [Inspect annotation traversal and scope](references/actions/inspect.md): establish applicability and semantic bindings.
- [Exclude return annotations from inner traversal](references/actions/edit.md): apply the narrowly supported traversal change.
- [Validate enclosing-scope and body-local behavior](references/actions/validate.md): retain public verification for the modifying Action.

The canonical [Workflow](references/workflow.md) records dependencies and expected effects. Already satisfied inspection or editing work may be omitted from a current task DAG only with fresh supporting observations; validation remains required for the edit.

## Validation and stop conditions

Require both public regression scenarios:

- A method parameter and return annotation can refer to a previously bound class-level `TypeVar` without an undefined-name diagnostic.
- A name assigned only in the method body remains undefined in the return annotation.

Run the current annotation regression suite as well. Refresh observations invalidated by the edit. Treat checks as PASS, FAIL, or UNKNOWN: a hard prerequisite failure rejects this plan; an unknown prerequisite permits probes only. Structural compatibility is not repair success.

Stop and reassess if return annotations have no correct enclosing-scope processing pass, if the traversal exclusion would skip their analysis altogether, or if preserving the existing decorator exclusion is impossible without a broader unsupported change.

## Evidence and limits

This is a single-source Workflow, not a cross-project Pattern. The historical fix is a one-line traversal omission change with two regression assertions. Historical test execution is not supplied.

A later qualification attestation reports one fail-to-pass and seventeen pass-to-pass cases, but only for changed test files with original-base control. Whole-project regression and cross-project transfer were untested. That attestation is provenance, not historical knowledge available before the cutoff.

See [provenance](references/provenance.json) and [evidence cards](references/episode.md). The evaluation definitions are **not executed**. Formal evaluation must keep knowledge and checkpoints frozen, avoid publishing current task plans as verified historical knowledge, and obtain independent hidden acceptance only after the solver stops.
