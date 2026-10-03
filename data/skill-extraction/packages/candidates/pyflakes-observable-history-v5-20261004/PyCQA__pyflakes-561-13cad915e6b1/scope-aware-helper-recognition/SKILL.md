---
name: scope-aware-helper-recognition
description: "Repair Python static-analyzer recognition of module-qualified typing helpers when import aliases or lexical shadowing make receiver-spelling checks unreliable."
---

# Scope-aware helper recognition

## Activation and boundaries

Activate when a Python static analyzer recognizes a typing helper under a canonical module name but misses the equivalent helper under an imported module alias. Examples include missed overload recognition and related annotation diagnostics.

This workflow is conditional on the current recognition owner using a name-based attribute receiver and having lexical import bindings with module-origin metadata. It is supported by one historical repair, not a cross-project Pattern.

Clarify and probe first if only a directly imported `Literal` alias fails, the receiver is a chained attribute, or current binding metadata is unknown. The original report includes a directly imported `Literal` alias, but the supplied implementation changes module-qualified attribute recognition and the supplied regression asserts aliased `typing.overload`.

Do not activate for runtime import failures, ordinary undefined names, attributes on arbitrary objects, or a failure elsewhere in an analyzer that already performs nearest-binding import-origin resolution.

## Operations

1. [Probe recognition and locate current owners](references/actions/probe-recognition.md).
2. [Replace receiver spelling with nearest import-origin resolution](references/actions/resolve-import-origin.md).
3. [Add the supplied aliased-overload regression](references/actions/add-alias-regression.md).
4. [Validate edits and preservation boundaries](references/actions/validate-recognition.md).

Use the [Workflow](references/workflow.md) as a sourced dependency model, not a transcript of historical execution. Bind semantic owners to the current public checkout. Historical paths in the [episode](references/episode.md) are not current bindings.

## Current probes and prerequisites

Establish the current expression shape, recognition owner, supported typing-module identities, scope traversal semantics, and import-origin metadata. Compare public canonical and aliased overload reproductions. Confirm that a spelling-based recognition gap actually exists.

Unknown prerequisites authorize probes only. A hard applicability failure rejects the repair plan. Stop if implementing the mechanism requires an unsupported alias-analysis system, chained-attribute resolution, or an invented bridge.

## Validation and preservation

Both modifying Actions retain the explicit validation Action. Public checks must observe aliased overload recognition and preserve:
- Canonical supported-module recognition.
- Nearest lexical binding, including shadowing by a non-import or unrelated import.
- The existing direct-name recognition branch.
- The attribute-shape guard and helper-name predicate.
- Existing annotation regression assertions.

Run the original reported `Literal` reproduction separately when relevant; an overload test alone does not establish every Literal alias case.

Bind each current Oracle by `action_id/source_oracle_id` to a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>` and render the bound commands before execution. Empty command arrays in these cards are placeholders, not executable guidance.

A current TaskContext supplies the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Use PASS/FAIL/UNKNOWN, refresh facts invalidated by edits, and distinguish expected effects from observed results. Structural plan PASS predicts compatibility, not repair success.

## Evidence and limits

The [implementation](references/evidence/implementation.md) adds nearest-scope import-origin recognition. The [regression](references/evidence/regression.md) supplies an aliased overload assertion at the historical commit; original historical execution is unknown. The [title](references/evidence/title.md) and [report](references/evidence/report.md) describe the original symptom.

A later qualification reports one fail-to-pass and 50 pass-to-pass outcomes in changed test files only. Whole-project regression and cross-project transfer are untested. This is a contemporary provenance attestation, not an event backdated before the cutoff. See [provenance](references/provenance.json).

Functional definitions remain unexecuted. During formal evaluation, keep knowledge and checkpoints frozen; do not publish a current plan as newly verified historical knowledge. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time. Obtain independent hidden acceptance after the solver stops; hidden tests never supply guidance or commands.

## Evaluation resources

- [Activation cases](evals/activation-cases.json)
- [Applicability cases](evals/applicability-cases.json)
- [Functional cases](evals/functional-cases.json)
