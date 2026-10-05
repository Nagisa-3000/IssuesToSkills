---
name: inferred-truthiness-diagnostics
description: "Correct Python boolean-refactoring diagnostics when truthiness is tested on an expression node rather than its successfully inferred value."
---

# Inferred truthiness diagnostics

Canonical Skill and Workflow ID: `workflow:verified-history:f4d7dae35352f15a7ccdd7e8`.

## Activation and exclusions

Activate for a Python static analyzer that suggests `middle if condition else fallback` for `condition and middle or fallback`, despite a middle operand that can be inferred as `False`. Inspect whether inference succeeds but the diagnostic selector subsequently requests truthiness from the original syntax node.

Clarify when the symptom is reported without a public reproduction, current code anchors, or a located diagnostic owner. Do not activate for runtime parser failures, formatting preferences, arbitrary inference defects, or a checker that already uses the inferred value and fails for a different reason.

This is a single-repair Workflow, not a Pattern or a proven cross-project abstraction.

## Current probes and bindings

Obtain a public TaskContext containing the issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings.

Locate these semantic owners in the current checkout:

- `boolean-refactoring-checker`: the Python diagnostic selector for the `and/or` expression.
- `boolean-refactoring-tests`: the public diagnostic fixtures and expectations.

[Inspect the mechanism](references/actions/inspect.md). Verify the successful-inference path, the result's truthiness interface, unavailable-inference handling, and the fixture harness. Do not treat symbol-name similarity as evidence of compatibility.

The public report distinguishes `(a and b) or c` from `b if a else c` with `a=True`, `b=False`, and `c=True`: the former yields `True`, the latter `False`.

Unknown prerequisites authorize probes only. Hard failures reject a modifying plan. Do not edit if owner bindings, inference semantics, or the mechanism remain unknown.

## Operations

The [historical Workflow](references/workflow.md) links:

1. [Inspect the inference-to-truthiness path](references/actions/inspect.md).
2. [Correct the truthiness receiver](references/actions/edit.md).
3. [Add exact diagnostic regression assertions](references/actions/regression.md).
4. [Validate both modifications and preserved behavior](references/actions/validate.md).

Bind semantic roles to current public code; historical paths are documented only in [the episode](references/episode.md). Current ordering follows compatible ports, prerequisites, and verification dependencies, not merely list position. An already-satisfied operation can be omitted only with current evidence supplying its effects and compatible PortValues. Retain explicit validation for every modification performed.

## Validation and stopping

For each oracle, bind `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Render bound commands before executing them. Record PASS, FAIL, or UNKNOWN under `oracle:<action_id>:<source_oracle_id>`. Historical commands do not authorize execution in another checkout.

Require the False-inferred name to produce `simplify-boolean-expression` with the fallback message rather than the unsafe ternary recommendation. Require the adjacent name assigned `42` to retain `consider-using-ternary`. Review unavailable-inference handling against the pre-edit policy and run the current public fixture suite.

Edits make validation observations stale, not preservation requirements optional. Refresh stale observations after all relevant changes. Stop on missing public bindings, ambiguous receiver semantics, unexpected diagnostics, or adjacent regressions. Never adjust expectations merely to accept unexpected output.

Structural plan PASS predicts compatibility, not repair success. During formal evaluation, keep knowledge and checkpoints frozen; after the solver stops, obtain independent hidden acceptance. Do not publish a current task plan as newly verified historical knowledge.

## Evidence and limits

The [four evidence cards](references/episode.md) describe the original report, merged implementation, and committed regression assertions. Historical CI/test execution is unknown.

The later independent qualification inspected original-base, base-with-regression, and historical-fixed controls. It supports one fail-to-pass and twelve pass-to-pass observations within changed-test scope. Whole-project regression and cross-project transfer were not checked. Its validation date is not historical learned content.

This Skill does not prove that arbitrary falsey expressions can be simplified without affecting condition evaluation or side effects. Do not use it to rewrite user programs.

[Provenance](references/provenance.json) preserves source identity and qualification hashes. [Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status **not_executed**.
