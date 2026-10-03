---
name: preserve-annotation-bindings
description: "Repair Python static-analysis scope updates when an annotation-only binding overwrites an existing value binding and loses export or usage information."
---

# Preserve existing bindings during annotation-only updates

This is a conditional Workflow Skill, not a cross-project Pattern.

## Activation

Activate when current public evidence indicates that:

- A Python static analyzer stores name bindings in a scope or namespace.
- An annotation-only declaration can replace an existing binding.
- That replacement loses meaningful metadata, such as export membership or import-use information.
- The current binding insertion owner can distinguish annotation-only bindings from assignments with values.

The historical motivating case involved a runtime export declaration followed by an annotation-only declaration in another conditional branch. See the [episode](references/episode.md).

**Clarify or probe first** when the symptom is known but the binding overwrite mechanism is not established. Do not activate solely because a project contains annotations or an unused-import warning.

**Do not activate** for valued annotated assignments, runtime execution of annotations, unrelated import resolution failures, or analyzers whose existing binding semantics intentionally require annotation-only declarations to replace values.

## Current probes and bindings

Locate the current semantic owners rather than assuming historical paths:

1. The scope-binding insertion owner.
2. The annotation-only binding classifier.
3. The export-binding and unused-import consumers.
4. The annotation regression test owner and its public runner.

Inspect whether the incoming annotation-only binding overwrites an existing binding in the same scope. Check that an absent name can still receive an annotation binding and that an ordinary incoming assignment still replaces an existing binding.

Use the [inspection Action](references/actions/inspect.md). Unknown prerequisites permit inspection only. A failed mechanism check rejects this workflow.

## Operations

- [Inspect the overwrite mechanism](references/actions/inspect.md).
- [Guard annotation-only replacement](references/actions/guard.md).
- [Add the export regression assertion](references/actions/regression.md).
- [Validate both edits and adjacent behavior](references/actions/validate.md).

The [Workflow](references/workflow.md) defines dependencies and retained assurances. Its outputs and effects are expectations, not claims of execution in a current checkout.

## Validation and stopping rules

Bind public current commands to the validation oracle before executing them. Historical test locations are reference material, not current bindings.

Confirm:

- The motivating export/annotation example produces no diagnostics.
- An absent name can acquire an annotation-only binding.
- Ordinary assignments still replace prior bindings.
- Annotation expressions retain their intended import-use handling.
- The relevant annotation tests pass.

After either edit, prior validation observations are stale. Re-run validation; do not confuse stale observations with a loss of the required behavior assurances.

Stop if the guard would suppress ordinary assignments, if the current analyzer uses incompatible binding semantics, or if preservation checks fail. If current public tests cannot be run, report validation as UNKNOWN rather than claiming repair success.

## Evidence and limits

The historical fix guards the shared scope update against replacement by an incoming annotation-only binding. It does not use unconditional `setdefault`.

Historical regression evidence is an assertion added at the repair commit; the supplied historical material does not establish a historical test execution. A later qualification reports one fail-to-pass case and 46 pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer remain untested.

See [evidence](references/evidence/fix.md), [regression evidence](references/evidence/regression.md), and [provenance](references/provenance.json). Evaluation definitions in this package are [not executed](evals/functional-cases.json).
