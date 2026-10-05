---
name: optional-export-inference-guard
description: "Contain a Python static analyzer crash when module __all__ exists in locals but its value cannot be inferred, using a narrow inference-failure guard while retaining undefined-variable diagnostics and successful export checks."
---

# Optional export inference guard

Canonical Skill and Workflow ID: `workflow:verified-history:9a3cbe2612faf6a1d7c341e8`.

This is a conditional, source-grounded Workflow supported by one historical repair. It is not a cross-project Pattern.

## Activation and exclusions

Activate when public evidence establishes all of the following:

- A Python static analyzer discovers `__all__` in module locals.
- Its optional module-export check consumes an inferred value for that name.
- Consumption raises the inference library's documented inference-failure exception and produces a fatal analyzer error.

A minimal public probe is `__all__ += []` without a preceding definition. Presence in locals does not guarantee successful inference.

Clarify a report that mentions only “undefined variable” or “inference failed”: request a public reproduction and traceback. Do not activate for an ordinary undefined-variable diagnostic without a crash, a failure after successful inference, an unrelated subsystem, or a non-Python interface.

## Current evidence and binding

Create a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, tri-state semantic checks, actual owner bindings, observed PortValues where applicable, and current Oracle bindings.

Locate these owners in the current checkout:

- `module-export-checker`: the optional checker consuming inferred module exports.
- `export-regression-suite`: public fixtures and diagnostic expectations for module exports and undefined variables.

Use [Inspect](references/actions/inspect.md) to establish the exact failing expression, exception type, successful path, and test convention. Historical paths in the [episode](references/episode.md) are reference locators, not current bindings.

UNKNOWN prerequisites authorize probes only. A hard FAIL rejects the proposed mechanism. Matching names alone do not establish semantic applicability.

## Operations

The [historical Workflow](references/workflow.md) connects these operations:

1. [Inspect the boundary](references/actions/inspect.md).
2. [Guard inference consumption](references/actions/guard.md).
3. [Add the minimal regression](references/actions/regression.md).
4. [Validate both edits](references/actions/validate.md).

Catch only the documented inference-failure exception around the inference-consumption expression. Return from the optional export check on that failure. Preserve existing uninferable-sentinel handling, subsequent successful-value checks, and independent undefined-variable diagnostics.

The implementation edit and regression edit can follow inspection independently. Both precede validation. Current ordering follows semantic prerequisites and verification dependencies, not historical list position. Omit an operation only when current evidence already establishes its effect; keep explicit validation for every retained modifying operation.

## Validation and execution boundary

For every Oracle, bind `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty command arrays in historical contracts require current binding; they do not authorize an invented or historical command.

Observe the minimal regression, the applicable original reproduction, neighboring undefined-variable cases, and valid list/tuple export behavior. An expected diagnostic may cause a nonzero linter exit; distinguish that from a fatal analyzer error.

Edits invalidate the freshness fact `public-validation-observed`, not the behavior assurances. Refresh that observation only after the required checks pass. Record skips as untested, not passed.

[Functional evaluations](evals/functional-cases.json) are definitions with status **not_executed**. Structural plan PASS predicts compatibility, not repair success. Independent hidden acceptance, if available, occurs after the solver stops and must not supply guidance.

## Stop conditions and limits

Stop if the exception type or boundary differs, an early return would discard required diagnostics, owner bindings remain uncertain, or available public checks cannot establish preserved behavior. Do not broaden the handler to `Exception`, accept a fatal error in diagnostic expectations, or modify unrelated inference machinery.

Historical CI/test execution is **unknown**; the supplied historical evidence contains committed assertions, not historical test-run results. Later independent qualification covers `changed-test-files-with-original-base-control` only. Its exact limits are: **Changed test files only; whole-project regression and cross-project transfer are untested.**

See [provenance](references/provenance.json) and the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression](references/evidence/regression.md) evidence cards.

Formal knowledge and checkpoints stay frozen during evaluation. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before its input time. Do not publish a current task plan as newly verified historical knowledge.
