---
name: normalize-iterator-node-identifiers
description: "Repair a Python iteration-mutation checker that reads .name from an Attribute iterable exposing .attrname, while retaining inference guards and existing mutation diagnostics."
---

# Normalize iterator node identifiers

## Activation

Activate when current public evidence establishes a Python static-analysis iteration checker whose iterable-side identifier comparison assumes `.name`, although an Attribute iterable exposing `.attrname` reaches that comparison. The supported reproduction iterates an enum-backed class-attribute set while removing elements from a separately constructed set copy.

Activation is semantic, not repository-specific. Clarify or probe if the failing expression, node type, or semantic owner is unknown.

Do not activate for runtime collection-mutation exceptions, unrelated inference failures, incompatible AST interfaces, or receiver-side identifier failures. This history does not support arbitrary AST normalization, generalized alias analysis, or exception suppression.

## Current probes and prerequisites

Create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues where applicable, and current Oracle bindings.

Locate:

- `iteration-condition-owner`: the shared list/set mutation condition.
- `ast-node-api-owner`: the current Name and Attribute interfaces.
- `iteration-regression-owner`: iteration fixtures and diagnostic expectations.
- `iteration-test-runner-owner`: their public test runner.

Confirm reachable iterable shapes, Name `.name`, Attribute `.attrname`, receiver-side `.name` safety, the existing inferred-object equality guard, and fixture conventions. Existence predicates use role-qualified keys and boolean values; resolve them against current resources. Historical paths are evidence, not current bindings.

## Operations

1. [Inspect applicability](references/actions/inspect.md).
2. [Normalize iterable identifier selection](references/actions/repair.md).
3. [Add the separate-copy regression](references/actions/regression.md).
4. [Validate target and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) reconstructs the source-backed realization. Current ordering follows prerequisites and semantic dependencies. The two edits may occur in either order; validation follows every retained edit. Already satisfied operations may be omitted only with current evidence, without dropping validation for retained modifications.

## Public validation

Bind and render current public commands before execution. Each current Oracle maps `action_id` and `source_oracle_id` to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Empty source commands require current binding; historical commands do not authorize execution.

Require:

- No Attribute `.name` exception or wrapped checker crash.
- No `modified-iterating-set` warning for removal from the separate copy.
- Name iterables still use `.name`.
- The inferred-object equality guard remains unchanged.
- Existing list, set, and dictionary expectations remain, except justified fixture location changes.

PASS/FAIL/UNKNOWN are observations, not inferred from predicate names. UNKNOWN prerequisites authorize probes only; hard FAIL rejects the plan. Structural PASS predicts compatibility, never repair success. Refresh stale validation after editing, execute public checks, and obtain independent hidden acceptance only after the solver stops. Keep formal knowledge frozen; do not publish a current plan as historical knowledge.

## Stop conditions and limits

Stop if additional unsupported iterable kinds reach the two-way branch, receiver-side access is unsafe, the inference guard requires weakening, or validation produces unexplained diagnostic differences. Do not invent an adapter or broader repair.

This single-history Workflow is not a Pattern or proof of cross-project transfer. Historical test and CI execution are unknown. Later qualification has scope `changed-test-files-with-original-base-control`, with exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.` Authored evals are not executed.

Time-reconstructed admission must exclude the current query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Supporting resources

- [Episode](references/episode.md)
- [Title evidence](references/evidence/title.md)
- [Report evidence](references/evidence/body.md)
- [Implementation evidence](references/evidence/fix.md)
- [Regression evidence](references/evidence/regression.md)
- [Provenance](references/provenance.json)
- [Activation cases](evals/activation-cases.json)
- [Applicability cases](evals/applicability-cases.json)
- [Functional cases](evals/functional-cases.json)
