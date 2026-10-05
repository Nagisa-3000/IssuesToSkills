---
name: context-item-resource-diagnostics
description: "Repair resource-management false positives caused by immediate-parent-only recognition of Python with items, while preserving diagnostics for unmanaged calls in the body."
---

# Context-item resource diagnostics

## Activation and exclusions

Activate when a Python resource-management diagnostic flags a resource call nested in a conditional expression used as a `with` item, and current inspection confirms that the diagnostic exempts only calls whose immediate parent is the `with` node.

Do not activate merely because the flagged call has a `with` ancestor. A separate resource call in the body remains unmanaged and must remain diagnosable. This Workflow does not cover asynchronous context managers, arbitrary languages, resource escape analysis, or a different diagnostic mechanism.

Clarify or probe when the flagged location, diagnostic owner, AST library, frame boundary, or item-span semantics are unknown. One verified repair supports this Workflow; it does not establish a cross-project Pattern.

## Operations

1. [Probe the current semantic owners and AST boundaries](references/actions/probe.md).
2. [Modify recognition and add public regression assertions](references/actions/repair.md).
3. [Validate the changed checker and adjacent diagnostics](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records the sourced realization. Its ordering is not an unconditional current task plan. Drop an operation only when current evidence establishes that its effect is already satisfied.

## Current binding requirements

Construct a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve semantic owners in the current checkout; historical paths are references, not automatic bindings.

Each current Oracle maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Record its semantic check under `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution. Empty commands in the contracts mean unbound, not permission to execute historical commands or guess hidden-test commands.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject the plan. Structural PASS predicts compatibility, not repair success. Port compatibility requires agreement on semantic role, artifact kind, language, scope, phase, and state.

## Validation and stopping

Observe all of these boundaries:

- Conditional context-item resource calls, including both ternary branches, avoid the false positive.
- The original multiple-item `open`/`nullcontext` reproduction avoids the false positive.
- Direct single-line and multiline context items retain correct diagnostics.
- A separate resource call in the `with` body still warns.
- Existing adjacent resource-management assertions retain their diagnostic expectations.

Refresh validation observations after every edit. Stop if the current mechanism differs, parent traversal or frame boundaries cannot be bound safely, source spans cannot distinguish header expressions from body calls, or adjacent warnings disappear. Do not replace item recognition with blanket suppression of all `with` descendants.

The historical implementation used an inclusive line-range approximation to item membership. It is not proof of structural ownership for every syntax form or every nested resource call.

## Evidence and limits

See the [episode](references/episode.md), [provenance](references/provenance.json), and evaluation definitions: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json).

Historical tests are committed assertions; historical CI execution is unknown. Later qualification used an original-base control and selected functional tests only. Whole-project correctness and cross-project transfer were not tested. The newly authored Skill evaluations are **not_executed**.

During formal evaluation, keep knowledge and checkpoints frozen; do not publish a current task plan as newly verified historical knowledge. Time-reconstructed admission must exclude the task's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query time, including discovery-context dependencies. After the solver stops, obtain independent hidden acceptance separately from public validation.
