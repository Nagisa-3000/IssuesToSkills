---
name: preserve-annotation-bindings
description: "Repair Python static-analysis binding insertion when an annotation-only declaration overwrites an existing binding and destroys export or usage tracking."
---

# Preserve annotation-only binding semantics

## Activation

Activate when current public evidence shows that a Python analyzer inserts an annotation-only binding over an existing value-bearing or specialized binding in the same scope. A characteristic reproduction assigns `__all__` in one branch and annotates it without a value in the alternative branch, causing an exported import to be reported unused.

This is one focused Workflow supported by one independently verified historical repair, not a cross-project Pattern.

## Exclusions and unknowns

Do not activate for genuine reassignment, including an annotated declaration with an assigned value. Do not apply this repair to runtime namespace behavior, unrelated export parsing, or incompatible language interfaces.

Probe or clarify when the incoming annotation classification, insertion owner, scope selection, or cause of the diagnostic is unknown. If current evidence shows that the existing binding survives and a different subsystem causes the warning, reject this workflow.

## Operations

- [Inspect current owners and the overwrite](references/actions/inspect.md).
- [Guard annotation-only insertion](references/actions/guard.md).
- [Add the public regression assertion](references/actions/regression.md).
- [Validate both edits and preserved behavior](references/actions/validate.md).

The [historical workflow](references/workflow.md) records dependencies. The [episode](references/episode.md) and [evidence cards](references/evidence/body.md) explain the supported mechanism. Historical file paths are reference material, not current owner bindings.

## Current binding discipline

Before modifying code, establish a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Each current Oracle maps its Action ID and source Oracle ID to a public current instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Empty command arrays in this package are unbound templates, not executable checks; historical paths and commands do not authorize current execution.

Use PASS/FAIL/UNKNOWN checks. Unknown prerequisites authorize probes only. Hard applicability failures reject the modifying plan. Predicate names alone do not prove semantic compatibility. Structural PASS predicts compatibility, not repair success.

Implementation and regression edits may proceed in either order after owner discovery. Both retain explicit validation. Re-observe invalidated facts after edits and record actual results rather than intended effects.

## Validation and stop conditions

Validate that:
- Existing bindings survive incoming annotation-only declarations.
- An annotation for an absent name still inserts a binding.
- Non-annotation bindings still replace existing entries.
- Annotation-with-value declarations retain assignment semantics.
- Scope selection and surrounding usage propagation remain unchanged.
- The assigned-export reproduction has no unexpected diagnostics.

Stop if the repair would suppress a real assignment, change scope selection, discard required usage metadata, or require an unsupported adapter.

## Limits and evaluation

Historical evidence supplies a merged implementation and regression assertion, not a historical execution log. Later qualification reports one fail-to-pass and 46 pass-to-pass cases in changed test files with original-base control. Whole-project regression and cross-project transfer are untested. Qualification is post-cutoff provenance, not backdated learned content. All packaged evaluation suites remain `not_executed`.

Obtain independent hidden acceptance only after the solver stops; do not use hidden tests or gold-derived commands as guidance. During formal evaluation, keep knowledge and checkpoints frozen and do not publish current task plans as historical knowledge. Time-reconstructed training catalogs exclude the current issue, fix, cluster, aliases, copies, and sources unavailable before the query input time.

See [provenance](references/provenance.json) for the authoritative record and qualification limits.
