---
name: parse-before-line-filtering
description: "Repair Python duplicate-code preprocessing when diagnostic suppression removes source lines before secondary AST analysis, breaking valid syntax or original source coordinates."
---

# Parse before line filtering

## Conditional activation

Activate when public current evidence establishes that:

- Original Python source is valid.
- Duplicate-code preprocessing reparses source to identify imports or function signatures.
- Diagnostic suppression removes physical lines before that secondary parse.

A suppressed function body can leave an empty suite. Early compaction can also disconnect structural line ranges from original source coordinates.

Clarify when only an exception is known: obtain source, options, traceback, and current preprocessing order. Do not activate for invalid original source, unrelated initial parser failures, incompatible non-Python interfaces, or a pipeline already parsing complete source before suppression.

## Operations

1. [Probe applicability and bind semantic owners](references/actions/probe.md).
2. [Retain complete source and defer suppression](references/actions/edit.md).
3. [Validate corrected and adjacent behavior](references/actions/validate.md).

Read the [episode](references/episode.md), [historical Workflow](references/workflow.md), and evidence for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [committed assertions](references/evidence/regression.md).

Locate current semantic owners:

- `duplicate-preprocessing`: ingestion, complete-source storage, structural exclusions, and normalized comparison-line construction.
- `duplicate-regression-tests`: public duplicate-code suppression and preprocessing tests.

Historical paths are evidence, not automatic current bindings.

## Current probes and prerequisites

Build a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Inspect actual parser input. Confirm the diagnostic-enablement API uses the intended diagnostic identity and original one-based physical coordinates. Locate callback-free callers and public tests before editing.

Each Oracle must map `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty contract commands require current binding; historical commands are not execution authorization.

Use PASS/FAIL/UNKNOWN. Unknown prerequisites authorize probes only; hard applicability failures reject the plan. Structural PASS predicts compatibility, not repair success. Resolve owner aliases before read/write conflict checks and require exact semantic compatibility of connected ports.

## Repair boundary

Keep complete decoded source through AST-dependent preparation. Carry an optional diagnostic-enablement callback separately through the relevant layers. Apply suppression during normalized comparison-line construction using original one-based line numbers.

Preserve diagnostic suppression, original reporting coordinates, enabled duplicate reports, import/signature exclusions, and callback-free operation. Do not hide syntax errors, insert synthetic suites into user source, disable structural analysis, or remove suppression support.

## Validation and stopping

Require current public observations of:

- Intact source reaching structural parsing.
- Disabled lines excluded afterward without renumbering retained coordinates.
- Scoped and per-line suppression without fatal parsing output.
- Enabled reports, structural exclusions, raw-string/docstring handling, and callback-free behavior meeting public expectations.

Check expected output independently of absence of fatal output: a report can survive while another file crashes. Respect fixture-specific diagnostic exit expectations rather than demanding zero from every linter invocation.

Refresh stale validation observations after edits. Stop on unresolved bindings, unknown callback semantics, incompatible ports, failed checks, or missing preservation evidence. Source review alone does not prove runtime success.

Obtain independent hidden acceptance only after the solver stops; do not incorporate hidden results into this Skill. Formal knowledge and checkpoints remain frozen. Do not publish current task plans as newly verified historical knowledge.

## Limits

This is a single-source Workflow, not a Pattern or a cross-project transfer claim. Historical CI/test execution is unknown. Later qualification has scope `changed-test-files-with-original-base-control` and exact limits: **Changed test files only; whole-project regression and cross-project transfer are untested.**

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions are **not_executed**.

See [provenance](references/provenance.json). Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before query time.
