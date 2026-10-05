---
name: filtered-comprehension-scope-guard
description: "Repair a Python static-analysis false positive when a filtered comprehension's local target is confused with a same-named assignment in an enclosing exception handler."
---

# Filtered comprehension scope guard

## Activate conditionally

Use this Workflow when a Python variable checker reports a comprehension-local name as used before assignment, and public inspection shows that a same-named enclosing-function assignment is influencing a comprehension-homonym branch.

The supported historical case is a generator expression inside a `try`, with a filter referring to its own iteration target and an assignment to the same spelling in an `except` block.

- **Activate:** the public reproduction and current AST inspection identify this filter/homonym interaction.
- **Clarify or probe:** the diagnostic matches, but the responsible scope branch or filter AST shape is unknown.
- **Do not activate:** the name genuinely lacks a local binding, the diagnostic comes from another mechanism, or the implementation is not a compatible Python variable checker.

This is one historical Workflow, not a cross-project Pattern. Similar wording alone does not establish applicability.

## Current probes and bindings

Start with [locate the scope interaction](references/actions/locate.md). Locate the current semantic owners rather than assuming historical file paths:

1. Variable-use dispatch and its comprehension/enclosing-function homonym condition.
2. The AST representation of the reported filter name.
3. Public functional-test registration and diagnostic assertions.

Record the public issue, pinned checkout, hashed code anchors, actual owner bindings, observed facts, PortValues and semantic checks in a current TaskContext. Check whether the name's immediate parent is a filter expression whose parent is a comprehension and whether that expression belongs to the comprehension's filter list. The historical guard supported exactly that structural test; it did not implement an arbitrary ancestor search.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites authorize probes only. A hard mismatch rejects the editing plan.

## Operations

- [Locate](references/actions/locate.md): reproduce and inspect without changing code.
- [Repair](references/actions/repair.md): exclude the supported filter shape from the enclosing-function homonym condition, retaining the surrounding dispatch.
- [Regression](references/actions/regression.md): add a public assertion for the generator/filter/exception-handler collision.
- [Validate](references/actions/validate.md): validate both modifications and adjacent variable-checker behavior.

The [historical Workflow](references/workflow.md) records the supported mechanism and dependencies. Its Actions are author-authored operational contracts, not a claim that those operations were historically executed in this exact order.

## Validation and stopping

Before execution, bind each Action oracle to a current public instruction, an argv command and evidence references. Render those commands for the user. Record the semantic check under `oracle:<action_id>:<source_oracle_id>`. Historical commands are reference data, not current execution authorization.

Confirm that the target reproduction emits no `used-before-assignment`, that the new functional assertion is actually collected, and that relevant existing variable-analysis tests retain their expected diagnostics. Check that the edit does not disable homonym handling generally or bypass the existing late-binding/loop-variable checks.

Edits stale earlier validation observations. Refresh them after all modifications. Structural plan PASS predicts compatibility, not repair success. Stop on failed public validation, incompatible AST ownership, unsupported filter nesting, or unrelated changes required to make the patch work. During formal evaluation, freeze knowledge and checkpoints; do not publish a current task plan as newly verified historical knowledge. Independent hidden acceptance follows only after the solver stops.

## Evidence and limits

See [episode](references/episode.md), [evidence cards](references/evidence/title.md), and [provenance](references/provenance.json).

Historical regression assertions were available at the repair commit; historical CI/test execution is **unknown**. A supplied independent replay in 2026 qualifies the historical repair with original-base controls: one added regression changed from failure to pass and 22 selected existing cases remained passing. This is changed-test-files-with-original-base-control qualification, not whole-project correctness or cross-project transfer.

All [evaluation definitions](evals/functional-cases.json) remain **not_executed**. Source qualification did not execute this newly authored Skill.
