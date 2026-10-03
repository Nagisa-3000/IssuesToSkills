---
name: comprehension-walrus-binding
description: "Repair Python static-analysis scope handling when assignment-expression targets inside comprehensions or generator expressions are incorrectly confined to comprehension-local scopes."
---

# Comprehension assignment-expression binding

## Activation

Activate when a Python static analyzer reports an assignment-expression target as undefined after a comprehension or generator expression, and current public code shows that the target is being stored in a comprehension-local scope.

A representative symptom is an undefined-name diagnostic for `y` in:

```python
if any((y := x[0]) for x in [[True]]):
    print(y)
```

This Skill is about the analyzer's lexical binding model, not whether a lazy generator executes or whether a variable is definitely initialized at runtime.

Clarify first when only a diagnostic is provided, the analyzer implementation is unavailable, or the current scope owner cannot be identified.

Do not activate for ordinary comprehension iteration variables, unsupported Python syntax, unrelated undefined-name reports, or requests to make all comprehension assignments escape their scopes.

## Current probes and bindings

Use the [scope ownership probe](references/actions/probe.md) to locate these semantic owners in the current checkout:

- **binding-classifier**: classifies stored names by their parent AST construct.
- **binding-inserter**: records bindings into the active scope stack.
- **comprehension-scope-model**: represents generator/comprehension-local scopes.
- **scope-regression-tests**: exercises assignment-expression visibility and adjacent scope behavior.

Record current public issue details, pinned base revision, hashed code anchors, observations, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings in a TaskContext. Do not treat historical paths as current bindings.

Each current Oracle must map `action_id` and `source_oracle_id` to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render and execute those bound commands, not an assumed historical command.

Unknown prerequisites authorize probes only. A failed semantic prerequisite rejects the repair plan.

## Operations

1. [Inspect current binding ownership](references/actions/probe.md).
2. If the historical mechanism applies, [classify assignment-expression bindings and route them past comprehension scopes](references/actions/repair.md).
3. [Validate target visibility and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records the supported mechanism and dependencies. Already-satisfied operations may be omitted from a current task DAG, but a modifying operation always retains its validation operation.

## Validation and stopping

Require public checks for a single generator expression and nested comprehensions, together with adjacent ordinary-assignment, annotation, and iteration-variable behavior. Refresh facts invalidated by an edit.

Stop if the current language model differs materially, scope-stack boundaries are not understood, adjacent binding semantics change unexpectedly, or public tests fail. Structural compatibility is not proof of repair success. Independent hidden acceptance, if part of the host evaluation, occurs only after the solver stops; it is not guidance for this Skill.

## Evidence and limits

The [episode](references/episode.md) and [provenance](references/provenance.json) identify one verified historical repair. This is a focused Workflow, not a cross-project Pattern.

Historical regression tests are assertions available at the repair commit; the supplied evidence does not establish their execution at that historical time. Later qualification reports two fail-to-pass and 123 pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer remain untested. That later qualification is provenance, not knowledge backdated before the cutoff.

Evaluation definitions are unexecuted:

- [Activation cases](evals/activation-cases.json)
- [Applicability cases](evals/applicability-cases.json)
- [Functional cases](evals/functional-cases.json)
