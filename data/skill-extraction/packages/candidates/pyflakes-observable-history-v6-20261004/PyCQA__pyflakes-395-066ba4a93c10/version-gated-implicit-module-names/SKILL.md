---
name: version-gated-implicit-module-names
description: "Repair a Python static analyzer's false undefined-name warning for module-level __annotations__ by recognizing the implicit name only on supported Python versions and retaining public regression validation."
---

# Version-gated implicit module names

## Activate conditionally

Use this Workflow when current public evidence shows all of the following:

- A Python static analyzer reports module-level `__annotations__` as undefined.
- The analyzer has an implicit module-name registry, or an equivalent semantic owner.
- Python-version capability checks govern which implicit names are recognized.
- The requested repair matches the historical policy: recognize `__annotations__` at module scope on Python 3.6 and later.

This is a focused, single-repair Workflow, not a general rule that runtime-created names are builtins.

**Clarify** when the analyzer's target Python version differs from its host version, when scope ownership is unclear, or when the requested policy requires proving that annotations actually execute before each use.

**Do not activate** for arbitrary undefined names, function-local annotation behavior, unrelated class-scope diagnostics, or a request to make `__annotations__` an unconditional builtin.

## Current probes and binding

Before editing, collect the public issue, pinned base revision, hashed code anchors, observed diagnostics, and current test entry points. Bind these semantic owners in the current checkout:

- `implicit-module-name-registry`
- `python-version-capability-policy`
- `undefined-name-regression-suite`

Inspect how the registry participates in scope lookup. Determine whether the current analyzer uses host-version checks, target-version checks, or another capability model. The historical repair used host `sys.version_info`; do not silently transfer that choice to a target-version analyzer.

Execute [the diagnosis operation](references/actions/diagnose.md) without modifying the checkout. Unknown prerequisites authorize inspection and public probes only. A hard semantic mismatch rejects the repair plan.

## Operations

1. [Diagnose and bind the policy owners](references/actions/diagnose.md).
2. [Edit the version-gated registry and regression](references/actions/repair.md).
3. [Validate the repaired behavior and adjacent behavior](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) records the historical mechanism and dependencies. Current ordering follows bound ports, prerequisites, and validation obligations rather than list position. Operations already satisfied by current evidence may be omitted only if their required assurances remain established.

## Validation and stop conditions

For each current oracle, record `action_id`, `source_oracle_id`, public instruction, argv command, and public evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render and execute those current bound commands; this package supplies no universal executable command.

Require observable checks for:

- No undefined-name diagnostic for the reported annotated-module reproduction on a supported version.
- The bare module-level `__annotations__` regression policy on Python 3.6 or later.
- A version-guarded regression test rather than unsupported syntax execution on older versions.
- Retention of existing magic-global behavior and version-dependent loop AST handling.
- Public undefined-name regression tests passing.

After an edit, refresh stale diagnostic and validation observations. PASS/FAIL/UNKNOWN must reflect actual current evidence. Structural compatibility does not establish repair success. Stop on failing public checks, unresolved version semantics, unavailable owner bindings, or unverified adjacent behavior. Independent hidden acceptance, if part of the evaluation environment, occurs after the solver stops and does not become guidance.

## Evidence and limits

See [the episode](references/episode.md), [provenance](references/provenance.json), and the four packaged evidence cards linked there.

Only one independent bug cluster and fix support this Workflow. Historical regression evidence records an assertion added at the repair commit, not a historical test execution. Later qualification reports one fail-to-pass and 61 pass-to-pass cases in changed test files only; whole-project regression and cross-project transfer were not tested.

This package's evaluation definitions are **not executed**. Current plans and probe results are not newly verified historical knowledge. Formal knowledge remains frozen; time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
