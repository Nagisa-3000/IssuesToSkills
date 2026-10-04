---
name: async-ast-classification-extension
description: "Conditionally extend an omitted asynchronous function AST classification using existing ordinary-function semantics and runtime capability gating, with fresh public validation."
---

# Async AST classification extension

This local template is supported by two independent bug clusters and fixes in Pyflakes. It does not establish cross-project transfer.

## Activation and exclusions

Activate **for inspection** when an analyzer handles an ordinary function correctly but fails on its asynchronous counterpart, and a synchronous-only AST classification may explain the difference. Supported manifestations are annotated-argument scope lookup and intentional typing-overload recognition.

Clarify when the public reproduction, diagnostic, semantic owner, or runtime policy is unspecified. A missing-parent exception, redefinition warning, or presence of `async def` alone does not establish applicability.

Do not apply when async classification is already correct, ordinary-function semantics are inappropriate at the affected classification, async syntax is unsupported, decorator resolution is defective, or another causal defect is established.

## Current probes and bindings

Create a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Resolve owners and aliases before conflict checks. Historical paths are reference context, not current bindings.

Compare public synchronous and asynchronous probes. Inspect the relevant classification, its ordinary-function representation, the downstream analysis path, capability policy, and public coverage. Establish the causal omission before editing.

UNKNOWN prerequisites authorize probes only. Hard prerequisite failures reject the modifying plan. Matching predicate labels does not establish semantic behavior.

## Operations

Choose one coherent source-specific alternative:

- Scope: [inspect](references/actions/scope-inspect.md), [extend and cover](references/actions/scope-edit.md), [validate](references/actions/scope-validate.md).
- Overload: [inspect](references/actions/overload-inspect.md), [extend and cover](references/actions/overload-edit.md), [validate](references/actions/overload-validate.md).

Reuse existing function semantics and representation. Do not change downstream parent traversal, decorator identity recognition, or ordinary diagnostic rules to conceal the symptom.

The [primary realization](references/workflow.md) and [additional realization](references/realizations/overload.md) are source-specific causal reconstructions, not execution transcripts. Do not concatenate their independent histories into one historical Workflow. Their ports are not interchangeable; no bridge is supplied.

## Conditional Pattern

```arex-pattern-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590",
  "mechanism": "Extend a synchronous-only AST classification to include asynchronous function definitions under the runtime capability gate, reusing existing function semantics rather than changing downstream analysis.",
  "roles": [
    {
      "id": "diagnose-classification-omission",
      "effects": [{"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"}],
      "alternatives": [
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-inspect",
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-inspect"
      ],
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix"],
      "required": true
    },
    {
      "id": "extend-classification-and-cover",
      "effects": [
        {"key": "async-classification-extended", "value": true, "evaluator": "evidence"},
        {"key": "async-regression-present", "value": true, "evaluator": "evidence"}
      ],
      "alternatives": [
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit",
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit"
      ],
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "required": true
    },
    {
      "id": "validate-target-and-preservation",
      "effects": [
        {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
        {"key": "async-target-behavior-correct", "value": true, "evaluator": "evidence"}
      ],
      "alternatives": [
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-validate",
        "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-validate"
      ],
      "evidence_refs": ["PyCQA/pyflakes:401:regression", "PyCQA/pyflakes:470:regression"],
      "required": true
    }
  ],
  "required_effects": [
    {"key": "async-classification-extended", "value": true, "evaluator": "evidence"},
    {"key": "async-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "async-target-behavior-correct", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-function-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-compatibility-preserved", "value": true, "evaluator": "evidence"},
    {"key": "downstream-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "applicability": [
    {"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-semantics-appropriate", "value": true, "evaluator": "evidence"},
    {"key": "runtime-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "exclusions": [
    {"key": "async-classification-already-correct", "value": true, "evaluator": "evidence"},
    {"key": "different-root-cause-established", "value": true, "evaluator": "evidence"},
    {"key": "async-syntax-unsupported", "value": true, "evaluator": "evidence"}
  ],
  "partial_order": [
    {
      "before": "diagnose-classification-omission",
      "after": "extend-classification-and-cover",
      "reason": "Establish causal omission, ordinary-function semantic suitability, and capability policy before modification.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix"]
    },
    {
      "before": "extend-classification-and-cover",
      "after": "validate-target-and-preservation",
      "reason": "Every performed modification requires fresh public target and preservation checks.",
      "evidence_refs": ["PyCQA/pyflakes:401:regression", "PyCQA/pyflakes:470:regression"]
    }
  ],
  "supporting_workflow_ids": [
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:realization:scope",
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:realization:overload"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression",
    "PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"
  ],
  "cross_project": false
}
```

## Validation and stopping

Each current Oracle maps `action_id/source_oracle_id` to a public current instruction, argv command, and evidence references. Record the semantic check as `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty historical command arrays are unbound placeholders, not execution authorization.

Require passing target analysis, ordinary-function counterparts, adjacent diagnostic controls, affected tests, and supported-runtime compatibility checks. Record actual commands, outputs, tested scope, and PASS/FAIL/UNKNOWN results. Unavailable checks remain UNKNOWN unless another adequate public check establishes the assurance.

Stop before editing if causality or ordinary-function semantic suitability remains unknown. FAIL or unresolved UNKNOWN prevents acceptance. Do not weaken assertions, suppress warnings globally, or mask the final parent-traversal exception.

Current evidence may justify omitting already satisfied operations. Every retained modifying Action retains its validation Action. Edits invalidate observation freshness, not preservation requirements; refresh stale observations. Structural PASS predicts compatibility, never repair success.

## Evidence and limits

See [episodes](references/episode.md), [provenance](references/provenance.json), and the linked evidence cards. Historical execution remains unknown: committed assertions are not historical execution logs.

Independent later replays qualify existing artifacts only. Scope qualification has one fail-to-pass and eleven pass-to-pass cases; overload qualification has one fail-to-pass and 23 pass-to-pass cases. Both are restricted to changed test files with original-base controls. Whole-project correctness, cross-project transfer, and authored Skill execution are untested.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`.

During formal evaluation, freeze knowledge and checkpoints; never publish a current task plan as verified historical knowledge. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable strictly before query input time. Independent hidden acceptance occurs after the solver stops; hidden checks never become execution guidance.
