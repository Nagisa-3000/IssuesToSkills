---
name: nonlocal-assignment-filter
description: "Repair a used-before-assignment false positive when exception-handler assignment filtering incorrectly treats an explicitly declared nonlocal name as a local binding."
---

# Nonlocal-aware assignment filtering

Use this conditional Workflow when a Python static analyzer reports a name as used before assignment inside a `try` block, although that same name is explicitly declared `nonlocal` in the current function frame and has an enclosing binding.

This Skill has one historical repair as support. It is not a cross-project Pattern.

## Activation and exclusions

Activate when public code and a reproduction indicate all of the following:

- A nested function explicitly declares the reported name `nonlocal`.
- The enclosing function initializes that name.
- The nested function reads it in a `try` block and assigns to it in an exception handler.
- The diagnostic appears to arise from exception-handler assignment filtering rather than actual missing initialization.

Clarify or probe if the declaration's frame, the enclosing binding, or the filtering owner is unknown. Do not activate merely because a function contains *some* nonlocal declaration: the declaration must name the queried variable.

Do not apply this repair to genuine local use-before-assignment, missing enclosing bindings, unrelated diagnostics, or an analyzer with a materially different scope representation without establishing compatible current semantics.

## Current probes and bindings

Before editing, establish a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, actual owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `assignment-filter`: name-resolution logic that filters candidate assignments associated with exception handlers.
- `scope-frame`: the API identifying the queried name's function frame and its declarations.
- `assignment-regression-suite`: public diagnostic fixtures and expected-message assertions.

Use [the inspection Action](references/actions/inspect.md) to confirm the name-specific declaration and the position of the exception-handler filter. Historical paths are reference material, not automatic current bindings.

Prerequisite checks are tri-state: PASS, FAIL, or UNKNOWN. UNKNOWN permits inspection only; a hard failure rejects the proposed edit. Matching predicate labels alone does not establish semantic compatibility.

## Operations

1. [Inspect the scope and filtering boundary](references/actions/inspect.md).
2. [Add the name-specific nonlocal guard and paired regression cases](references/actions/repair.md).
3. [Validate the repair and retained diagnostics](references/actions/validate.md).

The [historical Workflow](references/workflow.md) defines dependencies and retained assurances. Its operations are authored from the historical diff and assertions; it is not an execution log.

Render each current Oracle binding as `action_id/source_oracle_id`, its public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Historical commands do not authorize current execution. Bind commands to the actual public checkout before running them; do not use hidden or gold-derived tests.

## Validation and stopping

Require observable checks that:

- The declared nonlocal case no longer emits `used-before-assignment`.
- A declaration of an unrelated nonlocal does not suppress a genuine local diagnostic.
- Existing exception-handler and control-flow diagnostic fixtures retain their expected results.
- The guard preserves the candidate result produced by earlier resolution logic and is positioned before the relevant exception-handler filtering.

After edits, refresh validation observations. Stop if the declaration is not in the relevant frame, the query name does not match, the filtering mechanism differs, or adjacent diagnostics regress. Do not broaden the exemption to all names in a function containing `nonlocal`.

Structural plan compatibility is not proof of repair success. Execute public checks and record outcomes separately. Independent hidden acceptance, if required by the host, occurs after the solver stops. Do not publish a current task plan as newly verified historical knowledge during formal evaluation.

## Evidence and limits

See [the episode](references/episode.md), [provenance](references/provenance.json), and the packaged [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. The supplied later qualification independently replayed original-base, base-with-regression, and historical-fixed controls, with a consistent runtime hash. It supports the selected fixture's fail-to-pass result and retained selected tests, not whole-project correctness or transfer. Its declared scope is changed-test-files with original-base control; whole-project regression was not checked.

All authored [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) cases remain unexecuted. Freeze knowledge/checkpoints during formal evaluation. For earlier-time catalog use, exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before its input time.
