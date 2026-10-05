---
name: returned-instance-private-usage
description: "Repair a Python unused-private-member false positive when a named object returned from __new__ initializes a private attribute subsequently read through self."
---

# Returned-instance private usage

This conditional Workflow Skill addresses a narrow receiver-name mismatch in a Python static analyzer. Its canonical Skill and Workflow ID is `workflow:verified-history:c87ac9d043b1a02e14aba0d2`.

## Activation

Activate when public code and observed diagnostics establish that:

- A named local object receives a private attribute assignment inside `__new__`.
- A simple-name return returns that object.
- An instance method reads the same private attribute through `self`.
- The analyzer nevertheless reports the assignment as an unused private member.

Clarify when the assignment scope, return expression, consumer, or diagnostic is unknown. Do not activate for genuinely unread members, other languages, unrelated warnings, general alias analysis, interprocedural factories, or complex return expressions. Nested-scope identity analysis is outside the demonstrated repair.

## Current probes

Pin the current public base and record hashed code anchors. Locate the current semantic owners:

- `private-member-checker`: private assignment/read matching logic.
- `private-member-regressions`: diagnostic fixtures and expectations.
- `public-test-runner`: supported public fixture execution mechanism.

Build a current TaskContext containing the public issue, pinned base, anchors, observed facts, semantic checks, real role bindings, observed PortValues, and current Oracle bindings. Each Oracle binding identifies its Action and source Oracle, current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution; historical paths and commands are not current execution authority.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only. Hard semantic failures reject an editing plan. Structural PASS predicts compatibility, not repair success.

## Operations

1. [Diagnose](references/actions/locate.md) the receiver mismatch without editing.
2. [Repair](references/actions/repair.md) assignment/read matching using guarded simple-name returns within `__new__`.
3. [Add regressions](references/actions/regressions.md) for alternative returned names and a non-name return.
4. [Validate](references/actions/validate.md) both edits and retained adjacent behavior.

The [Workflow](references/workflow.md) defines semantic dependencies. Already satisfied operations may be omitted only with current evidence and compatible observed ports. Every modifying operation retains its explicit validation closure.

## Validation and stopping

Require observed public checks showing no target warning for consumed private attributes on returned locals. Preserve ordinary `self`/`cls` matching and diagnostics for genuinely unused private members. Non-name return values must not cause an unsafe `.name` access.

Both edits invalidate validation freshness, not the behavior assurances. Refresh observations against the latest implementation and fixture anchors. Stop if scope ownership differs, the public mismatch cannot be confirmed, adjacent diagnostics regress, or validation is unavailable. Never use blanket diagnostic suppression as this repair.

Formal evaluation freezes knowledge and checkpoints. Do not publish a current task plan as verified historical knowledge. Independent hidden acceptance occurs separately after the solver stops; no hidden-test guidance is included.

## Support and limits

This is a single-source Workflow, not a Pattern or a cross-project claim. Read the [episode and qualification audit](references/episode.md), [provenance](references/provenance.json), and evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [committed assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. Later independent qualification is limited to changed-test files with an original-base control; whole-project correctness and cross-project transfer were not checked. The authored [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are all `not_executed`.
