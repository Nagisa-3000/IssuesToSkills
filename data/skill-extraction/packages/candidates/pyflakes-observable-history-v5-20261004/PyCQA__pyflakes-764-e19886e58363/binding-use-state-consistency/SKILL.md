---
name: binding-use-state-consistency
description: "Repair annotation-only binding reads that store a boolean use marker where later scope-sensitive analysis expects structured use metadata; activate only after confirming the representation mismatch in current Python analyzer code."
---

# Binding use-state consistency

This focused Workflow Skill repairs a specific state-representation mismatch in a Python static analyzer. It is not a general recipe for every boolean-subscript exception.

Canonical Skill and Workflow ID: `workflow:verified-history:a9020121b14a346d4f659c0e`.

## Activation

Activate when public evidence indicates all of the following:

- An annotation-only outer binding is read outside postponed-annotation handling.
- That read marks the binding as used.
- A later local assignment to the same name triggers scope-sensitive analysis.
- The consumer indexes use metadata, but the annotation-read producer stores a truthy boolean.

A useful public reproduction is:

```python
x: int
x.__dict__

def f():
    x = 1
```

The historically asserted outcome is an undefined-name diagnostic for the outer read and an unused-local diagnostic for the inner assignment, not a checker exception.

Clarify or probe when the symptom is present but the producer, consumer, or annotation mode is unknown. Do not activate for ordinary runtime attribute failures, unrelated boolean indexing, or a checker whose use metadata follows a different contract.

## Current probes and bindings

Use [the inspection Action](references/actions/inspect.md) to locate the current semantic owners:

- `binding-use-producer`: handling reads of annotation-only bindings.
- `binding-use-consumer`: scope-sensitive assignment analysis that consumes use metadata.
- `annotation-regression-tests`: public tests for annotation-only bindings and local assignments.

Historical paths are recorded only in [the episode](references/episode.md). Resolve current bindings independently; do not treat old line numbers or paths as current anchors.

Before proposing edits, collect the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Record checks as PASS, FAIL, or UNKNOWN. Unknown prerequisites permit inspection only. A hard semantic mismatch rejects this workflow.

## Operations

The [historical workflow](references/workflow.md) links these operations:

1. [Inspect the producer-consumer contract](references/actions/inspect.md).
2. [Repair the use-state producer](references/actions/repair.md).
3. [Add the interaction regression](references/actions/regression.md).
4. [Validate both modifications](references/actions/validate.md).

The two edits may proceed independently after inspection. Validation must cover both final edits. Already satisfied operations may be omitted only when current evidence establishes their effects; that does not change the historical workflow.

For each current Oracle, bind its Action ID and source Oracle ID to a public instruction, an argv command, and evidence references. The semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound current commands before execution. Historical instructions do not authorize unadapted commands.

## Validation and preservation

Verify:

- The reproduction does not crash.
- The outer annotation-only read still reports an undefined name.
- The inner unused assignment still reports an unused local.
- Use metadata retains the scope and read-node information expected by consumers.
- Adjacent annotation tests pass, including relevant postponed-annotation handling.

Do not suppress diagnostics, remove scope checks, or merely guard the consumer against booleans. The evidenced repair changes the producer's representation while retaining its control flow.

## Stop conditions and limits

Stop if current code lacks the same producer-consumer mismatch, structured metadata has a different meaning, or the reproduction has different intended diagnostics. Investigate rather than extrapolate to other languages or unrelated analyzers.

The historical regression is an assertion added at the repair commit, not proof of historical test execution. A later qualification attests one fail-to-pass and 43 pass-to-pass outcomes in changed test files only. Whole-project regression and cross-project transfer are untested.

The [evidence cards](references/episode.md#evidence) preserve historical observations; [provenance](references/provenance.json) separately records contemporary qualification. Evaluation definitions remain `not_executed`. Structural plan compatibility does not establish repair success. Execute current public checks, refresh invalidated observations, and obtain independent hidden acceptance after the solver stops; hidden checks must not enter guidance. Formal knowledge and checkpoints remain frozen during evaluation.
