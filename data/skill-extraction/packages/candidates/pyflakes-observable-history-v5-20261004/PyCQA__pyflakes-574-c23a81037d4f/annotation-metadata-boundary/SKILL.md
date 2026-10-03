---
name: annotation-metadata-boundary
description: "Repair Python AST analysis that treats Annotated metadata as forward type annotations while preserving genuine type checks and ordinary expression traversal."
---

# Annotation metadata boundary

## Activation and exclusions

Activate when public evidence shows a Python analyzer interpreting metadata in `Annotated[type, metadata, ...]` as a forward type annotation, such as a syntax diagnostic for `'>1'`.

First inspect the current implementation. The construct's name alone does not establish applicability. Clarify if the public diagnostic or reproduction is missing.

Do not activate for runtime metadata validation, unrelated parser failures, requests to suppress all diagnostics inside `Annotated`, or non-Python interfaces without a supported realization. This history does not establish arbitrary alias resolution or cross-project transfer.

## Operations

- [Inspect](references/actions/inspect.md) the current subscript traversal, annotation-state controller, AST representations, and public symptom.
- [Repair](references/actions/repair.md) the positional boundary: retain the first argument's existing context and visit metadata in ordinary-expression state.
- [Validate](references/actions/validate.md) the reproduction, genuine forward references, nesting, and adjacent traversal.

See the [historical Workflow](references/workflow.md), [episode](references/episode.md), and [provenance](references/provenance.json). Historical paths are evidence, not current owner bindings.

## Current binding requirements

Before editing, establish a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Resolve semantic owners and aliases in the current checkout before checking read/write conflicts. Ports must agree in semantic role, artifact kind, language, scope, phase, and state.

For each Oracle, bind `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Use semantic check key `oracle:<action_id>:<source_oracle_id>`. Render those bound commands before execution. Empty command arrays in this package are unbound placeholders, not execution authorization.

Checks are PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject a repair plan. Structural PASS predicts compatibility, not repair success. Refresh stale observations after changes and execute public validation. Independent hidden acceptance occurs only after the solver stops; hidden or gold-derived commands do not enter guidance.

## Preservation and stop conditions

Preserve genuine first-argument forward-reference diagnostics, ordinary metadata expression analysis, surrounding annotation state, existing `Literal` behavior, target/context traversal, and fallback traversal for non-multi-argument forms.

Stop if current recognition semantics conflict with the historical terminal-name approach, state restoration is unsafe, supported AST shapes remain unknown, or checks reveal lost diagnostics. Do not broaden suppression or invent an adapter.

## Evidence limits

One independently verified repair supports this Workflow, not a Pattern. Historical tests are assertions available at the commit; supplied evidence contains no historical execution log.

The later qualification attestation reports two fail-to-pass and forty pass-to-pass cases in changed test files with original-base control. Whole-project regression and cross-project transfer are untested. This post-cutoff attestation is provenance, not backdated knowledge.

Evaluation definitions are **not_executed**: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json).

Formal knowledge and checkpoints remain frozen. Never publish a current task plan as newly verified historical knowledge during formal evaluation. Time-reconstructed catalogs exclude their own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.
