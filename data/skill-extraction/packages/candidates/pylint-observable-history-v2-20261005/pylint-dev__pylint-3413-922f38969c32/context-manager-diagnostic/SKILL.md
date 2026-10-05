---
name: context-manager-diagnostic
description: "Implement an inference-backed Python refactoring diagnostic for known resource allocations and acquisition methods that can use context managers, preserving message control and resource lifetime behavior."
---

# Context-manager diagnostic

## Activation and exclusions

Activate for a public request to add or repair a Python static-analysis suggestion for known resource operations outside context-manager syntax, when the analyzer offers safe callable inference, AST visitors, and a diagnostic registry.

Clarify requests that do not distinguish a lint suggestion from automatic rewriting or runtime cleanup. Do not activate for runtime leak monitoring, whole-program ownership proofs, arbitrary user-defined factories, or incompatible language interfaces.

This is a single-source Workflow, not a Pattern or evidence of cross-project transfer. Its ID is `workflow:verified-history:a2197ca95e3d5f6edcfac42f`.

## Current probes

Use [the probe Action](references/actions/probe.md) to locate current semantic owners:

- `python-refactoring-checker`: registry, visitor routing, message-enable gates, and callable inference.
- `python-functional-fixtures`: diagnostic fixtures, expectations, message-control tests, and interpreter exclusions.
- `diagnostic-consumers-and-docs`: resource-owning internal consumers and public documentation.

Historical paths in [the episode](references/episode.md) are evidence, not current bindings. Record the public issue, pinned base, hashed anchors, owner bindings, observed facts, semantic checks, observed PortValues, and current Oracle bindings in the TaskContext.

Inspect inferred qualified names rather than matching source spellings. Establish whether each operation returns a resource or acquires/starts an existing one. Inspect assignment/return visitor aliases and diagnostic-enable decorators.

Unknown prerequisites authorize locating or read-only probes only. A hard incompatibility rejects the plan.

## Operations

1. [Probe current boundaries](references/actions/probe.md).
2. [Implement and integrate](references/actions/implement.md): register the diagnostic, classify inferred callables, integrate visitors, add assertions, and review client lifetimes.
3. [Validate](references/actions/validate.md): execute current public checks and inspect complete diagnostics and adjacent behavior.

The [historical Workflow](references/workflow.md) records the supported mechanism. Current ordering follows compatible ports, observed prerequisites, dependencies, and verification requirements—not historical list position alone.

## Validation and stopping

For every Oracle, bind `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render current bound commands before running them. Empty source command arrays are not executable bindings.

Use PASS/FAIL/UNKNOWN. Structural PASS predicts compatibility, not repair success. Refresh stale validation observations after edits. Stop without claiming success when:

- Required inference, owner bindings, or public checks remain unknown.
- Direct `with` examples receive the new message.
- Suppression or adjacent diagnostics regress.
- A client conversion changes ownership, output consumption, or resource lifetime.
- Proposed scope requires unsupported general ownership reasoning.

After the solver stops, obtain independent hidden acceptance without importing hidden checks into the Skill or changing frozen knowledge.

## Limits

The historical implementation used finite inferred-name sets. It was not a leak detector. Explicit `close()` or `release()` did not prevent the suggestion. Resource-returning operations were checked through assignment/return routing, not every possible call position. Allocating a resource before later entering `with resource:` could still receive a suggestion.

Builtin `open()` was uninferable on PyPy in the historical tests; only its separate fixture was excluded. Condition acquisition and multiprocessing locks were explicitly unsupported or inference-limited.

The [evidence cards](references/evidence/fix.md), [regression card](references/evidence/regression.md), and [provenance](references/provenance.json) distinguish implementation, committed assertions, and validation-only replay. Historical CI execution is unknown. The supplied qualification covers selected changed-test cases with an original-base control, not whole-project correctness or transfer. The [functional eval definitions](evals/functional-cases.json) are not executed.
