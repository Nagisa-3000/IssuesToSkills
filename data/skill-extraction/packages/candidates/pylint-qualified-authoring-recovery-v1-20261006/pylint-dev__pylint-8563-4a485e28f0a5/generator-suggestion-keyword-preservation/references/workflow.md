# Historical realization

This single-source realization preserves the existing recommendation while repairing its rendered replacement. The validation operation expresses checks required by the committed assertions; it does not claim historical CI ran.

```arex-workflow-v4
{
  "id": "workflow:verified-history:4f600acd843f37945bbd0765",
  "goal": "Produce valid generator suggestions that preserve existing keyword arguments.",
  "mechanism": "Within the existing single-positional-list-comprehension branch, wrap the extracted generator body when keywords follow and append ordered keyword AST renderings.",
  "action_ids": [
    "workflow:verified-history:4f600acd843f37945bbd0765:inspect",
    "workflow:verified-history:4f600acd843f37945bbd0765:repair",
    "workflow:verified-history:4f600acd843f37945bbd0765:validate"
  ],
  "source_ids": ["pylint-dev/pylint:8563:repair:4a485e28f0a5"],
  "required_effects": [
    {"key": "keyword-aware-suggestion-rendering", "value": true, "evaluator": "evidence"},
    {"key": "paired-keyword-regression-assertions", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "keyword-free-suggestion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-eligibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:4f600acd843f37945bbd0765:inspect",
      "after": "workflow:verified-history:4f600acd843f37945bbd0765:repair",
      "reason": "Current applicability and owner bindings must establish the matching rendering branch before modification.",
      "evidence_refs": ["pylint-dev/pylint:8563:body", "pylint-dev/pylint:8563:fix"]
    },
    {
      "before": "workflow:verified-history:4f600acd843f37945bbd0765:repair",
      "after": "workflow:verified-history:4f600acd843f37945bbd0765:validate",
      "reason": "The modified renderer and paired assertions require fresh observation of exact output and preserved adjacent behavior.",
      "evidence_refs": ["pylint-dev/pylint:8563:fix", "pylint-dev/pylint:8563:regression"]
    }
  ]
}
```
