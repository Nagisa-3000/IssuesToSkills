---
name: async-overload-classification
description: "Repair false unused-redefinition diagnostics for async typing overloads when overload recognition accepts synchronous function AST nodes but omits async function nodes."
---

# Async overload classification

## Activation and exclusions

Activate when a Python static analyzer accepts successive synchronous `typing.overload` declarations followed by an implementation, but reports unused-redefinition diagnostics for the equivalent async sequence.

This workflow applies only after current inspection confirms that overload recognition has a synchronous-only function-node guard. It does not authorize a blanket exemption for repeated async functions.

Clarify or probe when the diagnostic, decorator identity, synchronous baseline, runtime policy, or classification owner is unknown. Do not activate for coroutine runtime errors, invalid overload signatures, ordinary undecorated redefinitions, or failures caused by decorator/import resolution.

## Current probes and bindings

Use [inspection](references/actions/inspect.md) to locate these current semantic owners:

- `overload-classification`: recognition of typing overload declarations.
- `function-node-family`: compatibility-aware function AST type definitions.
- `overload-regression-tests`: public tests of overload/redefinition behavior.

Historical paths in the [episode](references/episode.md) are context, not current bindings. Record a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before read/write conflict checks.

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only. A hard mechanism failure rejects the repair plan. Matching predicate labels alone does not prove semantic claims.

## Operations

1. [Inspect the diagnostic and node boundary](references/actions/inspect.md).
2. [Extend the function-node family and add regression coverage](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [canonical historical Workflow](references/workflow.md) records the supported mechanism. Current ordering follows port compatibility, prerequisites, and verification dependencies, not merely list position. Already satisfied operations may be omitted only with fresh current evidence; every modification retains its explicit validation Action.

Action effects describe targets, not observed execution results.

## Validation and acceptance

Require current public checks establishing:

- Async overload declarations followed by an async implementation produce no unused-redefinition diagnostics.
- Equivalent synchronous overloads remain accepted.
- Ordinary unused redefinitions remain diagnosed.
- Typing decorator resolution remains unchanged.
- AST availability and async test syntax follow the supported-runtime policy.

Bind each Oracle by `action_id` and `source_oracle_id` to a public current instruction, argv command, and evidence references. Render those bound commands and record checks under `oracle:<action_id>:<source_oracle_id>`. Empty historical command arrays are not executable bindings.

Refresh observations invalidated by editing. Structural plan PASS predicts compatibility, not repair success. After the solver stops, obtain independent hidden acceptance through the evaluation host; hidden tests and gold-derived commands must not enter guidance.

## Stop conditions and limits

Stop if the current classifier already recognizes async function nodes, if decorator resolution is the actual cause, or if the proposed change suppresses ordinary redefinition diagnostics. Failed or UNKNOWN required validation prevents acceptance.

Support consists of one verified repair in one repository, not a cross-project Pattern. Historical regression code establishes assertions available at the repair commit; no historical execution transcript was supplied. The later qualification covers changed test files only, with one fail-to-pass and 23 pass-to-pass cases. Whole-project regression and cross-project transfer are untested.

See the [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression assertions](references/evidence/regression.md), [provenance](references/provenance.json), and unexecuted [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites.

Current task plans are not newly verified historical knowledge and must not be published as such during formal evaluation. Freeze formal knowledge and checkpoints. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.
