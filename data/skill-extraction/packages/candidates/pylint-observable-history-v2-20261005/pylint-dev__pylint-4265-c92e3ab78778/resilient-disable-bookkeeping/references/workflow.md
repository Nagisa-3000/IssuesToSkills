# Historical Workflow: tolerate missing advisory IDs

The four operations describe the supplied repair and its conditional reuse. Their contracts state expected effects, not newly observed execution outcomes. The probe and validation are evidence-backed procedures; they do not assert undocumented historical author actions or CI runs.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b",
  "goal": "Prevent missing numeric-message advisory lookup from interrupting configured disables.",
  "mechanism": "Catch KeyError locally in numeric-ID advisory registration and retain a mixed-ID configuration regression.",
  "action_ids": [
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:probe",
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:guard",
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:regression",
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4265:repair:c92e3ab78778"],
  "required_effects": [
    {"key": "missing-advisory-id-tolerated", "value": true, "evaluator": "evidence"},
    {"key": "mixed-id-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "known-numeric-registration-preserved", "value": true, "evaluator": "evidence"},
    {"key": "symbolic-disable-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-errors-not-suppressed", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:probe",
      "after": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:guard",
      "reason": "Establish that the failing lookup belongs to advisory numeric-ID registration before narrowing its exception boundary.",
      "evidence_refs": ["pylint-dev/pylint:4265:fix"]
    },
    {
      "before": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:probe",
      "after": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:regression",
      "reason": "Bind identifiers and the public regression harness to the current implementation.",
      "evidence_refs": ["pylint-dev/pylint:4265:regression"]
    },
    {
      "before": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:guard",
      "after": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:validate",
      "reason": "Validate configuration continuation and preserved registration after the code modification.",
      "evidence_refs": ["pylint-dev/pylint:4265:fix", "pylint-dev/pylint:4265:regression"]
    },
    {
      "before": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:regression",
      "after": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:validate",
      "reason": "The final validation must exercise the retained configuration regression.",
      "evidence_refs": ["pylint-dev/pylint:4265:regression"]
    }
  ]
}
```

The guard and regression Actions have no mandatory ordering between them. A current causal probe can use the regression before the guard; final validation follows both modifications.
