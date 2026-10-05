---
name: async-binding-dispatch
description: "Repair a binding-redefinition rule when a dispatched asynchronous context-manager statement reaches a match that handles only its synchronous counterpart; preserve existing loop and context-manager diagnostics."
---

# Async binding dispatch

## Activation

Activate when a public reproduction shows a binding-redefinition linter rule panicking on an asynchronous context-manager statement, and current code inspection confirms that the dispatcher admits that statement but the rule's statement match omits it.

Clarify or probe first when only “panic in an async function” is known. Async syntax alone does not establish this mechanism.

Do not activate for parser errors, runtime context-manager failures, unrelated rules, or an asynchronous variant already handled correctly. This is a single-repair Workflow, not a validated cross-project Pattern.

## Current binding and probes

Before proposing an edit, construct a public TaskContext containing the pinned base, hashed code anchors, issue reproduction, observed facts, and real bindings for these semantic owners:

- `binding-rule-dispatch`: the AST checker call sites that invoke the rule.
- `binding-redefinition-rule`: statement matching, binding extraction, body traversal, and diagnostic generation.
- `binding-rule-regressions`: the public rule fixtures and expected diagnostics.

Use [inspect dispatch](references/actions/inspect.md) to establish whether a dispatched asynchronous context-manager variant is missing from the rule's accepted statement variants. Inspect existing synchronous context-manager and synchronous/asynchronous loop handling as adjacent behavior.

Concrete Rust AST bindings are required for the implementation operation. A Python fixture is test input, not a Python implementation port. Do not invent an adapter to another AST representation.

## Operations

1. [Inspect dispatch and accepted variants](references/actions/inspect.md).
2. If current evidence establishes the mismatch, [align statement handling and regression assertions](references/actions/repair.md).
3. Retain [public validation](references/actions/validate.md) for every modification.

The [historical Workflow](references/workflow.md) records the source-specific mechanism and dependency closure. Current task ordering follows current ports, prerequisites, and semantic evidence, not list position alone.

The repair shares the existing context-manager binding extraction and body traversal between synchronous and asynchronous context-manager statements. It does not bypass the rule or swallow all unexpected statements. Where current callers already supply statements, narrow the rule entry point to statements and update callers consistently. Add both reused-name and distinct-name regression cases, retaining loop coverage.

## Validation and stopping

Bind each Action oracle to a public current instruction, argv array, and evidence references before execution. Record the semantic check key as `oracle:<action_id>:<source_oracle_id>`. Render those bound commands for review. Historical commands are evidence only; they do not authorize execution against a current checkout.

Run the public reproduction and the relevant repository rule tests. Require:

- no panic for the original no-binding asynchronous context-manager reproduction;
- a diagnostic at the inner reused binding;
- no diagnostic for the distinct-name control;
- retained synchronous context-manager, synchronous/asynchronous loop, assignment, unpacking, and scope-boundary behavior;
- a consistent statement-only signature and callers if that interface change is applied.

Disable automatic snapshot acceptance during verification. Review any expected-output edits semantically, rather than treating regenerated snapshots as proof.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only. A hard mechanism or binding mismatch rejects the edit plan. Stop if public validation fails, if a dispatched variant needs different semantics, or if preserving adjacent behavior requires an unsupported repair. Refresh stale validation observations after modifications.

Structural compatibility does not establish repair success. Obtain independent hidden acceptance only after the solver stops; hidden tests are not guidance. Do not publish current task plans as newly verified historical knowledge during formal evaluation.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and the [functional definitions](evals/functional-cases.json).

Historical regression assertions were available at the repair commit; historical CI/test execution is unknown. Later independent qualification supports one exact Rust library test, not whole-project correctness or transfer. The newly authored evaluation suites have not been executed.

For time-reconstructed training admission, exclude this source's own issue, fix, cluster, aliases, copied sources, and all discovery inputs unavailable before the query input time. Keep formal knowledge and checkpoints frozen.
