# Workflow: recognize helpers through imported origin

This reconstructs the supplied implementation and regression mechanism. Dependencies reflect semantic requirements and the declared snapshot ports, not a recorded historical execution sequence.

```arex-workflow-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055",
  "goal": "Recognize module-qualified typing helpers through the nearest imported binding rather than receiver spelling.",
  "mechanism": "Search inner-to-outer scopes, stop at the first receiver binding, require a supported typing-module import origin, and retain existing helper-name filtering.",
  "action_ids": [
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:probe",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:regression",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "required_effects": [
    {"key": "module-helper-origin-resolution", "value": "nearest-supported-import", "evaluator": "evidence"},
    {"key": "alias-overload-regression", "value": "present", "evaluator": "evidence"},
    {"key": "current-public-validation", "value": "pass", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "nearest-binding-controls-recognition", "value": true, "evaluator": "evidence"},
    {"key": "direct-name-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "helper-name-predicate-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-bindings-not-typing", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:probe",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
      "reason": "Locate the current owner and establish compatible scope and import-origin metadata before editing.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix"]
    },
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:regression",
      "reason": "The declared regression input consumes the production-edited snapshot. This is an authored port dependency, not evidence of historical ordering.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"]
    },
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate",
      "reason": "Validate the production modification and its preserved branches.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix"]
    },
    {
      "before": "workflow:verified-history:2f5b3f202404ca13ec4e8055:regression",
      "after": "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate",
      "reason": "The regression must exist before its public execution can validate the edits.",
      "evidence_refs": ["PyCQA/pyflakes:561:regression"]
    }
  ]
}
```

Current DAGs may omit already satisfied operations only when current evidence and compatible port bindings establish their state. Do not infer success from the historical source.
