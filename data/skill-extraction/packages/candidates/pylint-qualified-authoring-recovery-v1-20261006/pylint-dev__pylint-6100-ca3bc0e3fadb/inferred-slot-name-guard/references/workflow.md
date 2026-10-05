# Historical realization: guarded inferred slot-name collection

This realization describes the repair mechanism and its committed regression coverage. The validation action specifies what must be checked in a current use; it does not assert that historical CI ran or that this authored workflow has executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:d6e93404a2d76602b0907d8c",
  "goal": "Prevent inferred nonstring slot objects from crashing inherited-slot analysis while retaining valid slot comparisons.",
  "mechanism": "Inspect the inferred-name consumer, replace an inference-truthiness assumption with safe attribute extraction and string filtering, and validate a no-crash regression alongside inherited-slot assertions.",
  "action_ids": [
    "workflow:verified-history:d6e93404a2d76602b0907d8c:inspect",
    "workflow:verified-history:d6e93404a2d76602b0907d8c:guard",
    "workflow:verified-history:d6e93404a2d76602b0907d8c:validate"
  ],
  "source_ids": ["pylint-dev/pylint:6100:repair:ca3bc0e3fadb"],
  "required_effects": [
    {"key": "inferred-slot-string-filter-installed", "value": true, "evaluator": "evidence"},
    {"key": "nonliteral-slot-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "valid-inherited-slot-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-slot-validation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:d6e93404a2d76602b0907d8c:inspect",
      "after": "workflow:verified-history:d6e93404a2d76602b0907d8c:guard",
      "reason": "Confirm that the inferred branch consumes an optional, potentially nonstring value before applying this narrowly scoped guard.",
      "evidence_refs": ["pylint-dev/pylint:6100:body", "pylint-dev/pylint:6100:fix"]
    },
    {
      "before": "workflow:verified-history:d6e93404a2d76602b0907d8c:guard",
      "after": "workflow:verified-history:d6e93404a2d76602b0907d8c:validate",
      "reason": "The changed collector and new fixture require refreshed no-crash and inherited-slot checks.",
      "evidence_refs": ["pylint-dev/pylint:6100:fix", "pylint-dev/pylint:6100:regression"]
    }
  ]
}
```
