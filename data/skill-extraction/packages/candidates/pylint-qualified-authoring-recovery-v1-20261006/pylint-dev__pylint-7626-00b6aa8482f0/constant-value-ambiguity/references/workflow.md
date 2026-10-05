# Historical realization: preserve constant-value ambiguity

This realization describes the supplied repair mechanism. Current execution must first establish equivalent semantic owners and prerequisites; historical list order alone is not sufficient.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3",
  "goal": "Prevent unsafe Boolean rewrite suggestions caused by unequal same-type inferred constants while retaining definite-value diagnostics.",
  "mechanism": "Opt in to constant-value ambiguity checking at the inference helper and suppress rewrite diagnostics when inference is uncertain.",
  "action_ids": [
    "workflow:verified-history:b8f0f43a57ace4a8864a27f3:probe",
    "workflow:verified-history:b8f0f43a57ace4a8864a27f3:repair",
    "workflow:verified-history:b8f0f43a57ace4a8864a27f3:validate"
  ],
  "source_ids": ["pylint-dev/pylint:7626:repair:00b6aa8482f0"],
  "required_effects": [
    {"key": "opt-in-constant-ambiguity", "value": true, "evaluator": "evidence"},
    {"key": "uncertain-rewrite-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "default-inference-contract-preserved", "value": true, "evaluator": "evidence"},
    {"key": "definite-value-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:probe",
      "after": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:repair",
      "reason": "The repair requires observed same-type unequal constants and compatible helper and consumer bindings.",
      "evidence_refs": ["pylint-dev/pylint:7626:body", "pylint-dev/pylint:7626:fix"]
    },
    {
      "before": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:repair",
      "after": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:validate",
      "reason": "Changed inference, diagnostic emission, and regression expectations require fresh public validation.",
      "evidence_refs": ["pylint-dev/pylint:7626:fix", "pylint-dev/pylint:7626:regression"]
    }
  ]
}
```

The probe is a current-use prerequisite inferred from the supplied report and implementation, not a claim that an undocumented historical probe was executed. Validation describes the committed assertion boundary; historical execution remains unknown.
