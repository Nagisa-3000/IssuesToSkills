---
name: valid-special-method-allowlist
description: "Repair a false-positive Python special-method-name diagnostic when a documented valid method is missing from the checker's explicit accepted-name registry."
---

# Valid special-method allowlist repair

## Activation

Activate when current public evidence establishes that a Python checker rejects a valid special method because the explicit accepted-name registry consumed by its name diagnostic omits that method.

The supported historical repair concerns `__index__`. This package is a focused Workflow, not a multi-source Pattern or proof of cross-project transfer.

- **Clarify or probe** if method validity, diagnostic ownership, registry membership, or the public reproduction is unknown.
- **Do not activate** for misspelled names, signature or return-value diagnostics, or rejection caused by another rule when the method is already registered.
- Never disable the diagnostic globally or accept arbitrary double-underscore names.

## Current probes and bindings

Pin the public base and record hashed code anchors. Locate these semantic owners in the current checkout:

- `special-method-acceptance-registry`: the accepted-name collection actually consumed by the diagnostic.
- `special-method-diagnostic-regression-suite`: the public functional fixture and its diagnostic expectations.

Trace registry membership handling, reproduce the warning with the diagnostic enabled, establish method validity using public documentation, and inspect the harness's no-warning convention. Historical paths in the [episode](references/episode.md) are evidence, not current bindings.

A current TaskContext records the public issue, pinned base, hashed anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id` and `source_oracle_id` to a public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render bound commands before execution. Empty contract commands require current public bindings; historical commands do not authorize execution. Checks are PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard applicability failures reject the plan.

## Operations

Use the [Workflow](references/workflow.md) and its linked Actions:

1. [Probe the registry omission](references/actions/probe.md).
2. [Register the valid method narrowly](references/actions/register.md).
3. [Add the no-warning regression](references/actions/regression.md).
4. [Validate both edits](references/actions/validate.md).

The edits may occur in either order after diagnosis. Validation follows both. A current DAG may omit an already satisfied operation only with current supporting evidence; retain explicit validation for every performed modification. Resolve owner aliases before checking read/write conflicts. Do not invent unsupported bridges between incompatible ports.

## Validation and stopping

Run the bound public minimal reproduction and functional suite with the relevant diagnostic enabled. Require no name warning for the valid method, continued warnings for existing invalid-name cases, and unchanged unrelated diagnostic expectations.

Edits stale validation observations, not behavior-preservation obligations. Refresh stale facts. Structural plan PASS predicts compatibility, not repair success.

Stop if validity is unsupported, registry ownership is unconfirmed, public checks cannot run, or unexpected diagnostics remain. Do not broaden acceptance or weaken assertions to force a pass. Failed or unavailable validation blocks a successful-repair claim.

Formal knowledge and checkpoints remain frozen during evaluation. Obtain independent hidden acceptance after the solver stops; hidden tests and gold-derived commands never enter guidance. Earlier-query catalogs exclude this source when unavailable at query time or when the query concerns its own issue, fix, cluster, aliases, or copied sources.

## Evidence and limits

See the [episode](references/episode.md), its four evidence links, and [provenance](references/provenance.json). Historical CI/test execution is **unknown**. Committed assertions are not historical pass claims.

Later qualification has scope `changed-test-files-with-original-base-control` and limits: `Changed test files only; whole-project regression and cross-project transfer are untested.` It did not execute this Skill.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status **not_executed**.
