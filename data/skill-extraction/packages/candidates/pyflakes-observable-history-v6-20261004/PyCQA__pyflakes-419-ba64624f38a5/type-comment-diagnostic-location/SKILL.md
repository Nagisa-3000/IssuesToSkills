---
name: type-comment-diagnostic-location
description: "Repair malformed type-comment diagnostics that inherit an associated statement's position instead of the comment's own coordinates, when the diagnostic interface supports a position-only carrier."
---

# Type-comment diagnostic location

## Activation

Activate conditionally when a Python analyzer parses type comments separately and reports a malformed comment at an earlier associated statement's line.

An incorrect line number alone is insufficient. First use the [probe](references/actions/probe.md) to establish in the current public checkout that:

- The comment's own line and column are already available.
- The syntax-diagnostic path receives an associated AST node with different coordinates.
- The diagnostic consumer accepts an object exposing `lineno` and `col_offset` without requiring other AST semantics.
- Changing the diagnostic position carrier need not change semantic comment association.

Unknown facts authorize investigation only, not editing.

## Exclusions

Do not apply this workflow to ordinary Python parser errors, missing type-comment detection, parser-relative coordinates requiring translation, or consumers requiring additional AST semantics. This single historical repair does not support an invented adapter for those cases.

## Operations

Follow the semantic dependencies in the [workflow](references/workflow.md):

1. [Confirm the position path](references/actions/probe.md).
2. [Separate diagnostic coordinates from association](references/actions/edit.md).
3. [Validate the regression and adjacent behavior](references/actions/validate.md).

Actions identify semantic owners, not historical file bindings. Locate current owners and bind them explicitly before use.

## Current execution requirements

Construct a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Match producer and consumer ports on semantic role, artifact kind, language, scope, phase, and state.

For each Oracle, bind its action ID and source Oracle ID to a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>` and render the bound command before execution. Empty historical contract command arrays do not authorize execution or indicate success.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites permit probes only; hard failures reject the plan. Structural PASS predicts compatibility, not repair success. After editing, refresh stale observations and execute public checks. Independent hidden acceptance occurs after the solver stops; hidden tests never enter this guidance.

## Validation and stopping

Require a malformed-comment regression asserting the intended syntax diagnostic at the comment's own line. The historical minimal regression uses an assignment on line 1 and a malformed comment on line 2.

Also run relevant annotation tests and review the diff for unchanged parsing inputs, diagnostic class, and semantic association. Stop if association changes, diagnostics disappear, the consumer is incompatible, or a public check fails. Do not emit a successful validation output for UNKNOWN or unexecuted checks.

The repair carries both line and column; the supplied regression independently asserts only the line.

## Limits and historical authority

This is one verified historical Workflow, not a Pattern or a cross-project guarantee. [Historical assertions](references/evidence/regression.md) do not establish historical test execution.

Later qualification reports one fail-to-pass and fourteen pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer are untested. This attestation is post-cutoff provenance, not backdated learned content. No package evals or current checks have been executed by this author.

Keep formal knowledge and checkpoints frozen during evaluation. Time-reconstructed training catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time. Do not publish a current task plan as verified historical knowledge.

See [episode](references/episode.md), [provenance](references/provenance.json), and [eval definitions](evals/functional-cases.json).
