---
name: root-scope-nonlocal-guard
description: "Repair a Python static-analysis assignment crash caused by following a nonexistent enclosing scope after encountering a module-level nonlocal declaration, while retaining the invalid-nonlocal diagnostic and nested-scope behavior."
---

# Root-scope nonlocal guard

## Activation

Activate when public evidence shows all of the following:

- A Python static analyzer encounters a module-level `nonlocal` declaration followed by an assignment.
- Assignment checking enters a nonlocal-related enclosing-scope path.
- That path dereferences the parent of a root scope, which has no parent.

An invalid declaration is still expected to receive its ordinary diagnostic. This Skill prevents an analyzer crash; it does not make module-level `nonlocal` valid Python.

Clarify if the report mentions only a generic scope error or omits the triggering code. Do not activate for unrelated inference failures, parser rejection before assignment checking, or crashes involving a parent that exists.

## Current probes and bindings

Use [locate and diagnose](references/actions/diagnose.md) to locate the current assignment-checking owner and its public functional-test owner. Do not assume the historical file paths still apply.

Record a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding must identify its Action ID and source Oracle ID, public instruction, argv command, and current evidence references. Record its check under `oracle:<action_id>:<source_oracle_id>`.

Use PASS/FAIL/UNKNOWN checks:

- UNKNOWN prerequisites permit diagnosis only, not edits.
- A hard failure of the mechanism or language binding rejects this workflow.
- A structural PASS predicts plan compatibility, not repair success.

Render current bound commands before executing them. Historical commands are evidence, not current execution authorization.

## Operations

1. [Locate and diagnose](references/actions/diagnose.md): establish whether root-scope parent absence actually enables the failing branch.
2. [Guard and add regression](references/actions/guard.md): require an enclosing parent before taking that branch, and add a module-level invalid-nonlocal assignment regression.
3. [Validate diagnostics and adjacent behavior](references/actions/validate.md): run current public reproduction and repository tests, inspecting diagnostic output as well as process results.

The [historical Workflow](references/workflow.md) records the evidenced dependency structure. A current plan may omit operations already satisfied, but every code or test modification must retain validation. Re-observe stale validation after any modification.

## Validation and stops

Success requires public evidence that the root-scope case produces its invalid-nonlocal diagnostic without a fatal analyzer error, while ordinary assignments and existing nested nonlocal cases retain their behavior. A lint command may legitimately exit nonzero because the source is invalid; do not interpret that alone as a crash.

Stop if:

- Current root scopes have parents, or the failing path differs materially.
- The guard would suppress required diagnostics or bypass unrelated checking.
- Current public test bindings cannot be established.
- A modified test accepts fatal errors, loses existing assertions, or fails to exercise an assignment.
- Target or adjacent public checks fail.

Do not broaden the repair to exception swallowing or blanket skipping of assignments.

## Evidence and limits

Read the [episode](references/episode.md) and [provenance](references/provenance.json). This is one repository-specific historical realization, not an independently supported cross-project Pattern. Its reusable mechanism is conditional on current semantic evidence.

Historical test execution is unknown; committed assertions are known. Later source qualification establishes a controlled historical fail-to-pass within its stated scope, not execution of this Skill's [functional cases](evals/functional-cases.json).

The qualification scope is `changed-test-files-with-original-base-control`. Its limits are: “Changed test files only; whole-project regression and cross-project transfer are untested.”

During formal evaluation, keep knowledge and checkpoints frozen; do not publish current task plans as historical knowledge. Earlier-query training catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and any discovery source unavailable before query time. Obtain independent hidden acceptance only after the solver stops; hidden tests must not enter guidance.
