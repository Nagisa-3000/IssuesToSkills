# Historical realization: inferred staticmethod exemption

This contract reconstructs a reusable conditional Workflow from the report, implementation, and committed assertions. It does not claim the authoring probes or evaluation cases ran historically.

```arex-workflow-v4
{
  "id": "workflow:verified-history:d64e04a769c8484780ab2708",
  "goal": "Avoid ordinary method-argument diagnostics for decorators inferred as builtins.staticmethod.",
  "mechanism": "After direct staticmethod handling and before ordinary missing-receiver checks, return for inferred builtins.staticmethod identity; retain targeted regression assertions and ordinary-method controls.",
  "action_ids": [
    "workflow:verified-history:d64e04a769c8484780ab2708:probe",
    "workflow:verified-history:d64e04a769c8484780ab2708:repair",
    "workflow:verified-history:d64e04a769c8484780ab2708:validate"
  ],
  "source_ids": ["pylint-dev/pylint:7300:repair:0fa2d6e43b25"],
  "required_effects": [
    {"key": "inferred-staticmethod-exemption-installed", "value": true, "evaluator": "evidence"},
    {"key": "target-regressions-installed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-method-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "direct-staticmethod-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-method-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:d64e04a769c8484780ab2708:probe",
      "after": "workflow:verified-history:d64e04a769c8484780ab2708:repair",
      "reason": "Establish inferred identity and the diagnostic decision boundary before applying the local exemption.",
      "evidence_refs": ["pylint-dev/pylint:7300:body", "pylint-dev/pylint:7300:fix"]
    },
    {
      "before": "workflow:verified-history:d64e04a769c8484780ab2708:repair",
      "after": "workflow:verified-history:d64e04a769c8484780ab2708:validate",
      "reason": "Observe the repaired checker against targeted and adjacent assertions after changing code and fixtures.",
      "evidence_refs": ["pylint-dev/pylint:7300:fix", "pylint-dev/pylint:7300:regression"]
    }
  ]
}
```
