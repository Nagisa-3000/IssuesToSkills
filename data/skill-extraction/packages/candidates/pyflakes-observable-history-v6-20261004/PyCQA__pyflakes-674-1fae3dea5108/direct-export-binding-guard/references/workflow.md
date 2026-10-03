# Historical Workflow

Constrain specialized export dispatch using the stored name's immediate parent. Preserve ordinary classification for indirect targets and assert its unused-import behavior.

The public validation obligation below is an authored operational requirement. Its satisfaction in a current checkout must be observed; no historical test execution is inferred.

```arex-workflow-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "goal": "Prevent indirect module export targets from entering assignment-value analysis while preserving direct export and ordinary import behavior.",
  "mechanism": "Gate specialized dispatch on an immediate assignment-statement parent and add an indirect-target diagnostic regression.",
  "action_ids": [
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "required_effects": [
    {"key": "special-export-dispatch-direct-parent-only", "value": true, "evaluator": "evidence"},
    {"key": "indirect-export-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "direct-export-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
      "reason": "Confirm current parent semantics and consumer expectations before editing the dispatch boundary.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
      "reason": "This realization adds the boundary regression to the guarded candidate; the ordering is a port dependency, not a claimed historical execution sequence.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
      "reason": "The modified dispatch requires public crash and adjacent-behavior checks.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
      "reason": "Exercise the added assertion on the final candidate.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"]
    }
  ]
}
```
