---
name: bound-method-termination-recognition
description: "Repair return-consistency false positives caused by excluding inferred bound methods from existing NoReturn annotation recognition."
---

# Bound-method termination recognition

## Activation and exclusions

Activate when current public evidence shows all of the following:

- A Python return-consistency diagnostic occurs on a function whose apparent fallthrough path calls a method annotated `NoReturn`.
- Callable inference produces a bound-method representation.
- That representation exposes the return annotation, but the termination recognizer excludes it through a function-definition-only guard.

Clarify or probe if the annotation, inferred representation, owning recognizer, or diagnostic is unknown. Unknown prerequisites authorize inspection, not editing.

Do not activate for genuinely reachable fallthrough after an ordinary returning method. This Workflow does not establish support for arbitrary callable wrappers, other bottom types, new annotation-resolution rules, or cross-project transfer.

## Current evidence and bindings

Locate these semantic owners in the current checkout:

- `return-termination-recognizer`: the helper recognizing non-returning inferred callables.
- `return-consistency-regression-suite`: fixtures and expected diagnostics exercising return consistency.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Historical paths in [the episode](references/episode.md) are evidence, not current bindings.

First reproduce the diagnostic and inspect inference, annotation access, and the accepted-kind guard. Confirm existing function-definition annotation recognition before modifying it.

## Operations

Use the complete [Workflow](references/workflow.md):

1. [Probe the callable-kind mismatch](references/actions/probe.md).
2. [Extend the guard and add regression contrasts](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

Keep the change narrow: admit the supported bound-method kind alongside function definitions, without changing annotation interpretation or suppressing the diagnostic globally.

## Validation and stopping

Bind each source Oracle to a current public instruction, argv command, and evidence references; render those commands before execution. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Historical commands do not authorize current execution.

Required observations:

- The truthful `NoReturn` method caller no longer receives the return-consistency warning.
- The ordinary returning method caller still receives it.
- The incorrectly annotated `NoReturn` method caller remains treated as non-returning by this check.
- Existing function-definition recognition and adjacent return-consistency expectations remain intact.

Checks are PASS, FAIL, or UNKNOWN. A hard prerequisite failure rejects the plan; missing evidence permits probes only. Structural PASS predicts compatibility, not repair success. After an edit, refresh stale observations and run public validation.

Stop if annotation access is incompatible, inference is ambiguous, the guard already accepts the wrapper, or preservation checks fail. Do not invent a bridge or broaden callable support.

Formal knowledge and checkpoints remain frozen. Do not publish a current task plan as newly verified historical knowledge during formal evaluation. Independent hidden acceptance, when required, occurs after the solver stops. Earlier-query catalogs must exclude the task's own issue, fix, cluster, aliases, copied sources, and any discovery source unavailable before query time.

## Evidence and limits

This is a single-source Workflow, not a Pattern. See [episode and evidence index](references/episode.md), [provenance](references/provenance.json), and the unexecuted [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions.

Historical CI/test execution is unknown. Later independent qualification establishes only the supplied scope: `changed-test-files-with-original-base-control`.

Scope limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

That qualification did not execute this newly authored Skill.
