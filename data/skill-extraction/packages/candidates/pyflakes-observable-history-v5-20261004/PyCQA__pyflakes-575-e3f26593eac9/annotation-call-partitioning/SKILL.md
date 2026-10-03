---
name: annotation-call-partitioning
description: "Repair Python static-analysis false positives caused by treating typing-factory names and field labels as forward references, while preserving analysis of actual type expressions."
---

# Annotation-call partitioning

## Activate conditionally

Use this Workflow when a Python static analyzer reports undefined names from string metadata inside a typing-factory call nested in an annotation or typing expression. Typical candidates are the declared name or field labels of `TypedDict` or `NamedTuple`, including labels containing punctuation.

The repair mechanism is **argument-role-aware traversal**: analyze metadata outside annotation context and analyze actual type expressions inside annotation context.

Before editing, confirm in the current checkout that:

- The affected call is recognized through typing-aware name resolution, rather than merely sharing a function name.
- Annotation state propagates into its arguments.
- Metadata strings are being interpreted as type expressions.
- Actual type-expression strings still need forward-reference analysis.

If these facts are unknown, perform the [owner and behavior probe](references/actions/probe.md) only. Do not infer applicability from matching filenames or issue wording.

## Exclusions and clarification

Do not activate for runtime `TypedDict` construction failures, invalid Python syntax, or unrelated missing imports. Do not suppress all undefined-name diagnostics in typing calls.

Clarify when the analyzer uses another language, has no equivalent annotation-state traversal, or the reported factory cannot be resolved as a typing construct. This package supplies no cross-language adapter and no independently verified cross-project realization.

## Operations

1. [Locate semantic owners and reproduce the distinction](references/actions/probe.md).
2. [Partition metadata and type-expression traversal](references/actions/partition.md).
3. [Add public regression assertions](references/actions/regressions.md).
4. [Validate the modified traversal and tests](references/actions/validate.md).

The [canonical historical Workflow](references/workflow.md) records dependencies and evidence. Current plans may omit satisfied operations only after observing their prerequisites and retaining validation of any edits.

Historical paths are documented in [the episode](references/episode.md); locate current owners by behavior. They are not automatic current bindings.

## Validation and stopping

Bind public current oracles before execution. Check both sides of the distinction:

- Factory names and field labels produce no false undefined-name diagnostics.
- Missing names in true type positions still produce diagnostics.
- Nested type expressions continue to account for imported names.
- Ordinary call analysis and typing-name resolution remain intact.

Stop if the factory cannot be reliably classified, metadata traversal loses genuine expression checks, or the traversal causes missing or duplicate diagnostics. Re-probe after edits invalidate prior observations. A compatible plan is not evidence of repair success.

Current TaskContext must record the public issue, pinned base, hashed code anchors, bindings, observed facts and PortValues, semantic checks, and public current oracle instructions and argv. Use PASS/FAIL/UNKNOWN: UNKNOWN permits probes only; a failed hard prerequisite rejects the repair plan. Render and execute bound current commands, not historical commands.

## Evidence and limits

This is a single-source Workflow, not a Pattern. The historical implementation and regression assertions were available before the authoritative cutoff. Historical test execution results were not supplied.

A later qualification attestation reports two fail-to-pass and 47 pass-to-pass cases within changed test files, with an original-base control. It does **not** establish whole-project regression safety or cross-project transfer and is not backdated historical knowledge.

See [provenance](references/provenance.json), [evidence cards](references/evidence/fix.md), and the unexecuted [functional definitions](evals/functional-cases.json). Formal knowledge remains frozen during evaluation; do not publish current plans as newly verified history. Independent hidden acceptance, if required by the host, occurs after the solver stops and is not a source of guidance.
