---
name: pragma-symbol-token-integrity
description: "Repair underscore-containing symbolic message names fragmented by a Python pragma lexer when current public evidence establishes an omitted underscore in the identifier token class."
---

# Pragma symbol token integrity

## Conditional activation

Activate when current public parser output splits a supported underscore-containing symbolic message name and inspection establishes that the symbolic-message token class excludes underscore. A numeric identifier working where a symbolic identifier fails is a diagnostic clue, not sufficient proof.

Ask for current parser output and owner inspection if only a failed disable directive is known. Do not activate for missing plugins, unknown registered messages, incorrect pragma scope, intentionally restricted naming grammars, or identifiers already parsed intact. Arbitrary punctuation, Unicode naming changes, and other-language parsers are outside the supported realization.

## Current probes and operations

1. [Probe and bind the current owners](references/actions/probe.md). Establish the omission-driven fragmentation mechanism without editing source.
2. [Repair the localized character class and author exact-output regression assertions](references/actions/repair.md), only after prerequisites pass.
3. [Validate the changed parser and adjacent grammar](references/actions/validate.md). Retain this public validation after every modifying Action.

See the [historical Workflow](references/workflow.md) and [episode](references/episode.md). Historical paths are reference bindings only; locate current objects by semantic ownership.

A current TaskContext must record the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings. Each current Oracle maps `action_id/source_oracle_id` to a public instruction, argv command, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty command arrays in the contracts require current binding; historical commands do not authorize execution in a new checkout.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only; hard failures reject the repair plan. Structural PASS predicts compatibility, not repair success. Refresh stale observations after editing.

## Validation and stop conditions

Require the complete symbolic name exactly once in the parsed messages list and preservation of action `disable`. Check ordinary and hyphenated names, numeric identifiers, multiple messages, and existing malformed-pragma behavior. If a public registered-message integration fixture is available, also verify actual symbolic disabling; otherwise report parser-only coverage.

Stop if ownership is unresolved, underscores are intentionally forbidden, the parser already preserves the symbol, the proposed edit changes unrelated grammar, or adjacent checks fail. Environment failures remain UNKNOWN. Do not broaden the regex to unrelated characters merely to obtain passing tests.

## Assurances and limits

Preserve adjacent pragma grammar across the composed plan. Validation observations can become stale; behavior-preservation requirements cannot be discarded.

This is one source-specific Workflow, not a Pattern or demonstrated cross-project abstraction. The implementation added underscore to an existing ASCII-letter/hyphen class; its committed regression asserted exact parsing of `raw_input-builtin`. Historical CI execution is unknown.

Independent qualification later established one fail-to-pass and ten pass-to-pass results in the changed parser test file, with original-base controls. It did not establish whole-project regression safety, plugin integration, transfer, or execution of this Skill. See [provenance](references/provenance.json) and the [implementation evidence](references/evidence/fix.md).

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`. After public checks and solver stop, obtain independent hidden acceptance without incorporating hidden material into guidance. Formal knowledge and checkpoints remain frozen. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and all sources unavailable before its input time.
