# Canonical historical realization

Dependencies express current semantic prerequisites grounded in the repair, not an invented historical execution trace.

```arex-workflow-v4
{
  "id": "workflow:verified-history:9458ec98dda8784befed789c",
  "goal": "Credit annotated keyword-only parameters without weakening missing-type diagnostics.",
  "mechanism": "Extend the parameter-type evidence set using the separate aligned keyword-only parameter and annotation collections before missing-type comparison.",
  "action_ids": [
    "workflow:verified-history:9458ec98dda8784befed789c:probe",
    "workflow:verified-history:9458ec98dda8784befed789c:edit",
    "workflow:verified-history:9458ec98dda8784befed789c:validate"
  ],
  "source_ids": ["pylint-dev/pylint:3092:repair:ce2af67d0e96"],
  "required_effects": [
    {"key": "annotated-keyword-only-coverage", "value": true, "evaluator": "evidence"},
    {"key": "focused-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-annotation-credit-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-type-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:9458ec98dda8784befed789c:probe",
      "after": "workflow:verified-history:9458ec98dda8784befed789c:edit",
      "reason": "Confirm the omission, policy, annotation alignment, and current owners before editing.",
      "evidence_refs": ["pylint-dev/pylint:3092:body", "pylint-dev/pylint:3092:fix"]
    },
    {
      "before": "workflow:verified-history:9458ec98dda8784befed789c:edit",
      "after": "workflow:verified-history:9458ec98dda8784befed789c:validate",
      "reason": "Validate the modified collector and committed regression shape after they exist.",
      "evidence_refs": ["pylint-dev/pylint:3092:fix", "pylint-dev/pylint:3092:regression"]
    }
  ]
}
```
