---
name: ancestor-policy-filter
description: "Conditionally repair Python ancestry-count false positives by filtering explicitly exempt resolved ancestor identities while preserving excessive user-defined ancestry warnings."
---

# Ancestor policy filter

## Activation and exclusions

Activate when a public minimal standard-library-derived Python class triggers an excessive-ancestry diagnostic and current inspection establishes that explicitly exempt ancestors contribute to the count.

The supported mechanism is **filtering resolved qualified names from the existing transitive ancestor traversal before counting**.

- **Activate:** the reproduction fails, resolved identities are known, and current public policy authorizes specific exemptions.
- **Clarify/probe:** the reproduction, identities, counting owner, or policy authorization is unknown.
- **Do not activate:** nonexempt user-defined ancestry fully explains the warning; the task concerns abstract methods, method resolution, or a different metric.

Do not replace transitive ancestry with direct bases, raise the threshold, disable the diagnostic, or exempt all standard-library classes. One verified historical repair supports this Workflow; it is not a cross-project Pattern.

## Operations

1. [Inspect the current metric and policy](references/actions/probe.md).
2. [Filter the count and encode regression controls](references/actions/repair.md).
3. [Validate the candidate](references/actions/validate.md).

The [historical Workflow](references/workflow.md), [episode](references/episode.md), and evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [assertions](references/evidence/regression.md) describe the source. [Provenance](references/provenance.json) records qualification boundaries.

## Current binding and execution

Construct a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate semantic owners independently in the current checkout. Existence predicates use `role:<owner_role>` keys and boolean values. Policy claims require evidence-backed review, not predicate-name matching.

Bind each Oracle by Action ID and source Oracle ID to a current public instruction, argv command, and evidence references. Record its tri-state check under `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty contract commands require current binding and authorize no unspecified execution.

UNKNOWN prerequisites permit probes only. Hard failures reject the plan. Structural PASS predicts compatibility, not repair success. After edits, refresh stale observations and execute public checks. Obtain independent hidden acceptance after the solver stops; hidden tests never enter guidance.

## Validation and stopping

Require current observable evidence that:

- The supported standard-library-derived negative control no longer emits the ancestry warning.
- Excessive nonexempt user-defined ancestry still warns.
- Counts use the filtered transitive traversal.
- The configured strict threshold comparison remains unchanged.
- Adjacent design diagnostics pass their current public checks.

Stop or clarify if the public failure cannot be reproduced, exemption authorization is absent, resolved names do not match proposed entries, or legitimate-warning controls are suppressed. Do not broaden exemptions silently.

## Limits

Historical test assertions were committed; contemporaneous CI/test execution is unknown. Independent qualification checked in 2026 supports the historical repair only within changed-test-file scope with an original-base control. Whole-project correctness, cross-project transfer, and this Skill's functional cases were not executed.

The historical whitelist literally contained `bulitins.frozenset` and `typing.AsyncContextManger`. These spellings are implementation facts, not identities validated for current reuse.

Keep formal knowledge and checkpoints frozen during evaluation. Earlier-query admission excludes this repair's own issue, fix, cluster, aliases, copied sources, and information unavailable before query input time. A current task plan is not newly verified historical knowledge.
