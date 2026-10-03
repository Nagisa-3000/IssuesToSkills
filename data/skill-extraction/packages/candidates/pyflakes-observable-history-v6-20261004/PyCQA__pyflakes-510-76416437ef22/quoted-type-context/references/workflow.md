# Historical Workflow: recognized quoted type contexts

The diagnosis identifies missed annotation entry points. The repair adds scoped context entry and typing-member recognition. Public regression validation follows the edit. Current execution may omit already satisfied diagnosis work only when its facts and bindings remain current.

```arex-workflow-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e",
  "goal": "Count names in quoted typing expressions without interpreting ordinary runtime strings as annotations.",
  "mechanism": "Recognize typing constructs and enter existing annotation traversal at type-bearing AST positions with restoration of annotation state.",
  "action_ids": [
    "workflow:verified-history:3f957b40be188975fdc11a7e:locate",
    "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
    "workflow:verified-history:3f957b40be188975fdc11a7e:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "required_effects": [
    {"key": "quoted-type-name-use", "value": "recognized", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "runtime-string-semantics", "value": "preserved", "evaluator": "evidence"},
    {"key": "annotation-state-restoration", "value": "preserved", "evaluator": "evidence"},
    {"key": "typing-literal-semantics", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:3f957b40be188975fdc11a7e:locate",
      "after": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
      "reason": "Identify recognized typing positions and existing annotation machinery before changing traversal.",
      "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"]
    },
    {
      "before": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
      "after": "workflow:verified-history:3f957b40be188975fdc11a7e:validate",
      "reason": "Check repaired quoted contexts and adjacent runtime strings against public assertions after modifying traversal.",
      "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"]
    }
  ]
}
```
