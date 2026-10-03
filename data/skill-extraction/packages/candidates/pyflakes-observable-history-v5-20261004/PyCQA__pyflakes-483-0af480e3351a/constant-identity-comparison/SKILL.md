---
name: constant-identity-comparison
description: "Repair Python AST identity-comparison diagnostics that miss recursively constant tuples, while preserving singleton exemptions and nonconstant-tuple behavior."
---

# Constant identity comparison diagnostics

## Activation and exclusions

Activate when a Python AST-based checker diagnoses `is` or `is not` against scalar literals but misses empty tuples or tuples composed recursively of constants, and the current diagnostic policy requires that coverage.

Clarify when only a compiler warning is supplied: obtain the public reproduction, checker owner, supported Python versions, and intended diagnostic policy. Do not activate for runtime object-identity changes, non-Python AST interfaces, arbitrary constant folding, or a policy that flags every tuple regardless of its contents.

This is a conditional Workflow supported by one verified historical repair, not a cross-project Pattern.

## Current probes

Use [inspection](references/actions/inspect.md) before editing. Locate and bind these semantic owners in the current public checkout:

- `constant_classifier`: singleton and constant AST classification.
- `identity_comparison_checker`: pairwise comparison traversal and diagnostic selection.
- `identity_diagnostic`: public diagnostic text.
- `identity_regression_tests`: public regression assertions.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Historical paths in the [episode](references/episode.md) are context, not current bindings.

Each current Oracle binding maps `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution; historical commands do not authorize execution.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites permit probes only; hard failures reject a modifying plan. Structural PASS predicts compatibility, not repair success.

## Operations

1. [Inspect the current classification gap](references/actions/inspect.md).
2. If the gap and compatible policy are confirmed, [repair classification, diagnostic integration, and assertions](references/actions/repair.md).
3. [Validate corrected and preserved behavior](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) records dependencies. Current ordering follows ports, prerequisites, semantic evidence, and verification rather than list position. Already satisfied or inapplicable work may be omitted, but every modifying operation retains its explicit validation. Refresh observations invalidated by edits.

## Validation

Observe diagnostics for `x is ()` and `x is (1, '2', True, (1.5, ()))`. Observe no identity-literal diagnostic for `x is (x,)` or singleton-only identity operands. Preserve scalar-literal diagnostics, both operand positions, both identity operators, pairwise chained-comparison traversal, and ordinary child traversal.

The historical additions assert the two positive tuple cases and the variable-tuple negative case. Other boundaries derive from implementation branches and current preservation requirements; they are not additional historical test executions.

## Stop conditions and limits

Stop or narrow the repair if current policy differs, owners cannot be bound, supported AST variants cannot be assessed, or the proposed classifier treats variable-containing tuples as constants. Do not extend this mechanism to unary expressions or arbitrary constant folding without separate evidence.

Record actual public execution results and unknown coverage. Independent hidden acceptance occurs only after the solver stops; hidden tests and gold-derived commands never enter guidance. Do not publish a current task plan as newly verified historical knowledge.

See [provenance](references/provenance.json) and the evidence cards for [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [assertions](references/evidence/regression.md).

The supplied contemporary qualification reports two fail-to-pass and 28 pass-to-pass checks within changed test files with an original-base control. Whole-project regression and cross-project transfer are untested. This is a provenance attestation, not pre-cutoff learned content or a historical execution log.

All authored eval suites are `not_executed`. Formal knowledge and checkpoints remain frozen during evaluation. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and every source unavailable before query input time.
