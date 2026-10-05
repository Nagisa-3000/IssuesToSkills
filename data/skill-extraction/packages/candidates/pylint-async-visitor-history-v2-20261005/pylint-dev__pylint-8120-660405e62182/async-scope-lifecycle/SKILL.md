---
name: async-scope-lifecycle
description: "Restore scope lifecycle parity in Python AST checkers when missing asynchronous function entry and exit hooks cause assignment-type state to leak between independent scopes."
---

# Async scope lifecycle parity

## Activation and exclusions

Activate when a Python AST assignment-type checker reports a type redefinition between **different async function scopes**, equivalent synchronous functions remain isolated, and current inspection confirms missing or inequivalent async scope lifecycle registrations.

- **Activate:** unrelated types assigned to the same local name in separate async functions or methods trigger a cross-scope warning, and the checker omits the corresponding async lifecycle hooks.
- **Clarify/probe:** the symptom exists, but dispatch, state ownership, or synchronous behavior is unknown.
- **Do not activate:** assignments occur within one scope, async lifecycle parity already exists, or a different inference mechanism explains the warning.

This is a conditional workflow supported by one historical repair, not a general rule that async diagnostics are false positives.

## Current probes and bindings

Pin the public current base and record hashed code anchors. Locate the assignment-type checker, visitor dispatcher, scope-state stack, regression fixture, and public test entry point by semantic role. Historical paths are recorded only in [the episode](references/episode.md).

Use [inspection](references/actions/inspect.md) to compare synchronous and asynchronous entry and exit behavior. Run public examples with separate async functions and methods reusing a local name with different types, plus synchronous equivalents. Confirm whether assignment state leaks into the enclosing scope.

A current TaskContext must contain the public issue, pinned base, hashed anchors, observed facts, semantic checks, real owner bindings, any observed PortValues, and current Oracle bindings. This package uses evidence predicates rather than artifact ports. Predicate names alone do not prove their claims.

UNKNOWN prerequisites authorize probes only. A hard mechanism mismatch rejects the repair.

## Operations

1. [Inspect and bind the lifecycle mechanism](references/actions/inspect.md).
2. [Restore async entry and exit parity](references/actions/repair.md).
3. [Add independent-scope regression assertions](references/actions/regressions.md).
4. [Validate both edits and retained behavior](references/actions/validate.md).

The [historical workflow](references/workflow.md) records the supported mechanism and dependency closure. Current plans may omit already-satisfied operations, but every modifying operation retains its validate Action. Ordering follows current semantic dependencies, not historical list position.

## Validation and stopping

Require no cross-scope warning for independent async functions and methods. Preserve synchronous scope isolation, established class/module lifecycle behavior, and legitimate within-scope type-change diagnostics.

Bind every Oracle to a current public instruction, argv command, and evidence references. Record the semantic check key as `oracle:<action_id>:<source_oracle_id>` and render bound commands before executing them. Historical commands do not authorize current execution.

Execute the bound public checks, inspect the final diff, and refresh stale observations after edits. Record PASS, FAIL, or UNKNOWN; structural PASS predicts compatibility, not repair success.

Stop if dispatch does not support the presumed async node hooks, the scope mechanism differs, regression assertions cannot expose the old behavior, or adjacent behavior changes. Do not suppress the warning or globally clear state as a substitute for scope isolation.

## Authority and limits

See the [episode](references/episode.md), evidence for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical CI execution is unknown. Later independent qualification checked the changed fixture and one adjacent test with original-base controls; whole-project correctness and cross-project transfer are untested. This qualification is not execution of the newly authored [functional cases](evals/functional-cases.json), which remain **not_executed**.

During formal evaluation, freeze knowledge and checkpoints; do not publish a current task plan as newly verified history. Time-reconstructed catalogs must exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before query time. Obtain independent hidden acceptance only after the solver stops.
