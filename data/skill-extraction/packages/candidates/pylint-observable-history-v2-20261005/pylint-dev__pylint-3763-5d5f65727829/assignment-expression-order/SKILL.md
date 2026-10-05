---
name: assignment-expression-order
description: "Conditionally repair false used-before-assignment diagnostics for Python conditional expressions whose test assigns before a branch reads; preserve genuine early-read diagnostics and narrowly bound legacy AST-location workarounds."
---

# Assignment-expression evaluation order

## Activation and exclusions

Activate when a Python variable checker emits `used-before-assignment` even though a conditional-expression test assigns the disputed variable before the selected branch reads it:

```python
foo if (foo := 3 - 2) > 0 else 0
```

Supported containing statements are ordinary assignment, annotated assignment, initialized augmented assignment, and standalone expression statements. Activation depends on evaluation order and checker ownership, not a repository name.

Clarify or probe when the expression, containing statement, frame relationship, AST representation, or actual diagnostic is unknown. Do not activate for genuine early reads:

```python
assert err_a, (err_a := 2)
print(err_b and (err_b := 2))
```

Do not suppress all assignment-expression diagnostics, remove independent `pointless-statement` warnings, rewrite general data flow, or transfer this Python realization to an incompatible AST interface.

## Current probes and bindings

Construct a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `variable-order-checker`: definition/read ordering and conditional-expression exceptions.
- `runtime-version-policy`: runtime predicates relevant to AST locations.
- `assignment-expression-regressions`: public fixtures and diagnostic expectations.
- `public-test-runner`: current public fixture runner.

Historical locations are documented in [the episode](references/episode.md); they are not implicit current bindings.

Use [inspection](references/actions/inspect.md) to observe diagnostics, containing statement/value types, execution order, frame identity, ancestry, and AST locations without editing tracked files. Version alone does not establish a multiline-string location defect.

## Operations

Follow the semantic dependencies in the [Workflow](references/workflow.md):

1. [Inspect and bind](references/actions/inspect.md).
2. [Repair recognition and regression coverage](references/actions/repair.md).
3. [Validate public diagnostics and boundaries](references/actions/validate.md).

Broaden only the evidenced containing-statement gate. Retain the conditional-expression value requirement, same-frame check, and ancestor check.

The historical repair also accommodates pre-3.9 multiline joined-string locations. Apply that branch only when current evidence supports its mechanism; retain all version, equal-line, statement-type, and joined-string guards. It does not authorize general same-line suppression.

Retain genuine early-read diagnostics and the standalone expression's independent warning. An already-correct checkout needs no speculative edit. Every performed edit retains its explicit validation Action.

## Validation and stopping

Bind each source Oracle to a current public instruction, argv command, and evidence references; render bound commands before executing them. Historical commands are evidence, not execution authorization. Record semantic checks under `oracle:<action_id>:<source_oracle_id>` as PASS, FAIL, or UNKNOWN.

UNKNOWN prerequisites permit probes only. Hard semantic mismatches reject the plan. Structural PASS predicts compatibility, not repair success.

After editing, refresh stale validation observations. Test positive fixtures, negative fixtures, adjacent checker behavior, and applicable runtime boundaries without updating expected outputs during validation.

Stop or narrow the claim if:

- The assignment does not actually precede the read.
- Frame, ancestry, or current AST semantics fail the supported prerequisites.
- A negative fixture loses E0601 or the standalone expression loses its independent diagnostic.
- A public check fails.
- Applicable runtime coverage remains unavailable or skipped.

Do not claim successful validation while an applicable required check remains UNKNOWN. Obtain independent hidden acceptance after the solver stops; hidden tests and gold-derived commands never become guidance. Formal knowledge and checkpoints remain frozen during evaluation. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and inputs unavailable before query time.

## Evidence and limits

This is a single-source Workflow, not a Pattern or a cross-project transfer claim. Its support consists of the [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [committed assertions](references/evidence/regression.md). See [provenance](references/provenance.json).

Historical CI/test execution is unknown. Later independent qualification inspected original-base, base-with-regression, and historical-fixed controls using a consistent runtime: the original suite passed, adding the regression to the base failed the assignment-expression fixture, and the fixed revision passed. Scope is changed-test-files-only, with one fail-to-pass target, 22 original-to-fixed passes, and two skips. Whole-project correctness, all runtime branches, and cross-project transfer were not checked.

That qualification validates the historical source, not this newly authored Skill. [Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions remain `not_executed`.
