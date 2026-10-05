---
name: comprehension-unused-name-guard
description: "Conditionally repair false unused-variable diagnostics for comprehension target homonyms when an existing target-name exclusion covers arguments but not the shared unused-name dispatch."
---

# Comprehension unused-name guard

## Activation

Activate when a Python static analyzer incorrectly reports an outer local container as unused even though it supplies the iterable of a comprehension with an identically named target, **and current code inspection confirms the supported dispatch mechanism**.

Representative public reproduction:

```python
def f():
    project_id = []
    assert (project_id > 0 for project_id in project_id)
```

The supported mechanism is an existing comprehension-target-name exclusion nested inside unused-argument handling, leaving the ordinary local-variable branch unprotected. Similar diagnostic wording alone does not establish applicability.

If the symptom is reported but the mechanism or owner is unknown, clarify the public reproduction and perform only the [probe](references/actions/probe.md). Do not activate for genuine unused locals, runtime assertion failures, undefined-name defects, or unrelated inference failures.

## Current probes and bindings

Pin the current public base and record hashed code anchors. Locate these semantic owners in the current checkout:

- unused-name dispatch;
- comprehension-target collection;
- diagnostic fixtures;
- diagnostic validation harness.

Historical paths in [the episode](references/episode.md) are evidence, not current bindings. Reproduce the diagnostic and inspect how target-name membership reaches both unused-name branches. Distinguish the outer iterable expression from the comprehension's target binding.

Build a current TaskContext containing the public issue, pinned base, anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings. Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only; contradictory evidence rejects this workflow.

Each current Oracle maps `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty contract commands require current binding; historical commands do not authorize execution.

## Operations

1. [Confirm the mechanism](references/actions/probe.md).
2. [Broaden the existing exclusion and maintain regression fixtures](references/actions/repair.md).
3. [Validate target and adjacent diagnostics](references/actions/validate.md).

Use the [Workflow contract](references/workflow.md). Ports must agree on semantic role, artifact kind, language, scope, phase, and state. Current ordering follows actual dependencies, not merely historical list order. Structural PASS establishes compatibility, not repair success.

## Validation and stop conditions

Compare pre-edit and post-edit public diagnostic output. Require no `unused-variable` for the homonymous outer iterable in generator and list-comprehension cases. Validate the annotation/comprehension expectation and preserve ordinary unused-local, unused-argument, undefined-name, and used-before-assignment diagnostics.

Do not prove correctness solely by removing expected messages. Inspect actual analyzer output. These are analyzer fixtures, not application runtime assertions.

Stop when the existing guard already covers both branches, target-set semantics differ, the reproduction cannot establish the mechanism, current commands remain unbound, or adjacent diagnostics regress. Refresh stale validation after any edit. Never globally disable unused-variable diagnostics or rename the homonym to evade the reproduction.

## Authority and limits

This is one focused historical Workflow, not a Pattern or cross-project template. See [evidence and qualification boundaries](references/episode.md) and [provenance](references/provenance.json).

Historical committed regression assertions are known; historical CI/test execution is unknown. Later independent qualification compared original base, base with committed regressions, and historical fixed code in a consistent runtime. Its scope is changed-test-files-with-original-base-control. Whole-project correctness and cross-project transfer are untested.

The later qualification does not execute the newly authored [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), or [functional](evals/functional-cases.json) suites. All remain `not_executed`.

Current plans are not newly verified historical knowledge. During formal evaluation, freeze knowledge and checkpoints, do not publish task-derived plans, and obtain independent hidden acceptance after the solver stops. Earlier-query admission excludes this source's own issue, fix, cluster, aliases, copied sources, and any source unavailable before the query time.
