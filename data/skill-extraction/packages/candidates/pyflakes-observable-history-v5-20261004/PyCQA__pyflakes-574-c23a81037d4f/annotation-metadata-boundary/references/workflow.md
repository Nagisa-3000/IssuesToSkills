# Historical Workflow

This is a sourced reconstruction of the repair mechanism and its regression assertions, not a historical execution transcript.

```arex-workflow-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6",
  "goal": "Prevent Annotated metadata strings from being interpreted as forward types while preserving type and expression analysis.",
  "mechanism": "Partition arguments by position and temporarily leave annotation state for metadata traversal.",
  "action_ids": [
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "required_effects": [
    {"key": "metadata-string-forward-parsing", "value": false, "evaluator": "evidence"},
    {"key": "repair-public-validation", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "first-argument-type-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "metadata-expression-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "surrounding-annotation-state", "value": "preserved", "evaluator": "evidence"},
    {"key": "literal-handling", "value": "preserved", "evaluator": "evidence"},
    {"key": "target-context-and-fallback-traversal", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
      "after": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
      "reason": "Locate the context boundary, recognition semantics and slice representations before editing.",
      "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix"]
    },
    {
      "before": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
      "after": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate",
      "reason": "The traversal change requires target and preserved-behavior checks after modification.",
      "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"]
    }
  ]
}
```

Resources: [inspect](actions/inspect.md), [repair](actions/repair.md), [validate](actions/validate.md).

All packaged Actions belong to this canonical Workflow. Current ordering follows observed ports, prerequisites, dependencies, and verification needs rather than list position alone. Already satisfied operations may be omitted only with current supporting observations.
