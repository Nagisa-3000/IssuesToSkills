# Historical Workflow

This canonical realization describes the supplied repair mechanism. Action effects are conditional requirements, not newly observed execution results. The probe and validation contracts are authored operationalizations of the report, implementation, and committed assertions; no historical execution sequence is asserted.

```arex-workflow-v4
{
  "id": "workflow:verified-history:2d9cfc7283460de886b0b9d6",
  "goal": "Correct false undefined-name diagnostics for decorator-local generator bindings without hiding genuinely undefined names.",
  "mechanism": "Retain the consumed-name gate and permit function-decorator context to bypass the comprehension/upper-function homonym exception; retain the exception elsewhere.",
  "action_ids": [
    "workflow:verified-history:2d9cfc7283460de886b0b9d6:probe",
    "workflow:verified-history:2d9cfc7283460de886b0b9d6:repair",
    "workflow:verified-history:2d9cfc7283460de886b0b9d6:validate"
  ],
  "source_ids": ["pylint-dev/pylint:3791:repair:a054796d7008"],
  "required_effects": [
    {"key": "decorator-bound-name-accepted", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-boundary-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "genuine-undefined-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nondecorator-homonym-protection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-check-path-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:2d9cfc7283460de886b0b9d6:probe",
      "after": "workflow:verified-history:2d9cfc7283460de886b0b9d6:repair",
      "reason": "The reported parameter-name control and implemented scope guard establish the mechanism that must be bound before a current edit.",
      "evidence_refs": ["pylint-dev/pylint:3791:body", "pylint-dev/pylint:3791:fix"]
    },
    {
      "before": "workflow:verified-history:2d9cfc7283460de886b0b9d6:repair",
      "after": "workflow:verified-history:2d9cfc7283460de886b0b9d6:validate",
      "reason": "The edited guard and added positive and negative assertions require post-edit diagnostic observations.",
      "evidence_refs": ["pylint-dev/pylint:3791:fix", "pylint-dev/pylint:3791:regression"]
    }
  ]
}
```
