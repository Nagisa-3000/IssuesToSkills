---
name: positional-only-keyword-accounting
description: "Repair Python call analysis when a keyword captured by **kwargs incorrectly satisfies a same-named required positional-only parameter."
---

# Positional-only keyword accounting

## Activation and exclusions

Activate when a Python call analyzer omits a missing-required-argument diagnostic for a call like:

```python
def required(a, /, **kwargs):
    return a

required(a=43)
```

The keyword belongs to `kwargs`; it does not supply positional-only parameter `a`.

Clarify if the inferred signature, keyword collector, diagnostic output, or accounting implementation is unknown. Do not activate for ordinary keyword-bindable parameters, non-Python argument models, already-correct analysis, or signatures without a keyword collector. The latter have a separate keyword-rejection path that this repair does not authorize changing.

## Current probes

Use [locate](references/actions/locate.md) to bind the current semantic owners of call-argument accounting and its public regression harness. Historical file paths are evidence, not current bindings.

Establish with public code and probes that:

1. The inferred callable has a required positional-only parameter and `**kwargs`.
2. The call supplies its name only as a keyword.
3. Keyword processing incorrectly marks the positional parameter supplied.
4. Existing required-parameter analysis can report the missing value.
5. The current runtime and harness support positional-only syntax.

UNKNOWN prerequisites authorize inspection and probes only. A contradicted mechanism rejects the modifying plan.

## Linked operations

The [historical workflow](references/workflow.md) supports these conditional operations:

1. [Locate and confirm the satisfaction transition](references/actions/locate.md).
2. [Guard that transition and add public regression assertions](references/actions/repair.md).
3. [Validate the target diagnostic and adjacent behavior](references/actions/validate.md).

Use current metadata and bindings, not a wholesale historical patch. Skip satisfaction only when the keyword matches a positional-only name and a keyword collector exists. Preserve positional supply, normal keyword binding, defaults, mixed signatures, and the existing no-collector rejection path.

## Validation and stopping

Run the bound current public regression oracle after every modification. Require the missing-argument diagnostic for keyword-only supply of the required positional-only name. The four legal controls must remain free of that diagnostic:

- supplying the positional-only parameter positionally;
- supplying it positionally alongside a normal keyword parameter;
- omitting a defaulted positional-only parameter;
- supplying an ordinary parameter by keyword.

Inspect the unchanged no-collector path and run relevant current public neighboring checks. Their precise expectations must come from the current checkout.

Stop if inference remains unresolved, the guard cannot be isolated safely, a public oracle cannot run, or neighboring behavior regresses. Further edits make validation observations stale.

A current TaskContext must contain the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Map each `action_id/source_oracle_id` to a public current instruction, argv, and evidence references; its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Historical commands do not authorize current execution.

Checks are PASS, FAIL, or UNKNOWN. Structural PASS predicts compatibility, not repair success. Obtain independent hidden acceptance after the solver stops, without using hidden checks as guidance.

## Authority and limits

Read [the episode](references/episode.md), [source provenance](references/provenance.json), and the evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [assertions](references/evidence/regression.md).

This is a single-source Workflow, not a Pattern or a cross-project template. Historical assertions were committed; historical CI/test execution is unknown. Later source qualification has scope `changed-test-files-with-original-base-control` and exact limits: “Changed test files only; whole-project regression and cross-project transfer are untested.” It does not execute this Skill's evaluations.

[Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions remain `not_executed`.

Keep formal knowledge and checkpoints frozen during evaluation. Earlier-query catalogs must exclude the current task's own issue, fix, cluster, aliases, copied sources, and every discovery input unavailable before query time.
