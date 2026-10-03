# Historical Workflow: assignment-expression scope routing

The repair distinguished assignment-expression bindings from ordinary assignments before scope insertion. Only the distinguished binding type crossed consecutive comprehension/generator scopes. Regression assertions covered both a single generator and nested comprehension scopes.

The inspection operation below is a reusable prerequisite derived from the documented defect and implementation locations; no historical inspection execution is claimed. The validation operation records the public assertions to check, not an invented historical run.

```arex-workflow-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4",
  "goal": "Make assignment-expression targets in comprehensions visible in their containing non-comprehension scope without leaking ordinary iteration bindings.",
  "mechanism": "Classify assignment-expression bindings separately and skip consecutive comprehension scopes when selecting their insertion scope.",
  "action_ids": [
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
    "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "required_effects": [
    {"key": "assignment-expression-target-scope", "value": "nearest-containing-non-comprehension-scope", "evaluator": "evidence"},
    {"key": "public-scope-regressions", "value": "passed", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-binding-scope-selection", "value": "unchanged", "evaluator": "evidence"},
    {"key": "annotation-binding-treatment", "value": "unchanged", "evaluator": "evidence"},
    {"key": "iteration-variable-locality", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
      "after": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
      "reason": "Locate classification and insertion owners and confirm the scope-routing defect before changing them.",
      "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix"]
    },
    {
      "before": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
      "after": "workflow:verified-history:fd9457af9cbbabf21f89fac4:validate",
      "reason": "Re-observe target visibility and preserved binding behavior after modifying routing and adding regression assertions.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"]
    }
  ]
}
```
