---
name: quoted-type-context
description: "Repair false unused-import diagnostics when quoted type expressions in recognized typing constructs are not visited in annotation context, while preserving ordinary runtime-string behavior."
---

# Quoted type context

Use this Workflow when a Python AST-based analyzer reports an import as unused even though it appears in a quoted type expression in a recognized typing construct, especially the first argument of `cast` or a typing-member subscription.

This is a conditional repair workflow, not a blanket rule that strings contain names. Its canonical ID is `workflow:verified-history:3f957b40be188975fdc11a7e`.

## Activation

Activate when public evidence indicates:
- A quoted type in a recognized typing call or subscription fails to count as a use.
- The analyzer already has annotation-string processing that can be entered from additional AST contexts.
- Current bindings can identify the call/subscription visitors, typing recognition helper, annotation-state owner, and public annotation tests.

Clarify when the report does not distinguish type strings from runtime values, or when the relevant symbol's binding is unknown.

Do not activate for ordinary string values, unrelated unused-import diagnostics, or analyzers without a compatible Python annotation traversal mechanism. Do not interpret arbitrary function arguments or arbitrary subscriptions as annotations.

## Current probes and operations

1. [Locate and diagnose](references/actions/locate-context.md): reproduce the diagnostic using public input; locate semantic owners and inspect symbol recognition and annotation-state handling.
2. [Repair context entry](references/actions/repair-context.md): bind recognized typing constructs to annotation traversal, with safe state restoration and narrowly scoped string handling.
3. [Validate target and neighbors](references/actions/validate-context.md): run public regressions for quoted type uses, aliases, nested subscriptions, runtime strings, and existing special typing-string behavior.

The [historical Workflow](references/workflow.md) records the sourced dependencies. The [episode](references/episode.md) explains the repair and its limits. Historical filenames are reference context, not current checkout bindings.

## Current execution requirements

Before editing, establish a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. For each Oracle, record its Action ID, source Oracle ID, public instruction, current argv command, and evidence references. Use semantic check keys of the form `oracle:<action_id>:<source_oracle_id>`.

Render and run only those current bound commands. No current checkout or commands are supplied by this package. Historical snippets are examples and test assertions, not authorization to run historical commands unchanged.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit diagnosis probes only. Hard applicability failures reject the repair plan. A structurally compatible plan does not establish repair success. After edits, refresh stale validation observations and run the public validation Action; independent hidden acceptance, if part of the surrounding evaluation, occurs only after the solver stops.

## Preservation and stopping conditions

Preserve ordinary runtime-string semantics, restoration of annotation state, and special handling of typing literals. The second argument of `cast` must not become annotation syntax merely because it is a string.

Stop or request more evidence if:
- Current bindings cannot distinguish typing constructs from unrelated names.
- The proposed change broadens annotation interpretation to ordinary runtime strings.
- Annotation context leaks beyond the intended traversal.
- Public checks fail or required preservation checks remain UNKNOWN.

The historical recognition helper resolves imported bare names through scopes, including renamed imports. Its attribute branch recognizes the literal roots `typing` and `typing_extensions`; the supplied history does not establish arbitrary module-alias or shadowed-attribute correctness. Inspect current behavior rather than claiming these cases are historically covered.

## Evidence and validation limits

One verified repair supports this Workflow; it does not support a multi-source Pattern or cross-project generalization. Historical tests are assertions present at the repair commit, not evidence of historical execution. A later qualification reports four fail-to-pass and 31 pass-to-pass cases in changed test files with original-base control. Whole-project regression and cross-project transfer remain untested. Functional eval definitions here are **not_executed**.

See [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), and [functional cases](evals/functional-cases.json).
