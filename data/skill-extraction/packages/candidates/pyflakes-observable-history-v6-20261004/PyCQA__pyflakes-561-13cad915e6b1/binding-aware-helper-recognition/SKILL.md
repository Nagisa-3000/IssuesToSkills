---
name: binding-aware-helper-recognition
description: "Repair Python static-analysis recognition of imported typing helpers when module aliases must be resolved through lexical bindings rather than identifier spelling."
---

# Binding-aware helper recognition

Use this Workflow when a Python static analyzer recognizes special typing helpers by syntax, but fails to recognize an imported module alias such as `import typing as t; @t.overload`.

The supported mechanism is narrow: for an attribute whose receiver is a simple name, resolve that name through the scope stack, nearest scope first, and recognize it only when the first binding is an import of a supported typing module. Do not skip a nearer non-import binding to find an outer typing import.

## Activation and exclusions

Activate when current public evidence shows:
- A special helper detector handles simple-name attribute receivers.
- Module spelling, rather than the resolved import binding, controls recognition.
- A supported typing-module alias is misclassified.

Clarify or probe when the symptom is merely an undefined string inside `Literal`, or when the report concerns a directly imported helper alias. The original report included a directly imported `Literal` alias, but the supplied implementation changes **module receiver recognition**, and the supplied regression specifically covers an aliased module used with `overload`. Do not assume this repair fixes every direct-import alias case.

Do not activate for runtime import failures, arbitrary object attributes, unrelated annotation parsing, or a different-language analyzer without separately supported operations.

## Current probes and operations

1. [Locate and review the detector and binding model](references/actions/probe.md).
2. [Change receiver recognition and add a focused regression](references/actions/repair.md).
3. [Validate the repair and adjacent behavior](references/actions/validate.md).

Resolve semantic owners in the current checkout; the historical paths in [the episode](references/episode.md) are not current bindings. Prerequisites with UNKNOWN status authorize read-only probes, not edits. A hard prerequisite failure rejects this Workflow.

Current execution requires a public TaskContext with a pinned base, hashed anchors, actual owner bindings, observed facts and PortValues, and public Oracle bindings. Each Oracle binding uses the semantic check key `oracle:<action_id>:<source_oracle_id>` and supplies a current instruction, argv command, and evidence references. Render and execute those bound commands; this package intentionally supplies no assumed current test command.

## Validation and stop conditions

Confirm that aliased supported modules receive the same helper treatment as their unaliased forms. Preserve existing direct-name recognition, non-typing behavior, and nearest-binding shadowing semantics. Stop and investigate if scope bindings lack reliable module provenance, if the receiver is not a simple name, or if current tests expose a broader semantic change.

Refresh validation observations after edits. Structural compatibility is not repair success. Tests defined here are not executed; obtain current public results and, where formal evaluation applies, independent hidden acceptance after the solver stops. Do not turn a current task plan into historical knowledge.

## Evidence and limits

- [Historical episode](references/episode.md)
- [Canonical Workflow](references/workflow.md)
- [Source provenance](references/provenance.json)
- [Original report](references/evidence/body.md)
- [Implementation](references/evidence/fix.md)
- [Regression assertion](references/evidence/regression.md)

This is a single-source Workflow, not a multi-source Pattern. Historical tests are assertions present at the repair revision, not proof of historical execution. The later qualification reports one fail-to-pass and fifty pass-to-pass cases in changed test files only; whole-project regression and cross-project transfer were not tested.
