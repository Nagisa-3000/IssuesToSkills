# Canonical historical Workflow

This realization covers all packaged Actions. Current bindings and results remain separate from historical evidence.

```arex-workflow-v4
{
  "id": "workflow:verified-history:3af38f4091bb3d8442540d61",
  "goal": "Recommend symbolic names for accepted lowercase numeric IDs while preserving existing diagnostic and directive behavior.",
  "mechanism": "Uppercase the numeric-ID mapping lookup key at the symbol resolver while retaining original input spelling.",
  "action_ids": [
    "workflow:verified-history:3af38f4091bb3d8442540d61:probe",
    "workflow:verified-history:3af38f4091bb3d8442540d61:normalize",
    "workflow:verified-history:3af38f4091bb3d8442540d61:regression",
    "workflow:verified-history:3af38f4091bb3d8442540d61:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5000:repair:bbaa7bc9200a"],
  "required_effects": [
    {"key": "numeric-symbol-lookup-case-insensitive", "value": true, "evaluator": "evidence"},
    {"key": "lowercase-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "uppercase-recommendations-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unknown-id-error-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-id-spelling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:3af38f4091bb3d8442540d61:probe",
      "after": "workflow:verified-history:3af38f4091bb3d8442540d61:normalize",
      "reason": "Establish accepted lowercase IDs, uppercase keys, and raw resolver lookup before editing.",
      "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:fix"]
    },
    {
      "before": "workflow:verified-history:3af38f4091bb3d8442540d61:probe",
      "after": "workflow:verified-history:3af38f4091bb3d8442540d61:regression",
      "reason": "Establish the public reproduction and registry-backed symbols before asserting recommendations.",
      "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:regression"]
    },
    {
      "before": "workflow:verified-history:3af38f4091bb3d8442540d61:normalize",
      "after": "workflow:verified-history:3af38f4091bb3d8442540d61:validate",
      "reason": "Observe changed lookup behavior and unchanged error handling.",
      "evidence_refs": ["pylint-dev/pylint:5000:fix", "pylint-dev/pylint:5000:regression"]
    },
    {
      "before": "workflow:verified-history:3af38f4091bb3d8442540d61:regression",
      "after": "workflow:verified-history:3af38f4091bb3d8442540d61:validate",
      "reason": "Final validation includes the strengthened lowercase multi-ID regression.",
      "evidence_refs": ["pylint-dev/pylint:5000:regression"]
    }
  ]
}
```
