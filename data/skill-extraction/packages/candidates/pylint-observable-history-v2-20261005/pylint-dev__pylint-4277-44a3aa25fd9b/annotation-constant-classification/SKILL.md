---
name: annotation-constant-classification
description: "Repair annotation-driven class naming that mistakes ClassVar for a constant declaration, preserving Final-based constant naming, configured styles, and Enum behavior."
---

# Annotation-driven constant classification

## Conditional activation

Activate when a public Python reproduction shows a `ClassVar` class attribute receiving a class-constant naming diagnostic, and current inspection confirms that the annotation classification branch causes it.

`ClassVar` identifies class-level storage, not constantness. The evidenced repair uses `Final`, rather than `ClassVar`, as the annotation-based constant signal.

Clarify when the declaration, annotation, diagnostic category, or naming configuration is missing. Do not activate for ordinary instance naming, dataclass field discovery, general typing inference, or Enum-only policy complaints. Import aliases, string annotations, import-origin inference, other annotation wrappers, and other languages are outside the evidenced mechanism.

## Current probes and operations

Use [Inspect](references/actions/inspect.md), conditionally [Repair](references/actions/repair.md), then [Validate](references/actions/validate.md). The [Workflow](references/workflow.md) retains the modifying operation's verification closure.

Before editing:

1. Pin the public base and locate the current classifier, annotation recognizer, and naming suite by semantic role.
2. Record hashed code anchors, real bindings, naming configuration, public diagnostics, and annotation AST shapes.
3. Confirm that `ClassVar` alone selects constant naming.
4. Resolve role aliases before conflict checks and bind matching Action ports.

The current TaskContext retains the public issue, pinned base, hashed anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Each Oracle maps Action ID/source Oracle ID to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution; historical commands are not current execution authority.

Checks are PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject the repair plan. If the policy is already correct, omit the repair using current evidence rather than reapplying historical code.

## Repair and verification

Keep annotation recognition separate from naming policy. The supported recognizer requires an annotated assignment, unwraps an outer subscript, and compares a name or attribute suffix. Use `Final` for annotation-based constant naming while retaining Enum classification and configuration lookup.

Public assertions distinguish ClassVar/Final, bare/qualified/subscripted forms, initialized/annotation-only declarations, and default uppercase/configured snake_case constant styles. After edits, refresh stale validation observations and run both differential and adjacent checks.

Structural compatibility predicts compatibility, not repair success. An observation record can contain failures or unknowns; completion requires passing checks. Do not automatically regenerate diagnostics to conceal regressions.

## Stop conditions and limits

Stop if the public symptom cannot be reproduced, owners cannot be bound, another mechanism causes the diagnostic, required runtime support is missing, or adjacent behavior regresses. Do not suppress `invalid-name` globally or rename mutable attributes merely to hide this defect.

This is a single-source Workflow, not a cross-project Pattern. [Historical evidence](references/episode.md) records committed assertions; historical CI execution is unknown. Later qualification covers changed-test files with selected original-base controls only, not whole-project regression or transfer. [Functional cases](evals/functional-cases.json) remain unexecuted.

Keep knowledge and checkpoints frozen during formal evaluation; do not publish a current task plan as historical knowledge. Obtain independent hidden acceptance after the solver stops, without using hidden or gold-derived commands in guidance. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

See [provenance](references/provenance.json) for immutable source identity and validation-only qualification.
