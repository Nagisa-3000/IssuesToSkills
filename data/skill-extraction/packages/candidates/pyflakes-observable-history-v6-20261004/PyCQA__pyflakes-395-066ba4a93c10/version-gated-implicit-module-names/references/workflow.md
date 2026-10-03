# Canonical Workflow

Recognize the supported implicit module name through a version-gated module registry, retaining existing compatibility behavior and a guarded regression assertion. The operation sequence is an evidence-grounded reconstruction, not an execution transcript.

```arex-workflow-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8",
  "goal": "Remove the supported-version false undefined-name warning for module-level __annotations__.",
  "mechanism": "Bind the module implicit-name and version-policy owners; conditionally register __annotations__ for Python 3.6 and later; add and publicly validate a version-guarded regression.",
  "action_ids": [
    "workflow:verified-history:4817630500584ee0981edde8:diagnose",
    "workflow:verified-history:4817630500584ee0981edde8:repair",
    "workflow:verified-history:4817630500584ee0981edde8:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "required_effects": [
    {"key": "supported-module-annotations-recognition", "value": true, "evaluator": "evidence"},
    {"key": "guarded-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "existing-magic-global-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "version-dependent-loop-types-preserved", "value": true, "evaluator": "evidence"},
    {"key": "pre36-registration-boundary-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:4817630500584ee0981edde8:diagnose",
      "after": "workflow:verified-history:4817630500584ee0981edde8:repair",
      "reason": "The version and scope policy must be located and shown compatible before changing implicit-name recognition.",
      "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix"]
    },
    {
      "before": "workflow:verified-history:4817630500584ee0981edde8:repair",
      "after": "workflow:verified-history:4817630500584ee0981edde8:validate",
      "reason": "Validation must inspect and exercise the resulting implementation and guarded regression, not stale pre-edit observations.",
      "evidence_refs": ["PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"]
    }
  ]
}
```
