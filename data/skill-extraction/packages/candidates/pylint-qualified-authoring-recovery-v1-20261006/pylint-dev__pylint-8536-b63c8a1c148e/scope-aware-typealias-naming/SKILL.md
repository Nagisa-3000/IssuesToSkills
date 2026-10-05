---
name: scope-aware-typealias-naming
description: "Repair missing naming diagnostics for explicit function-local TypeAlias assignments when an existing naming checker incorrectly routes them through ordinary-variable naming."
---

# Scope-aware TypeAlias naming

This conditional Workflow reuses an existing explicit-alias recognizer and naming policy in the function-local assignment branch. It represents one historical repair, not a Pattern or evidence of cross-project transfer.

Canonical Skill/Workflow ID: `workflow:verified-history:b980c9ec644c821d41e50e10`.

## Activation and exclusions

Activate when public evidence shows that an explicitly `TypeAlias`-annotated function-local assignment misses the alias naming diagnostic or receives ordinary-variable treatment, while the checker already supports explicit-alias recognition and a distinct alias naming category.

Clarify when annotation syntax, naming configuration, diagnostic ownership, or current scope routing is unknown.

Do not activate for implicit aliases, Python `type` statements, runtime type errors, a missing alias naming policy, or a checker without a compatible explicit-alias recognizer. This history does not support inventing a recognizer, bridge, or new naming policy.

## Current probes and bindings

Create a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `local-name-classifier`: eligible function-local assignment naming dispatch.
- `typealias-recognizer`: existing explicit-alias annotation predicate.
- `naming-regression-suite`: public naming fixtures and diagnostic expectations.

Run the [probe](references/actions/probe.md) before modifying an unconfirmed owner. Predicate-name matches do not prove semantic compatibility. Unknown prerequisites authorize probes only; hard failures reject the plan. If current behavior is already correct, do not invent a defect.

## Operations

Use the [Workflow contract](references/workflow.md):

1. [Probe classification and scope guards](references/actions/probe.md).
2. [Route explicit local aliases to alias naming](references/actions/route.md).
3. [Add regression controls](references/actions/regression.md).
4. [Validate the final implementation and fixtures](references/actions/validate.md).

Current ordering follows ports, actual prerequisites, semantic dependencies, and verification closure—not historical list position. Already satisfied operations may be omitted only when current evidence establishes their effects and preserves required validation.

## Validation

Bind each Oracle to a public current instruction, argv command, and evidence references. Record its check as `oracle:<action_id>:<source_oracle_id>` and render bound commands before execution. Historical commands are evidence, not executable authorization.

Require the bad explicit local alias to receive alias-category `invalid-name`; good simple and union-valued aliases must not receive it. An ordinary union annotation must remain an ordinary variable declaration. Preserve existing top-level alias expectations, ordinary-variable fallback, local-membership checks, argument exclusion, and import-redefinition guards.

Refresh validation observations after edits. PASS/FAIL/UNKNOWN are distinct: unknown or required skipped checks do not establish success. Structural PASS predicts compatibility, not repair success. Execute public checks and obtain independent hidden acceptance after the solver stops. Keep formal knowledge and checkpoints frozen; hidden outcomes must not revise this package.

## Stops and limits

Stop if owner compatibility fails, the recognizer or alias naming category is absent, preserved guards cannot be maintained, or public controls fail. Do not extend this mechanism to unrelated syntax or scopes without separate evidence.

Historical tests are committed assertions; historical CI/test execution is unknown. Later qualification has scope **changed-test-files-with-original-base-control**, with the exact limit: **Changed test files only; whole-project regression and cross-project transfer are untested.** The newly authored functional cases remain `not_executed`.

Time-reconstructed admission excludes the current task's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

Resources: [episode](references/episode.md), [Workflow](references/workflow.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression](references/evidence/regression.md), [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), and [functional cases](evals/functional-cases.json).
