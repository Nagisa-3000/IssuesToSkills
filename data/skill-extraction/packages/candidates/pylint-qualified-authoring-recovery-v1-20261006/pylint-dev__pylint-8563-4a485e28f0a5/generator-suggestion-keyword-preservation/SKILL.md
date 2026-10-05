---
name: generator-suggestion-keyword-preservation
description: "Preserve keyword arguments and valid Python syntax in generator-comprehension suggestions without changing diagnostic eligibility."
---

# Generator suggestion keyword preservation

Use this conditional Workflow when a Python diagnostic recommends replacing a list comprehension with a generator expression but drops existing keyword arguments from the suggested call.

Canonical Skill/Workflow ID: `workflow:verified-history:4f600acd843f37945bbd0765`.

## Activation

Activate when public observations identify a keyword-losing generator suggestion. Before editing, confirm that the current implementation constructs the replacement from exactly one positional list-comprehension argument and that the keyword-rendering interface matches this mechanism.

Clarify when the original call, emitted suggestion, or current code is unavailable. Inspection is permitted while applicability remains UNKNOWN; modification is not.

Do not activate for:

- Runtime errors without a suggestion-rendering defect.
- Calls with multiple positional arguments.
- General source-to-source rewriting.
- Blanket suppression of diagnostics on keyword-bearing calls.
- Another language or an incompatible AST/rendering interface.

The historical repair retained the diagnostic on `min([...], default=42)`. It corrected the suggested call rather than implementing the reporter's requested suppression.

## Current probes and bindings

Use [inspect](references/actions/inspect.md) to locate these semantic owners in the current public checkout:

- `generator-suggestion-renderer`: replacement-call construction.
- `generator-suggestion-regressions`: fixture inputs and diagnostic expectations.
- `generator-suggestion-test-runner`: public regression harness.

Historical paths are recorded only in [the episode](references/episode.md); they are not automatic current bindings.

Create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before read/write conflict checks. Producer and consumer ports must agree on semantic role, artifact kind, language, scope, phase, and state.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites authorize probes only. Hard incompatibilities reject the plan. Structural PASS predicts compatibility, not repair success.

## Operations

1. [Inspect rendering](references/actions/inspect.md): observe keyword loss, locate owners, and record the positional gate and adjacent baseline.
2. [Repair rendering and assertions](references/actions/repair.md): conditionally parenthesize the generator body, append keyword AST renderings in order, and add paired regression cases.
3. [Validate](references/actions/validate.md): execute bound public checks for exact suggestion text, syntax, diagnostic eligibility, and keyword-free behavior.

The [historical Workflow](references/workflow.md) defines dependencies and assurances. Its Actions are authored conditional operations grounded in artifacts, not separately verified historical execution events.

## Validation and stopping

Bind every Oracle to a current public instruction, argv command, and evidence references. The semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render and execute those bound commands; empty command arrays in the Action cards require current binding and authorize no execution by themselves.

After modification, refresh stale observations. Keep validation in the plan even if repair operations are reordered or narrowed. Never regenerate expected output merely to match a defective suggestion.

Stop if owners cannot be located, the mechanism differs, public checks cannot be bound, keywords disappear, syntax is invalid, eligibility changes unexpectedly, or adjacent diagnostics regress. Do not invent adapters or claim broader transfer.

## Evidence and limits

This is a single-source Workflow, not a Pattern. Read the [evidence cards](references/episode.md#evidence) and [provenance](references/provenance.json).

Historical tests are committed assertions; historical CI execution is unknown. Later independent qualification inspected original-base, base-with-regression, and historical-fixed controls. Its scope was `changed-test-files-with-original-base-control`. Its exact limits are: “Changed test files only; whole-project regression and cross-project transfer are untested.”

That qualification did not execute the newly authored Skill evaluations. The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`.

During formal evaluation, freeze knowledge and checkpoints. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and every discovery source unavailable before the query input time. Do not publish a current task plan as newly verified historical knowledge. Independent hidden acceptance occurs after the solver stops.
