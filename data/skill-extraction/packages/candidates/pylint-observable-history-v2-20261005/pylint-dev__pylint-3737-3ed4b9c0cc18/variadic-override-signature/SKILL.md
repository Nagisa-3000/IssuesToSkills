---
name: variadic-override-signature
description: "Repair a Python override-signature false positive when a declared-default-count comparison ignores positional variadics, while preserving ordinary mismatch diagnostics."
---

# Variadic override signature compatibility

## Activation

Activate when a Python static checker reports a signature mismatch for an override collecting `*args, **kwargs`, the base method has a defaulted parameter, and current inspection implicates a declared-default-count comparison.

Clarify if signatures, the diagnostic, or a public reproduction are missing. Do not activate for runtime forwarding errors, unrelated argument-count diagnostics, or an already-correct checker.

This is a single supported Workflow, not a cross-project Pattern. It supports a positional-variadic exception in a particular diagnostic branch, not universal compatibility of variadic overrides.

## Current probes

Create a public TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these owners in the current checkout:
- `override-signature-checker`: the Python branch comparing override defaults with reference defaults.
- `override-signature-regression-suite`: public signature-diagnostic tests.

[Inspect and reproduce](references/actions/inspect.md) before editing. Establish the causal branch and positional variadic representation; the diagnostic name alone is insufficient. Natural-language prerequisites require evidence-backed review or probes, not matching predicate names.

UNKNOWN prerequisites authorize probes only. Hard failures reject the repair.

## Operations

1. [Inspect the mechanism](references/actions/inspect.md).
2. [Guard the comparison and add coverage](references/actions/repair.md).
3. [Validate corrected and retained behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) records the sourced mechanism and dependencies. Current ordering follows compatible ports, prerequisites, semantic dependencies, and validation obligations. Already satisfied operations may be omitted only with current evidence.

Bind every Oracle to a public current instruction, argv command, and evidence references; render the bound commands before execution. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Empty contract command arrays are unbound declarations, not executable authorization. Historical paths and commands in the [episode](references/episode.md) are not current bindings.

## Validation and stop conditions

Require:
- No `signature-differs` at the collecting override.
- Retained expected diagnostics for ordinary nonvariadic default-loss controls.
- Independent review that the preceding argument-mismatch branch remains unchanged.

Refresh validation observations after edits. PASS, FAIL, and UNKNOWN are distinct; skipped or unexecuted checks are not PASS. Structural plan PASS predicts compatibility, never repair success.

Stop if the default-count branch is not causal, positional variadic detection cannot be reliably bound, public controls regress, validation remains unknown, or the proposed change suppresses unrelated diagnostics. Do not extend the exception to `**kwargs` alone or other argument categories without additional evidence.

## Authority and limits

See the [episode](references/episode.md), [implementation evidence](references/evidence/fix.md), [regression evidence](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical CI/test execution is unknown. Committed assertions are not execution logs. Later independent qualification covers changed test files with an original-base control; whole-project regression and cross-project transfer are untested. It did not execute the authored [functional cases](evals/functional-cases.json). [Activation](evals/activation-cases.json) and [applicability](evals/applicability-cases.json) cases are also unexecuted definitions.

During formal evaluation, freeze knowledge and checkpoints. Never publish a current task plan as newly verified historical knowledge. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. Obtain independent hidden acceptance after the solver stops; hidden tests never supply guidance.
