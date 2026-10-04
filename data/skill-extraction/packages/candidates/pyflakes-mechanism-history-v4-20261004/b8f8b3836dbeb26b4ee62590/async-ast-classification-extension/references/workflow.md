# Primary historical realization: scope classification

This source-specific reconstruction does not assert historical execution.

```arex-workflow-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:realization:scope",
  "goal": "Keep annotated asynchronous argument binding within its intended function scope.",
  "mechanism": "Extend a synchronous-only AST classification to include asynchronous function definitions under the runtime capability gate, reusing existing function semantics rather than changing downstream analysis.",
  "action_ids": [
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-inspect",
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit",
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-validate"
  ],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
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
  "dependencies": [
    {
      "before": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-inspect",
      "after": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit",
      "reason": "Establish causal omitted registration and review registry representation and capability policy.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"]
    },
    {
      "before": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit",
      "after": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-validate",
      "reason": "Observe the changed registry and committed regression shape through fresh public checks.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"]
    }
  ]
}
```
