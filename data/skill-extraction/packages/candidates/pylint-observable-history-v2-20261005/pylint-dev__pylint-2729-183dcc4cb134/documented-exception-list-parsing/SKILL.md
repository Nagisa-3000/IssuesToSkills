---
name: documented-exception-list-parsing
description: "Repair false missing-exception-documentation warnings caused by rejecting or failing to split a documented exception list, after confirming the mismatch in the current Python docstring parser."
---

# Documented exception list parsing

This conditional Workflow Skill has one historical repair as support. It is not a Pattern or a claim of cross-project transfer.

## Activation and exclusions

Activate when a Python documentation checker reports an exception as undocumented although a Sphinx raises field or Google Raises entry includes its name in a multiple-exception declaration.

First confirm a documentation recognition or extraction defect. Ask for the public reproduction, docstring, warning output, and checker configuration when these are unavailable.

Do not activate for genuinely missing documentation, disabled checking, configuration defects, or failures confined to exception inference. Other languages, arbitrary type grammars, and new NumPy-style list support are outside the evidenced scope.

## Current probes

Use [diagnose](references/actions/diagnose.md) before editing. Locate these semantic owners in the current public checkout:

- `docstring-type-parser`: Python type recognition and documented-exception collection.
- `raise-doc-tests`: public tests for missing-raises diagnostics.

Historical paths in [the episode](references/episode.md) are not current bindings. Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Compare list declarations with singleton and genuinely missing-documentation controls. Inspect whether recognition rejects the list or collection retains an unsplit declaration. Unknown prerequisites permit probes only; hard mismatches reject the plan. Do not force an edit if the reproduction already works.

## Operations

Follow the dependencies and matching ports in [the workflow](references/workflow.md):

1. [Diagnose](references/actions/diagnose.md) without source edits.
2. [Repair](references/actions/repair.md) recognition and extraction together, adding public regressions.
3. [Validate](references/actions/validate.md) the edited checkout and adjacent behavior.

Preserve singleton declarations, existing supported type forms, genuine missing-documentation warnings, and Google's existing description handling. Do not suppress warnings globally or change exception inference to compensate for documentation parsing.

## Validation and stopping

Map each current Oracle's `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Render bound commands before execution. Historical commands do not authorize current execution. Use `oracle:<action_id>:<source_oracle_id>` check keys with PASS, FAIL, or UNKNOWN.

An edit invalidates `public-validation-observed`, not the behavior assurances. Refresh validation after the final edit. Recording results is not equivalent to passing them: acceptance requires the target behavior and every preserved assurance to pass.

Stop if the reproduction remains broken, real missing documentation stops warning, supported syntax regresses, owner bindings mismatch, or reliable checks cannot run. Structural plan PASS predicts compatibility, not repair success. Obtain independent hidden acceptance, where required, after the solver stops; formal knowledge and checkpoints remain frozen. Never use hidden tests or gold-derived commands as guidance.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and evidence cards for [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. Later independent qualification checked only the changed raise-documentation test file: the original base passed 44 tests; base with the added regressions failed two tests while retaining 44 passes; the fixed tree passed all 46. Whole-project regression and cross-project transfer were not checked.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are unexecuted definitions. Source qualification did not execute them.

Time-reconstructed training admission must exclude own issue, fix, cluster, aliases, copied identities, and every source unavailable before the query input time. Do not backdate discovery or qualification.
