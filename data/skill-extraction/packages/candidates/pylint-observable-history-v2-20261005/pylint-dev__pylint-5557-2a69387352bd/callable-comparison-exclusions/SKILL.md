---
name: callable-comparison-exclusions
description: "Conditionally repair Python callable-comparison false positives caused by inferred raising functions or typing special forms, while preserving ordinary bare-callable diagnostics."
---

# Callable comparison exclusions

## Activation and exclusions

Activate for inspection when a Python static analyzer reports a bare-callable comparison warning for an intentionally compared value, particularly a typing constant or a function with a direct body-level `Raise`.

`Any` and `Optional` are symptom examples, not sufficient applicability evidence. Before editing, establish that current safe inference exposes the supported function-like representation and that the diagnostic counts eligible bare callables.

Clarify if the public reproduction, inferred operand, or current diagnostic owner is unavailable. Do not activate for legitimate omitted calls to ordinary functions, runtime equality failures, unrelated typing diagnostics, or non-Python implementations.

## Current workflow

1. [Inspect](references/actions/inspect.md): locate current semantic owners, reproduce the warning, and inspect safe inference, immediate body nodes, qualified decorator names, and the warning gate.
2. [Repair](references/actions/repair.md): conditionally exclude direct-body raising functions and `typing._SpecialForm`-decorated function-like operands from the eligible callable count; add public regressions.
3. [Validate](references/actions/validate.md): execute bound public reproductions and regression controls after every modification.

The [historical workflow](references/workflow.md) is a source-supported realization, not authorization to execute historical commands in a current checkout. Historical paths appear in the [episode](references/episode.md) and evidence cards; bind reusable operations to current semantic owners.

## Applicability and current bindings

Build a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve aliases before checking read/write conflicts. Ports must agree on semantic role, artifact kind, language, scope, phase, and state; matching words alone do not establish compatibility.

For each Oracle, bind `action_id` and `source_oracle_id` to a public current instruction, argv command, and evidence references. The semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty contract command arrays require current binding; they are not executable commands.

Use PASS/FAIL/UNKNOWN. UNKNOWN prerequisites permit probes only; hard failures reject editing. Structural PASS predicts compatibility, not repair success. Read probes must not invoke compared callables or edit tracked source.

## Mechanism and preservation

The supported implementation:

- safely infers each comparison operand;
- checks the existing bare-callable node category before accessing function-specific attributes;
- excludes nodes decorated with the qualified name `typing._SpecialForm`;
- excludes nodes with a `Raise` among immediate body elements;
- emits the diagnostic only when exactly one eligible bare callable remains.

Preserve ordinary nonraising bare-callable warnings, existing noncallable comparison behavior, and unrelated diagnostics. Do not globally disable the diagnostic or relax test expectations.

The shallow body scan is not an always-raises proof. It includes a direct raise after another statement, but does not authorize recursive, conditional, nested, or transitive raise analysis. Arbitrary decorators, callable instances, all typing objects, and cross-language adaptations are outside this realization.

## Validation and stopping

Public validation must observe absence of the target warning for `Any`, `Optional`, and a direct-body raising function, while retaining positive controls for ordinary functions and baseline behavior for two ordinary callables and noncallable pairs. Inspect diagnostic identities and locations, not just exit codes.

Stop before editing if inference is ambiguous, APIs are incompatible, the mechanism is unsupported, or current public Oracles are unbound. Stop after editing if controls fail, inference crashes, or required checks remain UNKNOWN. Edits stale the validation observation, not the preserved-behavior requirements; rerun validation after further changes.

This is a single-source Workflow, not a Pattern or transfer claim. Historical regression assertions are known; historical CI/test execution is unknown. Later source qualification covered changed test files with original-base controls and selected neighboring tests, not whole-project correctness or cross-project transfer. Newly authored functional definitions remain unexecuted.

During formal evaluation, keep knowledge and checkpoints frozen. Do not publish a current task plan as verified historical knowledge. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query time. Independent hidden acceptance, if required, occurs after the solver stops and is not guidance.

## Resources

- [Episode and qualification audit](references/episode.md)
- [Workflow](references/workflow.md)
- [Provenance](references/provenance.json)
- Evidence: [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regressions](references/evidence/regression.md)
- Evaluations: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), [functional](evals/functional-cases.json)
