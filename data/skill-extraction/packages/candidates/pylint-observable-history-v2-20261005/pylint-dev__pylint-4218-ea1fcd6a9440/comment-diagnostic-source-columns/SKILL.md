---
name: comment-diagnostic-source-columns
description: "Repair Python comment-note diagnostic columns when token-relative marker offsets are incorrectly reported as source-line coordinates; locate the current owner, use the verified token-start anchor when applicable, and validate columns without changing note detection."
---

# Comment diagnostic source columns

## Activation

Activate when a Python comment-note diagnostic reports the same small column for comments at different source positions, and public code review shows that its column is derived from a marker's index inside the comment token rather than the token's position in the source line.

This Skill addresses a specific coordinate repair: anchor the diagnostic **immediately after the comment's `#`**, using the comment token's source start plus one. It does **not** locate the first non-whitespace character or the matched TODO/FIXME marker. For `# TODO`, the historical corrected column is 1, not 2, in zero-based source coordinates.

Clarify if the required anchor or coordinate convention is unspecified. Do not activate for missing warnings, incorrect matching, non-comment diagnostics, or a consumer that explicitly requires the matched marker's position. Repository identity alone is not an activation condition.

## Current probes and bindings

Before editing, create a public TaskContext containing the current issue, pinned base, hashed code anchors, observed facts, and actual bindings for:

- `comment-note-emitter`: the Python owner that matches comment notes and emits their diagnostics.
- `comment-note-regression-suite`: the public fixtures and test runner checking diagnostic output.

Use [the probe Action](references/actions/probe.md) to confirm token/source coordinate semantics. Unknown prerequisites permit read-only probes, not edits. A hard semantic mismatch rejects this workflow.

Ports describe evidence artifacts, not executable Python objects. Bind owners in the current checkout; historical paths in [the episode](references/episode.md) are discovery hints only.

## Operations

1. [Probe the coordinate owner and anchor](references/actions/probe.md).
2. [Repair the column and public expectations](references/actions/repair.md), only after applicability is established.
3. [Validate coordinate and adjacent behavior](references/actions/validate.md).

The [Workflow contract](references/workflow.md) records the single historical realization. Current ordering follows its semantic dependencies and live observations; an already satisfied operation may be omitted only with current evidence. Do not omit validation of a modifying operation.

## Validation

Bind each source oracle to a current public instruction, argv command, and evidence references in TaskContext. Use semantic keys `oracle:<action_id>:<source_oracle_id>`. Render the actual bound commands before execution; historical commands do not authorize current execution.

Check standalone, inline, indented, spaced, and unspaced comments. Confirm the source column equals the hash token's start column plus one. Preserve warning count, line, text, note recognition, case handling, and configurable matching behavior. Run relevant adjacent public tests.

Record PASS, FAIL, or UNKNOWN separately for each check. Structural compatibility is not repair success. Refresh stale validation observations after any edit. Stop on failed preservation checks; do not blindly regenerate expectations to accept current output.

## Failure and limits

Stop or seek clarification when token coordinates are unavailable, column units differ, the desired anchor differs, or the emitter cannot be located. Encoding conversions, tab display widths, other languages, and cross-project transfer are not verified here.

The historical regression evidence consists of committed assertions; historical CI/test execution is unknown. Later independent qualification used original-base, base-with-regression, and historical-fixed controls. It establishes changed-test causality with limited adjacent coverage, not whole-project correctness. The authored [evaluation suites](evals/functional-cases.json) remain **not executed**.

This is one-source workflow knowledge, not a multi-source Pattern. Keep formal knowledge frozen during evaluation; no task-specific plan becomes newly verified history. Independent hidden acceptance is obtained only after the solver stops.
