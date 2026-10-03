---
name: decorator-binding-type-guard
description: "Repair Python overload-decorator recognition when a scope binding is inspected for import-specific metadata without first checking its binding type."
---

# Decorator binding type guard

## Activation

Use this Workflow when a Python static analyzer recognizes overload decorators by resolving a bare decorator name in a scope, and may read import-specific metadata from a binding that is not an import.

Strong signals include:

- A recognizer compares a resolved binding's qualified name with `typing.overload`.
- Ordinary locally assigned decorators pass through the same recognition branch.
- That branch verifies name membership but not the binding class before accessing import metadata.

An unspecified analyzer failure or release regression alone is insufficient. Locate and inspect the current recognizer before proposing an edit.

Do not activate for decorator execution errors, unrelated name-resolution defects, or an attribute-form decorator branch with no corresponding unsafe bare-name lookup. This Skill is not a general decorator or typing repair template.

## Operations

1. [Locate and inspect the recognition boundary](references/actions/inspect.md).
2. If current evidence confirms the unsafe access, [guard the binding and add the regression](references/actions/repair.md).
3. [Validate ordinary decorators and preserved overload recognition](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records the source-supported dependency order. Already satisfied probes may be omitted from a current plan only when fresh public observations establish their outputs and prerequisites.

## Current binding and probes

Bind these semantic owners in the current checkout:

- `overload-decorator-recognizer`: the implementation deciding whether decorators denote the special overload marker.
- `scope-binding-model`: binding classes, including the class representing a from-import.
- `decorator-recognition-tests`: public regression tests for decorator classification and repeated-definition diagnostics.

Do not treat historical file paths as current bindings. Record the public issue, pinned base, hashed anchors, observed facts, semantic checks, owner bindings, PortValues, and current Oracle bindings in the current TaskContext.

Check that a bare-name branch can resolve both import and non-import bindings. Confirm that the relevant import-binding class supplies the qualified-name metadata used by the comparison. Inspect short-circuit ordering before modifying code.

## Validation and execution

Bind each Action oracle to a public current instruction, an argv command appropriate to the checkout, and supporting current evidence. Render these bound commands before execution. The check key is `oracle:<action_id>:<source_oracle_id>`. No historical command is supplied or authorized by this package.

Required observable checks:

- A locally assigned decorator does not cause import-metadata access on a non-import binding.
- Three same-name function definitions using the supplied ordinary-decorator pattern produce exactly two unused-redefinition diagnostics.
- Actual from-import overload recognition still works.
- The neighboring attribute-form recognition branch remains unchanged and passes available public tests.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only; a hard applicability failure rejects the repair plan. After editing, refresh invalidated observations and run the explicit validation Action. Structural compatibility does not establish repair success. Independent hidden acceptance, if part of the host evaluation, occurs after the solver stops and must not shape guidance.

## Stop conditions and limits

Stop without this repair if the current binding model does not support the evidenced type guard, the metadata owner cannot be determined, or the suspected unsafe lookup is absent. Do not invent an adapter or apply a blanket exception handler.

The historical change supports one focused Workflow, not a cross-project Pattern. Historical regression material is a test assertion available at the repair commit, not a supplied execution log. A later qualification verified one fail-to-pass and thirteen pass-to-pass cases in changed test files only; whole-project regression and cross-project transfer remain untested.

See [episode and qualification limits](references/episode.md), [provenance](references/provenance.json), and the unexecuted [functional definitions](evals/functional-cases.json).
