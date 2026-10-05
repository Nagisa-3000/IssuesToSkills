# Historical workflow: narrowly exempt direct comprehension filter tests

This is a newly authored representation of the supplied repair, not a historical execution transcript. Probe and validation operations describe the evidence-supported investigation and checks; their execution in a new checkout must be observed independently.

```arex-workflow-v4
{
  "id": "workflow:verified-history:afcebec8041ecae4f0debb6d",
  "goal": "Remove the handler-name collision false positive for a direct comprehension filter test without losing genuine exception-scope diagnostics.",
  "mechanism": "Condition the exception-handler assignment-candidate filter on whether the use is a direct member of a comprehension's filter-test list.",
  "action_ids": [
    "workflow:verified-history:afcebec8041ecae4f0debb6d:probe",
    "workflow:verified-history:afcebec8041ecae4f0debb6d:repair",
    "workflow:verified-history:afcebec8041ecae4f0debb6d:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5817:repair:67055f422132"],
  "required_effects": [
    {"key": "direct-filter-collision-diagnostic", "value": "absent", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "genuine-exception-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-candidate-filter-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:afcebec8041ecae4f0debb6d:probe",
      "after": "workflow:verified-history:afcebec8041ecae4f0debb6d:repair",
      "reason": "The guard requires the actual direct-filter AST relation and the responsible candidate-filter owner.",
      "evidence_refs": ["pylint-dev/pylint:5817:body", "pylint-dev/pylint:5817:fix"]
    },
    {
      "before": "workflow:verified-history:afcebec8041ecae4f0debb6d:repair",
      "after": "workflow:verified-history:afcebec8041ecae4f0debb6d:validate",
      "reason": "The changed guard and added regression require fresh target and adjacent-behavior checks.",
      "evidence_refs": ["pylint-dev/pylint:5817:fix", "pylint-dev/pylint:5817:regression"]
    }
  ]
}
```
