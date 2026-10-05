---
name: guarded-call-argument-access
description: "Prevent an analyzer crash when a specialized Python AST check indexes the first positional argument of an empty call, using a short-circuit eligibility guard and a focused regression."
---

# Guarded call argument access

Use this Workflow when a Python static-analysis checker assumes that a recognized call has at least one positional argument, and public evidence shows an empty call reaching an unchecked `args[0]` access.

This is a single-source, conditional Workflow, not a cross-project Pattern. Its historical support concerns an `enumerate()` loop and a list-index refactoring check. Broader transfers require current evidence.

## Activation and exclusions

Activate when:

- A public reproduction contains an empty call in a loop analyzed by a specialized checker.
- A traceback or current code review identifies first-positional-argument access without a preceding nonempty-arguments guard.
- The intended behavior is to skip an inapplicable optimization/refactoring check rather than crash the analyzer.

Clarify when the crash location, AST representation, or intended checker behavior is unknown. Probe before proposing an edit.

Do not activate for a runtime error in the user's program alone, parser failures, unrelated indexing, or requests to make an invalid empty call execute successfully. This repair does not make `enumerate()` without arguments valid Python runtime behavior.

## Current probes and bindings

Build a current TaskContext from the public issue and pinned checkout. Record hashed code anchors, observed facts, semantic checks, concrete owner bindings, observed PortValues, and public Oracle bindings. Locate these semantic owners rather than assuming historical paths:

- `call-eligibility-checker`: the specialized AST checker that reads the first positional argument.
- `checker-regression-fixture`: the fixture and harness covering that checker.

Use [Inspect eligibility](references/actions/inspect.md) without changing files. Confirm that an early return for empty arguments is appropriate and that valid-call handling must remain unchanged.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize inspection only; a hard mismatch rejects this Workflow. Matching role names alone does not establish applicability.

## Operations

1. [Inspect eligibility](references/actions/inspect.md).
2. [Guard first-argument access](references/actions/guard.md).
3. [Add the empty-call regression](references/actions/regression.md).
4. [Validate both edits and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records source-supported dependencies. A current plan may omit an already-satisfied edit only after recording why it is satisfied; it must still validate the resulting behavior.

Before execution, bind each Oracle to a current public instruction, an argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the actual bound commands in the current plan. Empty command arrays in the historical contracts mean that current binding is required, not that validation has run.

## Validation and stopping

Analyze the empty-call reproduction without executing the invalid program as the success criterion. Require no analyzer `IndexError` or fatal analysis failure from the targeted checker. Run the current regression harness and adjacent valid-call cases, checking that existing diagnostic expectations remain unchanged.

Stop if:

- The argument container or AST semantics differ from the historical mechanism.
- Empty positional arguments do not justify skipping the specialized check.
- The crash comes from another owner.
- A guard changes valid-call diagnostics unexpectedly.
- Public validation cannot run or its outcome remains UNKNOWN.

After edits, refresh stale observations. Structural plan PASS predicts compatibility, not repair success. Do not report completion until public checks have actually passed; obtain independent hidden acceptance only after the solver stops.

## Evidence and limits

See [episode](references/episode.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression assertion](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical test execution is unknown. A later independent qualification reproduced the failure and verified the historical fix within the exact scope `changed-test-files-with-original-base-control`. Its limits are: `Changed test files only; whole-project regression and cross-project transfer are untested.` That replay did not execute this Skill's [functional definitions](evals/functional-cases.json).

During formal evaluation, keep knowledge and checkpoints frozen; do not publish a task plan as newly verified historical knowledge. Earlier-query catalogs must exclude this source's own issue, fix, cluster, aliases, copied sources, and all inputs unavailable before the query time.
