---
name: exception-return-path-completeness
description: "Conditionally repair a Python return-consistency analyzer that overlooks exception-handler fallthrough despite a value-returning try body, preserving explicit-None and adjacent control-flow behavior."
---

# Exception return-path completeness

## Activation and exclusions

Activate for a missing static return-consistency diagnostic when a function returns an expression in a `try` body but a handled exception path falls through implicitly:

```python
def example(obj):
    try:
        return obj.attribute
    except AttributeError:
        pass
```

Clarify when the public reproduction, diagnostic policy, analyzer owner, or AST representation is unknown. Do not activate merely because code contains exception handling.

Exclude application runtime-policy changes, return-type inference, and unrelated diagnostic suppression. This history does not establish correctness for `finally`, generators, asynchronous functions, or newer exception constructs. An incompatible AST requires separate evidence, not mechanical translation of historical class names.

## Current probes

Build a public TaskContext with the issue, pinned base, hashed code anchors, actual semantic-owner bindings, observed facts, semantic checks, observed PortValues, and current Oracle bindings.

Locate the return-completeness analyzer and public regression harness. Observe:

- Diagnostics for handler fallthrough and both explicit-`None` forms.
- Current `try` and handler child structure.
- Existing conditional, nested-function, and raise behavior.
- Whether ignored handlers or overly permissive aggregation explain the missing warning.

Use PASS/FAIL/UNKNOWN. UNKNOWN prerequisites authorize probes only; hard applicability failures reject the repair. Matching names are not proof of matching semantics.

## Operations

1. [Probe and bind](references/actions/probe.md).
2. [Repair aggregation and assertions](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [Workflow](references/workflow.md) specifies dependencies. Current ordering follows ports, prerequisites, semantic evidence, and validation—not historical list position. Already-observed or inapplicable operations may be omitted from a current task DAG, but every edit retains its validation closure.

## Validation and stopping

Require a warning for the single fallthrough-handler case and the mixed-handler variant. Require no warning when `return None` occurs inside the handler or after the `try/except`. Preserve retained conditional, nested-function, and raise expectations. Any internal explicit-`None` adjustments must preserve existing runtime results.

Each current Oracle maps `action_id/source_oracle_id` to a public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution; historical paths and empty source commands do not authorize current execution.

Stop if the defect cannot be reproduced, AST compatibility fails, explicit-`None` negatives become false positives, adjacent expectations regress, or public validation is unavailable or unresolved. Refresh observations made stale by edits. Structural PASS predicts compatibility, not repair success. Obtain independent hidden acceptance only after the solver stops.

## Evidence and limits

This is one historical Workflow, not a Pattern or transfer guarantee. Read the [episode](references/episode.md), [provenance](references/provenance.json), and evidence cards: [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. The supplied 2026 three-control qualification is validation-only: changed-test-file coverage with original-base control, not whole-project regression or cross-project transfer. It did not execute this Skill's functional cases.

[Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`. Do not publish a current task plan as newly verified historical knowledge during formal evaluation. Frozen, time-reconstructed catalogs must exclude own issue/fix/cluster/aliases/copied sources and all discovery sources unavailable before query time.
