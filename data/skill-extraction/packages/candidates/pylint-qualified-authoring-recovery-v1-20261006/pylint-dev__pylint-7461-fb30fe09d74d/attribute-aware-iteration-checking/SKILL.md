---
name: attribute-aware-iteration-checking
description: "Repair a Python mutation-during-iteration checker that reads a simple-name field from an attribute iterator AST node, preserving copy handling and adjacent mutation diagnostics."
---

# Attribute-aware iteration checking

This conditional Workflow addresses an AST field-access mismatch in a mutation-during-iteration checker. Its supported mechanism is narrow: extract `attrname` from an attribute iterator and `name` from a simple-name iterator, without changing existing inference guards or receiver comparison semantics.

## Activation

Activate when current public evidence identifies:

- A dictionary mutation check failing on an iterator's unsupported `.name` access.
- An iterator domain consisting of compatible simple-name and attribute AST forms.
- A loop over an instance dictionary attribute with assignment into a local dictionary copy.
- A separately guarded assignment receiver for which the existing `name` comparison remains valid.

If the traceback, owner, or node interfaces are unknown, clarify and inspect first. Do not activate for parser syntax failures, runtime dictionary mutation exceptions, unrelated inference failures, incompatible AST interfaces, or repairs requiring broader alias analysis.

## Operations

1. [Inspect applicability](references/actions/inspect.md): locate current semantic owners, inspect node interfaces and guards, and establish the public failure.
2. [Repair and add the regression](references/actions/repair.md): discriminate iterator forms and retain a copy-loop regression.
3. [Validate](references/actions/validate.md): run current public reproduction and adjacent diagnostic checks.

The [historical Workflow](references/workflow.md) specifies dependencies and assurances. The [episode](references/episode.md) records historical locators, source observations, and qualification limits. [Provenance](references/provenance.json) records authoritative identity and validation-only attestations.

## Current binding and execution

Historical paths are locators, not current bindings. Resolve `iteration-checker` and `iteration-functional-tests` against the current checkout.

Before editing, create a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real role bindings, observed PortValues, and current Oracle bindings. Producer and consumer ports must match their semantic role, artifact kind, language, scope, phase, and state.

Bind every Oracle by `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these current bound commands; historical commands do not authorize execution in another checkout.

Use PASS/FAIL/UNKNOWN for semantic checks. Unknown prerequisites permit probes only; hard failures reject the repair path. Expected Action effects are not observed results.

## Validation and stopping

After editing, invalidate the previous public validation observation and retain the explicit validation Action. Require observable evidence that:

- The attribute-copy reproduction no longer raises the unsupported-field exception or fatal AST checker error.
- Assignment into the copied mapping produces no dictionary-mutation diagnostic.
- Ordinary simple-name behavior, existing inference guards, and relevant adjacent mutation diagnostics remain intact.

Stop if the receiver is outside the guarded simple-name domain, accepted iterator forms are incompatible, or the repair would require changing inference or alias semantics. Missing commands, tests, or observations leave validation UNKNOWN.

Structural PASS predicts compatibility, not repair success. Execute public checks, refresh stale facts, record actual outcomes, stop the solver, and obtain independent hidden acceptance separately.

## Limits

This is a single-source Workflow, not a Pattern or claim of cross-project transfer. Historical CI/test execution is unknown; the evidence includes committed regression assertions.

Later independent qualification has scope `changed-test-files-with-original-base-control`. Its exact limits are: **Changed test files only; whole-project regression and cross-project transfer are untested.** It does not execute these newly authored functional eval definitions.

Keep formal knowledge and checkpoints frozen during evaluation. Do not publish a current task plan as newly verified historical knowledge. Earlier-query catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before query input time.
