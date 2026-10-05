---
name: conservative-private-member-scan
description: "Repair a Python private-member usage scan that reads a name-only AST field from a compound receiver, using a receiver-type guard and conservative search termination."
---

# Conservative private-member scan

## Activation and exclusions

Activate when public evidence identifies a private-member usage scan over Python Name and Attribute nodes, an unchecked receiver-name access, and a compound receiver such as `self.__class__` that triggers an analyzer crash.

Clarify when only the exception text is available. Establish the failing owner, receiver shape, and candidate-search control flow before editing.

Do not activate for application runtime errors, unrelated AST failures, incompatible node interfaces, or requirements for precise attribution of arbitrary compound receivers. This Workflow supplies a conservative crash repair, not an inference algorithm.

## Current probes

Use [inspection](references/actions/inspect.md) to bind these semantic owners:
- `private-usage-scan`: the private-member usage checker.
- `private-usage-regressions`: its public fixtures and diagnostic expectations.

Record the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings in a current TaskContext. Historical paths in [the episode](references/episode.md) are not automatic current bindings.

Each current Oracle maps `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Render bound commands before execution. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Empty source command arrays require current binding; they do not authorize skipping validation.

Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only. Hard failures reject the repair. Structural PASS predicts compatibility, never repair success.

## Operations

1. [Inspect the receiver assumption](references/actions/inspect.md).
2. [Guard the scan and add the regression](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) supplies the dependency and verification closure. Current ordering follows ports, prerequisites, semantic dependencies, and validation. Omit already-satisfied operations only when current evidence establishes their outputs and effects.

The evidenced mechanism checks receiver type before reading `.name`. A non-Name receiver **breaks** the current candidate's usage-search loop. In its `for/else` structure, this suppresses the candidate's unused-member warning. The break occurs before attribute-name comparison: it does not prove that the compound expression references the candidate. Do not substitute `continue`.

## Validation and stopping

Retain the explicit validate Action after the modifying Action. Refresh stale validation observations after edits. Verify:
- The chained receiver causes no fatal analyzer crash.
- The fixture acquires no unexpected unused-private-member warning.
- Bare-name and accepted simple-receiver behavior remains intact.
- Argument exclusion and ordinary unused-member emission remain intact.

Stop if the node model or search structure differs, conservative suppression is unacceptable, baseline failures cannot be isolated, or public checks fail. Do not broaden the edit into exception swallowing or unsupported inference.

Completion requires passing public checks on the current snapshot, not merely an existing test report. Obtain independent hidden acceptance after the solver stops; hidden tests must not enter guidance. Do not publish a current task plan as newly verified historical knowledge.

## Evidence and limits

See [episode](references/episode.md) and [provenance](references/provenance.json). One independently qualified repair supports this Workflow; no Pattern or cross-project transfer is claimed.

Historical assertions were committed with the repair; historical CI execution is unknown. Later independent qualification covers changed-test scope with an original-base control, not whole-project correctness. Authored [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) cases remain unexecuted.

For time-reconstructed training, exclude the query's own issue, fix, cluster, aliases, copied sources, and every discovery input unavailable before query input time. Keep formal knowledge and checkpoints frozen.
