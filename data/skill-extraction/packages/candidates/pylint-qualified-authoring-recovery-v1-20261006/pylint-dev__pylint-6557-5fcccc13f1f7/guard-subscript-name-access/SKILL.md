---
name: guard-subscript-name-access
description: "Conditionally repair a Python AST dictionary-lookup checker that reads a Name-only field from an unchecked inner subscript base, using a narrow type guard, a public regression, and validation of preserved diagnostics."
---

# Guard subscript name access

## Activation

Activate when current public evidence establishes all of the following:

- A static-analysis checker examines dictionary lookups during `.items()` iteration.
- The failing expression resembles `mapping[obj.item[0]]`.
- The inner subscript base is an Attribute rather than a Name.
- The checker reads that base's `.name` without first restricting it to a Name node.

Clarify or probe when only the exception symptom is known. Do not activate for application runtime attribute errors, runtime dictionary errors, or failures involving a different AST assumption. An attribute-valued dictionary expression is not itself excluded: distinguish the dictionary expression from the inner key-subscript base.

## Current probes and bindings

Use [Locate and confirm](references/actions/locate.md) before modifying code. Resolve these semantic owners in the current checkout:

- `lookup-checker`: the dictionary index lookup diagnostic branch.
- `lookup-regression-suite`: its public fixture, expectations, and runner.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Historical paths in the [episode](references/episode.md) are not automatic current bindings.

UNKNOWN prerequisites permit probes only. A hard mechanism failure rejects this Workflow.

## Operations

1. [Locate and confirm](references/actions/locate.md) the unsafe read and supported Name path.
2. [Guard and add regression](references/actions/repair.md): reject non-Name inner bases before reading `.name`, retaining existing conditions and expectations.
3. [Validate public behavior](references/actions/validate.md) against the edited candidate.

The [historical Workflow](references/workflow.md) specifies dependencies and preservation obligations. Current ordering follows compatible ports, current prerequisites, and validation freshness, not merely historical list position. Already-satisfied operations may be omitted only with current evidence; modifying operations retain explicit validation.

## Validation and stopping

For each current Oracle, record Action ID, source Oracle ID, public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution. Empty source command arrays and historical commands do not authorize execution.

Use PASS, FAIL, and UNKNOWN. Structural PASS predicts compatibility, not repair success. Require fresh public observations showing:

- the attribute-subscript case produces neither the reported exception nor a fatal analysis message;
- supported Name-based redundant lookups retain intended diagnostics;
- existing negative cases retain their expectations;
- the regression exercises static analysis of the loop body, not merely application execution.

Stop on ambiguous bindings, a different mechanism, weakened expectations, suppressed supported diagnostics, or failed validation. Do not catch AttributeError broadly or invent an attribute-to-name adapter. Refresh stale observations after edits. Independent hidden acceptance, when supplied, occurs after the solver stops.

## Evidence and limits

This is one focused Workflow supported by one independently qualified historical repair, not a Pattern or a cross-project transfer claim.

See [episode and qualification audit](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical assertions are known; historical CI/test execution is unknown. Later qualification is validation-only and does not execute the authored Skill evaluations.

Exact qualification scope: `changed-test-files-with-original-base-control`.

Exact limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

[Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions remain `not_executed`.

During formal evaluation, keep knowledge and checkpoints frozen and never publish current task plans as newly verified history. Time-reconstructed admission excludes the query's own issue, fix, cluster, aliases, copied sources, and every source unavailable before the query input time.
