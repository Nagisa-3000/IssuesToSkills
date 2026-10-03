---
name: explicit-type-alias-value-analysis
description: "Repair Python static analysis that misses imported names inside string-valued explicit TypeAlias assignments, by routing recognized alias values through annotation analysis while preserving ordinary assignment behavior."
---

# Explicit type-alias value analysis

Canonical Skill and Workflow ID: `workflow:verified-history:d3771ee821e88935b9bcf1ce`.

## Activate when

A Python static analyzer reports an imported name as unused when that name appears inside the string-valued right-hand side of an explicitly annotated type alias, such as:

```python
from os import PathLike
from typing_extensions import TypeAlias

PathLikeStr: TypeAlias = "PathLike[str]"
```

The likely semantic owner is the annotated-assignment visitor. Activation requires checking the current implementation; a matching symptom alone does not establish applicability.

## Exclusions and clarification

- Do not activate for ordinary string assignments whose contents are not annotations.
- Do not apply this repair to an unrelated unused-import problem merely because it involves typing.
- Newer type-alias syntax with a different AST owner requires a separately supported analysis.
- If the current analyzer lacks annotation-value processing or binding-aware recognition of typing markers, clarify the architecture before editing. This Skill does not supply an invented adapter.
- Recognition of aliases, qualified names, or shadowed markers must be established from the current typing-marker recognizer. The supplied historical evidence does not establish every recognition form.

## Current probes and operations

1. [Locate and check the semantic owner](references/actions/probe.md). Inspect the annotated-assignment dispatch, annotation handler, and typing-marker recognizer. Reproduce the reported distinction between alias strings and ordinary annotation strings.
2. [Edit value dispatch and regression coverage](references/actions/edit.md). Only when the prerequisites pass, route values of recognized `TypeAlias` annotations through annotation analysis. Keep ordinary value traversal and missing-value behavior.
3. [Validate the change](references/actions/validate.md). Run public reproductions, regression cases, and adjacent annotation tests with commands bound to the current checkout.

The [historical Workflow](references/workflow.md) describes the evidence-supported repair mechanism, not an execution record for the current task. The [episode](references/episode.md) records the original report, implementation, and regression assertions.

## Validation and stopping

Stop rather than edit if the semantic owner cannot be located, the recognizer does not identify the marker under test, or the proposed annotation handler has incompatible semantics. Unknown prerequisites permit read-only probes, not modifications.

After editing, refresh stale observations and verify:

- Imported names used in explicit string aliases are recognized.
- Non-string aliases still work.
- Module and class scopes behave correctly.
- Annotated assignments without values do not manufacture uses.
- Ordinary non-alias strings do not become annotation expressions.
- Adjacent annotation diagnostics remain intact.

A failing public check requires investigation; structural compatibility does not prove a successful repair.

## Current task binding

Before execution, record a public issue, pinned base revision, hashed code anchors, observed facts, semantic checks, resolved owner bindings, and observed PortValues. Bind every Action oracle to a current public instruction and argv command. Use semantic check keys of the form `oracle:<action_id>:<source_oracle_id>` and record `PASS`, `FAIL`, or `UNKNOWN`.

Render and execute the bound current commands, not presumed historical commands. Resolve owner aliases before read/write conflict checks. Preserve all behavior assurances when composing a plan; observations invalidated by editing must be refreshed. Independent hidden acceptance, if used, occurs after the solver stops and is not exposed as guidance.

Formal knowledge and checkpoints remain frozen during evaluation. A time-reconstructed catalog must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.

## Evidence and limits

This is a single-repair Workflow, not a cross-project Pattern. Its support comes from one verified repair available before the cutoff. Historical tests are recorded as assertions present at the repair revision, not as invented historical test executions.

The later qualification attestation reports one fail-to-pass and 51 pass-to-pass results in changed test files with an original-base control. Whole-project regression and cross-project transfer remain untested. That attestation is provenance, not knowledge backdated to the historical repair.

See [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), and [functional definitions](evals/functional-cases.json). All authored eval suites are `not_executed`.
