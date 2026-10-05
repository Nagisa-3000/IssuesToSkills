---
name: keyword-only-type-coverage
description: "Repair false missing-type-documentation warnings when a Python checker accepts ordinary signature annotations but omits annotated keyword-only parameters from its type-evidence collector."
---

# Keyword-only type evidence

## Conditional activation

Activate for a Python parameter-documentation checker that warns about missing types for described, annotated keyword-only parameters after `*`, while accepting comparable ordinary signature annotations.

Before authorizing an edit, confirm in the current public checkout:

- Signature annotations count as accepted parameter type evidence.
- The warned names are keyword-only, annotated, and described in the docstring.
- The AST exposes keyword-only parameters and their annotations separately.
- Those collections are aligned.
- The collector credits ordinary annotations but omits keyword-only annotations.

Unknown facts authorize the [probe](references/actions/probe.md), not the edit. A collector that already credits keyword-only annotations rejects this repair mechanism.

## Exclusions and limits

Do not apply this Workflow to positional-only `/` handling, variadic annotations, return documentation, malformed docstrings, or a policy requiring explicit docstring types despite signature annotations. The historical report explicitly left `/` untested.

This is a single-repair Workflow, not a general argument-normalization Pattern. Cross-project transfer and whole-project correctness are untested.

## Current bindings and operations

Create a public TaskContext with the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners rather than reusing historical paths:

- `parameter-type-evidence-collector`: gathers names with accepted type evidence before the missing-type comparison.
- `parameter-documentation-test-suite`: exercises the checker and adjacent documentation diagnostics.

Follow the [canonical Workflow](references/workflow.md):

1. [Probe the omission](references/actions/probe.md).
2. [Extend coverage and add the regression](references/actions/edit.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

Current ordering follows compatible ports, prerequisite observations, and verification dependencies, not historical list position. Already satisfied or inapplicable operations may be omitted from a current task DAG; do not omit validation of modifications.

## Validation and stopping

Bind each Oracle to a current public instruction, argv command, and evidence references. Record its semantic check as `oracle:<action_id>:<source_oracle_id>` and render bound commands before executing them. Empty historical contract commands require current binding; historical commands do not authorize execution.

Use PASS/FAIL/UNKNOWN. Unknown prerequisites permit probes only; hard failures reject the modifying plan. Structural PASS predicts compatibility, not repair success.

After edits, refresh stale observations and require:

- No missing-type warning for described, annotated keyword-only parameters.
- Ordinary annotation credit remains unchanged.
- Genuinely absent accepted type evidence still produces the configured diagnostic.
- The public adjacent documentation suite passes.

Stop on ambiguous owner bindings, unproven annotation alignment, policy mismatch, a nondiscriminating regression, or adjacent failures. Do not exempt all keyword-only parameters or suppress the diagnostic.

After the solver stops, obtain independent hidden acceptance separately. Hidden checks must not supply guidance or commands. Freeze formal knowledge and checkpoints; exclude this candidate from reconstructed queries involving its own issue, fix, cluster, aliases, copied sources, or any source unavailable before query input time.

## Evidence and execution boundary

The [episode](references/episode.md) links all four historical evidence cards. [Provenance](references/provenance.json) records the exact source and qualification hash. Evaluation definitions are in [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional cases](evals/functional-cases.json).

Historical test execution and CI status are unknown. The supplied 2026 qualification independently replayed the original base, base with committed regression, and historical fixed checkout. It supports one fail-to-pass and 109 pass-to-pass cases in the changed test file only. It neither establishes whole-project regression safety nor executes these newly authored Skill cases.
