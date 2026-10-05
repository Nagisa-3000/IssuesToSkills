---
name: annotation-feature-detection
description: "Conditionally repair alias-sensitive postponed-annotation detection in a Python static analyzer by using canonical module future-feature metadata instead of local namespace bindings."
---

# Alias-independent annotation feature detection

## Activation and exclusions

Activate when current public evidence shows all of the following:

- An aliased `annotations` future import causes spurious undefined-variable or used-before-assignment diagnostics in annotations.
- The corresponding unaliased import does not cause those diagnostics.
- The analyzer detects the feature through a local binding named `annotations`, rather than canonical module future-feature metadata.

If the symptom matches but the detector or metadata semantics are unknown, probe first. Do not authorize edits from symptom similarity alone.

Do not activate for ordinary runtime undefined names, invalid future-import syntax, unrelated import alias handling, or a detector already using correct canonical metadata. This is a single-source Workflow, not a general cross-project Pattern.

## Current context and probes

Record the public issue, pinned base, hashed code anchors, observed facts, current semantic owner bindings, PortValues, and public oracle bindings.

Locate these owners in the current checkout:

- `annotation-feature-detector`: decides whether postponed annotation evaluation is enabled.
- `module-feature-metadata`: exposes canonical future-feature names for a module.
- `annotation-regression-suite`: owns annotation diagnostic assertions and collection configuration.

Run the [probe](references/actions/probe.md). Inspect the actual metadata produced by aliased, unaliased, and absent future imports. A familiar attribute name does not prove compatible semantics.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only; hard incompatibility rejects the plan. Each current oracle must bind `action_id` and `source_oracle_id` to a public instruction, argv command, and current evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before executing them. Empty command arrays in source contracts are placeholders, not execution authorization.

## Linked operations

1. [Discriminate the mechanism](references/actions/probe.md).
2. [Repair the semantic detector](references/actions/repair.md).
3. [Add focused regression assertions](references/actions/regression.md).
4. [Validate both edits and adjacent behavior](references/actions/validate.md).

The [Workflow](references/workflow.md) declares dependencies and assurances. Current ordering follows semantic prerequisites, compatible ports, and verification dependencies, not merely list position. Already-satisfied operations may be omitted only with current evidence. Retain the validate Action for every modification performed.

## Validation and stopping

Require actual collection and execution of the four alias-specific annotation cases: containing-class return, later-class parameter, later-class attribute, and self-referencing attribute. Require no spurious target diagnostics in those positions.

Also check unaliased imports, absent-feature behavior, and an ordinary runtime undefined-name control. These are current safety obligations, not claims that every control was present in the historical committed fixture.

Stop if:

- Canonical metadata is unavailable or alias-sensitive.
- The current reproduction has a different mechanism.
- The detector is already correct.
- A target case is missing or skipped.
- Adjacent behavior regresses.
- A prerequisite or public oracle cannot be bound.

Do not suppress diagnostics globally, rename the user's alias, or invent an unsupported bridge. Refresh stale observations after edits. Distinguish a behavior assurance from the freshness of a validation observation.

Structural plan PASS predicts compatibility, not repair success. Run public checks and record actual results. Independent hidden acceptance occurs after the solver stops; hidden tests must not enter guidance. Keep formal knowledge and checkpoints frozen.

## Evidence and limits

Read the [episode](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical CI and test execution are unknown. The repair commit supplies implementation and committed regression assertions. Separately supplied qualification, checked in 2026, establishes one fail-to-pass and seven pass-to-pass outcomes within changed-test-files-with-original-base-control scope; one selected control was skipped. It does not establish whole-project correctness, cross-project transfer, or execution of this Skill's eval definitions.

For time-reconstructed admission, exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. This repair is not prior knowledge for its own issue.
