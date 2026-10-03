---
name: conditional-doctest-placeholder
description: "Conditionally initialize a synthetic doctest underscore binding when a module-level underscore binding already exists, preventing source-less binding collisions while preserving diagnostics."
---

# Conditional doctest placeholder initialization

Use this Workflow when a Python static analyzer initializes a synthetic `_` binding for doctests and an existing module-level `_` binding makes that initialization enter an unsafe binding-collision path.

## Activation

Activate when current public evidence establishes all of the following:

- Doctest analysis is enabled.
- The doctest initializer inserts a source-less synthetic `_` binding.
- The module scope may already contain `_`.
- A reproduction or code review connects that insertion to a collision path that assumes an AST source exists.

Ask for clarification or probe when the scope owner, initialization behavior, or collision mechanism is unknown. Do not activate merely because an exception mentions `None.parent`.

Do not apply this repair to unrelated AST-parent defects, general name-shadowing policy, runtime doctest execution, or analyzers with different scope semantics. One verified repair supports this Workflow; it does not establish a cross-project Pattern.

## Current probes and bindings

Start with [locate and reproduce](references/actions/locate.md). Resolve these semantic owners in the current public checkout:

- `doctest-initializer`: doctest scope setup and synthetic binding initialization.
- `binding-collision-handler`: binding replacement logic and source traversal.
- `doctest-regression-tests`: public tests exercising doctest analysis.

Use a pinned base and hashed code anchors. Record current observed facts, real owner bindings, PortValues, and PASS/FAIL/UNKNOWN semantic checks. Historical paths are documented in [the episode](references/episode.md), not supplied as current bindings.

UNKNOWN prerequisites authorize probes only. A hard applicability failure rejects this Workflow.

## Operations

The [canonical Workflow](references/workflow.md) connects:

1. [Locate and reproduce](references/actions/locate.md).
2. [Guard synthetic initialization](references/actions/guard.md).
3. [Add the collision regression](references/actions/regression.md).
4. [Validate both modifications](references/actions/validate.md).

Skip an operation only when current evidence establishes that its required effect is already satisfied. Keep validation in the closure of every retained modifying operation.

The supported mechanism is narrow: consult the module scope before inserting the synthetic `_`. If the module already defines `_`, skip that insertion. Do not replace this with a broad exception handler or a general relaxation of AST-parent traversal.

## Validation and stop conditions

Bind each Oracle to current public instructions and argv commands before execution. Record the semantic check as `oracle:<action_id>:<source_oracle_id>`. Historical commands are evidence only, not current execution authorization.

Check that:

- The public reproduction completes without the source-less binding crash.
- The imported `_` remains eligible for the ordinary unused-import diagnostic when the doctest does not use it.
- Existing doctest behavior, including initialization when the module has no `_`, remains intact.

Stop if `_` belongs to a different scope than assumed, skipping insertion changes required diagnostics, the collision has another cause, or current validation fails. Refresh observations invalidated by edits.

Structural plan PASS predicts compatibility, not repair success. Execute public validation; independent hidden acceptance, if available, occurs after the solver stops. Never publish the current task plan as newly verified historical knowledge.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and the [implementation evidence](references/evidence/fix.md).

The historical regression is an assertion present at the repair commit; supplied evidence does not establish its historical execution. A later qualification reports one fail-to-pass and 229 pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer are untested. That qualification is a contemporary provenance attestation, not a pre-cutoff event.

Evaluation definitions are unexecuted:

- [Activation cases](evals/activation-cases.json)
- [Applicability cases](evals/applicability-cases.json)
- [Functional cases](evals/functional-cases.json)
