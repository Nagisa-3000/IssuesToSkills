# Historical realization

This source-specific realization captures the guarded accounting correction and its committed public regression boundary. It does not claim that these newly authored operations were historically executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89",
  "goal": "Restore missing-required-argument reporting when **kwargs captures a positional-only parameter name.",
  "mechanism": "Avoid the supplied-state update for same-name positional-only keywords accepted by a keyword collector; retain existing required/default checking.",
  "action_ids": [
    "workflow:verified-history:33b6359d2826e0cbb3dcbe89:locate",
    "workflow:verified-history:33b6359d2826e0cbb3dcbe89:repair",
    "workflow:verified-history:33b6359d2826e0cbb3dcbe89:validate"
  ],
  "source_ids": ["pylint-dev/pylint:8559:repair:2db55f6a4896"],
  "required_effects": [
    {"key": "captured-keyword-does-not-satisfy-positional-only", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {
      "key": "adjacent-binding-behavior-preserved",
      "value": true,
      "evaluator": "evidence",
      "description": "Preserve ordinary keyword binding, positional supply, mixed signatures, defaults, and the existing no-collector rejection path."
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:locate",
      "after": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:repair",
      "reason": "Confirm and bind the erroneous satisfaction transition before modifying it.",
      "evidence_refs": ["pylint-dev/pylint:8559:body", "pylint-dev/pylint:8559:fix"]
    },
    {
      "before": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:repair",
      "after": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:validate",
      "reason": "Implementation and regression edits require fresh public observations of the target and legal controls.",
      "evidence_refs": ["pylint-dev/pylint:8559:fix", "pylint-dev/pylint:8559:regression"]
    }
  ]
}
```
