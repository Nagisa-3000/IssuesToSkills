---
name: early-option-abbreviation-parity
description: "Align early CLI option preprocessing with established downstream abbreviation behavior when shortened options bypass early callbacks, preserving canonical options, neighboring routing, and argument consumption."
---

# Early-option abbreviation parity

## When to activate

Activate for a Python CLI with two processing layers when public evidence shows that:

- Selected options invoke callbacks before the main parser.
- The downstream parser accepts abbreviations.
- A canonical spelling invokes an early effect, but a supported shortened spelling bypasses that effect or receives incompatible downstream handling.

Clarify when only “the option is ignored” is reported. Obtain the exact invocation, intended effect, parser policy, and ownership before proposing edits.

Do not activate for deliberately exact-only parsers, plugin import failures after successful routing, applications without early preprocessing, or unresolved ambiguous prefixes.

## Current probes

Use [inspect routing](references/actions/inspect-routing.md) to locate the current semantic owners:

- `early-option-router`: registry, matching, argument splitting, and callback dispatch.
- `main-option-parser`: option namespace and abbreviation policy.
- `early-option-regressions`: public CLI/configuration tests.

Historical paths are recorded only in the [episode](references/episode.md). Bind actual current owners rather than reusing historical paths.

Create a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Compare full and shortened spellings using observable early effects. Inspect competing option names and value consumption.

Unknown prerequisites authorize probes only. Hard policy or ownership failures reject the edit plan.

## Operations

1. [Inspect routing and policy](references/actions/inspect-routing.md).
2. If the mismatch and safe boundaries are established, [edit matching and add an early-effect regression](references/actions/align-routing.md).
3. [Validate the repair and adjacent routing](references/actions/validate-routing.md).

The [historical Workflow](references/workflow.md) is an evidence-based reconstruction, not newly verified execution of a task plan.

For each current Oracle, bind `action_id` and `source_oracle_id` to a public instruction, an argv command, and current public evidence references. Use semantic check key `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty command arrays in the historical contracts require current binding; they do not authorize guessed commands.

## Validation and stopping

Check that:

- A supported abbreviation invokes its intended early callback.
- Canonical spellings retain their behavior.
- Neighboring options are not intercepted.
- Required values, supported value forms, and unmatched forwarding retain their behavior.
- The regression observes the early effect, not parsing success alone.
- Relevant existing public tests pass.

Use PASS/FAIL/UNKNOWN. Refresh validation observations after edits. Structural PASS predicts compatibility, not repair success. Failed adjacent checks block acceptance.

Stop if current policy, competing names, ownership, or public test bindings cannot be established. Do not broaden matching merely to suppress an error.

During formal evaluation, keep knowledge and checkpoints frozen. Do not publish current plans as historical knowledge. Obtain independent hidden acceptance only after the solver stops. Earlier-time catalogs must exclude the current issue, fix, cluster, aliases, copied sources, and every source unavailable before the query input time.

## Evidence and limits

The [report](references/evidence/body.md) describes a plugin-option spelling discrepancy. The [implementation](references/evidence/fix.md) adds prefix thresholds to early processing. The [committed regression](references/evidence/regression.md) observes verbose output for `--ve`; it does not cover every threshold or execute the original plugin reproduction.

Historical CI execution is unknown. Later source qualification covers changed test files only; whole-project regression and cross-project transfer are untested. This single repair supports a Workflow, not a multi-source Pattern. The authored [functional cases](evals/functional-cases.json), [activation cases](evals/activation-cases.json), and [applicability cases](evals/applicability-cases.json) remain unexecuted. See [provenance](references/provenance.json).
