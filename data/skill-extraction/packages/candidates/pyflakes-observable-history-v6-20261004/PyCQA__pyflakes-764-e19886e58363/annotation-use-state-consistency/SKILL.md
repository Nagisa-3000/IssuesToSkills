---
name: annotation-use-state-consistency
description: "Repair a Python static analyzer when annotation-only name loads record boolean usage state but downstream scope-sensitive stores require structured usage metadata."
---

# Annotation usage-state consistency

## Activation

Activate when a Python static analyzer crashes while checking an annotation-only name that is loaded in an outer scope and subsequently assigned in a nested function, and current inspection shows an inconsistent usage-state representation.

The historical signature was `TypeError: 'bool' object is not subscriptable`: an annotation load set a binding's `used` field to `True`, while a later store indexed that field to recover its scope.

Clarify when the exception matches but the binding producer, consumer, or triggering scope relationship has not been located. Do not activate merely because a program contains annotations, reports an undefined name, or uses a boolean field. Do not apply this repair to an analyzer whose usage-state contract intentionally uses booleans or a different structured representation.

## Current probes and operations

1. [Inspect the usage-state producer and consumer](references/actions/inspect.md). Locate their semantic owners in the current checkout. Confirm the annotation-only load branch, postponed-annotation guard, and downstream scope-sensitive consumer.
2. [Repair metadata and add regression coverage](references/actions/repair.md). Apply only after the current representation and branch semantics are confirmed. Preserve the guard and control flow; record both the current scope and load node rather than a truthy sentinel.
3. [Validate the candidate](references/actions/validate.md). Bind public checks to the current checkout, execute them, and record results. Definitions and historical assertions are not execution results.

See the [canonical Workflow](references/workflow.md) and [historical episode](references/episode.md).

## Current binding requirements

Before execution, create a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before checking read/write conflicts.

For each Action oracle, bind `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before running them. This package supplies no pre-authorized current command.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites permit inspection only; a hard representation or branch mismatch rejects the repair. A structurally compatible plan predicts compatibility, not successful repair.

## Validation and preservation

The reproducer must finish analysis without the boolean-subscript crash while reporting both:

- the annotation-only outer name as undefined when loaded;
- the nested assignment as an unused local.

Check neighboring annotation cases, including postponed annotations, against current repository expectations. Refresh stale validation observations after every edit. Preserve undefined-name reporting, unused-local reporting, and unrelated annotation branch behavior across the plan.

Every modifying operation retains its explicit validation Action. If checks fail or adjacent behavior changes, stop and inspect rather than broadening this narrow repair automatically.

## Evidence and limits

This is a single-repair Workflow, not a cross-project Pattern. Historical paths and assertions appear only in references. The historical merged change and regression assertion were available before the cutoff; historical test execution is not supplied.

A later qualification attestation reports one fail-to-pass case and 43 pass-to-pass cases in changed test files with original-base control. It does **not** establish whole-project regression safety or cross-project transfer, and is not backdated learned content. Functional evaluations here remain `not_executed`.

Formal knowledge and checkpoints stay frozen during evaluation. Do not publish a current task plan as newly verified historical knowledge. Time-reconstructed training use must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. Independent hidden acceptance belongs after the solver stops and is not a source for public guidance.
