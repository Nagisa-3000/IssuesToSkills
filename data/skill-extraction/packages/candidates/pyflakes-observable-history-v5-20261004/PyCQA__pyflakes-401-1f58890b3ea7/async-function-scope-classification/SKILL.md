---
name: async-function-scope-classification
description: "Repair missing asynchronous-function scope classification in a Python AST checker when annotated async parameters cause scope lookup to ascend past the function boundary."
---

# Asynchronous function scope classification

## Activation and exclusions

Activate when current public evidence establishes both:
- A Python AST checker fails while binding an annotated asynchronous function parameter, potentially ending with `AttributeError: 'Module' object has no attribute 'parent'`.
- The scope lookup's node-to-scope classification omits asynchronous function definitions, although ordinary function definitions have an established function-scope representation.

The exception alone is insufficient. Clarify or probe when the reproduction, classifier owner, or supported-runtime policy is unknown. Do not activate for parser rejection of async syntax, unrelated missing parent links, an already correct async classification, or an incompatible AST model.

## Current probes

Use [inspect](references/actions/inspect.md) to locate the current semantic owners:
- Python AST scope classifier and ordinary function-scope representation.
- Runtime capability policy for asynchronous-function AST classes.
- Annotation regression test harness.

Trace the public reproduction through argument binding and scope lookup. Establish that the missing async classification explains the ascent beyond the function boundary. Determine the registry's actual value shape; do not assume the historical assignment syntax fits the current checkout.

Record a current TaskContext with public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Historical paths in [the episode](references/episode.md) are evidence, not current bindings.

## Operations

Follow the conditional [workflow](references/workflow.md):

1. [Inspect and diagnose](references/actions/inspect.md).
2. [Register async function scope and add the regression](references/actions/repair.md).
3. [Validate the repair and preserved behavior](references/actions/validate.md).

Classify asynchronous definitions using the ordinary function-scope representation, protecting access to AST classes unavailable on supported older runtimes. Add a no-diagnostic regression with a class name reused as an async parameter annotation and a `None` return annotation.

Do not mask the exception, invent a module parent, or alter unrelated scope entries. Preserve ordinary function classification, surrounding annotation tests, and compatibility behavior.

## Validation and stop conditions

Contracts describe required results, not observed success. Bind each source oracle to current public instructions, argv commands, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty commands in these cards are unbound obligations, not executable guidance.

Use PASS/FAIL/UNKNOWN. Unknown prerequisites permit probes only; a failed mechanism check rejects the repair. Refresh invalidated observations after editing. Execute the explicit validation Action, including the public reproduction and surrounding annotation tests. Report unavailable runtime coverage as UNKNOWN.

Stop if the missing-entry mechanism is absent, owners cannot be bound, or compatibility policy cannot be established safely. A structurally compatible plan predicts compatibility, not repair success. Current task DAGs may omit already satisfied operations only when current evidence and verification obligations remain intact.

## Evidence and limits

This is a single historical Workflow, not a Pattern or cross-project template. See [the episode](references/episode.md), [provenance](references/provenance.json), and the unexecuted [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites.

The supplied historical test is an assertion available at the merged commit; historical execution logs were not supplied. Contemporary qualification reports one fail-to-pass and eleven pass-to-pass cases in changed test files with original-base control only. Whole-project regression and cross-project transfer are untested. That qualification is provenance, not backdated historical knowledge.

During formal evaluation, freeze knowledge and checkpoints; do not publish a current task plan as newly verified historical knowledge. Time-reconstructed training catalogs exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. After the solver stops, obtain independent hidden acceptance without importing hidden tests or gold-derived commands into this guidance.
