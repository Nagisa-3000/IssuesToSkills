---
name: eager-default-classification
description: "Conditionally repair Python loop-closure false positives caused by omitted keyword-only default expressions, preserving positional default recognition and genuine late-binding warnings."
---

# Eager default classification

## Activation

Activate when a Python static analyzer reports a loop-cell warning on a loop variable appearing in a keyword-only parameter default, while an equivalent positional default is accepted. Activation authorizes diagnosis, not an unconditional edit.

The supported mechanism is a default-expression classifier that traverses positional defaults but omits keyword-only defaults. Confirm the current warning location, AST representation, and semantic owner before repairing.

Do not activate for genuine loop-variable references in function bodies, unrelated default-expression diagnostics, or another language's AST. This is a single-source Workflow, not a Pattern or a cross-project transfer claim.

## Current probes and bindings

Use [diagnosis](references/actions/diagnose.md) to:

- locate the current default-expression classifier and public loop-closure regression owners;
- compare keyword-only and positional eager-capture reproductions;
- inspect separate default collections, absent-default sentinels, and exact-node identity matching;
- distinguish default-expression references from genuine late-bound body references.

Historical paths in [the episode](references/episode.md) are search hints, not current bindings. Stop rather than invent an adapter if the current AST representation is incompatible.

Maintain a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before executing them; the empty command arrays in the historical contracts require current bindings.

Checks are PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only. Hard failures reject the plan. Predicate names alone do not establish semantic compatibility.

## Operations

1. [Diagnose the omitted collection](references/actions/diagnose.md).
2. [Repair classification and focused assertions](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) supplies the sourced dependency structure. Current ordering follows compatible ports, prerequisites, and semantic verification dependencies, not merely historical list position. Resolve current aliases before read/write conflict checks. Already satisfied operations may be omitted, but every performed edit retains its explicit validation Action.

## Validation and stop conditions

Require current public observations demonstrating:

- no loop-cell warning for escaping keyword-only eager default capture;
- continued recognition of positional default capture;
- retained warnings for genuine late-bound body references;
- safe handling of absent keyword-only defaults;
- exact-node matching rather than same-spelling name matching;
- retained function/lambda scope handling and unsupported-scope false fallback.

The sentinel, identity, and scope controls are authored validation obligations derived from the implementation, not additional historical regression assertions.

Stop if the omission is absent, the reproduction cannot be established, owner bindings remain uncertain, or AST compatibility fails. Do not globally disable the warning or delete genuine diagnostic expectations. Only adjust expected locations displaced by inserted regression lines.

An edit makes prior validation observations stale. Re-run current public checks after subsequent changes. Structural plan PASS predicts compatibility, not repair success. Failure or UNKNOWN prevents a success claim. Obtain independent hidden acceptance only after the solver stops.

## Authority and limits

The [episode and evidence cards](references/episode.md) distinguish the original report, merged implementation, and committed assertions. Historical CI/test execution is unknown.

The supplied contemporary qualification supports source resolution only within `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer were not checked. Qualification did not execute the newly authored Skill functional cases.

See [provenance](references/provenance.json) and the unexecuted [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites.

During formal evaluation, keep knowledge and checkpoints frozen. Do not publish a current task plan as newly verified history. Earlier-query admission must exclude the query's own issue, fix, cluster, aliases, copied sources, and every discovery input unavailable before its input time.
