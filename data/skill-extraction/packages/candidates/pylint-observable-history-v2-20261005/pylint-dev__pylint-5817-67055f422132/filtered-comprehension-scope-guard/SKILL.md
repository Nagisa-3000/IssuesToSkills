---
name: filtered-comprehension-scope-guard
description: "Repair a Python used-before-assignment false positive when a comprehension filter name collides with an exception-handler binding, after confirming the same assignment-filtering mechanism in the current checkout."
---

# Filtered comprehension scope guard

## Activation

Activate when a Python static analyzer reports a comprehension-local name as used before assignment inside a `try` block, and an exception handler binds the same spelling. The supported case is a name used directly as a filtered comprehension test, such as `[e for e in range(3) if e]`, followed by `except ValueError as e`.

Clarify when the report lacks a reproduction, AST relationship, or current assignment-resolution evidence. Do not activate for genuine uses of exception variables outside their handler, ordinary uninitialized locals, runtime exceptions, or unrelated comprehension inference failures.

## Current probes and bindings

Before editing, construct a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, role bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `assignment-candidate-filter`: assignment resolution that removes candidates associated with exception handlers not containing the use.
- `assignment-diagnostic-regressions`: public tests for used-before-assignment and exception-handler scope.

Use the [scope probe](references/actions/probe.md) to confirm that the offending name's parent is a comprehension node and that the name node is a direct member of its filter-test list. Also confirm that the exception-handler candidate filtering is responsible for the false diagnostic. Similar diagnostic text alone is insufficient.

## Operations

1. [Probe the collision and filtering owner](references/actions/probe.md).
2. [Narrow the handler-filter condition and add the regression](references/actions/repair.md).
3. [Validate the target and adjacent scope behavior](references/actions/validate.md).

The [historical workflow](references/workflow.md) records dependencies, not permission to reuse old paths or commands. Current ordering follows resolved ports and semantic prerequisites. Already satisfied probes may be omitted only with fresh public evidence.

The supported repair skips this particular candidate-filtering step when the use is a direct comprehension filter test. It does not disable used-before-assignment globally or treat exception variables as universally available.

## Validation and stopping

Bind each Oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution; historical commands are evidence, not current execution authority.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN prerequisites permit probes only; a hard failure rejects the repair plan. After modification, refresh stale diagnostic observations and execute public validation. Structural compatibility does not establish repair success.

Stop if the AST relation differs, filtering has already been corrected, the public reproduction cannot be established, or the narrow guard loses genuine exception-scope diagnostics. Do not broaden the exclusion merely to make tests pass. Obtain independent hidden acceptance after the solver stops; do not incorporate hidden tests into guidance or alter frozen formal knowledge/checkpoints.

## Evidence and limits

The [episode](references/episode.md) and [evidence cards](references/evidence/body.md) support one historical repair, not a cross-project pattern. Historical test assertions are known; historical CI execution is unknown. Later qualification checked the supplied original-base, regression-on-base, and fixed controls, with one fail-to-pass case and the selected original cases preserved. It did not check whole-project regressions or cross-project transfer and did not execute these newly authored Skill evals.

See [provenance](references/provenance.json), [activation cases](evals/activation-cases.json), [applicability cases](evals/applicability-cases.json), and [functional definitions](evals/functional-cases.json). All definitions remain unexecuted.

For time-reconstructed use, exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before query time. This Skill must not be represented as newly verified historical knowledge during formal evaluation.
