---
name: resource-lifetime-diagnostics
description: "Repair Python resource-context diagnostics that incorrectly require persistent executors to use with blocks or report assigned resources before their later context-manager use."
---

# Resource lifetime diagnostics

## Activation

Activate when a public Python static-analysis issue concerns an over-eager resource-context recommendation and current code demonstrates either:

- `ThreadPoolExecutor` or `ProcessPoolExecutor` constructors are classified as always requiring a `with` block; or
- a recognized resource constructor assigned to a variable is reported immediately even though that variable is subsequently used by `with`.

This is a conditional, single-repair Workflow, not a general resource-lifetime analysis framework. Its identity is semantic, not repository-specific.

Clarify when the diagnostic, inferred constructor identity, or expected lifecycle is uncertain. Do not activate for actual runtime resource leaks, unrelated lint messages, arbitrary custom context managers, or a request to disable all resource-context diagnostics.

## Current probes and bindings

First use [Inspect diagnostic ownership](references/actions/inspect.md). Locate the current semantic owners:

- `resource-diagnostic-owner`: constructor classification, diagnostic emission, assignment and context-manager visitors, and scope lifecycle;
- `resource-regression-owner`: public diagnostic fixtures, expected messages, and their test runner.

Record a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Historical paths are examples only; see [episode](references/episode.md).

For every Oracle, bind `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. The semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty historical command arrays are not executable authorization.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize inspection only. A hard mismatch rejects the plan. Structural PASS predicts compatibility, not repair success.

## Operations

1. [Inspect diagnostic ownership](references/actions/inspect.md): reproduce and identify applicable mechanisms without changing source.
2. [Correct lifecycle classification and deferred reporting](references/actions/repair.md): edit only the mechanisms demonstrated by current evidence and add matching public regression assertions.
3. [Validate diagnostic boundaries](references/actions/validate.md): execute current public checks, review preservation obligations, and refresh stale observations.

The [historical Workflow](references/workflow.md) documents the combined repair. A current plan may omit already-satisfied portions of the modifying operation, but may not omit validation after an edit. Do not add unsupported adapters or silently bind this Python realization to another language.

## Required validation

Check persistent thread and process executors without `with`, resources assigned and later used in `with`, module resources consumed in nested functions, and mixed used/unused tuple assignments. Retain warnings for recognized resources that remain unused by `with`, and preserve existing direct-with, context-manager-owned, automatic-release, and adjacent refactoring behavior.

The original regression assertions and their limits are recorded in [regression evidence](references/evidence/regression.md). Execute current public tests; do not infer success from historical expected-message files.

## Stop conditions and limits

Stop if inference cannot establish the callable identity, current scope semantics differ materially, bindings are missing, regression checks fail, or preservation behavior is UNKNOWN after an edit. Nested scopes, aliasing, attribute context expressions, and control-flow completeness require current investigation; the historical repair does not prove a general dataflow solution.

One independently qualified repair supports this Workflow. Qualification was replayed in 2026 against historical artifacts; it does not change their 2021 availability dates. It was limited to selected functional tests with original-base controls, not whole-project correctness or cross-project transfer. Historical CI execution is unknown. All newly authored [functional cases](evals/functional-cases.json) are unexecuted.

After public validation, stop the solver and obtain independent hidden acceptance outside this Skill. Never use hidden tests or gold-derived commands as guidance. Freeze formal knowledge and checkpoints during evaluation. A time-reconstructed catalog must exclude this Skill for its own issue, fix, cluster, aliases, copied sources, or any query predating its source availability.

## Resources

- [Episode and historical bindings](references/episode.md)
- [Workflow contract](references/workflow.md)
- [Title evidence](references/evidence/title.md)
- [Original report](references/evidence/body.md)
- [Implementation evidence](references/evidence/fix.md)
- [Regression evidence](references/evidence/regression.md)
- [Provenance](references/provenance.json)
- [Activation cases](evals/activation-cases.json)
- [Applicability cases](evals/applicability-cases.json)
- [Functional definitions](evals/functional-cases.json)
