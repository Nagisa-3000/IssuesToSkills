---
name: conditional-synthetic-binding
description: "Repair doctest analysis that inserts a synthetic underscore binding despite an existing module-level underscore binding, causing source-less binding traversal to crash."
---

# Conditional synthetic binding

## Activation

Activate when public evidence in the current checkout indicates all of the following:

- A Python static analyzer processes doctest examples in a temporary scope.
- The analyzer supplies a synthetic `_` binding for interactive/doctest semantics.
- A module-level `_` binding can already exist.
- Inserting the synthetic binding collides with that existing binding and reaches code that expects an AST-backed source.

Typical symptoms include an `AttributeError` while traversing `.parent` from a source-less synthetic binding. The historical report involved an import aliased to `_` and doctest checking enabled.

Clarify or probe if the failure path, module scope, or synthetic binding owner is unknown. Do not activate merely because a traceback mentions `None`, `.parent`, or `_`.

## Exclusions

This Skill does not establish a repair for:

- General AST-parent corruption unrelated to synthetic binding insertion.
- Runtime doctest execution failures.
- Arbitrary collisions involving other names or other scope models.
- A design in which an existing module binding is intentionally replaced by the doctest placeholder.

The evidence supports one narrowly scoped Workflow, not a cross-project Pattern.

## Current probes and operations

1. [Locate and diagnose the collision](references/actions/probe.md). Resolve semantic owners in the current checkout; inspect the doctest scope setup, module scope lookup, and binding insertion path. Use a public reproduction to distinguish this mechanism from unrelated failures.
2. [Guard insertion and add a regression](references/actions/repair.md). Insert the synthetic `_` only if `_` is absent from the module scope. Add a regression asserting that an unused module import aliased to `_` still produces the ordinary unused-import diagnostic rather than a crash.
3. [Validate the repair](references/actions/validate.md). Run the new regression and the relevant doctest test file, and check the absent-module-binding path and ordinary diagnostics.

These operations are conditional on current evidence, not permission to transplant historical paths or commands unchanged.

## Current binding and execution discipline

Before execution, construct a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, resolved owner bindings, observed PortValues, and current Oracle bindings.

For each Oracle, bind `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render those bound commands before execution. Historical commands in the references are evidence only.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize diagnosis only, not editing. A hard prerequisite failure rejects the repair plan. Structural PASS predicts compatibility, not repair success. After editing, refresh stale observations and execute the public checks. Independent hidden acceptance, if required by the host, occurs after the solver stops; hidden checks are not guidance.

## Validation and stop conditions

The repair must:

- Avoid a crash with a module-level import aliased to `_`.
- Preserve the unused-import diagnostic when the import is unused.
- Preserve synthetic `_` availability when no module-level `_` exists.
- Preserve adjacent doctest analysis and scope behavior.

Stop and reassess if the binding owner cannot be resolved, the collision mechanism differs, the guard changes required name-resolution semantics, or any preservation check fails. An unexecuted check remains UNKNOWN.

## Evidence and limits

See the [episode](references/episode.md), [historical Workflow](references/workflow.md), and [provenance](references/provenance.json).

The supplied implementation and regression assertions were available before the cutoff. Historical test execution results were not supplied. A later qualification attestation reports one fail-to-pass and 229 pass-to-pass cases within changed test files only; whole-project regression and cross-project transfer are untested. That attestation is not backdated historical knowledge.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions only and remain `not_executed`.
