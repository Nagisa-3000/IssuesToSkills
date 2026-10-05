# Historical workflow: boundness-gated receiver classification

This authored realization describes the supplied historical repair and regression assertions. It does not assert that this sequence was an observed developer task plan or that historical CI executed it. Current task ordering is derived from semantic dependencies and current bindings.

```arex-workflow-v4
{
  "id": "workflow:verified-history:5eae2300be395ac5633f17e5",
  "goal": "Restore protected-access diagnostics for ordinary-function and static-method parameters without removing legitimate bound-receiver exemptions.",
  "mechanism": "Require function boundness before fallback classification of its first argument as an implicit receiver; retain surrounding guards and add public diagnostic assertions.",
  "action_ids": [
    "workflow:verified-history:5eae2300be395ac5633f17e5:inspect",
    "workflow:verified-history:5eae2300be395ac5633f17e5:repair",
    "workflow:verified-history:5eae2300be395ac5633f17e5:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5989:repair:5c8384e811e3"],
  "required_effects": [
    {"key": "unbound-first-parameter-exemption-rejected", "value": true, "evaluator": "evidence"},
    {"key": "external-protected-access-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "legitimate-bound-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-protected-access-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "call-expression-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:5eae2300be395ac5633f17e5:inspect",
      "after": "workflow:verified-history:5eae2300be395ac5633f17e5:repair",
      "reason": "Establish that a first-parameter receiver exemption is suppressing the diagnostic and locate compatible semantic owners before modifying them.",
      "evidence_refs": ["pylint-dev/pylint:5989:body", "pylint-dev/pylint:5989:fix"]
    },
    {
      "before": "workflow:verified-history:5eae2300be395ac5633f17e5:repair",
      "after": "workflow:verified-history:5eae2300be395ac5633f17e5:validate",
      "reason": "The implementation and new assertions require fresh public diagnostic and adjacent-behavior checks after editing.",
      "evidence_refs": ["pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"]
    }
  ]
}
```
