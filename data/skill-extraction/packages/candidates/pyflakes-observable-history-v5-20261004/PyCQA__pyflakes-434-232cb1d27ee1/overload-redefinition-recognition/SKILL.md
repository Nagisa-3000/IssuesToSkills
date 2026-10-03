---
name: overload-redefinition-recognition
description: "Repair false unused-redefinition diagnostics for Python typing.overload declarations when recognition checks only the immediate scope or requires a single decorator."
---

# Overload redefinition recognition

## Activation and exclusions

Activate when a Python static analyzer incorrectly reports unused redefinitions for repeated `typing.overload` declarations followed by an implementation, particularly inside a class or with additional decorators.

Confirm one or both evidenced defects:

- Name-form decorator recognition searches only the immediate scope, missing an enclosing typing import.
- Recognition requires exactly one decorator instead of inspecting every decorator.

Clarify when decorator identity, diagnostic ownership, or the scope model is unknown. Do not activate for ordinary repeated definitions, a decorator merely named `overload`, runtime dispatch failures, or unrelated binding-lifecycle defects.

This is a focused Workflow supported by one verified historical repair, not a cross-project Pattern.

## Current probes and semantic bindings

Use [inspection](references/actions/inspect.md) to locate these owners in the current public checkout:

- **overload-recognition**: decides whether an existing function binding represents a typing overload.
- **unused-redefinition-reporting**: emits unused-redefinition diagnostics.
- **type-annotation-regressions**: owns public overload diagnostic tests.

Inspect scope-stack order, import-binding representation, supported decorator AST shapes, and the reporting call site. Establish whether the gate examines the previous binding. Historical paths in [the episode](references/episode.md) are context, not current bindings.

Record a current TaskContext with the public issue, pinned base, hashed anchors, observed facts, evidence-backed semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

## Operations

After applicability is established:

1. Apply [recognition repair](references/actions/repair.md): resolve names innermost first, stop at the first binding, and accept only the supported import identity for `typing.overload`.
2. Inspect all decorators with existential recognition rather than requiring exactly one.
3. Pass the scope stack from the reporting owner while continuing to inspect the existing binding.
4. Add [focused regression assertions](references/actions/regressions.md).
5. Retain [explicit validation](references/actions/validate.md) for both modifying Actions.

Preserve nearest-binding shadowing, ordinary redefinition reporting, the function-source guard, and existing attribute-form recognition. Do not infer support for async functions, other typing modules, arbitrary qualified expressions, or new binding representations from this evidence.

Use the [historical Workflow](references/workflow.md) as a dependency model, not a claimed historical execution sequence. Current ordering follows compatible ports, observed prerequisites, semantic dependencies, and verification. An operation may be omitted only when its effect is already established or it is demonstrably inapplicable; retain verification closure for every modification.

## Validation and stopping

Bind and render current public commands before execution. Empty command arrays in historical contracts do not authorize skipping validation.

Run class-local and multiple-decorator regressions, surrounding annotation tests, and preservation probes for ordinary redefinitions, non-typing lookalikes, nearest-binding shadowing, existing attribute recognition, and both decorator positions.

Use PASS/FAIL/UNKNOWN checks. Unknown prerequisites authorize probes only. Hard applicability failures reject the plan. Failed preservation checks or incompatible owners stop this repair pending investigation. Refresh observations invalidated by edits. Structural PASS predicts compatibility, not repair success.

Record exact execution scope. Obtain independent hidden acceptance only after the solver stops; hidden or gold-derived commands never enter this guidance.

## Evidence and limits

See [provenance](references/provenance.json) and [historical evidence](references/episode.md). Historical regression assertions were available at the repair commit; historical command execution is unknown.

A supplied later qualification attestation reports two fail-to-pass and fifteen pass-to-pass cases, limited to changed test files with an original-base control. Whole-project regression and cross-project transfer are untested. This attestation is not a backdated historical event or pre-cutoff learned content.

All evaluation definitions are **not_executed**. Current plans and observations are not newly verified historical knowledge and must not be published as such during formal evaluation. Keep formal knowledge and checkpoints frozen. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
