---
name: annotation-only-name-resolution
description: "Repair Python static-analysis name resolution when annotation-only declarations must be distinguished from value bindings and accepted in postponed annotations without suppressing ordinary undefined-name diagnostics."
---

# Annotation-only name resolution

## Activate conditionally

Use this Workflow when a Python AST-based analyzer mishandles a declaration such as `T: object` because it either discards the declaration entirely or treats it as a runtime value binding.

The historically supported distinction is:

- `T: object` does not supply a runtime value.
- Without postponed annotations, `def f(t: T): ...` still reports an undefined name.
- A string annotation such as `def g(t: 'T'): ...` can resolve the annotation-only declaration.
- With `from __future__ import annotations`, both forms can resolve it.

An issue asking simply to suppress the diagnostic on a bare annotation is not enough to justify that change. Inspect the annotation evaluation mode first.

Do not activate for a general type checker, import-resolution defect, or arbitrary forward-reference problem without evidence that annotation-only bindings and postponed annotation context are the relevant mechanism. Clarify if the current evaluator or binding model is unknown.

## Current probes and bindings

Before editing, pin the public checkout and record hashed code anchors. Locate these semantic owners rather than assuming historical paths:

- `annotation_binding_owner`: binding construction, assignment classification, name lookup, and annotation context management;
- `annotation_regression_owner`: public tests for annotated assignments, quoted annotations, future annotations, and unused variables.

Record a current TaskContext containing the public issue, pinned base, anchors, observed facts, semantic checks, owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render and execute only those current bound commands. No executable historical command was supplied.

## Operations

1. [Inspect current resolution semantics](references/actions/inspect.md).
2. [Represent annotation-only declarations and discriminate annotation contexts](references/actions/repair.md).
3. [Validate the distinction and adjacent diagnostics](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) supplies dependencies. The [episode](references/episode.md) explains the historical scope; [provenance](references/provenance.json) records source authority and qualification limits.

## Validation and stopping

Use PASS/FAIL/UNKNOWN for current checks. UNKNOWN prerequisites authorize inspection only, not editing. A hard prerequisite failure rejects this Workflow. Structural compatibility predicts applicability, not repair success.

After editing, refresh stale validation observations and run public regressions covering bare, string, and future annotations; ordinary runtime loads; value-bearing assignments; and unused-variable behavior. Every repair retains its validate operation.

Stop if the current implementation cannot distinguish annotation-only from value bindings, if the proposed change suppresses ordinary runtime undefined-name diagnostics, or if required public checks fail. Do not silently weaken the checks.

During formal evaluation, keep this Skill and historical evidence frozen. Do not publish a current task plan as historical knowledge. Independent hidden acceptance is obtained after the solver stops, not used to select commands or edits.

## Limits

This is one verified historical Workflow, not a cross-project Pattern. Historical tests are supplied assertions, not claimed historical executions. Later qualification reports two fail-to-pass and 39 pass-to-pass cases within changed test files only. Whole-project regression and cross-project transfer remain untested.

The historical implementation's postponed-context property checks string context **or** the future-annotations flag. Its predicate is not simply “inside any annotation.” Preserve that distinction when assessing current compatibility.

Evaluation definitions are [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json); all remain unexecuted.
