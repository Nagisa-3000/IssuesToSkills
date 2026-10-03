---
name: async-overload-function-recognition
description: "Repair false unused-redefinition diagnostics for async typing overloads when an existing overload exemption omits supported asynchronous function AST nodes."
---

# Async overload function recognition

Canonical Skill and Workflow ID: `workflow:verified-history:a571de127bfc56dc56819c7c`.

This conditional Workflow has one independently verified historical repair as support. It is not a Pattern or a cross-project generalization.

## Activation

Activate when a Python analyzer accepts intentional synchronous `typing.overload` redefinitions but warns about the equivalent async overload sequence, and the overload source-node gate may recognize only synchronous function definitions.

Clarify an unspecified diagnostic or missing public reproduction before selecting this repair. Do not activate merely because code contains `async def` or `@overload`.

Exclude ordinary undecorated redefinitions, decorator-resolution defects, unsupported async syntax, and unrelated binding errors. An already async-aware recognition gate contradicts this repair mechanism.

## Current probes and bindings

Create a current TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, actual owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `overload-recognition`: the predicate recognizing a binding as a typing overload.
- `function-node-family`: the owner of function AST types and runtime compatibility policy.
- `overload-regression-tests`: public overload diagnostic tests.

Historical paths appear only in [the episode](references/episode.md) and [evidence](references/evidence/fix.md). They are not current bindings. Resolve owner aliases before conflict checks.

[Inspect recognition](references/actions/inspect.md) to establish correct decorator resolution, sync acceptance, async failure, the omitted async AST type, compatibility policy, and existing coverage. UNKNOWN prerequisites authorize probes only; hard failures reject the modifying plan. Matching predicate names alone does not prove semantic behavior.

## Operations

Follow the [canonical Workflow](references/workflow.md):

1. [Inspect the recognition gate](references/actions/inspect.md).
2. [Extend the supported function-node family](references/actions/extend-function-family.md), only for a confirmed omission.
3. [Add public async regression coverage](references/actions/add-regression.md), if equivalent coverage is absent.
4. [Validate the target and adjacent behavior](references/actions/validate.md), retaining validation for every performed edit.

The historical Workflow is a causal reconstruction, not an execution transcript. Current plans may omit already-satisfied operations with current evidence; their ordering follows ports, prerequisites, dependencies, and verification obligations. Contract effects are expected effects until actually observed.

## Validation and stopping

Each Oracle must receive a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>`. Render and run the bound commands. Empty historical contract commands require current binding and do not authorize execution.

Require current confirmation that:

- Two async typing overload declarations followed by an async implementation produce no unused-redefinition warnings.
- Synchronous overload acceptance remains intact.
- Ordinary non-overload redefinitions retain their diagnostics.
- Supported-runtime AST compatibility remains intact.
- The affected public suite passes.

Record actual commands, outputs, scope, and PASS/FAIL/UNKNOWN results. Edits invalidate validation freshness, not preserved behavior requirements. Refresh stale observations after edits. Structural PASS predicts compatibility, never repair success.

Stop if the omission is absent, decorator identity is faulty, runtime compatibility cannot be established, or adjacent behavior regresses. FAIL or unresolved UNKNOWN prevents acceptance.

## Evidence and limits

See [episode](references/episode.md), [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression assertion](references/evidence/regression.md), and [provenance](references/provenance.json).

Historical tests are assertions available at the repair commit; historical execution logs are not supplied. A later qualification attestation reports one fail-to-pass and 23 pass-to-pass cases in changed test files with original-base control. Whole-project regression and cross-project transfer are untested. The attestation is provenance, not pre-cutoff learned content.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are unexecuted definitions.

During formal evaluation, freeze knowledge and checkpoints. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and any source not available strictly before query input time. Do not publish a current task plan as newly verified history. Independent hidden acceptance occurs after the solver stops; hidden tests and gold-derived commands never enter public guidance.
