# Historical Workflow

This contract represents the source-specific mechanism and validation obligation, not a claim that every authored operation ran historically in this exact order. Original historical execution is unknown.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a4e1808f638c9a903d335608",
  "goal": "Preserve complete digit-bearing symbolic identifiers in disable directives without changing adjacent parser behavior.",
  "mechanism": "Include ASCII digits in the symbolic token character class and pin complete parsed output with a regression assertion.",
  "action_ids": [
    "workflow:verified-history:a4e1808f638c9a903d335608:diagnose",
    "workflow:verified-history:a4e1808f638c9a903d335608:repair",
    "workflow:verified-history:a4e1808f638c9a903d335608:validate"
  ],
  "source_ids": ["pylint-dev/pylint:3666:repair:fe0a7f795343"],
  "required_effects": [
    {"key": "digit-bearing-symbol-preserved", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "adjacent-directive-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-token-grammar-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a4e1808f638c9a903d335608:diagnose",
      "after": "workflow:verified-history:a4e1808f638c9a903d335608:repair",
      "reason": "The narrow repair requires confirmation of lexical digit exclusion and valid digit-bearing symbolic names.",
      "evidence_refs": ["pylint-dev/pylint:3666:body", "pylint-dev/pylint:3666:fix"]
    },
    {
      "before": "workflow:verified-history:a4e1808f638c9a903d335608:repair",
      "after": "workflow:verified-history:a4e1808f638c9a903d335608:validate",
      "reason": "Exact output and neighboring behavior must be checked against the edited lexer and regression.",
      "evidence_refs": ["pylint-dev/pylint:3666:fix", "pylint-dev/pylint:3666:regression"]
    }
  ]
}
```
