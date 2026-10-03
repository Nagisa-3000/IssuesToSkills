# Historical workflow

The historical mechanism replaces the diagnostic position carrier, not the semantic association of the comment. The probe is a current applicability gate derived from the report and repair; no historical investigation execution is claimed.

Effects and outputs below are requirements for a successful current realization, not observed current results.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e",
  "goal": "Report malformed type comments at their own source location without changing semantic association or adjacent annotation behavior.",
  "mechanism": "Pass a lightweight comment-coordinate carrier instead of an associated AST node as the diagnostic-position argument to the separately parsed annotation handler.",
  "action_ids": [
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:probe",
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:edit",
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "required_effects": [
    {"key": "comment-location-reporting", "value": "corrected", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "semantic-comment-association-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:probe",
      "after": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:edit",
      "reason": "Confirm available comment coordinates, the mismatched position carrier, and consumer compatibility before editing.",
      "evidence_refs": ["PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"]
    },
    {
      "before": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:edit",
      "after": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate",
      "reason": "Observe the corrected diagnostic and adjacent behavior after modifying source and regression tests.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"]
    }
  ]
}
```
