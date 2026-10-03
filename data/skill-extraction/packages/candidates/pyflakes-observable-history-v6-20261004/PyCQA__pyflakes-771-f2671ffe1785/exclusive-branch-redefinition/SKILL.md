---
name: exclusive-branch-redefinition
description: "Repair false unused-redefinition diagnostics for same-name definitions in mutually exclusive match cases when a Python analyzer's shared branch-alternative classifier omits match statements."
---

# Exclusive-branch redefinition classification

## Activate conditionally

Use this Workflow when a Python static analyzer reports an unused-redefinition diagnostic for same-name definitions in different cases of a single `match` statement, and current inspection shows that the diagnostic relies on a shared alternative-branch classifier that handles other branching constructs but omits `match`.

The historical repair is narrowly supported: recognizing each match case's body as a separate alternative eliminated the reported false positive without changing the existing `if` and `try` alternatives.

Do not activate merely because a diagnostic mentions redefinition. Exclude sequential definitions, definitions in the same case, genuine unused redefinitions, and implementations whose problem lies in pattern binding or scope creation rather than branch classification. If the classifier or diagnostic mechanism is unknown, probe before selecting edits.

## Current probes and bindings

Before editing:

1. Bind the current semantic owners: diagnostic alternative classifier, match regression suite, and public test runner.
2. Reproduce the public report with two same-name function definitions in different match cases and a use after the match.
3. Inspect the caller of the classifier to confirm that its alternatives are used to determine mutually exclusive definitions.
4. Check the supported Python versions and whether referring to `ast.Match` requires a runtime guard.
5. Locate adjacent `if`/`try` and genuine-redefinition checks.

Use [the probe Action](references/actions/probe.md). Historical paths are recorded in [the episode](references/episode.md), not assumed to be current bindings.

Unknown prerequisites authorize inspection and public probes only. A hard mismatch, such as a non-Python owner or a classifier unrelated to this diagnostic, rejects this Workflow.

## Operations

The canonical [Workflow](references/workflow.md) connects:

- [Probe current applicability](references/actions/probe.md).
- [Recognize match-case alternatives](references/actions/classify.md).
- [Add the public regression assertion](references/actions/regression.md).
- [Validate the edits and adjacent behavior](references/actions/validate.md).

The two edits may follow the probe independently. Validation must follow both edits. An already-satisfied edit may be omitted in a current plan only after current evidence establishes its effect; its required validation and preserved behavior remain obligations.

## Validation and stopping

Bind public current oracles to concrete instructions and argv commands before execution. Render those commands in the current plan; no historical path or command grants execution authority. Record each binding under `oracle:<action_id>:<source_oracle_id>` and evaluate PASS, FAIL, or UNKNOWN.

Require:

- No unused-redefinition diagnostic for the match-case regression.
- Existing alternative classification for `if` and `try` remains unchanged.
- Genuine sequential redefinitions remain detectable.
- Supported runtimes can still import and use the analyzer.
- Relevant public tests pass.

Edits stale prior validation observations. Refresh them after all modifications. Stop and reassess if exclusivity semantics, version compatibility, or adjacent diagnostic behavior cannot be established. Structural compatibility is not repair success.

## Authority and limits

This is one historical Workflow, not a cross-project Pattern. Its source is a single independently verified repair available before the cutoff. See [provenance](references/provenance.json) and [evidence](references/evidence/fix.md).

The historical regression is an assertion present at the repair commit; the supplied historical record does not report its execution. A later qualification reports one fail-to-pass and seven pass-to-pass checks, limited to changed test files with an original-base control. Whole-project regression and cross-project transfer were not tested. That later attestation is provenance, not backdated historical knowledge.

The bundled [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions only and remain unexecuted. During formal evaluation, freeze this knowledge and checkpoints; do not publish a current task plan as historical knowledge. Independent hidden acceptance belongs after the solver stops, not in Action guidance.
