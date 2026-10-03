---
name: typing-factory-annotation-boundaries
description: "Repair false undefined-name diagnostics from typing factory calls nested in annotations by separating literal names and field labels from type-bearing arguments, while preserving genuine forward-reference diagnostics."
---

# Typing factory annotation boundaries

## Activate when

A Python static analyzer incorrectly treats literal names or field labels in a typing factory call as forward-reference expressions, particularly when the call appears inside an annotation or a typing subscription.

A characteristic public reproduction is:

```python
from typing import TypedDict

class Example(TypedDict):
    nested: TypedDict("Nested", {"foo/bar": str})
```

The supplied historical report described false undefined-name diagnostics for `Nested`, `foo`, and `bar`. The repair separated non-annotation factory metadata from type-bearing expressions.

This is a focused historical Workflow, not a cross-project Pattern. Its canonical ID is `workflow:verified-history:3257ebe843a343f545c15939`.

## Do not activate when

- The reported undefined name occurs in an actual type expression and is genuinely unresolved.
- The failure is a runtime typing error rather than analyzer traversal.
- The affected factory is unrelated to the supported `typing` recognition mechanism.
- The proposed repair requires unsupported language adapters or a redesign of symbol resolution.
- Current code already implements the required boundaries and public probes pass; use validation rather than repeating the edit.

If the owner or failure mechanism is unknown, clarify through read-only probes. Do not infer applicability merely from the presence of `TypedDict`.

## Current probes and bindings

Before planning an edit, construct a public TaskContext containing:

- Public issue and pinned base revision.
- Hashed anchors for the current call-expression visitor, typing-factory recognizer, annotation-state manager, child traversal helper, and annotation regression suite.
- Real bindings for `role:typing-call-traversal-owner` and `role:annotation-regression-owner`.
- Observed facts distinguishing factory metadata, type expressions, and ordinary arguments.
- Observed PortValues and current Oracle bindings.
- PASS, FAIL, or UNKNOWN semantic checks, including `oracle:<action_id>:<source_oracle_id>` for each bound oracle.

Locate semantic owners in the current checkout. Historical paths in the references are not current bindings. Bind each oracle to a public current instruction, an argv command, and public evidence references; render those commands before execution. Empty command arrays in the historical contracts are not executable authorization.

UNKNOWN prerequisites authorize probes only. A failed mechanism or owner check rejects the edit plan. Structural compatibility predicts neither test success nor repair success.

## Operations

1. [Inspect the boundary classification](references/actions/inspect.md): reproduce and identify which arguments should be interpreted as annotations.
2. [Partition traversal and add regression assertions](references/actions/partition.md): explicitly route type-bearing expressions through annotation handling and metadata through non-annotation handling.
3. [Validate the partition](references/actions/validate.md): check false positives, genuine forward references, nested type expressions, and adjacent behavior.

The [canonical Workflow](references/workflow.md) supplies dependencies and preserved behavior. The [episode](references/episode.md) explains the historical facts and limits.

## Validation and stop conditions

Validate both sides of the boundary:

- Literal factory names and field labels must not become undefined-name diagnostics merely because the call is nested in an annotation.
- Actual type-bearing strings and nested type expressions must still receive annotation analysis.
- Ordinary call traversal, factory recognition, and supported adjacent typing behavior must remain intact.

Every modifying operation retains its explicit validation Action. Edits invalidate observation freshness, not the requirement to preserve behavior. Refresh current probes after edits.

Stop and investigate if current factory recognition, AST shape, annotation-state semantics, or traversal helpers differ materially from the historical mechanism. Do not suppress all string diagnostics, skip the entire call, or broaden factory recognition without public evidence.

## Evidence and limits

The historical implementation also adjusted `TypeVar` constraints and bounds, `cast` type arguments, and functional `NamedTuple` declarations. These are supported adjacent cases, not evidence that arbitrary factories are safe to special-case.

Historical regression code is evidence of assertions available at the commit, not proof that commands were executed then. A later supplied qualification reports two fail-to-pass and 47 pass-to-pass cases within changed test files only. Whole-project regression and cross-project transfer are untested. The qualification is provenance, not pre-cutoff learned content.

All [eval definitions](evals/functional-cases.json) remain `not_executed`. During formal evaluation, keep this knowledge and checkpoints frozen; do not publish a current task plan as newly verified historical knowledge. Time-reconstructed training catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.
