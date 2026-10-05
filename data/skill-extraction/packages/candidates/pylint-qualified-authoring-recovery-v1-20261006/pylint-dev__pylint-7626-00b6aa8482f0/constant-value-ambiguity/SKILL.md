---
name: constant-value-ambiguity
description: "Repair Python static-analysis Boolean rewrite diagnostics that mistake multiple same-type inferred constants for one definite value, while retaining valid diagnostics for unambiguous operands."
---

# Constant-value ambiguity in Boolean rewrite diagnostics

## Activation

Activate when public evidence shows that a Python static analyzer suggests simplifying an `and`/`or` expression despite an operand having multiple possible constant values, especially after reassignment or branching.

The historical mechanism was a safe-inference helper that detected different inferred types but did not distinguish unequal constants of the same type. A Boolean rewrite consumer consequently treated an ambiguous operand as definite.

This is a conditional, single-repair Workflow, not a cross-project Pattern.

## Exclusions

Do not activate solely because a Boolean-expression diagnostic is unwanted. Do not apply this repair to parser failures, unrelated control-flow analysis, or an analyzer whose inference already rejects unequal constants. Do not generalize constant equality checks to arbitrary inferred objects.

Clarify or probe when the inference results, consumer, or current helper contract are unknown. A language other than Python or an incompatible inference interface requires separately supported guidance.

## Current probes and bindings

Before editing:

1. Record the public issue, pinned base revision, and hashes of relevant code anchors.
2. Locate the current semantic owners: the safe-inference helper, Boolean rewrite consumer, and public regression harness.
3. Observe the actual inferred alternatives for the operand. Establish whether unequal constant values survive same-type inference.
4. Observe the consumer's behavior for ambiguous, uninferable, definitely falsy, and definitely truthy operands.
5. Resolve current test commands and inference-confidence metadata requirements.

Use the [probe Action](references/actions/probe.md), then the [repair Action](references/actions/repair.md), followed by the [validation Action](references/actions/validate.md). The [Workflow](references/workflow.md) records their dependencies.

A current TaskContext must contain real owner bindings, observed PortValues, public evidence, and tri-state semantic checks. Unknown prerequisites permit probes only; hard failures reject this realization.

## Repair boundary

Introduce an opt-in, keyword-only constant-value comparison in the inference helper, preserving its default behavior. The Boolean rewrite consumer opts in and declines to emit either rewrite diagnostic when inference is absent or uninferable. Retain valid definite-value diagnostics and mark emitted diagnostics as inference-based.

Add public regressions for reassigned Boolean flags and unknown operands, along with definite-value controls. Historical file names and symbols are described in the [episode](references/episode.md); they are not current bindings.

## Validation and stopping

Render and execute current public Oracle commands bound to each Action's oracle ID. Historical commands are reference material, not execution authorization. Refresh observations after edits.

Stop if inference contracts differ materially, if the public reproduction does not show this mechanism, if default helper behavior changes, or if valid adjacent diagnostics disappear. Expand public validation when shared-helper callers may be affected.

Structural compatibility does not prove repair success. The Skill's [functional cases](evals/functional-cases.json) are definitions and remain unexecuted. Independent hidden acceptance belongs after the solver stops and must not enter guidance or frozen knowledge.

## Evidence and limits

Read the [source episode](references/episode.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [committed assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. Later independent qualification checked changed test files with an original-base control; it did not establish whole-project correctness or cross-project transfer. See [provenance](references/provenance.json).

Time-reconstructed use must exclude this source's own issue, fix, cluster, aliases, copied sources, and any discovery source unavailable before the query cutoff.
