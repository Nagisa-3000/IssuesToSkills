---
name: version-gated-implicit-module-names
description: "Repair a Python static checker's false undefined-name diagnostic for module-level __annotations__ when current inspection confirms an interpreter-version-gated implicit-name registry."
---

# Version-gated implicit module names

## Activation and exclusions

Activate when a Python static checker incorrectly reports module-level `__annotations__` as undefined on Python 3.6 or later, and current inspection confirms that implicit module names are modeled through a registry controlled by the running interpreter version.

The supported historical repair registered `__annotations__` behind a Python 3.6-plus gate and added a version-gated bare-reference regression. This is one focused Workflow, not a Pattern supported by multiple fixes.

Do not activate for:

- ordinary unbound variables or arbitrary double-underscore names;
- runtime `NameError` or missing runtime annotation initialization;
- function-local or class annotation behavior;
- checkers whose separately configured target version makes a runtime-version gate inappropriate;
- requests to suppress undefined-name diagnostics generally.

Do not infer that `__annotations__` is a builtin or exists at runtime in every module.

## Current probes and operations

1. [Inspect current semantic owners and reproduce the symptom](references/actions/inspect.md).
2. [Edit the version-gated implicit-name registry](references/actions/register.md).
3. [Add the version-gated public regression](references/actions/regression.md).
4. [Validate both edits and adjacent behavior](references/actions/validate.md).

Bind the current implicit-name model, interpreter-version policy, scope lookup, and undefined-name regression harness. Historical paths in the [episode](references/episode.md) are not current bindings.

Before modification, create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Each Oracle binding maps `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Use check key `oracle:<action_id>:<source_oracle_id>` and render the bound command before execution. Empty commands in these source contracts mean “not yet bound,” not authorization to execute a guessed historical command.

Checks are `PASS`, `FAIL`, or `UNKNOWN`. Unknown prerequisites authorize probes only; hard semantic failures reject the plan. Structural PASS predicts compatibility, not repair success. Outputs and effects in the contracts describe intended successful results, not observations already obtained.

The [historical Workflow](references/workflow.md) records source-supported dependencies. Current ordering follows compatible ports, prerequisites, current semantic evidence, and verification obligations rather than list position. If an edit is already satisfied, observe the corresponding current artifact and bind it explicitly; do not fabricate a change port.

## Validation and stopping

Retain the explicit validation Action for each modifying Action. Execute current public regressions and the original annotated reproduction. Preserve existing implicit names, ordinary undefined-name behavior, older-version registry selection, and any asynchronous-loop branches affected by a version-predicate refactor.

Refresh stale observations after edits. If older interpreters are unavailable, distinguish static boundary review from execution and report execution as unknown. Stop on ambiguous ownership, incompatible scope/version semantics, failing checks, or a need for unsupported changes. Never claim that an unexecuted required check passed.

Independent hidden acceptance occurs after the solver stops; hidden tests and gold-derived commands never enter guidance. Formal knowledge and checkpoints remain frozen. A current task plan is not newly verified historical knowledge and must not be published as such during formal evaluation. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Evidence and limits

The historical [title](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), and [regression assertion](references/evidence/regression.md) are packaged in full as focused evidence cards. Historical execution logs are not supplied.

The later qualification attestation reports one fail-to-pass and 61 pass-to-pass cases using changed test files with an original-base control. Whole-project regression safety and cross-project transfer are untested. This attestation is [provenance](references/provenance.json), not a backdated historical event.

The authored [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions only and remain `not_executed`.
