# Additional historical realization: overload recognition

Only the overload source supports these Actions. Combining implementation and coverage does not claim a historical execution order.

```arex-workflow-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:realization:overload",
  "goal": "Accept intentional asynchronous typing overload redefinitions without weakening adjacent diagnostics.",
  "mechanism": "Extend a synchronous-only AST classification to include asynchronous function definitions under the runtime capability gate, reusing existing function semantics rather than changing downstream analysis.",
  "action_ids": [
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-inspect",
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit",
    "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-validate"
  ],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
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
      "before": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-inspect",
      "after": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit",
      "reason": "Establish correct decorator identity, sync acceptance, async failure, and causal omission from the node gate.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix"]
    },
    {
      "before": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit",
      "after": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-validate",
      "reason": "Fresh checks must observe the extended gate and async regression.",
      "evidence_refs": ["PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"]
    }
  ]
}
```
