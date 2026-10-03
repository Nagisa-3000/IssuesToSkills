# Recognize match-case alternatives

This is a reconstruction from the reported reproduction, merged implementation,
and regression assertion. Effects describe required outcomes, not results
already observed in a current checkout.

```arex-workflow-v4
{
  "id": "mutually-exclusive-match-bindings",
  "goal": "Remove unused-name redefinition false positives between distinct Python match cases.",
  "mechanism": "Expose each match case body through shared alternative classification with AST availability protection, then encode and validate a regression.",
  "action_ids": [
    "mutually-exclusive-match-bindings:probe",
    "mutually-exclusive-match-bindings:recognize",
    "mutually-exclusive-match-bindings:regression",
    "mutually-exclusive-match-bindings:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:771"],
  "required_effects": [
    {"key": "match-cases-recognized-as-alternatives", "value": true, "evaluator": "evidence"},
    {"key": "distinct-case-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "existing-if-try-alternatives-preserved", "value": true, "evaluator": "evidence"},
    {"key": "sequential-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "python-ast-availability-respected", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "mutually-exclusive-match-bindings:probe",
      "after": "mutually-exclusive-match-bindings:recognize",
      "reason": "Confirm diagnostic ownership and the classifier omission before editing.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"]
    },
    {
      "before": "mutually-exclusive-match-bindings:probe",
      "after": "mutually-exclusive-match-bindings:regression",
      "reason": "Bind the regression to the public failure and current test owner.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:regression"]
    },
    {
      "before": "mutually-exclusive-match-bindings:recognize",
      "after": "mutually-exclusive-match-bindings:validate",
      "reason": "Observe behavior after implementation modification.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"]
    },
    {
      "before": "mutually-exclusive-match-bindings:regression",
      "after": "mutually-exclusive-match-bindings:validate",
      "reason": "Execute the encoded assertion; its definition alone does not prove success.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"]
    }
  ]
}
```

The two edits can occur in either order after diagnosis. Every retained edit
requires the explicit validation operation.
