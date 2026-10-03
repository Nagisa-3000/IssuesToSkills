---
name: guard-specialized-binding-metadata
description: "Repair Python static-analysis special-case detection when a bound name is treated as an import without checking its binding type; preserve ordinary decorator redefinition diagnostics."
---

# Guard specialized binding metadata

Use this Workflow when a Python static analyzer recognizes a special decorator by inspecting a name's scope binding, but accesses import-specific metadata without first establishing the appropriate import-binding type.

This Skill is supported by one verified historical repair. It is not a cross-project Pattern.

## Activation

Activate when current public code or a reproduction establishes all of the following:

- A special decorator recognizer resolves `ast.Name` nodes through a scope.
- Scope entries can include ordinary assignment bindings as well as import bindings.
- The recognizer accesses import-specific metadata, such as `fullName`, on a binding whose type has not been checked.
- Ordinary decorators must continue to receive ordinary repeated-definition diagnostics rather than being mistaken for the special decorator.

Clarify if the report only says that a release is broken, or if no public code or reproduction identifies the failing recognizer. Do not activate for unrelated decorator execution errors, missing imports, or a recognizer already proven to guard its metadata access correctly.

## Current probes and bindings

Start with [inspect the recognizer](references/actions/inspect.md). Locate these semantic owners in the current checkout:

- `special-decorator-recognizer`
- `scope-binding-types`
- `decorator-regression-tests`

Historical paths and symbol names in [the episode](references/episode.md) are evidence, not current bindings. Confirm the current binding model, evaluation order, diagnostic names, and test harness before editing.

Unknown prerequisites permit read-only probes only. A hard mismatch in language, binding semantics, or diagnostic expectations rejects this Workflow rather than authorizing an invented adapter.

## Operations

1. [Inspect binding and recognizer semantics](references/actions/inspect.md).
2. [Guard import-specific metadata access](references/actions/guard.md).
3. [Add the ordinary-decorator regression](references/actions/regression.md).
4. [Validate the guard and adjacent behavior](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) records historical dependencies. Current ordering is determined by the declared ports, current prerequisites, and validation closure, not merely by list position. Already satisfied operations may be omitted only when current public evidence establishes their effects and retains validation of any edits performed.

## Validation and stop conditions

Bind every validation oracle to a public current instruction, an argv command, and current evidence references before execution. Render those current commands in the task plan; historical evidence does not authorize a guessed command.

Check that:

- ordinary assignment-backed decorators are not mistaken for the special typing decorator;
- repeating a function definition three times with ordinary decorators yields two ordinary unused-redefinition diagnostics;
- supported import-backed special decorators still work;
- adjacent annotation/decorator tests remain passing.

After either edit, refresh stale validation observations. Structural compatibility is not proof of repair success. Stop on a failed public check, an unresolved binding-type distinction, or inability to preserve supported special-decorator behavior. Do not broaden the repair to every decorator form without new evidence.

## Limits and provenance

The historical regression is an assertion added at the repair commit, not a supplied historical execution log. The later qualification reports one fail-to-pass and thirteen pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer are untested.

See [evidence](references/episode.md#evidence), [provenance](references/provenance.json), and the unexecuted [functional definitions](evals/functional-cases.json). A current task plan is not newly verified historical knowledge and must not be published as such during formal evaluation.
