---
name: guard-assignment-target-tracking
description: "Guard name-based deferred resource tracking against unsupported Python AST assignment targets while preserving immediate diagnostics for container-item assignments."
---

# Guard assignment-target tracking

## Activation

Activate when a Python AST resource checker crashes on a container-item assignment because deferred tracking reads a name or attribute-name field from an unsupported target.

The supported mechanism is a narrow admission guard: deferred tracking accepts direct names and attributes; subscript targets bypass that tracking but retain a separate immediate resource-management diagnostic.

Clarify when the public reproduction, target type, or failing owner is unknown. Do not activate for runtime subprocess failures, unrelated inference failures, incompatible AST interfaces, or requests for full container-element lifetime analysis.

## Current probes and bindings

Use [inspection](references/actions/inspect.md) before editing. Establish a current TaskContext with:

- Public issue and pinned base.
- Hashed code anchors and real bindings for the context-manager assignment tracker, immediate resource diagnostic, and functional assertion owners.
- Observed target types for direct-name, attribute, list-item, and dictionary-item assignments.
- Evidence of unsupported-target admission into unsafe name extraction.
- Evidence that immediate diagnostics remain available when deferred tracking is skipped.
- Semantic checks, observed PortValues, and current Oracle bindings.

Historical paths in [episode](references/episode.md) are not current bindings. Resolve role aliases before read/write conflict checks. Natural-language mechanism claims require current evidence, not matching predicate names.

UNKNOWN prerequisites authorize probes only; hard failures reject a repair plan.

## Operations

See the canonical [Workflow](references/workflow.md):

1. [Inspect target admission](references/actions/inspect.md).
2. [Guard tracking and add regressions](references/actions/guard.md).
3. [Validate diagnostics and adjacent behavior](references/actions/validate.md).

Current task DAGs may omit already satisfied operations only with current evidence. Every executed modifying Action retains its explicit validation Action. Ordering follows ports and semantic prerequisites, not merely historical list position.

Bind each Oracle by `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Record the check as `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty commands in contracts denote unbound Oracles; historical commands do not authorize execution in another checkout.

## Validation and stopping

Require fresh observations that:

- List-item and dictionary-item resource assignments do not crash the checker.
- Each retains the immediate context-manager recommendation.
- Direct-name and attribute assignments retain deferred tracking.
- Existing inference and resource-call filters and context-manager handling remain intact.
- Adjacent public assertions retain their behavior.

Distinguish expected diagnostic exit statuses from internal exceptions. Record PASS, FAIL, or UNKNOWN; missing coverage is not PASS. Refresh stale code anchors and validation observations after edits.

Stop if the separate diagnostic path is absent, target semantics differ, or preservation checks fail. Do not catch all `AttributeError` exceptions, fabricate target names, or disable diagnostics globally.

Structural plan PASS predicts compatibility, not repair success. Independent hidden acceptance occurs after the solver stops and must not influence frozen knowledge or public checks. Do not publish a current task plan as newly verified historical knowledge during formal evaluation.

## Authority and limits

This is a single-source Workflow, not a Pattern or a verified cross-project abstraction. See [episode](references/episode.md), [implementation evidence](references/evidence/fix.md), and [provenance](references/provenance.json).

Historical regression assertions were committed with the repair; historical CI execution is unknown. Later independent source qualification used original-base, base-with-regression, and historical-fixed controls. Its scope is changed-test-files-with-original-base-control; whole-project correctness and cross-project transfer remain untested.

All authored [functional cases](evals/functional-cases.json) remain unexecuted. Source qualification does not execute these definitions.

Time-reconstructed catalogs must exclude the task's own issue, fix, cluster, aliases and copies, and every source unavailable before query input time.
