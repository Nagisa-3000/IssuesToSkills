# Historical Workflow

Distinguish assignment-expression bindings, route their insertion past contiguous comprehension scopes, and check enclosing uses in single and nested cases.

The probe is a conditional applicability gate derived from the report and implementation. Its inclusion does not claim that an undocumented historical probe was executed. Actions declare expected effects; current observations determine whether those effects hold.

```arex-workflow-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4",
  "goal": "Correct false undefined-name diagnostics on enclosing uses of assignment-expression targets introduced inside comprehensions.",
  "mechanism": "Use a distinct assignment-expression binding category and route its insertion past contiguous comprehension scopes to the first non-comprehension scope, then validate target and adjacent behavior.",
  "action_ids": [
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "required_effects": [
    {"key": "walrus-target-enclosing-scope-visible", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-assignment-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "iteration-variable-isolation-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-binding-bookkeeping-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
      "after": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
      "reason": "Current applicability and semantic ownership must be established before applying the evidenced classification and routing change.",
      "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix"]
    },
    {
      "before": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
      "after": "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate",
      "reason": "The routing edit and added assertions require fresh checks of the single and nested cases and preserved adjacent behavior.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"]
    }
  ]
}
```
