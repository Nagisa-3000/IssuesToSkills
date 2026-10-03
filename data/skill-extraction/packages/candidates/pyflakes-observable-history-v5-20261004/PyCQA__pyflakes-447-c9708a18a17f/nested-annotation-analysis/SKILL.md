---
name: nested-annotation-analysis
description: "Repair Python static-analysis traversal that misses names inside nested quoted type annotations, while preserving Literal string values and deferred annotation behavior."
---

# Nested quoted annotation analysis

Use this Workflow when a Python static analyzer reports an imported type as unused, or fails to resolve its name, because the type occurs inside a quoted fragment of a larger annotation.

A representative trigger is `Optional['Queue[int]']`: the outer expression is an annotation, and the inner string is a forward type expression rather than an ordinary runtime string.

## Activation and exclusions

**Activate** when public reproduction and current code inspection show that annotation traversal ignores nested string nodes.

**Clarify or probe first** when the warning is known but the owning visitor, annotation context, or deferred execution model is unknown.

**Do not activate** for ordinary runtime strings, genuine unused imports, or a request to parse string values inside `typing.Literal` as type expressions. Do not assume that every annotation-related warning has this cause.

This package supports one historical Python checker repair. It does not establish a cross-project Pattern, universal typing-string semantics, or support for arbitrary module aliases.

## Current probes and bindings

Before editing:

1. Record the public issue, pinned base, hashed code anchors, and observed diagnostic.
2. Locate the semantic owners: annotation traversal, string/constant visitors, deferred annotation execution, typing construct recognition, and public annotation tests.
3. Inspect whether nested strings are visited with annotation context and whether deferred callbacks retain that context.
4. Check whether `Literal` recognition distinguishes typing imports from unrelated names.
5. Bind the ports and public oracles in the [inspection Action](references/actions/inspect.md).

Current checks are `PASS`, `FAIL`, or `UNKNOWN`. Unknown prerequisites authorize inspection only; hard prerequisite failures reject this Workflow. Predicate labels alone are not evidence that a current implementation has the required semantics.

## Operations

- [Inspect and reproduce](references/actions/inspect.md).
- [Repair annotation-aware string traversal](references/actions/repair.md).
- [Validate target and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records dependencies, not a mandatory current task list. Already satisfied operations may be omitted only when current observations support that decision. Every edit still retains its explicit validation.

## Validation and stopping

Bind each source oracle to a current public instruction, argv command, and evidence references. Record its semantic check under `oracle:<action_id>:<source_oracle_id>`. Run the bound commands, not an assumed historical command.

Require observable checks for:

- Partially quoted annotations marking the referenced import as used.
- A fully quoted annotation containing another quoted type fragment.
- Postponed annotations retaining annotation context.
- `Literal` strings remaining values, including strings that are invalid Python expressions.
- Supported `typing` and `typing_extensions` forms.
- Existing overload recognition and non-annotation string behavior.
- Context restoration and applicable Python AST string-node representations.

Stop and reassess if the public reproduction does not isolate annotation traversal, if current literal semantics differ materially, if deferred processing cannot safely handle nested parsed strings, or if adjacent behavior regresses. Do not suppress unused-import warnings indiscriminately.

A structurally compatible plan does not prove repair success. Refresh observations invalidated by editing, report unexecuted checks as unknown, and obtain independent hidden acceptance only after the solver stops. Do not publish a current plan as newly verified historical knowledge during formal evaluation.

## Evidence and limits

See the [episode](references/episode.md), [source provenance](references/provenance.json), and [historical regression assertions](references/evidence/regression.md).

The supplied later qualification reports 4 fail-to-pass and 25 pass-to-pass checks for changed test files with original-base control. That is a contemporary provenance attestation, not a historical test execution. Whole-project regression and cross-project transfer remain untested. This package's evaluation definitions are **not executed**.

Formal knowledge remains frozen. Time-reconstructed training catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.
