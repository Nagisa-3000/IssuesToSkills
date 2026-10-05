---
name: deferred-receiver-attribute-check
description: "Repair deferred Python AST private-member analysis that reads a name-only field from a recognized type(self) call receiver, including method-parameter recovery after traversal state is cleared."
---

# Deferred receiver attribute check

## Activation

Activate when a public reproduction shows deferred private-member analysis accessing a receiver's `.name` even though that receiver is a call such as `type(self)`.

Confirm that the current implementation has a compatible narrow type-call recognizer and a mandatory-method-parameter helper whose transient tracking can be empty during class-exit analysis. Symbol existence alone does not prove this semantic match.

Clarify when the public reproduction, traceback, pinned base or current owner bindings are missing. Do not activate solely on an unrelated `'Call' object has no attribute 'name'` error.

## Exclusions

Do not ignore all call receivers, swallow exceptions or disable the checker. The historical regression **retains** an `unused-private-member` warning on the classmethod assignment despite the `type(self)` read. A different diagnostic policy, AST library, dynamic receiver inference or shadowed `type` semantics requires separate evidence.

## Operations

1. [Probe receiver shape and deferred state](references/actions/probe.md).
2. [Repair the narrow guard, parameter fallback and regression](references/actions/repair.md).
3. [Validate the public reproduction and adjacent behavior](references/actions/validate.md).

Resolve semantic owners in the current checkout. Historical paths in [the episode](references/episode.md) are not automatic current bindings. The [historical Workflow](references/workflow.md) is a sourced procedure, not an executed current task plan.

## Current execution discipline

Construct a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual bindings, observed PortValues and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a current public instruction, argv command and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render those bound commands before execution. Empty command arrays in source contracts require binding; they do not authorize skipping validation. Historical commands remain historical evidence.

Checks are PASS, FAIL or UNKNOWN. UNKNOWN prerequisites permit probes only; hard semantic failures reject this repair. Structural PASS predicts compatibility, not repair success. After edits, refresh stale validation observations and retain the explicit validation Action.

## Validation and stopping

Require:
- no receiver `.name` AttributeError or fatal checker error in the public reproduction;
- the regression assignment still receives its expected unused-private-member diagnostic;
- live first-parameter tracking remains usable;
- empty tracking uses guarded nearest-function fallback;
- missing function ancestry, missing positional arguments and non-name nodes produce false;
- neighboring private-member expectations and nonmatching receiver policy remain unchanged.

Stop if the receiver shape, traversal lifecycle, recognizer or diagnostic policy differs. Infrastructure failure leaves validation UNKNOWN. Once public validation is complete, stop solving; obtain independent hidden acceptance separately without modifying frozen knowledge or checkpoints.

## Evidence and limits

This package represents one historical Workflow, not a cross-project Pattern. Read the [episode](references/episode.md), evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [fix](references/evidence/fix.md), [regression](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical regression assertions were available at the fixed commit; historical CI execution is unknown. Later independent qualification supports only the changed-test selection with original-base control. Whole-project regression and cross-project transfer are untested. Qualification did not execute the authored [functional cases](evals/functional-cases.json).

All [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json) and functional definitions remain `not_executed`.

Time-reconstructed catalogs must exclude this Skill for its own issue, fix, cluster, aliases and copied sources, and for queries preceding any consumed historical source. Later qualification is validation metadata, never backdated historical knowledge.
