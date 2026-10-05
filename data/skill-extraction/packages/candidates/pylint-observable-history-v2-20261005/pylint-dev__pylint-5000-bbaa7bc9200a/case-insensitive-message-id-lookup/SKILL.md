---
name: case-insensitive-message-id-lookup
description: "Repair missing symbolic-name recommendations for accepted lowercase numeric message IDs when an uppercase-keyed symbol resolver uses the original input as its lookup key."
---

# Case-insensitive message-ID lookup

## Activation and exclusions

Activate when uppercase and lowercase numeric message IDs both control the same diagnostic, but only uppercase IDs receive a recommendation to use a symbolic name.

Clarify and probe when identifier acceptance, registry conventions, or resolver ownership are unknown. Do not activate for intentionally case-sensitive identifiers, symbolic-name casing, missing registration, unrelated configuration suppression, or a resolver that already handles both cases correctly.

This is a single historically supported Workflow, not a cross-project Pattern. Its implementation realization is Python; do not assume compatibility with another language or identifier system.

## Current probes

Create a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues where relevant, and current Oracle bindings.

Locate these semantic owners:

- `numeric-id-symbol-resolver`: converts numeric message IDs to symbolic names.
- `message-control-entrypoint`: processes public enable/disable directives.
- `symbolic-recommendation-regression-suite`: tests numeric-to-symbolic recommendations.

Establish that lowercase numeric IDs are accepted, registry keys are uppercase, and the recommendation path reaches a raw-key lookup in the resolver. Observe uppercase recommendations, unknown-ID errors, original-input spelling, and current registered symbols. Historical paths appear only in [the episode](references/episode.md); they are not current bindings.

## Operations

Use [the Workflow](references/workflow.md) and its complete Action contracts:

1. [Probe](references/actions/probe.md) the mechanism without source edits.
2. [Normalize](references/actions/normalize.md) only the numeric lookup key.
3. [Add regression assertions](references/actions/regression.md) for lowercase IDs.
4. [Validate](references/actions/validate.md) both edits and adjacent behavior.

The two edits require successful mechanism probes but do not intrinsically depend on one another. For causal diagnosis, prefer strengthening the regression first and observing its missing-recommendation failure against the unchanged resolver.

Resolve current resource aliases before read/write conflict checks. Unknown prerequisites permit probes only; hard failures reject the edit plan. Effects in contracts describe intended results, not observed execution.

## Validation and stopping

For every Oracle, bind `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>` with PASS, FAIL, or UNKNOWN. Render the bound commands before execution. Empty contract commands require current binding; historical commands do not authorize current execution.

After both edits, require public observations of:

- equivalent resolution of accepted uppercase and lowercase numeric IDs;
- separate recommendations for multiple lowercase IDs in one directive;
- correct enable/disable symbolic replacements and preserved input spelling;
- preserved uppercase recommendations and unknown-ID diagnostics;
- no numeric-ID recommendation for already-symbolic names.

Refresh validation observations after any further edit. Stop if normalization changes identifier acceptance, conflates distinct registered identities, alters symbolic-name handling, or changes the unknown-ID error path. A structural plan PASS predicts compatibility, not repair success.

After the solver stops, obtain independent hidden acceptance through the evaluation host. Hidden tests and gold-derived commands must not enter this Skill's guidance.

## Evidence and limits

See [the episode and evidence index](references/episode.md) and [provenance](references/provenance.json). Historical CI/test execution is **unknown**; committed expected results are assertions, not execution evidence.

The supplied later qualification reviewed original-base, base-with-regression, and historical-fixed controls under one runtime. It supports the historical repair only within selected changed-test-file controls. Whole-project regression and cross-project transfer are untested. It did not execute this newly authored Skill.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are **not_executed**. Current task plans are not newly verified historical knowledge. Keep formal knowledge and checkpoints frozen; earlier-query catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and any discovery source unavailable before its input time.
