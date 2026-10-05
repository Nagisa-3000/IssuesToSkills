# Historical Workflow

Replace immediate-parent-only recognition with frame-bounded recognition of the context-item region. Retain body warnings and validate public assertions. The validation contract describes required current checks supported by committed assertions; historical execution is unknown.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ec6290f765c15f3fdc7283d4",
  "goal": "Remove conditional context-item resource false positives while preserving unmanaged-body diagnostics.",
  "mechanism": "Replace immediate-parent exclusion with ancestor traversal bounded by the call frame and an inclusive context-item source interval; retain diagnostic boundary assertions.",
  "action_ids": [
    "workflow:verified-history:ec6290f765c15f3fdc7283d4:probe",
    "workflow:verified-history:ec6290f765c15f3fdc7283d4:repair",
    "workflow:verified-history:ec6290f765c15f3fdc7283d4:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4676:repair:e4cd2ef1b016"],
  "required_effects": [
    {"key": "context-item-recognition-corrected", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "unmanaged-body-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-resource-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ec6290f765c15f3fdc7283d4:probe",
      "after": "workflow:verified-history:ec6290f765c15f3fdc7283d4:repair",
      "reason": "Locate the diagnostic owner and establish compatible AST ancestry, frame, and item-span semantics before editing.",
      "evidence_refs": ["pylint-dev/pylint:4676:body", "pylint-dev/pylint:4676:fix"]
    },
    {
      "before": "workflow:verified-history:ec6290f765c15f3fdc7283d4:repair",
      "after": "workflow:verified-history:ec6290f765c15f3fdc7283d4:validate",
      "reason": "Observe the changed checker against the public reproduction, new context-item assertions, and retained body-warning control.",
      "evidence_refs": ["pylint-dev/pylint:4676:fix", "pylint-dev/pylint:4676:regression"]
    }
  ]
}
```
