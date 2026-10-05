---
name: typevar-acronym-default-style
description: "Repair a default TypeVar naming rule that rejects acronym-leading mixed-case names while preserving adjacent naming boundaries, custom configuration, and variance diagnostics."
---

# TypeVar acronym default style

Skill/Workflow ID: `workflow:verified-history:23d822a5fcdadb4939406c43`

## Activation

Activate when the **default TypeVar naming rule** rejects names such as `HVACModeT` or `IPAddressT`, and current public evidence identifies a mixed-case grammar branch that allows only one uppercase-start character per segment.

Clarify effective configuration when it is unknown. Do not activate for intentional custom expressions, ordinary class naming, variance-only diagnostics, arbitrary uppercase suffix acceptance, or an already-correct default rule.

This package is a single historical Workflow, not a Pattern or evidence of cross-project transfer.

## Current probes and bindings

Use [locate and diagnose](references/actions/locate.md) before editing. Locate the current semantic owners of the default TypeVar rule, regression assertions, and naming documentation. Historical paths in [the episode](references/episode.md) are orientation only.

Record a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Inspect effective configuration; distinguish `invalid-name` from variance diagnostics.

Bind each Oracle by `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render current bound commands before execution. Empty source-contract command arrays are not executable commands, and historical commands do not authorize current execution.

## Operations

Follow [the Workflow](references/workflow.md):

1. [Locate and diagnose](references/actions/locate.md).
2. [Repair the uppercase run and add boundary assertions](references/actions/repair.md).
3. [Validate the repair and adjacent behavior](references/actions/validate.md).

The supported mechanism adds repetition to the uppercase-start class inside the existing mixed-case branch. It does not substitute unrestricted PascalCase for the existing grammar.

Current ordering follows ports, prerequisites, and semantic dependencies, not historical list position. Omit already-satisfied operations only with current evidence. Retain the explicit validation Action for every executed modification.

## Validation and stopping

Checks are PASS/FAIL/UNKNOWN. UNKNOWN prerequisites authorize probes only; hard failures reject an edit plan. Structural PASS predicts compatibility, not repair success.

Require public checks showing:
- no `invalid-name` for `HVACModeT`, `IPAddressT`, and `_IPAddress`;
- continued rejection of `IPAddressU`, `DeviceType`, and underscore-separated all-capital forms;
- preserved ordinary positive names, leading-underscore boundaries, and variance suffix grammar;
- preserved custom-pattern selection and incorrect-variance diagnostics;
- naming examples consistent with the narrow relaxation.

Refresh stale validation observations after edits. Stop if current ownership is ambiguous, configuration explains the rejection, the defect is not reproduced, or the current grammar requires an unsupported redesign. Failed or UNKNOWN preservation checks prevent a success claim.

Obtain independent hidden acceptance after the solver stops. Keep formal knowledge and checkpoints frozen; do not incorporate hidden tests into guidance or publish a task plan as newly verified history. Earlier-query admission must exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before its input time.

## Evidence and limits

See [episode and qualification review](references/episode.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

Historical CI execution is unknown. Later independent source qualification supports only the supplied changed-test-file scope with original-base control. Whole-project correctness and cross-project transfer are untested. Qualification does not execute this Skill's [functional cases](evals/functional-cases.json); every authored eval suite remains `not_executed`.
