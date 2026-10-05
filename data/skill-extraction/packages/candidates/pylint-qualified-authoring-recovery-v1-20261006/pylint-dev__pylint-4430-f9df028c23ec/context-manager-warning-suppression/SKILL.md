---
name: context-manager-warning-suppression
description: "Repair false-positive resource-use advice in immediate Python context-manager implementation frames while preserving ordinary allocation and acquisition warnings."
---

# Context-manager warning suppression

## Activation

Activate when a Python static-analysis checker recommends using `with` for allocation or acquisition inside an immediate `__enter__` frame or a function whose decorator resolves to `contextlib.contextmanager`.

Clarify when the emitter, immediate frame, or decorator identity is unknown. Do not activate for missing-cleanup analysis, runtime leaks, global warning disabling, unrelated diagnostics, or async-only context managers.

This is a single-source Workflow, not a Pattern or evidence of cross-project transfer.

## Current probes

[Inspect the current owners](references/actions/inspect.md): the resource-advice emitter, immediate-frame API, resolved-decorator helper, and public diagnostic regression suite. Bind both allocation-assignment and replaceable-call emission paths. Historical paths in [the episode](references/episode.md) are discovery aids, not current bindings.

Maintain a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve owner aliases before conflict checks. Connected ports must agree on semantic role, artifact kind, language, scope, phase, and state.

Each current Oracle binding maps `action_id` and `source_oracle_id` to a public current instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty source commands require current binding; they do not authorize guessing historical commands.

Use PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject the modifying plan. A structural plan PASS predicts compatibility, not repair success.

## Operations

1. [Inspect and reproduce](references/actions/inspect.md).
2. [Edit the frame-local exclusion and public assertions](references/actions/edit.md).
3. [Validate suppression and preserved diagnostics](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records supported dependencies. Current ordering follows ports, prerequisites, and verification obligations. Already satisfied operations may be omitted only with current evidence; every retained edit retains explicit validation.

## Validation and stopping

Require silence for allocation and acquisition in both supported managed-frame forms, including qualified and imported contextmanager decorators. Retain ordinary-function and module-level allocation warnings, ordinary acquisition warnings, existing `with` silence, and safe inference and recognized-resource filters.

Run current public regressions and adjacent checker tests without expected-output update mode. Refresh stale observations after edits. An uninferable call does not demonstrate suppression.

Stop if the false positive does not reproduce, an owner cannot be bound, decorator resolution is unsupported, or the proposed exclusion broadens beyond the immediate-frame rule. Independent hidden acceptance occurs after the solver stops; this Skill does not claim it. Formal knowledge and checkpoints remain frozen during evaluation. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before its input time.

## Limits

The historical rule examines the immediate frame, not arbitrary ancestry. It recognizes the name `__enter__` without proving cleanup in `__exit__`. Missing-cleanup warnings, async context managers, helper-function ownership, arbitrary decorators, and interprocedural resource analysis are not established.

Historical tests are committed assertions; historical CI/test execution is unknown. Later independent qualification is validation-only: scope **changed-test-files-with-original-base-control**; limits **Changed test files only; whole-project regression and cross-project transfer are untested.** Newly authored evaluation definitions remain unexecuted.

See [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), [functional cases](evals/functional-cases.json), and evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [fix](references/evidence/fix.md), and [assertions](references/evidence/regression.md).
