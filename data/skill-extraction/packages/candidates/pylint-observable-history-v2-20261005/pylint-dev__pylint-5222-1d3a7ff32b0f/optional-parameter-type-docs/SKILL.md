---
name: optional-parameter-type-docs
description: "Repair false missing-parameter-documentation diagnostics for described NumPy-style parameter entries without inline types, while preserving legitimate missing-type diagnostics."
---

# Optional parameter type documentation

## Activation and exclusions

Activate when a Python documentation checker rejects a NumPy-style parameter entry consisting of a parameter name followed by an indented description, solely because the header omits `: type`.

Clarify when the actual diagnostic, docstring style, configuration, or description is unknown. Do not activate for genuinely absent descriptions, other documentation grammars, or return-type-only complaints.

This is a single-source Workflow, not a Pattern or a verified cross-project abstraction. See the [historical episode](references/episode.md), [Workflow](references/workflow.md), and [provenance](references/provenance.json).

## Current probes

Use [inspect](references/actions/inspect.md) to locate the current semantic owners of NumPy parameter-entry recognition, section splitting, documentation/type collection, and public tests. Pin the public checkout and hash code anchors. Reproduce the failure using both an annotated and an unannotated description-only parameter. Confirm the failure is entry recognition or collection, rather than disabled checking, style selection, or an actually missing description.

Historical paths in the episode are discovery locators, not current bindings.

Build a current TaskContext containing the public issue, pinned base, hashed anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty source command arrays require explicit current binding.

## Operations

1. [Inspect recognition and collection](references/actions/inspect.md).
2. When the supported mechanism is confirmed, [edit the NumPy parser and mixed-entry regression](references/actions/repair.md).
3. [Validate the diagnostic distinction and adjacent behavior](references/actions/validate.md).

Recognize a newline after the parameter identifier as an alternative to the colon delimiter. Keep documented-parameter membership separate from docstring-type membership. A description is not a type declaration.

Adapt to current capture groups and section representation. Do not blindly transplant the historical implementation: the supplied diff contains `print(entries)`, and its description-only branch uses delimiter group 2 as `param_desc`. Those are historical observations, not reusable requirements.

## Validation and stopping

Require public checks demonstrating that:

- Both annotated and unannotated description-only entries avoid `missing-param-doc`.
- The unannotated parameter still receives the legitimate `missing-type-doc`.
- Explicit docstring types, starred arguments, and adjacent supported styles retain their behavior.
- The edited regression checks the exact message set rather than merely the absence of one warning.

Unknown prerequisites authorize probes only. Hard failures or incompatible bindings reject the edit plan. Stop on unexplained neighboring failures, inability to execute current public checks, or contradictory reproduction. Any further edit invalidates the validation observation and requires affected checks to run again.

Structural PASS predicts compatibility, not repair success. After the solver stops, obtain independent hidden acceptance without importing hidden commands or results into this Skill.

## Evidence and limits

Historical evidence cards: [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression](references/evidence/regression.md).

Committed regression assertions were available at the historical revision; original CI/test execution is unknown. Later source qualification examined original-base, base-with-regression, and historical-fixed controls under one runtime digest. It establishes targeted changed-test-file resolution only, not whole-project correctness, return-type repair, malformed-entry correctness, or transfer.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are unexecuted definitions. Source qualification did not execute these Skill cases.

Keep formal knowledge and checkpoints frozen during evaluation. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources not available strictly before query input time.
