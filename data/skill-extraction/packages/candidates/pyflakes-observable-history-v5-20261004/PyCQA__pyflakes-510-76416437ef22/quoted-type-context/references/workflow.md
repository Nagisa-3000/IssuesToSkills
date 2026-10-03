# Workflow: recognize quoted type expressions at typing boundaries

This canonical Workflow captures a supported repair mechanism. Current task graphs may omit editing when already satisfied, but any performed modification must retain validation. The listed effects are targets, not observations from the current checkout.

```arex-workflow-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e",
  "goal": "Avoid false unused-import diagnostics for names referenced by supported quoted typing expressions without treating value strings as annotations.",
  "mechanism": "Recognize typing constructs, enter a restoring annotation context only at supported type-bearing boundaries, and preserve normal traversal elsewhere.",
  "action_ids": [
    "workflow:verified-history:3f957b40be188975fdc11a7e:inspect",
    "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
    "workflow:verified-history:3f957b40be188975fdc11a7e:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "required_effects": [
    {
      "key": "quoted-type-names-count-as-used",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "ordinary-value-strings-not-type-parsed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-context-restored",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "literal-special-handling-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "genuine-undefined-name-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:3f957b40be188975fdc11a7e:inspect",
      "after": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
      "reason": "Bind and inspect the current annotation traversal owner before changing typing-boundary behavior.",
      "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"]
    },
    {
      "before": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
      "after": "workflow:verified-history:3f957b40be188975fdc11a7e:validate",
      "reason": "The changed interpretation of strings requires positive type-use checks and negative ordinary-value checks on the modified code.",
      "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"]
    }
  ]
}
```

Operations: [inspect](actions/inspect.md), [repair](actions/repair.md), [validate](actions/validate.md).
