---
name: diagnostic-independent-import-tracking
description: "Repair configuration-dependent false unused-import diagnostics when disabling unrelated variable diagnostics skips shared name-resolution work needed to track imported references."
---

# Diagnostic-independent import tracking

## Activation

Activate for investigation when a Python static analyzer reports an actually referenced import as unused only with restricted diagnostic settings. The supported historical trigger is a class attribute initialized from a same-named import, particularly a call-wrapped reference:

```python
from math import e, pi

class Example:
    e = float(e)
    pi = pi
```

The call-wrapped and direct references are separate controls. Activate for repair only after current evidence connects the false warning to an early return that gates shared analysis on unrelated diagnostic enablement.

Clarify when the public reproduction, diagnostic configuration, or current analysis owner is unknown. Do not activate for genuinely unused imports, unresolved imports, unrelated scope defects, or a codebase where diagnostic flags do not skip shared analysis.

## Current probes and bindings

Create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners rather than assuming historical paths:

- `variable-use-analysis`: analysis that resolves references and accounts for import use.
- `restricted-import-regression-suite`: public tests covering import use with other diagnostics disabled.

Compare restricted and default configurations. Trace both initializer references. Inspect whether disabling undefined-variable and used-before-assignment causes an early return before shared definition, statement, or frame processing.

Unknown prerequisites authorize probes only. A confirmed incompatible mechanism is a hard failure for this workflow. Predicate names alone do not prove semantic claims.

## Operations

1. [Probe configuration-sensitive analysis](references/actions/probe.md).
2. [Repair the shared-analysis gate and regression](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [historical workflow](references/workflow.md) supplies the sourced dependency structure. Resolve current dependencies using bound ports, prerequisites, and evidence; do not infer execution order solely from file order.

Remove the gate only if it skips bookkeeping needed by an enabled consumer. Do not enable unrelated diagnostics, suppress unused-import, or rename the attributes as substitutes for repair. Remove obsolete enablement state only after checking its remaining references. Preserve needed diagnostic emission controls.

## Validation and stopping

For every Oracle, bind `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Render these commands before execution. Historical commands remain evidence, not authorization to execute against a current checkout.

Record PASS/FAIL/UNKNOWN under `oracle:<action_id>:<source_oracle_id>`. Require:

- No false unused-import warning for either initializer with restricted diagnostics.
- Correct default-configuration behavior.
- Genuine-unused imports remain reportable.
- Enabled undefined-variable and used-before-assignment diagnostics remain correct.
- Relevant existing import/variable controls and the added regression pass.

After edits, refresh stale validation observations. Stop on unbound owners, unresolved reproduction imports, unexpected diagnostics, conflicting modifications, or failing preservation checks. Infrastructure failures are UNKNOWN, not PASS. Structural PASS predicts compatibility, not repair success.

During formal evaluation, freeze knowledge and checkpoints, do not publish current task plans as verified history, and obtain independent hidden acceptance only after the solver stops. Earlier-query admission must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query time.

## Evidence and limits

See the [episode](references/episode.md), [provenance](references/provenance.json), and packaged evidence cards. This is a single-source Workflow, not a Pattern or cross-project guarantee.

Historical CI/test execution is unknown. The committed regression assertions are available at the historical revision. Later independent qualification has changed-test-only scope with an original-base control; it establishes neither whole-project correctness nor transfer. All authored evaluation suites, including [functional definitions](evals/functional-cases.json), remain **not_executed**.
