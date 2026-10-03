# Canonical Workflow

The historical repair separated metadata from type expressions in the Python call visitor and added regression assertions. The ordering below expresses semantic prerequisites, not a claim about recorded interactive execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939",
  "goal": "Eliminate metadata-string false positives in nested typing calls without losing forward-reference checks.",
  "mechanism": "Partition call arguments by typing role and traverse each partition under the appropriate annotation state.",
  "action_ids": [
    "workflow:verified-history:3257ebe843a343f545c15939:probe",
    "workflow:verified-history:3257ebe843a343f545c15939:partition",
    "workflow:verified-history:3257ebe843a343f545c15939:regressions",
    "workflow:verified-history:3257ebe843a343f545c15939:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "required_effects": [
    {"key": "metadata-not-forward-references", "value": true, "evaluator": "evidence"},
    {"key": "true-type-forward-references-checked", "value": true, "evaluator": "evidence"},
    {"key": "public-regressions-validated", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "typing-name-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-call-analysis-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:3257ebe843a343f545c15939:probe",
      "after": "workflow:verified-history:3257ebe843a343f545c15939:partition",
      "reason": "Locate current typing recognition and annotation-state owners before modifying traversal.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix"]
    },
    {
      "before": "workflow:verified-history:3257ebe843a343f545c15939:partition",
      "after": "workflow:verified-history:3257ebe843a343f545c15939:regressions",
      "reason": "The regression-ready checkout includes the partitioned traversal and assertions for both argument roles.",
      "evidence_refs": ["PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"]
    },
    {
      "before": "workflow:verified-history:3257ebe843a343f545c15939:regressions",
      "after": "workflow:verified-history:3257ebe843a343f545c15939:validate",
      "reason": "Validate the final implementation and regression assertions together.",
      "evidence_refs": ["PyCQA/pyflakes:575:regression"]
    }
  ]
}
```
