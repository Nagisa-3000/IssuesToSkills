---
name: annotation-metadata-boundary
description: "Repair Python AST annotation traversal when Annotated metadata is incorrectly treated as forward type syntax, while preserving type diagnostics and surrounding annotation state."
---

# Annotation metadata boundary

## Activation

Use this conditional Workflow when public evidence shows that a Python static analyzer treats metadata in `Annotated[T, metadata, ...]` as forward-reference type syntax. The historical symptom was a forward-annotation syntax error for `Annotated[int, '>1']`.

Clarify if the report lacks the triggering expression or the current traversal owner cannot yet be inspected. Do not activate for malformed syntax in the first type argument, runtime metadata validation, or a checker without a corresponding Python AST annotation-context mechanism.

Bare names and attributes ending in `Annotated` were recognized in the historical repair. This does not establish support for import aliases, semantic typing-name resolution, or arbitrary typing constructs.

## Current probes and operations

1. [Inspect](references/actions/inspect.md) the current subscript visitor, annotation-state manager, AST slice representations, and public reproduction.
2. If the defect and owners are established, [repair](references/actions/repair.md) the type/metadata traversal boundary and add public regression coverage.
3. After every modification, [validate](references/actions/validate.md) target behavior and preserved adjacent behavior.

See the [canonical Workflow](references/workflow.md), [historical episode](references/episode.md), and [provenance](references/provenance.json). Historical file paths are reference information, not current bindings.

## Execution conditions

Construct a current public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Each current Oracle maps `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render those bound commands before execution. Empty command arrays in these source contracts are placeholders requiring current binding, not executable historical instructions.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites permit probes only; hard failures reject the edit. Predicate labels alone do not prove semantic claims. Structural PASS predicts compatibility, not repair success.

## Validation and stopping

Require:
- metadata strings to be checked as ordinary expressions, not forward types;
- the first argument to retain type and forward-reference checking;
- enclosing annotation state to be restored;
- existing `Literal` behavior and ordinary fallback traversal to survive.

Refresh stale validation observations after an edit. Stop if the defect cannot be attributed to the supported traversal mechanism, owners cannot be bound, an unsupported bridge is needed, or public checks fail. Report untested AST/interpreter configurations explicitly.

Independent hidden acceptance, if required, occurs after the solver stops. Never use hidden tests or gold-derived commands as guidance. Formal knowledge and checkpoints remain frozen; current task plans are not newly verified historical knowledge and must not be published during formal evaluation. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Limits

This Workflow has one independently verified historical repair, not enough support for a Pattern. Historical regression evidence contains assertions, not historical execution logs. A later qualification reports two fail-to-pass and forty pass-to-pass cases, limited to changed test files with an original-base control. Whole-project regression and cross-project transfer remain untested.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`.
