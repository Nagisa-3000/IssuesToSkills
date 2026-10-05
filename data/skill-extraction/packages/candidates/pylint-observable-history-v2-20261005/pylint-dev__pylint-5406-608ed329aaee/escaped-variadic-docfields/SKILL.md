---
name: escaped-variadic-docfields
description: "Repair Sphinx-style Python parameter documentation when escaped variadic names fail recognition or signature matching, while preserving ordinary parameters and adjacent documentation styles."
---

# Escaped variadic documentation fields

## Activation and exclusions

Activate when a public reproduction implicates a Sphinx-specific Python parameter-documentation parser: escaped `\*args` or `\**kwargs` fields are not recognized, or unescaped starred fields incorrectly satisfy documentation under a confirmed strict Sphinx policy.

Clarify when the documentation style, enabled checker, runtime docstring text, or intended syntax is unknown. Do not activate for Google/NumPy-only parsing failures, unrelated Python string escapes, structured parameter metadata, or diagnostic-suppression requests.

This Workflow supports one historical repair, not a cross-project Pattern. It does not establish that bare `args` documentation satisfies a `*args` signature.

## Current probes

Before editing, pin the public base, hash code anchors, and locate these semantic owners:

- `sphinx-parameter-parser`: field recognition and documented-name extraction.
- `sphinx-variadic-fixtures`: public fixtures and diagnostic assertions.
- `escaped-docstring-example`: an applicable production variadic docstring, if present.

Use the [probe Action](references/actions/probe.md) to distinguish Python source spelling from runtime docstring text and compare ordinary, escaped starred, unescaped starred, and absent fields. A raw Python docstring preserves the documentation escape without the reported anomalous-backslash warning.

Confirm the intended policy from current public evidence. Do not impose the historical strict policy on a checkout with a conflicting specification.

## Operations

1. [Probe ownership and escaping](references/actions/probe.md).
2. [Repair recognition, normalization, and public assertions](references/actions/repair.md).
3. [Validate modified behavior and adjacent controls](references/actions/validate.md).

See the complete [historical Workflow](references/workflow.md). Current plans may omit already-satisfied work, but each modification retains its explicit validation closure. Resolve aliases before read/write conflict checks. Compatible ports and structural PASS predict compatibility, not repair success.

## Validation and stopping

Required public checks must establish:

- Escaped one-star and two-star Sphinx fields map to starred signature names.
- Unescaped starred fields do not satisfy documentation under the confirmed strict policy.
- Ordinary parameters still work, and absent variadic documentation still warns.
- Applicable raw escaped examples avoid the reported anomalous-backslash warning.
- Adjacent Google-style behavior and unrelated diagnostic expectations survive.

Refresh validation observations after every edit. Stop on policy conflict, incompatible owners, capture/extraction mismatch, adjacent regression, or an unavailable required public check. Sphinx rendering, if not executed, remains UNKNOWN; parser tests alone do not prove rendering success.

Maintain a current TaskContext with public issue identity, pinned base, hashed anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id/source_oracle_id` to a public instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution; historical commands are evidence, not current authorization.

Checks are PASS/FAIL/UNKNOWN. UNKNOWN prerequisites permit probes only; hard failures reject the plan. Acceptance requires PASS for required behavior, not merely a recorded validation attempt. Stop the solver before independent hidden acceptance.

## Learning and execution limits

Historical tests are committed assertions; historical CI execution is unknown. Later independent qualification supports selected changed-test controls only, not whole-project correctness or cross-project transfer. This Skill's [functional cases](evals/functional-cases.json) are unexecuted definitions.

Do not publish a current task plan as newly verified history during formal evaluation. Formal knowledge and checkpoints remain frozen. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before query time.

See [episode](references/episode.md), [provenance](references/provenance.json), and evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).
