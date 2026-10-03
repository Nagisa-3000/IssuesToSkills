# Historical Workflow

Supply a comment-coordinate carrier for the diagnostic while retaining the existing annotation parsing path and semantic association. Discovery is a conditional current operation grounded in the report and diff, not an invented historical execution record.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e",
  "goal": "Report invalid type comments at their actual source line.",
  "mechanism": "Separate diagnostic-position identity from the associated statement AST identity.",
  "action_ids": [
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:locate",
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:repair",
    "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "required_effects": [
    {"key": "comment-syntax-error-location", "value": "actual-comment-line", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "comment-semantic-association", "value": "unchanged", "evaluator": "evidence"},
    {"key": "annotation-parsing-and-message-kind", "value": "unchanged", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:locate",
      "after": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:repair",
      "reason": "Establish that actual comment coordinates exist but an associated statement supplies the diagnostic position.",
      "evidence_refs": ["PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"]
    },
    {
      "before": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:repair",
      "after": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate",
      "reason": "The edited carrier and regression require fresh position and preservation checks.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"]
    }
  ]
}
```

Current ordering follows port compatibility, observed prerequisites, and verification dependencies. Already satisfied discovery may be omitted from a current task DAG, but validation remains after modification. Historical source and assertion details remain immutable.
