---
name: mutually-exclusive-match-bindings
description: "Repair Python analyzer unused-name redefinition false positives across separate match cases when a shared branch-alternative classifier omits match case bodies."
---

# Mutually exclusive match bindings

## Activate conditionally

Activate only when current public evidence establishes all of the following:

- A Python analyzer reports an unused-name redefinition between definitions in **different cases of the same match statement**.
- The corresponding `if`/`else` control does not produce that diagnostic.
- The redefinition logic uses a shared alternative-branch classifier, and inspection confirms that it omits match case bodies.

If the reproduction, owner, or runtime policy is unknown, clarify or run the [probe](references/actions/probe.md) first. Merely encountering pattern matching is not sufficient.

## Exclusions

Do not apply this workflow to sequential definitions in one case, pattern captures, guards, exhaustiveness, undefined-name diagnostics, or a diagnostic owned by another mechanism. Do not globally disable redefinition reporting. This is a single-source Python Workflow, not a cross-project Pattern or a language-agnostic adapter.

## Operations and current bindings

1. [Probe](references/actions/probe.md): locate semantic owners and reproduce the omission.
2. [Recognize alternatives](references/actions/recognize.md): expose each case body separately while respecting AST availability.
3. [Encode regression](references/actions/regression.md): add the distinct-case no-diagnostic assertion.
4. [Validate](references/actions/validate.md): execute public regression and preservation checks after both edits.

Use the [workflow dependencies](references/workflow.md), current prerequisites, and compatible ports to construct the current task DAG. Historical list order is not mandatory. Already satisfied operations may be omitted only with current evidence; validation must still cover any retained modifying operation.

Before execution, obtain a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Bind semantic owners in the current checkout; [historical paths](references/episode.md) are not current bindings. Each Oracle binding maps action ID and source Oracle ID to a current public instruction, argv, and evidence references. Render those bound commands before execution. Empty historical command arrays do not authorize guessed commands.

Unknown prerequisites permit probes only. Hard failures reject the plan. Structural PASS predicts compatibility, not repair success.

## Acceptance and stop conditions

After edits, refresh stale observations. Require observed public checks for:

- No unused-name redefinition across distinct match cases.
- Continued detection of a genuine sequential unused-name redefinition.
- Unchanged existing `if` and `try` alternative behavior.
- Safe `ast.Match` availability handling for supported runtimes.
- A passing added regression and current adjacent match tests.

Stop if the omission is already absent, ownership differs, compatibility cannot be established, or preservation checks fail. Missing checks remain UNKNOWN; do not broaden diagnostic suppression to obtain a pass.

## Historical support and limits

The [episode](references/episode.md) and [provenance](references/provenance.json) document one verified resolution available before the cutoff. Historical tests are assertions present at the merged commit, not an observed historical test execution.

A separate 2026 qualification attestation reports one fail-to-pass and seven pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer are untested. This attestation is not backdated historical knowledge.

[Functional eval definitions](evals/functional-cases.json), [activation cases](evals/activation-cases.json), and [applicability cases](evals/applicability-cases.json) are not executed. Current plans and results are not newly verified historical knowledge and must not be published as such during formal evaluation. Formal knowledge and checkpoints remain frozen. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources not available before query input time. Obtain independent hidden acceptance after the solver stops; hidden tests do not enter public guidance.
