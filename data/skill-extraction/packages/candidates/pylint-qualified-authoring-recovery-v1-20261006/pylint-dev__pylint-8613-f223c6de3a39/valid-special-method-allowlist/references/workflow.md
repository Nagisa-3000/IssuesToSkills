# Historical Workflow

This authored realization represents the registry edit and regression assertion. Current probes and validation are conditional operations, not assertions of unknown historical execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:6811635fea96a3e3f778e2f1",
  "goal": "Remove a valid Python special-method name false positive without weakening invalid-name detection.",
  "mechanism": "Confirm an omitted valid name, extend the consumed acceptance registry narrowly, add a no-warning regression, and validate adjacent diagnostics.",
  "action_ids": [
    "workflow:verified-history:6811635fea96a3e3f778e2f1:probe",
    "workflow:verified-history:6811635fea96a3e3f778e2f1:register",
    "workflow:verified-history:6811635fea96a3e3f778e2f1:regression",
    "workflow:verified-history:6811635fea96a3e3f778e2f1:validate"
  ],
  "source_ids": ["pylint-dev/pylint:8613:repair:f223c6de3a39"],
  "required_effects": [
    {"key": "valid-method-accepted", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "invalid-name-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:6811635fea96a3e3f778e2f1:probe",
      "after": "workflow:verified-history:6811635fea96a3e3f778e2f1:register",
      "reason": "Confirm method validity and the registry omission before changing acceptance.",
      "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:fix"]
    },
    {
      "before": "workflow:verified-history:6811635fea96a3e3f778e2f1:probe",
      "after": "workflow:verified-history:6811635fea96a3e3f778e2f1:regression",
      "reason": "Bind the assertion to the reported false positive and current harness convention.",
      "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:regression"]
    },
    {
      "before": "workflow:verified-history:6811635fea96a3e3f778e2f1:register",
      "after": "workflow:verified-history:6811635fea96a3e3f778e2f1:validate",
      "reason": "Observe acceptance after changing the registry.",
      "evidence_refs": ["pylint-dev/pylint:8613:fix", "pylint-dev/pylint:8613:regression"]
    },
    {
      "before": "workflow:verified-history:6811635fea96a3e3f778e2f1:regression",
      "after": "workflow:verified-history:6811635fea96a3e3f778e2f1:validate",
      "reason": "Execute the added assertion and retained expectations after modifying the fixture.",
      "evidence_refs": ["pylint-dev/pylint:8613:regression"]
    }
  ]
}
```
