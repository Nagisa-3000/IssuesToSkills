---
name: quoted-type-context
description: "Repair false unused-import diagnostics when quoted type expressions occur in recognized typing casts or typing subscriptions, while preserving ordinary string and Literal behavior."
---

# Quoted type context

Use this Workflow when a Python static analyzer fails to recognize names inside quoted type expressions in recognized typing constructs. The historical example was a false unused-import warning for `Union` in `cast('Union[str, int]', 42)`.

This is a conditional repair procedure, not a claim that any current checkout needs the historical patch.

## Activation

Activate when public evidence shows either:

- A quoted first argument of a recognized typing `cast` fails to count referenced names as used.
- A partially quoted type expression inside a recognized typing subscription fails to count referenced names as used.

Clarify when only an unused-import diagnostic is supplied, without the triggering expression or current analyzer implementation.

Do not activate for arbitrary strings, unrelated unused imports, non-Python analysis, or a request to interpret every string as a type. Arbitrary module aliases and broader annotation syntax are not established by this episode.

## Current probes and binding

1. Pin the public base and inspect the reproduction.
2. Locate the current semantic owner of typing-name recognition, call/subscript traversal, string annotation handling, and annotation-context state.
3. Record hashed code anchors and real role bindings. Historical paths are reference material, not current bindings.
4. Observe whether the diagnostic reproduces and whether quoted annotation handling already exists.
5. Check import provenance, shadowing, nested context restoration, and the existing `Literal` branch.

Use the [inspection Action](references/actions/inspect.md), then conditionally the [repair Action](references/actions/repair.md), then the [validation Action](references/actions/validate.md). The [canonical Workflow](references/workflow.md) records their dependencies.

Unknown prerequisites permit inspection only. A hard mismatch—such as no compatible Python annotation traversal—rejects this repair plan. If behavior is already correct, do not edit merely to resemble historical code.

## Repair boundary

Recognize supported typing members using the analyzer's import bindings. Enter annotation context for typing subscriptions, without displacing special `Literal` handling. For `cast`, specially process only a quoted first positional argument; continue ordinary traversal of the rest of the call.

Restore annotation state even on exceptions. Preserve ordinary string values, including `cast(str, 'Optional[int]')`, and preserve genuine undefined-name diagnostics.

## Validation and stopping

Bind each source oracle to a current public instruction and argv command before execution. Render those bound commands; historical commands do not authorize current execution. Record PASS, FAIL, or UNKNOWN under `oracle:<action_id>:<source_oracle_id>`. Run the public reproduction, targeted regression cases, and available adjacent tests; refresh stale observations after edits.

Stop if the false warning remains, ordinary strings become annotations, `Literal` behavior changes, shadowed names are misclassified, or context leaks into later traversal. Report failures and unknown coverage rather than claiming completion.

A structurally compatible plan predicts applicability, not repair success. Current execution results must be recorded separately from this frozen Skill. Formal evaluation requires independent hidden acceptance after the solver stops; never use hidden tests or gold-derived commands as repair guidance.

## Evidence and limits

See the [episode](references/episode.md), [original report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

This package has one verified historical repair and supports a Workflow, not a multi-episode Pattern. Historical tests are assertions present at the repair commit; supplied evidence does not establish a historical test execution. A later qualification reports four fail-to-pass and 31 pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer remain untested. That qualification is a later provenance attestation, not pre-cutoff learned content.

The [evaluation definitions](evals/functional-cases.json) are not executed results.
