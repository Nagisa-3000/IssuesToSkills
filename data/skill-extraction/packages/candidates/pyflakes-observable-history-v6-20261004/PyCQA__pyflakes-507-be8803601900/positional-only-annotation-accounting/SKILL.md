---
name: positional-only-annotation-accounting
description: "Conditionally repair false unused-import diagnostics caused by a Python analyzer omitting positional-only parameter names and annotations from its function-argument accounting."
---

# Positional-only annotation accounting

## Activation and exclusions

Activate when public evidence shows that an imported name used in a positional-only parameter annotation is reported unused **and** inspection confirms that the function-argument collector omits positional-only arguments.

A representative public reproduction is:

```python
from datetime import datetime as Foo, time as Bar

def x(a: Foo, /, *, b: Bar):
    pass
```

Do not apply this repair merely because an unused-import diagnostic occurs. Exclude string-annotation resolution defects, import-resolution defects, unsupported parser syntax, and collectors that already account for positional-only annotations. Unknown causes require inspection, not an edit.

## Current probes and operations

Locate and bind these semantic owners in the current checkout:

- `function-argument-collector`: collects parameter names and annotations.
- `annotation-test-suite`: public regression harness for annotation references.

Use the [probe](references/actions/probe.md) to establish the omission, AST support, and public reproduction. If confirmed, [repair the collector](references/actions/repair.md), [add the regression](references/actions/regression.md), and [validate both edits](references/actions/validate.md). The [canonical Workflow](references/workflow.md) records dependencies and assurances.

Before execution, create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps its Action ID and source Oracle ID to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before running them. Empty command arrays in the Action cards are unbound templates, not executable authorization.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only; hard failures reject the repair plan. Port compatibility and structural PASS predict compatibility, not repair success.

## Validation and stopping

Required current checks are:

- An import used only by a positional-only annotation is not reported unused.
- The mixed positional-only/keyword-only reproduction no longer produces the false positive.
- Ordinary and keyword-only annotation accounting, parameter binding, genuine unused-import detection, and supported-runtime compatibility remain intact.
- The focused assertion and adjacent public annotation tests execute successfully.

Edits invalidate the freshness of public validation observations, not the required behavior assurances. Refresh those observations after the last edit. A skipped target assertion does not establish success on a runtime supporting the syntax. Stop on a different causal mechanism, failed check, unresolved prerequisite, or unbound required Oracle.

Obtain independent hidden acceptance after the solver stops; public checks alone do not establish hidden acceptance. Do not publish a current task plan as newly verified historical knowledge or during formal evaluation. Keep formal knowledge and checkpoints frozen. Time-reconstructed training catalogs must exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.

## Evidence and scope

Read the [episode](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), [regression](references/evidence/regression.md), and [provenance](references/provenance.json).

This is a single-repair Workflow, not a Pattern or a cross-project claim. Historical evidence supplies a merged implementation and committed regression assertion, not a historical execution log. Later qualification reports one fail-to-pass and 24 pass-to-pass cases in changed test files only; whole-project regression and cross-project transfer are untested. That later attestation is not backdated or treated as pre-cutoff learned content.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`. No current execution result or deterministic executed oracle is supplied.
