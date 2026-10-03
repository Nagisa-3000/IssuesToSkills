---
name: explicit-load-parent-context
description: "Repair an AST analyzer when augmented-assignment load analysis runs before target parent metadata exists, by passing known parent context explicitly and preserving ordinary load diagnostics."
---

# Explicit parent context for early load analysis

## Activation

Activate when a Python AST analyzer crashes while analyzing an augmented-assignment target as a load, and the load handler tries to recover parent context from metadata that has not yet been initialized.

A strong symptom is an `AttributeError` for missing parent metadata on a target `Name`, especially when analyzing a builtin name such as `print`. The historical examples were `print *= -1` and `print += 1`; these are diagnostic probes, not code to execute.

Clarify when there is only a generic AST traversal crash and the failing context lookup or initialization order is unknown. Do not activate for parser rejection, unrelated binding errors, or a traversal whose parent metadata is already established before load handling.

## Current probes and operations

1. [Inspect the load-context dependency](references/actions/inspect.md). Locate the semantic owners in the current checkout: name-load dispatch, augmented-assignment dispatch, parent-context lookup, and diagnostic regression tests. Establish whether the augmented-assignment target is analyzed before ordinary node traversal initializes its metadata.
2. [Pass context explicitly and add a regression](references/actions/repair.md). Change the load handler and its callers together. Ordinary name loads supply their established parent; augmented assignment supplies its owning statement. Preserve existing analysis order and builtin-print diagnostic logic.
3. [Validate the repair](references/actions/validate.md). Run current public regression checks and adjacent diagnostic tests using commands bound to the current checkout.

The [historical Workflow](references/workflow.md) records the dependency structure. The [episode](references/episode.md), [evidence cards](references/evidence/report.md), and [provenance](references/provenance.json) distinguish supplied historical observations from proposed current operations.

## Validation and stopping

Before modifying code, obtain current evidence that this initialization-order failure is present. Unknown prerequisites authorize inspection only. Stop if the load handler has other callers whose context requirements cannot be established, or if passing an immediate AST parent changes a diagnostic that depends on a different enclosing context.

After modification, verify that both reported augmented-assignment examples can be analyzed without an internal exception, that the added regression passes, and that existing incompatible-print and valid-assignment tests retain their behavior. Analyze source strings; do not execute the example programs.

Current TaskContext bindings must identify public code anchors, observed facts, matching PortValues, and current oracle commands. Render and run those bound commands rather than treating historical paths or commands as current authority. Treat checks as PASS, FAIL, or UNKNOWN; structural compatibility does not establish repair success.

## Limits

This is one historically supported Workflow, not a cross-project Pattern. It does not prescribe a general AST traversal rewrite or promise compatibility with arbitrary parent-context abstractions.

The historical regression is an assertion available at the repair commit, not evidence of a historical test execution. A later qualification reported one fail-to-pass and 126 pass-to-pass results within changed test files only. Whole-project regression and cross-project transfer were not tested. The packaged eval suites are definitions and remain `not_executed`.
