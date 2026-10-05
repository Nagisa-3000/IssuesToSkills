# Historical Workflow

This realization covers the inspection prerequisite, modifying operation, and explicit post-edit validation derived from one historical repair.

```arex-workflow-v4
{
  "id": "workflow:verified-history:79391484ce4048a1c8e1217a",
  "goal": "Remove a useless-delegation false positive for unavailable inherited arguments and a non-self-only override.",
  "mechanism": "Conservatively decline to prove signature equivalence when inherited argument metadata is unavailable, using a narrow non-self-only guard.",
  "action_ids": [
    "workflow:verified-history:79391484ce4048a1c8e1217a:inspect",
    "workflow:verified-history:79391484ce4048a1c8e1217a:repair",
    "workflow:verified-history:79391484ce4048a1c8e1217a:validate"
  ],
  "source_ids": ["pylint-dev/pylint:7319:repair:7fdf8d9ee090"],
  "required_effects": [
    {"key": "target-false-positive-removed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "inspectable-signature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "self-only-guard-boundary-preserved", "value": true, "evaluator": "evidence"},
    {"key": "fixture-interface-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:79391484ce4048a1c8e1217a:inspect",
      "after": "workflow:verified-history:79391484ce4048a1c8e1217a:repair",
      "reason": "Establish signature opacity and non-self-only arguments before selecting the guard.",
      "evidence_refs": ["pylint-dev/pylint:7319:body", "pylint-dev/pylint:7319:fix"]
    },
    {
      "before": "workflow:verified-history:79391484ce4048a1c8e1217a:repair",
      "after": "workflow:verified-history:79391484ce4048a1c8e1217a:validate",
      "reason": "Checker and regression edits require fresh target and preservation checks.",
      "evidence_refs": ["pylint-dev/pylint:7319:fix", "pylint-dev/pylint:7319:regression"]
    }
  ]
}
```
