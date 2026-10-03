# Workflow: recognize assignments hidden by definitions

The historical change establishes a directional mechanism: preserve existing definition-redefinition rules, then recognize an assignment when the names match. Its regression asserts that an unused assignment followed by a function definition yields the existing diagnostic.

Current execution requires inspection before mutation and explicit validation afterward. This is a supported reconstruction of the repair mechanism, not an execution transcript.

```arex-workflow-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf",
  "goal": "Restore the existing unused-redefinition diagnostic for a same-name definition that overwrites an assignment.",
  "mechanism": "Extend the definition binding's redefinition predicate with a same-name Assignment branch while retaining its inherited predicate, and assert the assignment-to-function case.",
  "action_ids": [
    "workflow:verified-history:ee79eebf2283561900232caf:inspect",
    "workflow:verified-history:ee79eebf2283561900232caf:repair",
    "workflow:verified-history:ee79eebf2283561900232caf:validate"
  ],
  "source_ids": [
    "PyCQA/pyflakes:760:repair:e9324649874a"
  ],
  "required_effects": [
    {
      "key": "definition-recognizes-same-name-assignment",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "assignment-function-regression-asserted",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-validation",
      "value": "passed",
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "inherited-redefinition-rule",
      "value": "preserved",
      "evaluator": "evidence"
    },
    {
      "key": "ordinary-assignment-rebinding-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    },
    {
      "key": "existing-unused-scope-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:ee79eebf2283561900232caf:inspect",
      "after": "workflow:verified-history:ee79eebf2283561900232caf:repair",
      "reason": "The reported collision must map to a definition-side predicate and an assignment binding before this implementation mechanism is applicable.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:body",
        "PyCQA/pyflakes:760:fix"
      ]
    },
    {
      "before": "workflow:verified-history:ee79eebf2283561900232caf:repair",
      "after": "workflow:verified-history:ee79eebf2283561900232caf:validate",
      "reason": "The changed predicate and newly added regression must be checked after modification; pre-edit observations do not validate the candidate.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:fix",
        "PyCQA/pyflakes:760:regression"
      ]
    }
  ]
}
```

Operations: [inspect](actions/inspect.md), [repair](actions/repair.md), [validate](actions/validate.md).

All outputs and effects in these contracts are expected states. Only current recorded probes can establish that an effect has been observed.
