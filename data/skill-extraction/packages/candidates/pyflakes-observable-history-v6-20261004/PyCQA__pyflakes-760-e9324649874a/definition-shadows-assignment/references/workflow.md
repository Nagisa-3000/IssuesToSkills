# Canonical Workflow

Extend the definition-binding redefinition predicate while leaving diagnostic policy in its existing owner. Add an assignment-shadowed-by-definition regression and validate the changed behavior plus adjacent behavior.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf",
  "goal": "Detect unused same-name assignments replaced by definitions without banning ordinary rebinding.",
  "mechanism": "Preserve superclass redefinition classification and add the same-name Assignment case to the definition binding predicate.",
  "action_ids": [
    "workflow:verified-history:ee79eebf2283561900232caf:locate-and-probe",
    "workflow:verified-history:ee79eebf2283561900232caf:extend-and-cover",
    "workflow:verified-history:ee79eebf2283561900232caf:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:760:repair:e9324649874a"],
  "required_effects": [
    {"key": "definition-assignment-rule-present", "value": true, "evaluator": "evidence"},
    {"key": "target-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "superclass-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-rebinding-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ee79eebf2283561900232caf:locate-and-probe",
      "after": "workflow:verified-history:ee79eebf2283561900232caf:extend-and-cover",
      "reason": "The report and patch require a compatible definition/assignment distinction and current diagnostic-policy review before modifying the binding predicate.",
      "evidence_refs": ["PyCQA/pyflakes:760:body", "PyCQA/pyflakes:760:fix"]
    },
    {
      "before": "workflow:verified-history:ee79eebf2283561900232caf:extend-and-cover",
      "after": "workflow:verified-history:ee79eebf2283561900232caf:validate",
      "reason": "The added regression must exercise the edited predicate; post-edit checks refresh stale observations.",
      "evidence_refs": ["PyCQA/pyflakes:760:fix", "PyCQA/pyflakes:760:regression"]
    }
  ]
}
```

All packaged Actions belong to this canonical realization. There are no independently supported alternative realizations.

The adjacent-behavior invariants are requirements for current execution, not claims that exhaustive preservation was historically demonstrated. Current review and probes must substantiate them.
