---
name: digit-bearing-directive-tokens
description: "Diagnose and repair Python directive lexers that truncate valid digit-bearing symbolic identifiers because their token character class excludes ASCII digits."
---

# Digit-bearing directive tokens

## Activate conditionally

Activate when a public inline disable directive loses part of a digit-bearing symbolic identifier, and current inspection confirms a Python regex lexer excludes digits from its symbolic identifier token.

A value such as `j3-custom-checker` becoming `-custom-checker` is a clue, not proof. Clarify or perform a non-editing probe when the lexical owner, valid identifier grammar, or exact parse output is unknown.

Do not activate for an intact identifier rejected by registration or lookup, an explicitly digit-forbidding grammar, an already digit-inclusive lexer, or an unsupported language realization.

## Operations

1. [Diagnose lexical loss](references/actions/diagnose.md). Locate current owners, inspect token precedence and character constraints, and record a public reproduction without editing.
2. [Repair the character class](references/actions/repair.md). Only after confirmation, add ASCII digits and a complete-output regression while retaining existing grammar.
3. [Validate target and adjacent behavior](references/actions/validate.md). Execute currently bound public checks and review the diff.

The [Workflow](references/workflow.md) records the source-specific dependencies. Historical paths belong to the [episode](references/episode.md), not automatic current bindings.

## Current execution requirements

Construct a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Bind each Action/source Oracle pair to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render bound commands before execution. Empty contract commands require current binding; they do not authorize guessing or copying historical replay commands. Checks are PASS, FAIL, or UNKNOWN. Unknown prerequisites authorize probes only; hard failures reject the edit plan. Structural PASS predicts compatibility, not repair success.

Current plans may omit already-satisfied operations only with current evidence of their outputs and assurances. Refresh stale validation observations after editing. Run public checks and obtain independent hidden acceptance after the solver stops; hidden tests and gold-derived commands never enter guidance. Keep formal knowledge and checkpoints frozen. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copies, and all sources unavailable before query input time.

## Preservation and stop conditions

Require nonempty parsed output, action `disable`, and the complete original symbolic identifier. Preserve ordinary symbolic names, existing hyphen/underscore handling, assignment syntax, multi-message directives, skip-file behavior, and malformed-input expectations. Retain minimum identifier length, token ordering, keyword handling, and numeric-message rules.

Stop if current observations contradict the lexical mechanism, public grammar prohibits digits, token precedence requires a different repair, bindings remain unresolved, or required validation fails or cannot execute. A diff alone is not repair success.

## Limits and resources

This is a single historical Workflow, not a multi-source Pattern or a cross-project guarantee. Original historical test execution is unknown. Later qualification covers only the changed parser test file: one fail-to-pass and eleven pass-to-pass controls. Whole-project regression and cross-project transfer are untested.

See the [episode and qualification boundary](references/episode.md), [provenance](references/provenance.json), and unexecuted [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) definitions.
