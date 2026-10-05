# Historical realization

This newly authored contract describes the reported problem, merged implementation, and committed assertions. It does not claim these contracts existed historically or that historical tests executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:c24ac7f0cdc266e6796600de",
  "goal": "Exclude supported raising function-like values from callable-comparison warnings while retaining ordinary callable diagnostics.",
  "mechanism": "Safely infer operands, exclude immediate-body Raise nodes and typing._SpecialForm-decorated function-like nodes from eligible callable counting, and retain the exactly-one emission condition.",
  "action_ids": [
    "workflow:verified-history:c24ac7f0cdc266e6796600de:inspect",
    "workflow:verified-history:c24ac7f0cdc266e6796600de:repair",
    "workflow:verified-history:c24ac7f0cdc266e6796600de:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5557:repair:2a69387352bd"],
  "required_effects": [
    {"key": "supported-exclusions-implemented", "value": true, "evaluator": "evidence"},
    {"key": "supported-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-callable-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "noncallable-and-unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:c24ac7f0cdc266e6796600de:inspect",
      "after": "workflow:verified-history:c24ac7f0cdc266e6796600de:repair",
      "reason": "Establish the supported inference and classification mechanism before modifying its owner.",
      "evidence_refs": ["pylint-dev/pylint:5557:body", "pylint-dev/pylint:5557:fix"]
    },
    {
      "before": "workflow:verified-history:c24ac7f0cdc266e6796600de:repair",
      "after": "workflow:verified-history:c24ac7f0cdc266e6796600de:validate",
      "reason": "Check exclusion assertions and retained diagnostic behavior after checker and fixture edits.",
      "evidence_refs": ["pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"]
    }
  ]
}
```
