# Historical workflow

The following contracts express the supplied repair mechanism and its semantic verification dependencies, not a recorded historical task trace.

```arex-workflow-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "goal": "Preserve existing bindings against annotation-only replacement without suppressing real assignments.",
  "mechanism": "Guard current-scope insertion by name absence or a non-Annotation incoming binding, and assert that assigned exports retain import usage credit.",
  "action_ids": [
    "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
    "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
    "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
    "workflow:verified-history:eedcc58f60ba24cb02758489:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "required_effects": [
    {"key": "annotation-preserves-existing-binding", "value": true, "evaluator": "evidence"},
    {"key": "export-annotation-regression-covered", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation-passes", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-bindings-still-replace", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotations-still-insert", "value": true, "evaluator": "evidence"},
    {"key": "existing-usage-propagation-retained", "value": true, "evaluator": "evidence"},
    {"key": "scope-selection-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
      "reason": "Locate insertion and confirm annotation-only classification and overwrite before changing binding semantics.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
      "reason": "Bind the public reproduction and current annotation test owner before adding the assertion.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
      "reason": "Validation must observe edited insertion behavior and preserved cases.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
      "reason": "Validation must include the new export/annotation assertion.",
      "evidence_refs": ["PyCQA/pyflakes:605:regression"]
    }
  ]
}
```

There is no required ordering between the two edits. Current ordering follows bound ports and semantic prerequisites, not list position.
