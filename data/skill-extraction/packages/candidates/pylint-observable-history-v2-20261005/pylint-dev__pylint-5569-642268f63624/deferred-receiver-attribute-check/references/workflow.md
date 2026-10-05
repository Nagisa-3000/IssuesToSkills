# Historical Workflow

Effects are contract obligations, not observed execution of newly authored Actions. Current plans must follow compatible ports, confirmed prerequisites and retained validation.

```arex-workflow-v4
{
  "id": "workflow:verified-history:c0bacc1cf00a988417910aa7",
  "goal": "Avoid name-only access on a recognized type-call receiver during deferred private-member checking while retaining the committed diagnostic.",
  "mechanism": "Guard the narrow receiver and recover mandatory parameter identity from function ancestry when transient tracking is absent.",
  "action_ids": [
    "workflow:verified-history:c0bacc1cf00a988417910aa7:probe",
    "workflow:verified-history:c0bacc1cf00a988417910aa7:repair",
    "workflow:verified-history:c0bacc1cf00a988417910aa7:validate"
  ],
  "source_ids": ["pylint-dev/pylint:5569:repair:642268f63624"],
  "required_effects": [
    {"key": "recognized-call-name-access-avoided", "value": true, "evaluator": "evidence"},
    {"key": "deferred-parameter-identity-recoverable", "value": true, "evaluator": "evidence"},
    {"key": "regression-diagnostic-retained", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "adjacent-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "narrow-receiver-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:c0bacc1cf00a988417910aa7:probe",
      "after": "workflow:verified-history:c0bacc1cf00a988417910aa7:repair",
      "reason": "Confirm the receiver, unsafe access and deferred parameter lifecycle before editing current owners.",
      "evidence_refs": ["pylint-dev/pylint:5569:body", "pylint-dev/pylint:5569:fix"]
    },
    {
      "before": "workflow:verified-history:c0bacc1cf00a988417910aa7:repair",
      "after": "workflow:verified-history:c0bacc1cf00a988417910aa7:validate",
      "reason": "Validate the modified implementation and retained diagnostic expectation together.",
      "evidence_refs": ["pylint-dev/pylint:5569:fix", "pylint-dev/pylint:5569:regression"]
    }
  ]
}
```
