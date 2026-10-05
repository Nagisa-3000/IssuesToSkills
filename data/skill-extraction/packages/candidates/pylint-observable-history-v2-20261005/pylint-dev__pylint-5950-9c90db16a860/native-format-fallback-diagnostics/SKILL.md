---
name: native-format-fallback-diagnostics
description: "Separate native output-format help and routing from Graphviz capability diagnostics in a Python CLI, preserving supported output and continuation when capability discovery is inconclusive."
---

# Native format and fallback diagnostics

## Activation and exclusions

Activate when a public report shows that a Python CLI supports native output serializers but reports only delegated Graphviz formats after an invalid format argument. The relevant defect is misleading format ownership or fallback diagnostics, not failure to serialize a valid native format.

Clarify when the requested format, public reproduction, diagnostic origin, or backend is unknown. Do not activate for diagram-content bugs, unrelated option parsing, a different renderer contract, or requests to normalize leading dots automatically.

This is a conditional Workflow supported by one historical repair. It is not a Pattern and does not establish cross-project transfer.

## Current probes

Establish a current public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate the current semantic owners for:

- output-format selection and CLI help;
- native serializer inventory;
- Graphviz availability and capability discovery;
- conversion dispatch;
- public format and adjacent import-path tests.

Run the [inspection operation](references/actions/inspect.md) before editing. UNKNOWN prerequisites authorize probes only. A hard semantic incompatibility rejects this realization. Historical paths and format inventories in the [episode](references/episode.md) are evidence, not automatic current bindings.

## Operations

Use the [Workflow contract](references/workflow.md):

1. [Inspect format ownership](references/actions/inspect.md).
2. [Repair routing and diagnostics](references/actions/repair.md).
3. [Validate public behavior](references/actions/validate.md).

Share the current native inventory between help and routing. Preflight only delegated formats through Graphviz. Distinguish missing Graphviz from a format Graphviz explicitly does not support. Warn and continue if capability discovery cannot be interpreted.

Do not hard-code the backend's format list or silently strip leading dots. Remove redundant downstream checks only when current inspection establishes that all affected conversion paths remain protected.

## Validation and stop conditions

Before execution, bind each oracle to a current public instruction, argv command, and evidence references. Render these bound commands; historical commands do not authorize execution. Store tri-state results under `oracle:<action_id>:<source_oracle_id>`.

Check native output without Graphviz, supported delegated output, known unsupported delegated output, unavailable Graphviz, uninterpretable capabilities, CLI help, and adjacent import-path behavior. Refresh stale validation observations after edits.

Stop if owners cannot be located, semantics are incompatible, public checks fail, or required assurances remain UNKNOWN. Structural PASS predicts compatibility, not repair success. Independent hidden acceptance occurs only after the solver stops; hidden tests must not become guidance. Do not publish current task plans as newly verified historical knowledge.

## Evidence and limits

The [historical evidence cards](references/evidence/fix.md), [regression card](references/evidence/regression.md), [episode](references/episode.md), and [provenance](references/provenance.json) distinguish historical assertions from later qualification.

Historical CI execution is unknown. Independent qualification replayed only the changed test file with original-base controls: two original cases passed; adding the regressions to the base produced three fixture setup errors; the historical fixed revision passed five cases. Whole-project correctness and cross-project transfer were not tested. This replay did not execute the newly authored Skill.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`. Time-reconstructed admission must exclude a query's own issue, fix, cluster, aliases, copied sources, and inputs unavailable before its query time.
