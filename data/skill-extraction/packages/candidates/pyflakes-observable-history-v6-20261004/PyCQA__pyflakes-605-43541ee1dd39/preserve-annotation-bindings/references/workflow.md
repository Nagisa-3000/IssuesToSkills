# Workflow: preserve bindings during annotation-only updates

Inspect the binding insertion semantics before editing. The guard and regression assertion both depend on that inspection. Validation follows both edits; their relative edit order is not a semantic requirement.

```arex-workflow-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "goal": "Prevent an annotation-only binding from replacing an existing scope binding and losing export-use information.",
  "mechanism": "Allow scope insertion when the name is absent or the incoming binding is not annotation-only.",
  "action_ids": [
    "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
    "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
    "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
    "workflow:verified-history:eedcc58f60ba24cb02758489:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "required_effects": [
    {"key": "annotation-replacement-guard-present", "value": true, "evaluator": "evidence"},
    {"key": "export-annotation-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-rebinding-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotation-insertion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-expression-use-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
      "reason": "Identify the shared scope updater and annotation-only classification before guarding replacement.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
      "reason": "Bind the public reproduction and current annotation test owner before adding an assertion.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
      "reason": "Observe behavior after modifying the binding update.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"]
    },
    {
      "before": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
      "after": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
      "reason": "Run the regression assertion after it is added.",
      "evidence_refs": ["PyCQA/pyflakes:605:regression"]
    }
  ]
}
```

All assurance predicates require current evidence-backed review or public probes. Matching predicate names does not prove them. Structural compatibility does not establish repair success.
