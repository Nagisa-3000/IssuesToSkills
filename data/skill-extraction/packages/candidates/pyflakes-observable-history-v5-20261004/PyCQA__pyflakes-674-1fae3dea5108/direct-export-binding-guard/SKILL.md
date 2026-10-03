---
name: direct-export-binding-guard
description: "Prevent Python static-analysis crashes when a special export name occurs inside an unpacking target by restricting export-binding construction to supported direct assignment parents."
---

# Direct export-binding guard

## Activate conditionally

Use this Workflow when a Python static analyzer gives special treatment to a module-level export declaration, but an indirect target such as `(__all__,)` reaches code that expects an assignment statement with a value.

Strong activation signals are:
- An internal error involving an AST target without a `.value` attribute.
- Export-binding dispatch selected by identifier and scope without checking the immediate parent.
- A direct assignment works, while tuple/list unpacking of the same name crashes or incorrectly creates an export binding.

Do not activate merely because an export list contains an undefined name. Do not apply this guard to another language or unrelated AST representation without independently establishing its semantics.

## Current probes and operations

1. [Inspect dispatch and parent shape](references/actions/inspect.md). Locate the current binding dispatcher, specialized export-binding constructor, scope representation, parent links, and import-warning tests.
2. [Guard specialized construction](references/actions/guard.md), only if current inspection confirms the same structural assumption.
3. [Add the unpacking regression](references/actions/regression.md), adapted to the current public test harness.
4. [Validate both edits](references/actions/validate.md). Confirm non-crashing fallback behavior and preservation of direct export declarations.

The [historical Workflow](references/workflow.md) records the supported repair. The [episode](references/episode.md) separates the original report, merged implementation, regression assertion, and later qualification.

## Current binding and execution rules

No current checkout, pinned base, commands, or executed results are supplied here. Before editing, establish public code anchors and real bindings for the semantic owner roles. Record observed facts and PortValues; matching role names alone does not prove semantic compatibility.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit inspection, not edits. A hard mismatch in AST semantics or fallback behavior rejects this Workflow.

Bind each historical oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render and execute those bound commands; historical commands in the evidence do not authorize execution in a different checkout. Refresh observations invalidated by either edit. Structural compatibility is not evidence of repair success.

## Validation and stop conditions

The unpacking regression must complete without an internal error and retain the unused-import warning. Supported direct module-level assignments must still receive export processing, including warning suppression for legitimately exported imports.

Stop if:
- The immediate parent is not a reliable representation of direct assignment.
- The current constructor supports different parent shapes.
- Generic binding fallback changes name resolution unexpectedly.
- The regression or adjacent direct-assignment checks fail.

Do not infer that the historical repair emits a new “invalid assignment” diagnostic. It avoids specialized export processing for indirect targets.

## Scope and authority

This is one historically supported Workflow, not a cross-project Pattern. The supplied later qualification covers changed test files only: one fail-to-pass case and 131 pass-to-pass cases. Whole-project regression and cross-project transfer remain untested. Historical tests are supplied assertions, not an independently documented historical test run. Eval definitions in this bundle are not executed.

[Provenance](references/provenance.json) preserves the authoritative source and cutoff. During formal evaluation, keep knowledge frozen and do not publish a current task plan as historical knowledge. Independent hidden acceptance, if available, occurs after the solver stops.
