---
name: guard-comparison-operand-access
description: "Repair a Python AST refactoring check that assumes every non-name comparison operand is a constant: locate the unsafe access, restrict extraction to supported node kinds, skip unsupported shapes, and validate crash regressions while preserving existing suggestions."
---

# Guard comparison operand access

## Activation

Activate when a Python AST-based refactoring check crashes while extracting a comparison operand, and current inspection shows a name branch followed by an unconditional constant-style attribute access. The evidenced repair applies to a min/max suggestion checker whose supported operand kinds are names and constants.

Clarify or probe first when the traceback, AST library, operand shape, supported kinds, or semantic owner is unknown. A negative literal may be represented by a unary-operation node rather than a constant; inspect the current AST instead of assuming representation.

Do not activate for runtime arithmetic errors, parser failures, unrelated visitors, or a checker that intentionally supports arbitrary expression inference. This is a single-source Workflow, not an independently established cross-project Pattern.

## Current probes and bindings

Before editing, record a TaskContext with the public issue, pinned base, hashed code anchors, current observations, semantic checks, actual owner bindings, observed PortValues, and bound current Oracles.

Locate these semantic owners rather than copying historical paths:

- `comparison-operand-extractor`: the refactoring checker logic extracting the right operand for a min/max comparison.
- `min-max-functional-regressions`: the public functional fixture and expected-output harness for that checker.

Use [inspect](references/actions/inspect.md) to establish that the current access is unsafe and that skipping unsupported shapes is compatible with the checker's purpose. Unknown prerequisites authorize probes only. A hard semantic mismatch rejects this Workflow.

## Operations

The [historical Workflow](references/workflow.md) links the complete contracts:

1. [Inspect operand extraction](references/actions/inspect.md).
2. [Guard extraction by node kind](references/actions/guard.md).
3. [Add unsupported-shape regressions](references/actions/regressions.md).
4. [Validate the guard and regressions](references/actions/validate.md).

Current dependencies follow semantic prerequisites and verification closure, not historical list order. Regression addition and guard editing can be ordered independently after inspection; validation must follow both modifications. Retain preservation obligations even if an already satisfied operation is omitted.

The repair is deliberately conservative: extract a name only from a name node, extract a value only from a constant node, and return from the local suggestion check for other operand kinds. Do not catch all exceptions, fold negative literals, infer arbitrary expressions, or broaden accepted operand kinds on this evidence alone.

## Validation and stopping

Bind each Action Oracle to a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>`. Render the actual bound commands before execution; historical commands are not execution authority.

Check the negative-literal and membership/list cases for absence of the crash and absence of an inappropriate min/max suggestion. Also run existing name/constant positive and negative examples and relevant neighboring public refactoring tests. A lint invocation may return a diagnostic-related nonzero code without crashing; inspect its output rather than equating every nonzero code with failure.

After an edit, refresh stale validation observations. PASS/FAIL/UNKNOWN checks distinguish established facts from assumptions. Structural PASS predicts compatibility, not repair success. Stop if the owner cannot be bound, the AST kinds differ materially, the public harness cannot establish expected diagnostics, or preserving supported behavior requires a different mechanism.

Do not declare success until public checks have actually run. After the solver stops, obtain independent hidden acceptance where applicable; hidden commands and results do not enter these instructions. Formal knowledge and checkpoints remain frozen.

## Evidence and limits

See [episode](references/episode.md), [source evidence](references/evidence/body.md), and [provenance](references/provenance.json). The supplied independent qualification establishes changed-test-file causal resolution with an original-base control, not whole-project correctness or transfer. Historical test assertions are known; historical CI/test execution is unknown.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions only and remain **not executed**.

Time-reconstructed training use must exclude the current task's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.
