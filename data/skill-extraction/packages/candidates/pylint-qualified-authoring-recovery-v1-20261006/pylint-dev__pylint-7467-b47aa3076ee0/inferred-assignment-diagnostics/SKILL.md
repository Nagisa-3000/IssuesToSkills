---
name: inferred-assignment-diagnostics
description: "Enrich an existing invalid special-class assignment diagnostic with the inferred AST node kind while preserving inference exemptions, diagnostic identity, source locations, and adjacent behavior."
---

# Inferred assignment diagnostics

## Activation

Activate when current public evidence shows a Python static analyzer already rejects inferred non-class values assigned to `__class__`, and the requested change is to identify the inferred AST node kind in that diagnostic.

Clarify a crash-only request before editing: locate the failure boundary and determine whether diagnostic enrichment is actually relevant. Do not activate for general AST parent traversal, unpacking inference repairs, runtime class-reassignment compatibility, other languages, or changes to which values are accepted.

This is one narrow historical Workflow, not a multi-source Pattern. The historical issue reports a tuple-assignment crash, but the supplied implementation changes diagnostic text and emission arguments only. It does not demonstrate a repair to arbitrary `.value` access.

## Current probes and bindings

Use [inspection](references/actions/inspect.md) to locate these semantic owners in the current checkout:

- `special-class-assignment-checker`
- `special-class-assignment-diagnostic`
- `special-class-assignment-regression-suite`

Historical paths are reference information, not current bindings. Record a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before conflict checks.

Each current Oracle maps `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Use the semantic check key `oracle:<action_id>:<source_oracle_id>`. Render bound current commands before execution; historical commands do not authorize execution in a new checkout.

Checks are PASS/FAIL/UNKNOWN. UNKNOWN prerequisites authorize probes only. Hard failures reject the editing plan. Natural-language applicability and preservation assurances require current review or public probes, not matching predicate names.

## Operations

1. [Inspect the existing inferred-value diagnostic boundary](references/actions/inspect.md).
2. If applicable and not already satisfied, [edit the message, emission argument, and corresponding assertions](references/actions/edit.md).
3. [Validate the changed diagnostic and preserved behavior](references/actions/validate.md).

See the [complete historical Workflow](references/workflow.md). Current ordering follows ports, prerequisites, semantic dependencies, and validation obligations—not merely historical list position. An already-satisfied edit may be omitted only with current evidence supplying the required state and validation inputs. Every performed modification retains its validate Action.

## Validation and stopping

Verify inferred AST class names for rejected instance and constant cases. Preserve diagnostic symbol, source spans, object labels, confidence, valid-class acceptance, uninferable exemptions, and relevant adjacent behavior. Review individual expected-output changes; blanket snapshot regeneration is not proof.

If relevant, run the public tuple-assignment reproduction separately. A crash blocks a crash-resolution claim; a pass does not establish an unsupported traversal mechanism.

Stop if no safe existing inferred-value emission boundary exists, if classification or traversal must change, if exemptions cannot be verified, or if public checks fail. Refresh stale validation observations after edits. Structural plan PASS predicts compatibility, not repair success.

During formal evaluation, keep knowledge and checkpoints frozen. Do not publish current task plans as newly verified historical knowledge. Stop before independent hidden acceptance. Earlier-query catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before query time.

## Evidence limits

Historical test execution is unknown. Later independent qualification covers selected changed-file tests with an original-base control, not whole-project regression or cross-project transfer. Newly authored functional cases remain unexecuted.

See [episode](references/episode.md), [implementation evidence](references/evidence/fix.md), [assertion evidence](references/evidence/regression.md), and [provenance](references/provenance.json).
