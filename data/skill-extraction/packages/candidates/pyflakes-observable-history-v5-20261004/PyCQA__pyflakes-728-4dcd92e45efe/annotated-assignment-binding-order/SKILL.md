---
name: annotated-assignment-binding-order
description: "Repair undefined-name suppression caused by binding an annotated assignment target before analyzing its initializer, while preserving annotation handling and adjacent diagnostics."
---

# Annotated assignment binding order

## Activation

Activate when a Python static analyzer reports an undefined name for an ordinary self-referential assignment such as `x = x`, but suppresses that diagnostic for `x: int = x` with no prior binding of `x`.

Also require current inspection to show that the annotated-assignment handler registers or visits the assignment target before analyzing the initializer.

Clarify or probe first when the report lacks a minimal reproduction, the scope contains a possible prior binding, or the implementation owner is unknown.

Do not activate for runtime execution errors, annotation syntax errors, forward-reference handling alone, or an analyzer whose initializer is already analyzed before target binding. This is a single-repair Workflow, not a cross-project Pattern.

## Current probes and bindings

1. Establish a public issue and pinned base; record hashes of relevant current code anchors.
2. Locate the semantic owners:
   - `annotated-assignment-handler`: the handler that analyzes annotation, initializer, and target.
   - `annotation-regression-suite`: public tests for annotated-assignment diagnostics.
3. Use a fresh scope to compare `x = x` and `x: int = x`. Record actual diagnostics rather than assuming the historical failure remains present.
4. Inspect whether the target visit installs a binding before initializer analysis. Record annotation-specific initializer branches and their behavior.
5. Bind the Actions and their public oracles to current code and executable public commands.

Historical paths and snippets are in [the episode](references/episode.md); they are not current checkout bindings.

## Operations

- [Inspect the failure and semantic owners](references/actions/inspect.md).
- [Delay target binding until after annotation and initializer analysis](references/actions/reorder.md).
- [Add an undefined-self-reference regression assertion](references/actions/regression.md).
- [Validate the repair and adjacent annotation behavior](references/actions/validate.md).

The immutable historical realization is recorded in [the Workflow](references/workflow.md). Current ordering must respect its semantic dependencies, not merely its listed Action order. Already satisfied operations may be omitted only when current evidence establishes their effects.

## Validation and stopping

Every modification requires the linked validation Action. Re-observe diagnostics after either code or test changes.

Required target behavior: in a fresh scope, `x: int = x` produces the analyzer's undefined-name diagnostic for the initializer reference. Compare against `x = x`.

Preserve existing annotation processing, any specialized initializer-as-annotation branch, assignments without an initializer, and adjacent type-annotation tests. Treat passing tests as evidence only for the checks actually run.

Stop without claiming a repair when:

- Current inspection does not establish premature target binding.
- The proposed movement alters unrelated annotation or initializer semantics.
- The reproduction or adjacent public tests fail after editing.
- Necessary current oracle bindings or behavioral checks remain unknown.

Unknown prerequisites authorize probes only. Failed applicability checks reject the repair plan. Structural compatibility does not establish repair success.

## Limits and evidence status

The supplied repair moved one target visit; it did not redesign annotation semantics. Historical regression evidence is an assertion committed with the repair, not evidence of historical test execution.

A later qualification attestation reports one fail-to-pass and 53 pass-to-pass cases in changed test files. It does not establish whole-project regression safety or cross-project transfer, and its 2026 timestamp is not pre-cutoff learned content. See [provenance](references/provenance.json).

All [evaluation definitions](evals/functional-cases.json) remain `not_executed`. No current checkout, commands, ports, or checks have been executed by this package authoring step.

For current use, record observed PortValues and tri-state semantic checks (`PASS`, `FAIL`, `UNKNOWN`). Each current oracle binding must map `action_id` and `source_oracle_id` to a public instruction, argv command, and evidence references, with check key `oracle:<action_id>:<source_oracle_id>`. Render the bound current commands; historical commands do not authorize execution. Formal evaluation keeps knowledge and checkpoints frozen, and obtains independent hidden acceptance only after the solver stops. Time-reconstructed catalogs must exclude this source's own issue, fix, cluster, aliases, copied sources, and any source unavailable before query input time.
