# Historical Workflow

Dependencies express semantic artifact and verification requirements, not an observed developer action chronology. The merged implementation and regression assertion support the repair; historical test execution is unknown.

```arex-workflow-v4
{
  "id": "annotation-binding-order",
  "goal": "Restore undefined-name reporting for an annotated initializer referencing its own unbound target.",
  "mechanism": "Analyze annotation and optional initializer before registering the target while retaining existing initializer dispatch.",
  "action_ids": [
    "annotation-binding-order.inspect",
    "annotation-binding-order.reorder",
    "annotation-binding-order.regression",
    "annotation-binding-order.validate"
  ],
  "source_ids": ["PyCQA/pyflakes:728"],
  "required_effects": [
    {"key": "annotated-self-reference-diagnostic", "value": "undefined-name", "evaluator": "evidence"},
    {"key": "regression-assertion", "value": "present", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-self-reference-diagnostic", "value": "undefined-name", "evaluator": "evidence"},
    {"key": "annotation-and-specialized-value-analysis", "value": "retained", "evaluator": "evidence"},
    {"key": "optional-initializer-support", "value": "retained", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "annotation-binding-order.inspect",
      "after": "annotation-binding-order.reorder",
      "reason": "Confirm the diagnostic mismatch and early-binding mechanism before editing.",
      "evidence_refs": ["PyCQA/pyflakes:728:body", "PyCQA/pyflakes:728:fix"]
    },
    {
      "before": "annotation-binding-order.reorder",
      "after": "annotation-binding-order.regression",
      "reason": "The regression operation consumes the handler-edited checkout; this is a package artifact dependency, not a historical chronology claim.",
      "evidence_refs": ["PyCQA/pyflakes:728:fix", "PyCQA/pyflakes:728:regression"]
    },
    {
      "before": "annotation-binding-order.reorder",
      "after": "annotation-binding-order.validate",
      "reason": "The handler modification requires public diagnostic and preservation validation.",
      "evidence_refs": ["PyCQA/pyflakes:728:fix", "PyCQA/pyflakes:728:regression"]
    },
    {
      "before": "annotation-binding-order.regression",
      "after": "annotation-binding-order.validate",
      "reason": "Execute the added or confirmed assertion against the repaired handler.",
      "evidence_refs": ["PyCQA/pyflakes:728:regression"]
    }
  ]
}
```
