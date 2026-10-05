---
name: configured-extension-initialization
description: "Repair a Python functional-test harness that reads configured extensions but omits their registration before applying extension-owned options."
---

# Configured extension initialization

Skill and canonical Workflow ID: `workflow:verified-history:8cca50f66c7ae1d6c7d7631c`.

## Activation

Use when current public evidence shows a Python functional-test harness reading per-test configuration that requests an available extension, then applying configuration without first registering that extension. Missing extension diagnostics and ineffective extension-owned options are relevant symptoms, not sufficient diagnoses by themselves.

Clarify when the configuration, plugin availability, diagnostic identity, or initialization order is unknown. Do not activate for an internal checker-analysis defect, an unavailable dependency, a production CLI problem alone, or an initializer that already registers extensions before applying options.

This is a single-history conditional Workflow, not a Pattern or a verified cross-project abstraction.

## Current probes

Start with [inspect initialization](references/actions/inspect.md). Bind current semantic owners:

- `functional-config-initializer`: per-test configuration reading and application.
- `extension-module-loader`: existing extension registration API.
- `config-list-normalizer`: existing plugin-list normalization helper.
- `functional-extension-fixtures`: source, configuration, and expected-output fixtures.
- `public-functional-runner`: public fixture discovery and assertion execution.

Historical paths appear only in [episode](references/episode.md) and [evidence](references/evidence/implementation.md); they are not automatic current bindings.

Build a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Each Oracle maps `action_id/source_oracle_id` to its public current instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty contract command arrays require current binding.

## Operations

1. [Inspect](references/actions/inspect.md) whether the registration stage is omitted.
2. [Register](references/actions/register.md) requested modules after configuration reading and before option application.
3. [Add regressions](references/actions/regressions.md) exercising extension-owned options and exact diagnostics; review adjacent extension fixtures newly exposed by loading.
4. [Validate](references/actions/validate.md) both edits and preserved adjacent behavior.

Use the dependencies in the [historical Workflow](references/workflow.md), not historical list position alone. Current plans may omit already-satisfied edits but must retain validation for every performed modifying Action. Ports must agree on semantic role, artifact kind, language, scope, phase, and state. Do not bind Python interfaces to incompatible concrete runtime objects or invent a bridge.

## Validation and stopping

Require public evidence of correct registration order, effective extension-owned options, exact diagnostic multiplicity and locations, and preserved ordinary functional behavior. Review absent-plugin-option and missing-option-file behavior. Do not blindly accept newly generated expected output.

Unknown prerequisites authorize probes only; hard failures reject the modifying plan. Mark checks PASS, FAIL, or UNKNOWN from actual evidence. Edits invalidate validation freshness, not the behavior assurances that must survive. Refresh stale observations after edits. Structural plan PASS predicts compatibility, not repair success.

Stop if registration already occurs correctly, loader semantics are incompatible, plugin import availability is the actual problem, or adjacent behavior regresses. Do not weaken assertions to obtain green tests.

Obtain independent hidden acceptance only after the solver stops. Hidden tests and gold-derived commands are not guidance inputs. Keep formal knowledge and checkpoints frozen. Earlier-time catalogs exclude the task's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before the query input time.

## Evidence and limits

Read the [episode](references/episode.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), [regressions](references/evidence/regressions.md), and [provenance](references/provenance.json).

Historical test/CI execution is unknown. Committed assertions are not execution logs. Later controlled source qualification supports only changed test files with original-base controls; whole-project regression and cross-project transfer remain untested. It does not execute this newly authored Skill. The [functional cases](evals/functional-cases.json) remain `not_executed`.
