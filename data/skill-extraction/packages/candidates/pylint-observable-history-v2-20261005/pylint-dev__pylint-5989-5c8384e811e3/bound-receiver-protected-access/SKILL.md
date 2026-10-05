---
name: bound-receiver-protected-access
description: "Repair missing protected-member diagnostics when an ordinary function or static method's first argument is incorrectly treated as an implicit bound receiver."
---

# Bound-receiver protected-access repair

## Activation

Activate when a Python static analyzer suppresses a protected-member diagnostic on the first parameter of an ordinary function or static method, and current public evidence suggests that an implicit-receiver exemption is responsible.

The supported mechanism is specific: a receiver-classification helper falls back to the nearest function's first argument without first establishing that the function is bound. Parameter position alone does not establish receiver identity.

Do not activate merely because an attribute starts with an underscore. Exclude intentionally permitted accesses, disabled diagnostics, unrelated inference failures, and analyzers whose receiver representation is incompatible with this mechanism. If the diagnostic is missing but its suppression path is unknown, clarify or probe before planning an edit.

## Current probes and bindings

1. Pin the public checkout and record the issue, code-anchor hashes, current diagnostic configuration, and reproduction.
2. Locate the semantic owners:
   - `receiver-classifier`: classifies implicit method receiver parameters.
   - `protected-access-checker`: applies protected-access exemptions and handles attribute expressions.
   - `protected-access-fixtures`: owns public diagnostic fixtures and expected results.
3. Reproduce an external protected-property access from both an ordinary function and a static method. Inspect whether the first parameter is incorrectly granted an implicit-receiver exemption.
4. Inspect the AST's boundness API, nearest-function search, empty-argument handling, active receiver stack, and call-expression handling. Do not assume current APIs match the historical implementation.

Use the [inspection Action](references/actions/inspect.md). Unknown prerequisites authorize inspection only. A hard failure of the mechanism or incompatible AST semantics rejects this workflow.

## Operations

Once current evidence establishes applicability, use the [repair Action](references/actions/repair.md) to restrict fallback receiver classification to bound functions and add public regression assertions. Keep legitimate instance, class, and metaclass receiver handling.

The historical repair also changed a related expression guard from a specialized self-type-call check to a general call-node check. Inspect that branch separately; do not transplant it into an unrelated current checker or claim it caused the reported false negative.

Every modifying operation retains the [validation Action](references/actions/validate.md). The complete historical realization is in [workflow.md](references/workflow.md); the original episode and historical paths are in [episode.md](references/episode.md).

## Validation and stopping

Bind each oracle to the current public checkout before execution. A current TaskContext must contain public issue identity, pinned base, hashed anchors, real owner bindings, observed facts, semantic checks, observed PortValues, and current Oracle bindings.

For each current Oracle, record `action_id`, `source_oracle_id`, public instruction, argv command, and evidence references. Use the check key `oracle:<action_id>:<source_oracle_id>` and render the bound argv for review. Empty historical command arrays are not executable commands.

Use PASS/FAIL/UNKNOWN:
- UNKNOWN requires a public probe; it does not authorize editing.
- FAIL on a prerequisite rejects the plan.
- Structural PASS predicts compatibility, not repair success.
- After editing, refresh diagnostic and adjacent-behavior observations.

Require the two external-access diagnostics, the existing protected-access expectations, legitimate bound-receiver behavior, and call-expression handling to pass current public checks. Stop on unexplained new diagnostics, failure to locate compatible semantic owners, or a broader failure requiring a different mechanism. Do not silently widen the patch.

Obtain independent hidden acceptance only after the solver stops. Do not use hidden tests, gold-derived commands, or evaluation feedback as guidance. Keep formal knowledge and checkpoints frozen during evaluation.

## Authority and limits

This is a single-source Workflow, not a multi-source Pattern or a cross-project guarantee. See [provenance](references/provenance.json) and the four [evidence cards](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), and [assertions](references/evidence/assertions.md).

The historical assertions were committed with the repair; historical CI execution is unknown. Later independent qualification established one fail-to-pass case with original-base controls within changed-test-file scope. It did not check the whole project or cross-project transfer and did not execute this Skill's functional definitions.

Activation, applicability, and functional suites are provided under `evals/`; all remain `not_executed`. Time-reconstructed catalogs must exclude their own issue, fix, cluster, aliases, copied sources, and every source unavailable before the query time.
