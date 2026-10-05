# Historical Workflow

This source-grounded reconstruction does not assert the original author's task sequence or historical CI execution. Validation effects are current-use obligations, not invented historical execution results.

```arex-workflow-v4
{
  "id": "workflow:verified-history:4244f18e715c9b86c7cef8e0",
  "goal": "Prevent compound-receiver crashes in private-member usage analysis while retaining ordinary simple-receiver behavior.",
  "mechanism": "Establish the unchecked receiver-name assumption, guard receiver type, conservatively break the candidate search on non-Name receivers, add the chained-receiver regression, and validate.",
  "action_ids": [
    "workflow:verified-history:4244f18e715c9b86c7cef8e0:inspect",
    "workflow:verified-history:4244f18e715c9b86c7cef8e0:repair",
    "workflow:verified-history:4244f18e715c9b86c7cef8e0:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5261:repair:0a1ebd488fcd"],
  "required_effects": [
    {"key": "receiver-assumption-established", "value": true, "evaluator": "evidence"},
    {"key": "guard-and-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "simple-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "argument-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-emission-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:4244f18e715c9b86c7cef8e0:inspect",
      "after": "workflow:verified-history:4244f18e715c9b86c7cef8e0:repair",
      "reason": "Receiver shape and candidate loop control flow establish where the guard belongs and what break means.",
      "evidence_refs": ["pylint-dev/pylint:5261:body", "pylint-dev/pylint:5261:fix"]
    },
    {
      "before": "workflow:verified-history:4244f18e715c9b86c7cef8e0:repair",
      "after": "workflow:verified-history:4244f18e715c9b86c7cef8e0:validate",
      "reason": "The edited checker and committed regression require public verification together.",
      "evidence_refs": ["pylint-dev/pylint:5261:fix", "pylint-dev/pylint:5261:regression"]
    }
  ]
}
```
