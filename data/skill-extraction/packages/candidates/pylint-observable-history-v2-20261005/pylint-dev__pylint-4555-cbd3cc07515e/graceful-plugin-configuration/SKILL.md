---
name: graceful-plugin-configuration
description: "Repair Python plugin-configuration startup failures caused by missing modules, reporting a configuration diagnostic while allowing ordinary analysis to continue."
---

# Graceful plugin configuration

## Conditional activation

Activate when a public reproduction shows `ModuleNotFoundError` while loading a configured Python plugin, startup aborts ordinary analysis, and current code has identifiable plugin lifecycle and diagnostic owners.

Clarify or perform read-only probes when the exception, startup phase, continuation policy, or reporting lifecycle is unknown. Do not activate for arbitrary plugin exceptions, incompatible registration APIs, non-Python loaders, or mandatory fail-fast policy.

This is a single-source Workflow, not a Pattern or a demonstrated cross-project generalization. Historical paths in the references are evidence, not current bindings.

## Current probes

Use [inspect](references/actions/inspect.md) to establish:

- The actual exception and plugin lifecycle phase.
- Retention of configured plugin identities, registration ordering, duplicate suppression, and optional configuration hooks.
- Whether configuration errors can occur before statistics, file context, and text-template initialization.
- Current owner bindings and public baseline observations for successful plugins and ordinary diagnostics.
- Compatibility of the historical `ModuleNotFoundError` boundary with current requirements. Historically the guarded blocks included registration and configuration hooks, not just imports.

Record a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Each Oracle maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render current bound commands before executing them. Historical commands do not authorize execution in a different checkout. Checks are PASS, FAIL, or UNKNOWN: unknown prerequisites authorize probes only; hard incompatibilities reject the plan. Structural PASS predicts compatibility, not repair success.

## Operations and validation

1. [Inspect startup and early reporting](references/actions/inspect.md).
2. [Repair the coupled plugin and diagnostic lifecycle](references/actions/repair.md).
3. [Validate recovery and adjacent behavior](references/actions/validate.md).

The [canonical Workflow](references/workflow.md) specifies dependencies and preserved behavior. Current plans may omit already satisfied operations only with current evidence; every modification retains its explicit validation closure.

Validate through the actual configuration/reporting path. Observe a plugin-specific configuration error, no unhandled missing-module startup traceback, and an ordinary source diagnostic after plugin failure. Also check valid plugins, duplicate suppression, optional hooks, early message state, default/custom templates, normal diagnostics, and propagation of exceptions outside the supported class.

A handled configuration error may legitimately produce a nonzero diagnostic exit status. Do not equate graceful continuation with unconditional exit status zero.

## Stop conditions and limits

Stop if owners remain unresolved, early reporting cannot be made safe using the evidenced mechanism, exception policy differs, preserved behavior fails, or public validation cannot run. Do not catch all exceptions, silently discard configuration errors, or invent an adapter for a different runtime.

Refresh stale validation observations after edits. Independent hidden acceptance occurs after the solver stops and is the host's responsibility. Hidden tests must not enter guidance. Keep formal knowledge and checkpoints frozen during evaluation; never publish a current plan as newly verified historical knowledge. Time-reconstructed admission must exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before query time.

See the [episode](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

The historical fixture directly asserted continued ordinary analysis, not complete configuration-error output. Historical CI execution is unknown. Later qualification verified one fail-to-pass and 31 pass-to-pass cases within changed-test-file scope with original-base controls; two cases were skipped. Whole-project regression and transfer are untested. This qualification did not execute this Skill.

All [functional definitions](evals/functional-cases.json), [activation definitions](evals/activation-cases.json), and [applicability definitions](evals/applicability-cases.json) remain unexecuted. See [provenance](references/provenance.json).
