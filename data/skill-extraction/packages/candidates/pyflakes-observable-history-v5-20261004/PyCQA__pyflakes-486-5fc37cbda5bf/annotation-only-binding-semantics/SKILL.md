---
name: annotation-only-binding-semantics
description: "Repair Python analyzer handling of annotation-only declarations when binding eligibility must distinguish postponed type references from runtime value semantics."
---

# Annotation-only binding semantics

## Activation and exclusions

Activate when a Python static analyzer conflates an annotation-only declaration such as `T: object` with a value assignment, or fails to recognize its name in quoted or future-postponed type references.

Clarify whether the reference is bare, quoted, postponed by a future import, or an ordinary value read. This workflow does **not** imply that every reference to an annotation-only name is valid.

Do not activate for unrelated parser failures, ordinary missing imports, general type inference, or an unsupported non-Python binding model. Do not change bare-reference behavior merely to satisfy the original report: the historical regression assertions retain `UndefinedName` for a bare parameter annotation without postponement.

## Current probes

Locate current semantic owners for annotation-assignment traversal, binding construction, scope lookup, annotation-context management, string-annotation parsing, and unused-binding diagnostics. Historical paths belong to [the episode](references/episode.md), not to current bindings.

Observe public examples for:

- `T: object` followed by `def f(t: T): pass`, without a future import.
- The same declaration followed by `def g(t: 'T'): pass`.
- Both forms with `from __future__ import annotations`.
- Unused annotation-only declarations in module, class, and function scope.
- A local annotation followed by a value assignment.
- Ordinary value reads and lookup past an annotation-only binding.

Unknown prerequisites permit probes only. Hard semantic failures reject a modifying plan.

## Operations

1. [Inspect current binding and context behavior](references/actions/inspect.md).
2. [Repair annotation-only binding and lookup semantics](references/actions/repair.md).
3. [Validate target behavior and adjacent diagnostics](references/actions/validate.md).

The [Workflow](references/workflow.md) reconstructs supported dependencies, not historical execution of this authored plan. Current ordering follows compatible ports, observed prerequisites, semantic dependencies, and verification rather than list position. Already-satisfied operations may be omitted only with current evidence. The modifying Action retains its explicit validation Action.

## Current validation protocol

Construct a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real role bindings, observed PortValues, and current Oracle bindings. Resolve role aliases before conflict checks.

Each current Oracle maps `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound current commands before execution. Empty historical command arrays are placeholders, not executable authorization.

Use PASS/FAIL/UNKNOWN. Structural PASS predicts compatibility, never repair success. Execute public checks and refresh stale observations after edits. Obtain independent hidden acceptance, when provided by the host, only after the solver stops.

## Failure conditions and limits

Stop or narrow the plan when owners cannot be bound, the mechanism does not explain the public failure, current runtime/stub policy is incompatible, required public checks are unavailable, or preservation checks fail.

Do not silence undefined names globally or promote annotation-only declarations to ordinary value assignments. The historical future flag directly participates in the postponed-condition property; do not extrapolate that detail into an unsupported runtime-read policy.

The historical unused function-local annotation-only behavior was explicitly a TODO. This workflow does not claim to fix it.

Historical tests are assertions available at the repair commit; historical execution is unknown. Contemporary qualification reports two fail-to-pass and 39 pass-to-pass cases in changed test files only. Whole-project regression and cross-project transfer are untested. Qualification is provenance, not a backdated event. Packaged eval definitions are **not executed**.

Formal knowledge and checkpoints remain frozen during formal evaluation. Do not publish a current plan as newly verified historical knowledge. Time-reconstructed training catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query time.

## Resources

- [Episode](references/episode.md), [Workflow](references/workflow.md), [Provenance](references/provenance.json)
- Evidence: [title](references/evidence/title.md), [body](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression assertions](references/evidence/regression.md)
- Evals: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), [functional](evals/functional-cases.json)
