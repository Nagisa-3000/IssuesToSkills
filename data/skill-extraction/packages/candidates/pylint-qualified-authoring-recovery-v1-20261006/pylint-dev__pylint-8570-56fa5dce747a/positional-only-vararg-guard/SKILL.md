---
name: positional-only-vararg-guard
description: "Repair a signature diagnostic that mistakes defaulted positional-only parameters before varargs for keyword-capable parameters, while preserving mixed-signature warnings."
---

# Positional-only vararg guard

## Activation and exclusions

Activate when a Python signature checker emits a keyword-before-varargs warning for a signature like `def f(option=True, /, *args): ...`, and current inspection confirms that its emission gate considers varargs and defaults without excluding a positional-only-only prefix.

Clarify when the diagnostic identity, argument partitions, or checker owner are unknown. Do not activate for runtime call errors, unrelated diagnostics, or a checker that already excludes this case. A positional-only marker alone is not sufficient: mixed signatures can still legitimately receive the warning.

## Current probes and linked operations

1. [Inspect the boundary](references/actions/inspect.md): locate the current diagnostic owner, establish argument-partition semantics, and reproduce the public false positive.
2. [Repair the narrow condition and regression assertions](references/actions/repair.md): inside the existing vararg/default gate, exclude signatures with positional-only parameters and no positional-or-keyword parameters.
3. [Validate target and adjacent behavior](references/actions/validate.md): execute the supported signature matrix and existing ordinary diagnostic controls.

The [workflow](references/workflow.md) records the historical mechanism and dependencies. The [episode](references/episode.md), [evidence cards](references/evidence/regression.md), and [provenance](references/provenance.json) distinguish historical assertions from later source qualification.

## Binding and conditional execution

Construct a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve semantic owners in the current checkout rather than assuming historical paths.

Bind each Action/source-oracle pair to a current public instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty command arrays in the historical contracts require current binding; they do not authorize an inferred command.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only; hard failures reject the plan. Confirm all port dimensions and actual semantic compatibility. A structural PASS predicts compatibility, not repair success. After modification, refresh stale validation observations while retaining behavior-preservation requirements.

## Validation and stop conditions

Require the target warning for the three mixed signatures and no target warning for the five positional-only-prefix signatures documented in [the regression evidence](references/evidence/regression.md). Preserve ordinary positional-or-keyword diagnostic behavior. Where the current implementation shares its visitor with async definitions, check equivalent async signatures; this is an additional current probe, not a historically executed fixture.

Stop or re-scope if the current AST semantics differ materially, the reproduction does not match the mechanism, the narrow guard already exists, mixed-signature warnings disappear, or public checks fail. Do not broaden the repair to suppress every signature containing `/`.

## Limits and learning boundary

This is one focused historical Workflow, not a cross-project Pattern or a general default-to-parameter mapping algorithm. Historical regression assertions were committed; historical test/CI execution is unknown.

Later qualification covers exactly `changed-test-files-with-original-base-control`. Its limits are: `Changed test files only; whole-project regression and cross-project transfer are untested.` It does not execute this Skill's functional cases, which remain `not_executed`.

Keep formal knowledge and checkpoints frozen. Obtain independent hidden acceptance after the solver stops; hidden tests must not shape guidance. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and any discovery input unavailable before query time.
