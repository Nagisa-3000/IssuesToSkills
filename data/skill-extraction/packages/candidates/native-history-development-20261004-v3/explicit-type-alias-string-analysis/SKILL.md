---
name: explicit-type-alias-string-analysis
description: "Repair false unused-import diagnostics for quoted explicit TypeAlias values by conditionally reusing existing annotation analysis while preserving ordinary assignment-value processing."
---

# Explicit type-alias string analysis

## Conditional activation

Activate when public evidence from a Python static analyzer shows all of the following:
- an imported type is incorrectly reported unused when referenced inside a quoted value of an explicit `TypeAlias` annotated assignment;
- the same reference is correctly recognized inside an ordinary quoted annotation;
- the current analyzer has scope-aware typing-marker recognition and reusable annotation-string processing.

Example: `PathLikeStr: TypeAlias = "PathLike[str]"` incorrectly leaves imported `PathLike` unused.

Clarify or probe when the marker identity, current dispatch, or comparison behavior is unknown. Do not activate for arbitrary string assignments, unrelated unused imports, runtime alias evaluation, or Python `type` statements. Repository identity alone is not an activation condition.

## Current probes and bindings

Use [inspect dispatch](references/actions/inspect-dispatch.md). Locate these semantic owners in the current public checkout:
- `annotated-assignment-handler`;
- `typing-marker-resolver`;
- `annotation-value-handler`;
- `annotation-regression-tests`.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings. Historical paths in [the episode](references/episode.md) are reference locators, not current bindings.

Evaluate prerequisites as PASS, FAIL, or UNKNOWN. UNKNOWN permits probes only. A failed semantic prerequisite rejects the repair plan; matching predicate names alone do not establish applicability.

## Operations

1. [Inspect dispatch](references/actions/inspect-dispatch.md).
2. [Modify alias-value routing](references/actions/route-alias-value.md).
3. [Add regression assertions](references/actions/add-regressions.md).
4. [Validate both modifications](references/actions/validate-regressions.md).

The [canonical Workflow](references/workflow.md) specifies dependencies. Current ordering follows observed ports, prerequisites, semantic dependencies, and verification obligations, not merely list position. Already-satisfied operations may be omitted only with current evidence; modifying Actions retain their explicit validation closure.

## Validation and stopping

Bind each Oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty command arrays in historical contracts are unbound, not executable success claims.

Require observable checks for:
- quoted and unquoted aliases at module and class scope;
- no-value declarations, including an unrelated import that must remain unused;
- preserved target and marker processing;
- unchanged ordinary non-`TypeAlias` value dispatch;
- the public reproduction and existing annotation tests.

Refresh observations invalidated by edits. Stop or revise on failed adjacent behavior, unresolved marker identity, or unavailable validation. Never broaden annotation treatment to all annotated assignment values.

Structural PASS predicts compatibility, not repair success. Execute public checks and report their scope. Independent hidden acceptance occurs after the solver stops and supplies no guidance here.

## Evidence and limits

This is one focused Workflow, not a Pattern or cross-project template. [Historical evidence](references/episode.md) supports one independent bug cluster and merged fix before the cutoff. Historical regression assertions are supplied; a historical test-run transcript is not.

The later [qualification attestation](references/provenance.json) reports one fail-to-pass and 51 pass-to-pass checks, limited to changed test files with an original-base control. Whole-project regression and cross-project transfer are untested. The attestation is provenance, not backdated learned content.

[Functional evaluation definitions](evals/functional-cases.json) remain `not_executed`. Formal knowledge and checkpoints remain frozen during evaluation. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
