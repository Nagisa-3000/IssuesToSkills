---
name: enclosing-scope-return-annotations
description: "Repair duplicate or incorrectly scoped return-annotation traversal when a Python static analyzer reports an enclosing-class annotation name as undefined, while retaining diagnostics for names defined only inside the function body."
---

# Enclosing-scope return annotations

## Activate conditionally

Use this Skill when a Python static analyzer incorrectly reports a class-defined name used in a method's return annotation as undefined, and current inspection indicates that the return annotation is traversed again after entering function scope.

The historical trigger was a class-level `TypeVar` used in both a parameter annotation and a return annotation. The transferable mechanism is **excluding a return annotation from a later function-scope child traversal when it already receives appropriate enclosing-scope handling**. It is not a general exemption for type names.

Do not activate solely because an undefined-name diagnostic mentions an annotation. Clarify or probe when the traversal owner, annotation evaluation model, or original diagnostic location is unknown.

## Exclusions

Do not apply this repair if:

- The name is genuinely absent from the annotation's applicable enclosing scope.
- There is no existing appropriate annotation-processing path.
- The current analyzer intentionally uses a materially different annotation model.
- The proposed change would make a function-body assignment visible to its own return annotation.
- The issue concerns runtime evaluation, type inference, or unrelated forward-reference handling rather than analyzer traversal.

## Current probes and operations

1. Bind the semantic owners for function traversal and annotation regression tests in the current public checkout. Use [inspect](references/actions/inspect.md).
2. Confirm both the reported false positive and the negative control: a name assigned only inside the function body must remain undefined in its return annotation.
3. If the mechanism matches, use [repair](references/actions/repair.md) to exclude return annotations from the function-scope re-traversal and add paired regressions.
4. Use [validate](references/actions/validate.md) after the edit. Refresh all observations invalidated by the repair.

These are conditional instructions, not claims that any current checkout has been inspected or repaired. Historical paths and assertions are documented in [the episode](references/episode.md); the canonical action dependencies are in [the workflow](references/workflow.md).

## Current binding and validation

Before execution, obtain a public TaskContext with the pinned base, hashed code anchors, observed facts, semantic checks, resolved owner bindings, observed PortValues, and current Oracle bindings. Each bound Oracle must map its Action ID and source Oracle ID to a current public instruction, an argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`.

Render the bound current commands before execution. Historical examples are evidence, not permission to execute a command in an unbound checkout. No deterministic oracle script is supplied.

Use PASS / FAIL / UNKNOWN:

- UNKNOWN prerequisites authorize inspection/probes only.
- A failed mechanism or behavior prerequisite rejects this repair.
- Structural PASS predicts compatibility, not successful repair.
- Repair success requires observed public validation; formal evaluation additionally requires independent hidden acceptance after the solver stops.

## Required preservation and stop conditions

Preserve diagnostics for genuinely undefined return-annotation names, especially names assigned only in the function body. Preserve ordinary function-body checking and existing decorator handling.

Stop if the return annotation would become unchecked, if enclosing-scope handling cannot be established, if the negative control stops reporting an undefined name, or if adjacent annotation tests fail. Do not suppress the diagnostic globally or introduce class-scope visibility into ordinary method-body name resolution.

## Evidence and limits

This is a single-repair Workflow, not a Pattern or a cross-project template. Its historical evidence supports a small traversal omission and two regression assertions. It does not establish support for every Python annotation mode.

The supplied later qualification reports one fail-to-pass and seventeen pass-to-pass results in changed test files with original-base control. Whole-project regressions and cross-project transfer were not tested. That qualification is a contemporary provenance attestation, not a historical execution event. This package's eval definitions remain `not_executed`.

See [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), and [functional cases](evals/functional-cases.json).
