---
name: signature-opacity-delegation
description: "Repair false-positive useless-delegation diagnostics when inherited builtin argument metadata is unavailable and an override has arguments beyond self."
---

# Signature-opacity delegation

A conditional Workflow Skill grounded in one verified historical repair.

## Activation and exclusions

Activate when a Python static analyzer reports useless delegation on an override forwarding to an inherited builtin or C-implemented method, and current probes establish that:

- the inherited argument list cannot be inspected;
- the override's argument names differ from `["self"]`; and
- the warning is a public, reproducible false positive.

An exception constructor introducing a default message is the historical example. Identify the diagnostic by behavior rather than version-specific spelling.

Do not activate for runtime constructor errors, unrelated inference failures, ordinary forwarding with an inspectable parent signature, or a self-only override. Do not suppress all builtin delegation warnings. Missing metadata is not a known empty argument list. An unfamiliar metadata representation requires semantic inspection before editing.

## Current probes and bindings

Build a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners:

- `delegation-diagnostic-owner`: the checker decision that determines whether an override merely delegates.
- `delegation-regression-owner`: public tests and expectations for that decision.

Use the [inspection Action](references/actions/inspect.md) to reproduce the warning and inspect inherited and overriding argument representations. Unknown prerequisites authorize probes only; hard applicability failures reject the repair plan.

Bind every source Oracle by `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Record the semantic check key `oracle:<action_id>:<source_oracle_id>` and render bound commands before executing them. Empty source command arrays require binding; historical commands are not authorization to execute in the current checkout.

## Operations

1. [Inspect the diagnostic and signature opacity](references/actions/inspect.md).
2. [Add the narrow guard and public regression](references/actions/repair.md).
3. [Validate the target and adjacent behavior](references/actions/validate.md).

The [Workflow](references/workflow.md) records dependencies. Current plans may omit work already satisfied by fresh observations, but every modification retains its validate Action. Ports must match semantic role, artifact kind, language, scope, phase, and state; similar names alone do not establish compatibility.

## Validation and stopping

Require fresh public checks showing no useless-delegation warning on the default-message exception constructor. Preserve existing inspectable-signature comparisons and genuine-delegation expectations. Confirm the added guard does not apply when override argument names are exactly `["self"]`; this does not imply every self-only wrapper must warn.

Stop and reassess if parent resolution is insufficient, absent metadata has different semantics, the reproduction remains incorrect, adjacent expectations change, or required validation is FAIL or UNKNOWN.

Edits invalidate observation freshness, not behavior-preservation obligations. Refresh stale checks after every edit. Structural PASS predicts plan compatibility, not repair success. Obtain independent hidden acceptance after the solver stops; hidden tests and gold-derived commands must not enter guidance.

## Evidence and limits

See the [episode and qualification audit](references/episode.md), [historical evidence](references/evidence/fix.md), and [provenance](references/provenance.json). Historical regression assertions were committed, but historical CI/test execution is unknown.

Contemporary source qualification has scope **changed-test-files-with-original-base-control**. Its exact limits are: **Changed test files only; whole-project regression and cross-project transfer are untested.** It does not execute this newly authored Skill.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`.

Formal knowledge and checkpoints stay frozen during evaluation. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and discovery inputs not available before query time.
