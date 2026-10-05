---
name: inference-failure-containment
description: "Contain inference-library failures at a Python length-condition checker boundary while retaining undefined-variable diagnostics and established diagnostics for inferable expressions."
---

# Inference failure containment

## Conditional activation

Activate when public reproduction and current code inspection show a Python static analyzer crashing while consuming argument inference for `len()` in a condition. The supported repair is a local catch of the inference library's `InferenceError` family followed by return from that checker invocation.

An exception name alone does not establish applicability. Begin with the [boundary probe](references/actions/probe.md).

Clarify if the failing input, traceback, current inference API, or public diagnostic harness is missing. UNKNOWN prerequisites authorize probes only, not edits.

## Exclusions

Do not use this Workflow for application runtime `NameError`, parsing failures, unrelated callbacks, or requests to infer unsupported types. Do not broaden the repair to `except Exception`, suppress independent variable checking, or catch errors around the entire callback.

This is a single-history Workflow, not a cross-project Pattern.

## Current binding and probes

Build a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues where present, and current Oracle bindings.

Locate and bind:

- `role:length-condition-checker`: the current Python callback consuming length-argument inference;
- `role:length-condition-regression-suite`: the public fixtures and diagnostic expectations exercising that callback.

Confirm the reproduced exception belongs to the currently available `InferenceError` family. Inspect how a local return interacts with independent undefined-variable checking. Historical paths in the [episode](references/episode.md) are evidence, not automatic current bindings.

Each current Oracle maps its Action ID and source Oracle ID to a current public instruction, argv array, and evidence references. Use semantic check key `oracle:<action_id>:<source_oracle_id>`. Render bound commands before executing them. Contract command arrays are empty because historical locations do not authorize current commands.

Checks are PASS, FAIL, or UNKNOWN. Hard incompatibility rejects the plan. Structural PASS predicts compatibility only, never repair success.

## Operations

1. [Probe and bind the inference boundary](references/actions/probe.md).
2. [Guard inference-result consumption](references/actions/guard.md).
3. [Define both unresolved-name regressions](references/actions/regression.md).
4. [Validate containment and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) specifies supported semantic dependencies. After probing, the two edits may occur in either order; public validation follows both. Current ordering follows bindings, prerequisites, and verification obligations rather than historical list position. Already satisfied operations may be omitted only with current evidence.

## Validation and stopping

Require direct undefined-name and undefined-name-subscript length conditions to complete analysis without an uncaught inference traceback. Both retain undefined-variable diagnostics; neither receives a speculative `len-as-condition` message.

Compare existing inferable-length and generator/comprehension cases against their retained diagnostic expectations. A diagnostic-producing analyzer can legitimately exit nonzero: interpret exit status through the current public harness rather than equating nonzero with a crash.

Refresh validation after either edit. Stop if the exception hierarchy is incompatible, the failure occurs outside this boundary, or adjacent behavior changes. Do not rewrite unrelated expectations to conceal a regression.

## Evidence and limits

The [episode](references/episode.md), [provenance](references/provenance.json), and [functional definitions](evals/functional-cases.json) distinguish historical assertions from execution.

Historical regression assertions were committed; historical CI/test execution is unknown. Independent qualification performed later used original-base controls and a changed-test-only scope. Whole-project correctness and cross-project transfer are untested. That qualification did not execute this Skill's functional cases, which remain **not_executed**.

Use public current checks only. Independent hidden acceptance occurs separately after the solver stops. During formal evaluation, freeze knowledge and checkpoints; do not publish a current task plan as newly verified historical knowledge. Time-reconstructed catalogs exclude the task's own issue, fix, cluster, aliases, copied sources, and every source unavailable before query time.
