---
name: assignment-expression-ordering
description: "Repair false used-before-assignment diagnostics for Python assignment expressions when expression evaluation order differs from source-coordinate ordering, especially multiline f-strings on older Python ASTs."
---

# Assignment-expression ordering

## Activation and exclusions

Activate when a Python static analyzer reports a name used before assignment even though a walrus expression binds it earlier in the same evaluated expression. The strongest supported case is a multiline concatenated f-string whose earlier formatted component assigns a name and whose later component reads it.

Clarify if code, interpreter version, AST representation, or evaluation order is unknown. Inspect conditional-expression handling when the defining statement is an annotated assignment, augmented assignment, or expression statement.

Do not activate for genuine earlier reads, unrelated scope resolution, missing walrus syntax support, or blanket diagnostic suppression.

## Current probes

Use [inspection](references/actions/inspect.md) to bind these semantic owners in the current public checkout:

- `assignment-use-checker`: the assignment-expression diagnostic decision;
- `runtime-version-policy`: interpreter/AST feature predicates;
- `assignment-expression-regressions`: public fixtures and diagnostic expectations.

Historical paths are references, not current bindings. Record the public issue, pinned base, hashed anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings in a TaskContext. Inspect statement ancestry, frame relation, runtime version, and definition/use coordinates.

Existence predicates use `role:<owner_role>` as their key, boolean values, and `file_exists` or `symbol_exists` evaluators. Existence alone does not establish semantic applicability.

Unknown prerequisites authorize probes only. A hard failure rejects the repair plan.

## Operations

1. [Inspect expression ordering](references/actions/inspect.md).
2. [Edit narrow rules and regression fixtures](references/actions/repair.md), only after confirming the mechanism.
3. [Validate corrected and preserved diagnostics](references/actions/validate.md).

See the [historical Workflow](references/workflow.md). Current ordering follows compatible ports, prerequisites, and verification dependencies, not historical list position. Already satisfied or inapplicable operations may be omitted only with current evidence; modifying operations retain their validation closure.

Do not blindly copy an old version guard. The historical f-string fallback applies inside existing assignment-expression eligibility logic, specifically to pre-3.9 Python, equal definition/use line numbers, assignment-like statements, and a `JoinedStr` value. Reliable modern coordinates must retain the accurate ordering path.

## Validation and stopping

Bind every oracle to a current public instruction, argv command, and evidence references. Record its semantic check under `oracle:<action_id>:<source_oracle_id>` as PASS, FAIL, or UNKNOWN. Render and execute bound commands; empty contract commands are placeholders, not executable authorization.

After editing, refresh stale validation observations. Verify positive cases in ordinary, annotated, and augmented assignments, conditional-expression contexts, genuine earlier-read controls, and unrelated diagnostic expectations.

Stop if the reproduction is absent, semantic owners cannot be bound, evaluation order conflicts with the proposed mechanism, negative controls lose diagnostics, or a required runtime branch cannot be exercised. Report unavailable branches as UNKNOWN rather than passed.

Structural PASS predicts compatibility, not repair success. Keep formal knowledge and checkpoints frozen during evaluation; never publish a current task plan as newly verified historical knowledge. Obtain independent hidden acceptance only after the solver stops. Time-reconstructed training use excludes the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Evidence and limits

Read the [episode](references/episode.md), [provenance](references/provenance.json), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

This is one historical Workflow, not a cross-project Pattern. Historical CI execution is unknown. Later source qualification covers changed-test files with an original-base control, not whole-project correctness, all interpreter branches, or transfer. [Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions remain unexecuted.
