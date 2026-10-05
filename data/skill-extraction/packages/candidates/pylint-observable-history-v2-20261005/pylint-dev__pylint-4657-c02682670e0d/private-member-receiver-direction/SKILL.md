---
name: private-member-receiver-direction
description: "Repair a Python private-member usage checker whose receiver-name comparison misses class writes read through an instance, while preserving the directional boundary for instance writes."
---

# Private-member receiver direction

## Activation and exclusions

Activate for a public Python `unused-private-member` false positive involving a private attribute written through `cls` and read through `self` in the same relevant class. Current inspection must show that receiver-name equality causes the missed use.

Clarify when the reproduction, receivers, enclosing class, diagnostic, or current checker is missing. Do not activate for unrelated unused locals, arbitrary receiver aliases, inheritance resolution, or requests to suppress warnings. If the current matcher already implements the directional relation, investigate separately rather than applying this repair.

This is a focused, single-source Workflow, not a Pattern or a claim of cross-project transfer.

## Current probes

Create a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Locate:

- `private-member-use-matcher`: the private assignment/read matching logic.
- `private-member-regression-suite`: public fixtures and diagnostic expectations.
- `public-check-runner`: the public test runner.

Do not treat historical paths as current bindings. Use [inspection](references/actions/inspect.md) to confirm the mechanism. UNKNOWN prerequisites authorize probes only; FAIL rejects this Workflow. Predicate-name agreement alone is not semantic evidence.

## Operations

1. [Inspect the write/read comparison](references/actions/inspect.md).
2. [Modify the directional matcher](references/actions/edit-matcher.md).
3. [Add positive and negative assertions](references/actions/edit-regressions.md).
4. [Validate both modifications](references/actions/validate.md).

The supported relation requires equal private attribute names:

| Write receiver | Read receivers recognized as use |
|---|---|
| `cls` | `cls`, `self` |
| `self` | `self` |

Do not make the relation symmetric. Do not invent alias inference or an unsupported bridge.

See the [historical Workflow](references/workflow.md). Current ordering follows ports and prerequisites, not list position. Already-satisfied operations may be omitted only with current evidence; retain public validation for every retained modifying Action.

## Validation and stopping

Bind every Oracle to a current public instruction, argv command, and evidence references. Render bound commands before executing them. Record tri-state results under `oracle:<action_id>:<source_oracle_id>`. Historical commands and later source-qualification commands do not authorize execution in a current checkout.

Require:
- no unused-private-member warning for a same-class `cls` write read through `self`;
- supported same-receiver uses recognized;
- retained unused-instance-member behavior when only a `cls` read exists;
- retained undefined-variable diagnostic for an unbound `cls`;
- no unexplained changes to established adjacent private-member diagnostics.

Refresh validation observations after edits. Stop on materially different receiver naming, scope, or AST semantics, unexplained diagnostic changes, or failing public checks. Do not rewrite expected outputs merely to hide failures. Structural plan PASS predicts compatibility, not repair success.

Independent hidden acceptance is obtained after the solver stops; hidden tests and gold-derived commands are not guidance. Formal knowledge and checkpoints remain frozen. Earlier-query catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and information unavailable before its input time.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and the evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. Committed assertions are not execution results. The later independent qualification inspected original-base, base-with-regression, and historical-fixed controls with consistent runtime identity. Its scope is changed-test-files with an original-base control, not whole-project correctness or cross-project transfer. It does not execute these authored Skill cases.

[Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`.
