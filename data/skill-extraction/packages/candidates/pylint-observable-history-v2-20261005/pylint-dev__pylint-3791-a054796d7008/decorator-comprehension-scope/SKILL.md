---
name: decorator-comprehension-scope
description: "Correct false undefined-name diagnostics for decorator-local comprehension bindings that share a decorated function parameter name, while preserving genuine undefined-name errors and non-decorator scope protections."
---

# Decorator comprehension scope

## When to activate

Use this conditional Workflow for a Python static name checker when public evidence shows:

- A generator expression in a function decorator binds an iteration variable.
- That name also occurs as a parameter of the decorated function.
- The checker incorrectly reports the bound generator variable as undefined.
- Changing only the function parameter name removes the false diagnostic.
- Current code has a consumed-name lookup and an exception for comprehension names with upper-function homonyms.

The historically demonstrated forms are generator expressions. Do not assume other comprehension forms are affected without current public probes.

Clarify or probe when the reproduction, scope classification, or current owner is unknown. Do not activate for genuinely unbound decorator names, ordinary function-body comprehensions, or a superficially similar diagnostic with a different mechanism.

This is a single-repair Workflow, not a Pattern or a verified cross-project abstraction.

## Current context and probes

Before editing, establish a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners:

- `name-resolution-checker`: consumed-name resolution and its comprehension/homonym guard.
- `decorator-context-classifier`: classification of the actual consumer node as function-decorator context.
- `scope-regression-suite`: public diagnostic fixtures and expected results.

Historical paths belong to the [episode](references/episode.md), not current bindings. Resolve current aliases before read/write conflict checks. Existence of a similarly named symbol is not proof of compatible semantics.

Each current Oracle must map `action_id` and `source_oracle_id` to a public instruction, current argv, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before executing them; empty source command arrays are not executable bindings.

## Operations

1. [Probe and bind the mechanism](references/actions/probe.md).
2. [Repair the guard and add regression assertions](references/actions/repair.md).
3. [Validate the diagnostic boundaries](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records the supported mechanism and dependencies. It is not an automatically authorized current task plan. Omit an operation only when its prerequisites and outputs are already observed in the current context. Match ports on all semantic dimensions.

## Validation and stop conditions

Accept both `x for x in range(3)` and `x * x for x in range(3)` in a decorator on a function with parameter `x`. Still diagnose:

- An unbound `x` passed directly to a separate decorator.
- An unbound `y` used in the generator body.

Retain the consumed-name requirement, non-decorator homonym protection, assignment-parent resolution, and downstream late-binding checking. Run the applicable public fixture suite and neighboring scope checks. Refresh validation observations after edits.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject the plan. Stop without claiming repair success if the mechanism differs, classifier semantics cannot be justified, negative controls disappear, or adjacent checks regress. Structural plan PASS predicts compatibility, not repair success. Incomplete validation remains UNKNOWN.

Obtain independent hidden acceptance after the solver stops. Hidden tests and gold-derived commands must not enter guidance. Do not publish current task plans as newly verified historical knowledge during formal evaluation.

## Evidence and limits

The [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md) support this Workflow. [Provenance](references/provenance.json) identifies the exact repair.

Historical CI/test execution is unknown. The later independent qualification has changed-test-only scope with original-base controls; whole-project regression and cross-project transfer are untested. Its inspection is recorded separately within the [episode](references/episode.md#validation-only-qualification-audit), not as historical mechanism evidence.

All [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) evaluations are definitions and remain unexecuted.

Keep formal knowledge and checkpoints frozen. Time-reconstructed training admission must exclude the query's own issue, fix, cluster, aliases, copied sources, and every discovery input unavailable before the query time.
