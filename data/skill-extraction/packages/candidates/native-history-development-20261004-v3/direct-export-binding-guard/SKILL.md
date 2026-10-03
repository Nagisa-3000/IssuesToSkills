---
name: direct-export-binding-guard
description: "Guard assignment-only export binding in a Python static analyzer when indirect module-level __all__ targets supply incompatible immediate AST parents."
---

# Direct export binding guard

## Activate conditionally

Use this focused Workflow when current public evidence establishes all of these facts:

- A Python static analyzer fails while analyzing an indirect module-level `__all__` target.
- Special export handling is selected using the name and module scope.
- The handler receives the name node's immediate AST parent and expects an assignment statement with a value.
- A destructuring target instead supplies a tuple or other incompatible parent.
- Ordinary binding is an available fallback.

The historical reproduction was `__all__, = ("fizz", "buzz")`. Static analysis must not crash simply because executing that source would fail unpacking.

An `__all__` mention, unused-import warning, or `AttributeError` alone is insufficient. Probe the current mechanism before editing.

## Exclusions

Do not apply when the guard already exists, the failure is runtime unpacking or parsing, the analyzer intentionally supports indirect exports through another representation, or current interfaces are not Python AST-compatible. A different parent model is not permission to invent an adapter.

This package has one independently resolved historical cluster. It is a Workflow, not a Pattern or cross-project template.

## Current probes and operations

Locate and bind the current semantic owners: name-store binding dispatcher, export-binding handler, and export-binding regression tests. Historical paths are reference locators only.

1. [Inspect the boundary](references/actions/inspect.md): establish current parent shapes, dispatch selection, consumer assumptions, and fallback.
2. [Guard and add a regression](references/actions/guard-and-regress.md): restrict special handling to compatible immediate assignment parents while retaining ordinary binding.
3. [Validate](references/actions/validate.md): execute public reproductions and tests, and verify adjacent behavior.

The [Workflow](references/workflow.md) defines dependencies. Already satisfied inspection can be omitted from a current task only with fresh evidence. Validation of an edit cannot be omitted.

## Current execution discipline

Record a TaskContext with public issue, pinned base, hashed code anchors, observed facts, semantic checks, resolved owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before read/write conflict checks.

For each Oracle, bind its Action ID and source Oracle ID to current public instructions, argv command, and evidence references. Record its tri-state result under `oracle:<action_id>:<source_oracle_id>`, and render the bound command before execution. Empty historical command arrays are not executable bindings.

UNKNOWN prerequisites authorize probes only. Hard failures reject the plan. Matching predicate names do not prove semantic claims. Structural PASS predicts compatibility, not repair success. Refresh observations invalidated by edits.

## Required validation and preservation

Require current evidence that:

- indirect targets no longer enter assignment-only export handling;
- the reported shape produces no internal `Tuple.value` exception;
- `import bar; (__all__,) = ("foo",)` produces an unused-import diagnostic for `bar`;
- direct module-level exports retain supported behavior;
- special handling remains module-scoped;
- earlier binding branches and ordinary fallback remain intact.

The historical guard accepted immediate parents `ast.Assign`, `ast.AugAssign`, and `ast.AnnAssign`. Confirm current representations before using that exact set. Do not invent a new invalid-assignment diagnostic.

## Stop conditions and limits

Stop when owners cannot be located, the parent model differs, preservation checks fail, or required public results remain UNKNOWN. Record failures rather than marking expected effects as observed.

No package-authoring execution occurred. [Functional evaluations](evals/functional-cases.json) are definitions with `status: not_executed`. Historical tests are assertions available at the merged commit, not a supplied historical execution transcript.

The contemporary qualification reports one fail-to-pass and 131 pass-to-pass cases, restricted to changed test files with original-base control. Whole-project regression and cross-project transfer are untested. This attestation is not backdated historical knowledge.

After the solver stops, independent hidden acceptance remains separate from public validation. Do not use hidden or gold-derived commands in guidance. Formal knowledge and checkpoints stay frozen; time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copies, and sources unavailable before query time. A current task plan is not newly verified historical knowledge and must not be published as such during formal evaluation.

See [episode](references/episode.md), [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), and [applicability cases](evals/applicability-cases.json).
