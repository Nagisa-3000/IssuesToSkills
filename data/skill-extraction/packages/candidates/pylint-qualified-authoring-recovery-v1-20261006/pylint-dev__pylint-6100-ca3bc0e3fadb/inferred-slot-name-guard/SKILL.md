---
name: inferred-slot-name-guard
description: "Repair a Python static-analysis slot-name collector that crashes when inference yields a node without a string value, while preserving valid inherited-slot diagnostics."
---

# Guard inferred slot names

## Activation

Use this workflow when a Python static analyzer collects `__slots__` names for inherited-slot comparison and a nonliteral slot expression can infer to an object without a usable string-valued `value` attribute.

Strong activation evidence is:
- A public reproduction such as `class Example: __slots__ = [str]`.
- A traceback from inferred slot-name collection showing an unguarded `.value` access.
- Current code confirming that inference success is mistaken for proof that the result carries a string slot name.

The identity is semantic, not repository-specific. This package is nevertheless supported by **one historical repair only**; transfer to another implementation requires current inspection and testing.

## Exclusions and clarification

Do not activate for ordinary invalid-slot diagnostics without a collector crash, or for unrelated attribute-access failures. Clarify when a traceback or collector binding is missing. Do not broaden this repair into changes to inference semantics, runtime slot validity, or all constant-handling branches.

A nonstring slot is not made valid by this workflow. Invalid-slot diagnostics remain the responsibility of their existing owner.

## Current probes and bindings

Start with [Inspect the collector](references/actions/inspect.md). Locate these semantic owners in the current pinned checkout:
- `slot-name-collector`: the inferred-name collection branch used by inherited-slot comparison.
- `slot-regression-suite`: public tests covering invalid inferred slot objects and valid inherited-slot comparisons.

Record the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, and observed port values in the current TaskContext. Bind each source oracle to a current public instruction, argv command, and evidence references. Render those bound commands before execution; historical commands are context, not automatic execution authority.

Unknown prerequisites authorize inspection only. A failed mechanism match rejects the editing plan.

## Operations

1. [Inspect the collector](references/actions/inspect.md): confirm the failing inferred branch and the adjacent string-name behavior.
2. [Guard and add regression coverage](references/actions/guard.md): use safe attribute extraction and append only string-valued inferred names; add a public no-crash fixture.
3. [Validate the change](references/actions/validate.md): run the bound public reproduction and focused regression tests, checking preserved inherited-slot diagnostics.

The [historical workflow](references/workflow.md) defines source-backed dependencies. Current ordering follows satisfied prerequisites and port compatibility, not merely list order.

## Validation and stopping

Accept the local repair only after current public checks demonstrate:
- The nonliteral slot reproduction produces no analyzer fatal error.
- Missing or nonstring inferred values are not appended as slot names.
- Valid inferred string names still participate in inherited-slot comparison.
- Existing duplicate-slot diagnostics and nonduplicate cases remain correct.

After edits, refresh stale observations. Structural compatibility does not prove repair success. Stop on unresolved bindings, unknown validation results, unrelated failures that prevent interpretation, or a need to change inference or diagnostics outside this repair's scope. Do not suppress broad diagnostics to obtain a passing test.

Formal evaluation knowledge and checkpoints remain frozen; do not publish a current task plan as historical knowledge. Independent hidden acceptance, if required, occurs after the solver stops.

## Evidence and limits

See the [episode](references/episode.md), [source provenance](references/provenance.json), and [evidence cards](references/evidence/fix.md). Historical regression assertions are known; historical CI execution is unknown. Later qualification supports the supplied repair only within `changed-test-files-with-original-base-control`. **Changed test files only; whole-project regression and cross-project transfer are untested.**

The authored evaluation suites are definitions and remain `not_executed`:
[activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json).
