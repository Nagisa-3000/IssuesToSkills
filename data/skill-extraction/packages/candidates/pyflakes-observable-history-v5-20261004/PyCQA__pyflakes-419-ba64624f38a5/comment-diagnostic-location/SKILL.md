---
name: comment-diagnostic-location
description: "Correct type-comment syntax-error locations when separately parsed comment text is diagnosed using an associated statement's coordinates rather than the comment's own coordinates."
---

# Comment diagnostic location

## Activation

Activate for a Python analysis pipeline that separately parses type comments and reports an invalid comment at the associated statement's line instead of the comment's actual line. Confirm that comment coordinates are available independently and that the diagnostic receives the statement as its position carrier.

Clarify and probe if only the incorrect line is known. An incorrect line alone does not establish this mechanism.

Do not activate for ordinary Python parser errors, incorrect message text, downstream display mapping errors, or pipelines already passing the correct comment coordinates.

## Operations

1. [Locate the position source](references/actions/locate.md). Bind current semantic owners and reproduce the public mismatch.
2. [Repair the carrier and regression](references/actions/repair.md). Separate diagnostic position from statement identity while preserving annotation semantics.
3. [Validate](references/actions/validate.md). Execute the public line regression and adjacent annotation checks.

The [historical Workflow](references/workflow.md) describes supported dependencies. Current operations are conditional applications, not claims that a historical developer followed this exact task plan. Historical paths appear only in the [episode](references/episode.md) and evidence.

## Current probes and bindings

Before editing, establish a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before read/write conflict checks. Matching predicate labels alone does not prove a semantic match.

Bind each Oracle's `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Use the semantic check key `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty historical command arrays are not executable authorization; adapt checks to the current public checkout.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only. Hard failures reject the repair plan. A structurally compatible plan predicts compatibility, not repair success.

## Validation and stopping

Require a public fixture with an assignment on line 1 and an invalid standalone type comment on line 2. Verify the syntax-error diagnostic reports line 2. Review propagation of both line and column, but do not infer historical column-test coverage from a line assertion.

Preserve comment-to-statement semantic association, parsed annotation text, explicit parser coordinates, diagnostic kind, and adjacent annotation behavior. Refresh invalidated observations after editing.

Stop if the position source differs from this mechanism, current owners cannot be bound, the regression misses the failing path, the carrier requires semantic AST mutation, or validation fails. Do not weaken the regression to obtain a pass.

## Limits and resources

This is one focused Workflow supported by one verified repair, not a Pattern or a claim of cross-project transfer. Historical tests are assertions available at the commit, not supplied historical execution logs. Functional eval definitions remain `not_executed`.

The later qualification attestation covers changed test files with original-base control: one fail-to-pass and fourteen pass-to-pass cases. Whole-project regression and cross-project transfer are untested. The attestation is not pre-cutoff learned content.

- [Episode](references/episode.md)
- [Workflow](references/workflow.md)
- [Provenance](references/provenance.json)
- Evidence: [title](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), [regression](references/evidence/regression.md)
- Evals: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), [functional](evals/functional-cases.json)

Keep formal knowledge and checkpoints frozen during evaluation. Do not publish current task plans as verified historical knowledge. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. Independent hidden acceptance, when provided by the host, occurs after the solver stops and is not repair guidance.
