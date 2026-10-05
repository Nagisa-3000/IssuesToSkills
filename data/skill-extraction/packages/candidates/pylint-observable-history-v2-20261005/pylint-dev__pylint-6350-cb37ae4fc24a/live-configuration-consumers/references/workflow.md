# Historical Workflow

Use live host configuration instead of constructor-time copies, with separate standalone initialization and public regression coverage.

```arex-workflow-v4
{
  "id": "workflow:verified-history:44cf4d12e6c9f03961fb6377",
  "goal": "Make configured similarity options reach runtime consumers without stale constructor copies.",
  "mechanism": "Alias the host configuration namespace in integrated mode, retain a private namespace in standalone mode, migrate option reads, remove redundant synchronization, and add public regression coverage.",
  "action_ids": [
    "workflow:verified-history:44cf4d12e6c9f03961fb6377:diagnose",
    "workflow:verified-history:44cf4d12e6c9f03961fb6377:repair",
    "workflow:verified-history:44cf4d12e6c9f03961fb6377:validate"
  ],
  "source_ids": ["pylint-dev/pylint:6350:repair:cb37ae4fc24a"],
  "required_effects": [
    {"key": "runtime-options-live", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "standalone-option-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "similarity-algorithm-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:44cf4d12e6c9f03961fb6377:diagnose",
      "after": "workflow:verified-history:44cf4d12e6c9f03961fb6377:repair",
      "reason": "Confirm stale copies, compatible live ownership, and safe initialization before changing option storage.",
      "evidence_refs": ["pylint-dev/pylint:6350:body", "pylint-dev/pylint:6350:fix"]
    },
    {
      "before": "workflow:verified-history:44cf4d12e6c9f03961fb6377:repair",
      "after": "workflow:verified-history:44cf4d12e6c9f03961fb6377:validate",
      "reason": "Public checks must observe the edited consumer and added regression.",
      "evidence_refs": ["pylint-dev/pylint:6350:fix", "pylint-dev/pylint:6350:regression"]
    }
  ]
}
```

The ordering is a conditional authored reconstruction. Historical assertions do not establish that this authored Workflow was executed. Current validation must separately discharge all preservation obligations.
