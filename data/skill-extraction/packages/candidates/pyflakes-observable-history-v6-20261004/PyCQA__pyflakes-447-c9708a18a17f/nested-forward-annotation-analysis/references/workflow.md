# Historical Workflow: context-aware nested annotation traversal

The implementation and regression assertions support the dependency sequence below. Action outputs and effects are expected contracts, not observed current execution results.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0",
  "goal": "Resolve imported names inside nested quoted Python type annotations without interpreting Literal string values as type expressions.",
  "mechanism": "Track annotation and Literal context, parse annotation strings through existing name analysis, and respect whether deferred processing is already running.",
  "action_ids": [
    "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:probe",
    "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:edit",
    "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "required_effects": [
    {"key": "nested-annotation-references-recognized", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "runtime-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "literal-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "existing-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "analysis-phase-integrity-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:probe",
      "after": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:edit",
      "reason": "Establish the nested annotation failure and bind annotation, string, typing-recognition, and deferred-analysis owners before modifying them.",
      "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix"]
    },
    {
      "before": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:edit",
      "after": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:validate",
      "reason": "The candidate must be checked for nested-reference recognition and adjacent Literal, overload, and deferred behavior.",
      "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"]
    }
  ]
}
```
