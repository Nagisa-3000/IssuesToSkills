---
name: postponed-annotation-member-check
description: "Conditionally suppress missing-member diagnostics inside postponed Python type annotations while preserving diagnostics for ordinary runtime member access."
---

# Postponed annotation member checks

Canonical Skill and Workflow ID: `workflow:verified-history:0c9590e0dcadfaf12ae0182b`.

This focused Workflow is supported by one historical repair. It is not a cross-project Pattern.

## Activation

Activate when a Python analyzer reports a missing-member diagnostic on an attribute inside a type annotation and the module enables `from __future__ import annotations`.

Clarify when the public reproduction, annotation context, future import, or interpreter context is unavailable. A missing member alone does not establish this mechanism.

Do not activate for ordinary runtime member access, eagerly evaluated annotations, unrelated inference failures, or requests to disable missing-member checking globally.

## Current probes and applicability

Use the [inspection Action](references/actions/probe.md) to locate current semantic owners:

- missing-member attribute visitor;
- postponed-evaluation detector;
- annotation-context detector;
- public member-diagnostic regression suite.

Historical paths in the [episode](references/episode.md) and evidence are not current bindings. Inspect actual helper semantics: similar names do not establish that they classify the reported expression correctly.

Construct a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before checking read/write conflicts.

UNKNOWN prerequisites authorize probes only. Hard mechanism failures reject the plan. If an equivalent guard is already effective, investigate another mechanism rather than adding a duplicate.

## Operations

The [Workflow](references/workflow.md) retains these operations:

1. [Inspect the annotation boundary](references/actions/probe.md).
2. [Add the conjunctive guard and public controls](references/actions/edit.md).
3. [Validate target suppression and adjacent diagnostics](references/actions/validate.md).

Current ordering follows ports, prerequisites, and verification dependencies rather than historical list position. Already satisfied operations may be omitted only with current evidence. Every modification retains its explicit validation Action.

## Validation

Bind every oracle to a public current instruction, argv command, and evidence references. Render the bound commands before execution. Record tri-state checks as `oracle:<action_id>:<source_oracle_id>` with PASS, FAIL, or UNKNOWN. Empty source commands require current binding; historical commands do not authorize execution.

Observe actual diagnostics:

- quoted and unquoted postponed annotations receive no missing-member diagnostic;
- ordinary runtime access to the absent member still receives that diagnostic;
- existing generated-member controls remain satisfied.

Refresh stale validation observations after editing. Structural PASS predicts compatibility, not repair success.

Stop if owner semantics remain unresolved, an oracle cannot be bound, or a public control fails. Do not conceal failure by changing expected diagnostics. Independent hidden acceptance occurs after the solver stops; hidden checks never become guidance.

## Evidence, scope, and limits

Read the [episode and validation-only audit](references/episode.md), [implementation evidence](references/evidence/fix.md), [regression evidence](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical tests are committed assertions; original historical CI/test execution is unknown. Later independent qualification supports the historical repair within `changed-test-files-with-original-base-control`.

Exact qualification limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

That qualification did not execute this newly authored Skill. Other languages, other analyzers, broad annotation-diagnostic suppression, and whole-project correctness are unsupported.

Evaluation definitions remain unexecuted:
[activation](evals/activation-cases.json),
[applicability](evals/applicability-cases.json), and
[functional](evals/functional-cases.json).

During formal evaluation, freeze knowledge and checkpoints. Time-reconstructed catalogs exclude the task's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time. A current task plan is not newly verified historical knowledge.
