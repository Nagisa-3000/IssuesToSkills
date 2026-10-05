# Historical realization

This is the sole historical realization. Its validation requirements derive from the public report, implementation, and committed assertion. They are obligations, not claims of historical CI execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0",
  "goal": "Prevent an Attribute inner subscript base from reaching Name-only field access while retaining supported dictionary-lookup diagnostics.",
  "mechanism": "Confirm the unchecked inner-base assumption, insert short-circuit Name discrimination, add the attribute-subscript regression, and validate public diagnostics.",
  "action_ids": [
    "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:locate",
    "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:repair",
    "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:validate"
  ],
  "source_ids": ["pylint-dev/pylint:6557:repair:5fcccc13f1f7"],
  "required_effects": [
    {"key": "unsafe-name-read-guarded", "value": true, "evaluator": "evidence"},
    {"key": "attribute-subscript-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "supported-name-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-negative-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:locate",
      "after": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:repair",
      "reason": "Confirm the reported inner-base assumption and bind the corresponding current branch before changing it.",
      "evidence_refs": ["pylint-dev/pylint:6557:body", "pylint-dev/pylint:6557:fix"]
    },
    {
      "before": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:repair",
      "after": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:validate",
      "reason": "Validate the guarded checker and added fixture together against post-edit state.",
      "evidence_refs": ["pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"]
    }
  ]
}
```
