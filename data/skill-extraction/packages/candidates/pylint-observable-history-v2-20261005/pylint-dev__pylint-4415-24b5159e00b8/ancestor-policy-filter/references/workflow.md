# Historical realization

Required effects are current execution targets, not observed Skill outcomes.

```arex-workflow-v4
{
  "id": "workflow:verified-history:58d864f47bb516a028d64059",
  "goal": "Remove ancestry false positives caused by explicitly exempt ancestors while retaining excessive user-defined ancestry warnings.",
  "mechanism": "Filter resolved qualified names from the existing transitive ancestor stream using an explicit exemption set before counting.",
  "action_ids": [
    "workflow:verified-history:58d864f47bb516a028d64059:probe",
    "workflow:verified-history:58d864f47bb516a028d64059:repair",
    "workflow:verified-history:58d864f47bb516a028d64059:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4415:repair:24b5159e00b8"],
  "required_effects": [
    {"key": "supported-exempt-ancestors-not-counted", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-validated", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "user-defined-ancestry-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-threshold-comparison-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-design-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:58d864f47bb516a028d64059:probe",
      "after": "workflow:verified-history:58d864f47bb516a028d64059:repair",
      "reason": "Filtering requires the actual counting owner, resolved ancestor identities, and evidence-supported exemption policy.",
      "evidence_refs": ["pylint-dev/pylint:4415:body", "pylint-dev/pylint:4415:fix"]
    },
    {
      "before": "workflow:verified-history:58d864f47bb516a028d64059:repair",
      "after": "workflow:verified-history:58d864f47bb516a028d64059:validate",
      "reason": "The changed count and assertions require verification of the removed false positive and retained legitimate warnings.",
      "evidence_refs": ["pylint-dev/pylint:4415:fix", "pylint-dev/pylint:4415:regression"]
    }
  ]
}
```
