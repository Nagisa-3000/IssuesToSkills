---
name: inferred-keyword-io-checks
description: "Repair Python static IO diagnostics that miss mode or encoding supplied through inferable unpacked dictionaries, preserving direct lookup, legitimate warnings, and argument-specific confidence."
---

# Inferred keyword IO checks

## Activation and exclusions

Activate when a Python static analyzer treats `mode` or `encoding` as absent even though a public reproduction supplies it through an inferable `**kwargs` dictionary. The supported mechanism is ordinary argument lookup followed, on lookup failure, by safe inference of unpacked dictionary values.

Clarify if the call, dictionary definition, analyzer, or inference behavior is unknown. Do not activate for runtime decoding errors, encoding-name validation, non-Python ASTs, or unrelated signature errors.

This is a single-source Workflow, not a Pattern or evidence of cross-project transfer.

## Current probes

Construct a current public TaskContext with the issue, pinned base, hashed code anchors, real semantic-owner bindings, observed facts, semantic checks, PortValues, and current Oracle bindings.

Locate the call-argument utilities, safe-inference interface, IO diagnostic checker, and public regression owners. Check whether ordinary lookup misses unpacked keywords, whether inference yields dictionary AST nodes with supported keys, and whether mode controls encoding diagnostics.

Use [inspection](references/actions/inspect.md), [repair](references/actions/repair.md), and [validation](references/actions/validate.md). The [historical Workflow](references/workflow.md) records source-grounded dependencies; it is not an executed current plan.

UNKNOWN prerequisites authorize probes only. FAIL rejects a modifying plan. PASS requires current evidence-backed review or observation, not matching predicate names.

## Operations

1. Reproduce the public warning and bind current semantic owners.
2. Preserve ordinary positional/named lookup precedence.
3. Add safe dictionary-keyword fallback only when ordinary lookup reports a missing argument.
4. Integrate mode and encoding separately. Preserve binary-mode gating, invalid-mode reporting, and `encoding=None` warnings.
5. Initialize confidence independently for mode and encoding so inferred mode does not change confidence for an absent encoding.
6. Add reviewed public regressions and execute their checks.

Each current Oracle must map `action_id/source_oracle_id` to a public instruction, argv, and evidence references. Its check key is `oracle:<action_id>:<source_oracle_id>`. Render those bound commands before execution. Historical commands do not authorize current execution.

## Validation and stopping

Validate warning presence, locations, and confidence for inferred text encoding, binary mode, invalid mode, absent encoding, and explicit `None`. Include supported builtin, IO-module, and path IO calls plus adjacent direct-argument cases.

Refresh stale validation observations after modification. Do not suppress all encoding warnings or blindly regenerate expected output. Stop on unresolved bindings, unsupported inference shapes, unsafe key assumptions, or unexpected public results. Structural plan PASS predicts compatibility, not repair success.

After the solver stops, obtain independent hidden acceptance separately. Do not incorporate hidden tests into guidance. Freeze formal knowledge and checkpoints during evaluation; do not publish a current task plan as verified historical knowledge. Earlier-time catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and discovery inputs not available before query time.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and evidence cards for the [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [assertions](references/evidence/regression.md).

Historical CI/test execution is unknown. Contemporary qualification is validation-only and does not execute the authored [functional cases](evals/functional-cases.json).

Qualification scope: `changed-test-files-with-original-base-control`.

Limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

Dynamic mappings, nested unpacking, ambiguous inference, nonconstant keys, duplicate keyword semantics, and other signatures require separate current evidence. The historical dictionary helper does not prove support for arbitrary mappings.
