---
name: live-configuration-consumers
description: "Repair Python analysis consumers that read stale constructor-time option copies when current public probes confirm compatible live configuration ownership."
---

# Live configuration consumers

This conditional Workflow addresses an accepted public option whose value reaches host configuration but not the analysis consumer. Its supported mechanism is replacing stale option copies with a live host namespace while retaining private option storage for standalone use.

## Activation and exclusions

Activate when current public evidence shows:
- An analysis option is accepted but does not affect its intended analysis.
- The host owns the authoritative configuration namespace.
- The consumer reads copies initialized before later configuration updates.
- Sharing the live namespace is compatible with initialization and supported construction modes.

Clarify when option scope, ownership, or update order is unknown. Do not activate for rejected options, configuration precedence errors, defective filtering despite correct runtime values, or unrelated diagnostics. In particular, ignoring imports for similarity analysis does not imply suppressing unused-import diagnostics.

## Current probes

Use [diagnosis](references/actions/diagnose.md) before editing. Bind the semantic owners `configuration-consumer` and `configuration-regression-suite` to current public code and tests. Historical paths in [the episode](references/episode.md) are locators, not automatic current bindings.

Construct a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before read/write conflict checks.

Each current Oracle binding maps action ID and source Oracle ID to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Historical commands do not authorize execution unchanged.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only; failed mechanism or compatibility prerequisites reject the modifying plan.

## Linked operations

1. [Diagnose configuration ownership and lifecycle](references/actions/diagnose.md).
2. [Repair namespace ownership and add public regression coverage](references/actions/repair.md).
3. [Validate option behavior and preservation assurances](references/actions/validate.md).

The [historical Workflow](references/workflow.md) is a source-specific reconstruction, not an executed current task plan. Current ordering follows matching ports, prerequisite evidence, and verification dependencies. Already satisfied operations may be omitted only with current evidence; every modification retains its validating Action.

## Validation and stop conditions

Require observable public checks establishing:
- Import-only duplication is ignored when the corresponding option is enabled.
- Eligible duplication is still detected under a suitable control.
- Independent diagnostics remain independently governed.
- Standalone construction retains its supported defaults.
- Every affected runtime option read uses the intended namespace.

Stop if sharing configuration would overwrite already parsed values, the namespace interface is incompatible, standalone behavior cannot be preserved, or a required public check fails. Do not substitute global diagnostic disabling or a threshold workaround.

An edit invalidates the freshness fact `public-validation-observed`; it does not invalidate the obligations to preserve adjacent behavior. UNKNOWN preservation checks prevent an unconditional success claim.

Structural PASS predicts compatibility, not repair success. Execute public checks, refresh stale observations, stop the solver, and obtain independent hidden acceptance separately. Keep formal knowledge and checkpoints frozen; do not publish current task plans as newly verified historical knowledge during formal evaluation. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Evidence and limits

See [episode](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

This is one Python repair, not a cross-project Pattern. Historical regression assertions were committed, but contemporaneous execution is unknown. Later independent qualification covered only the changed test file with original-base control: one fail-to-pass and ten pass-to-pass cases. Whole-project correctness and cross-project transfer were not tested.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions and remain **not_executed**.
