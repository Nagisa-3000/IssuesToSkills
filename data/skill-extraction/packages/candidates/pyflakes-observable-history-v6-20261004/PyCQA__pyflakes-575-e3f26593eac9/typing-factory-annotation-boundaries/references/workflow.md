# Canonical Workflow: partition typing-factory annotation traversal

This Workflow reconstructs the supported repair mechanism. Read/probe and validation operations express how to establish current applicability and test the repair; they do not invent historical command executions.

```arex-workflow-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939",
  "goal": "Eliminate false undefined-name diagnostics for typing-factory metadata while retaining analysis of actual type expressions.",
  "mechanism": "Classify recognized typing-factory call components and traverse metadata outside annotation context while traversing type-bearing expressions inside it.",
  "action_ids": [
    "workflow:verified-history:3257ebe843a343f545c15939:inspect",
    "workflow:verified-history:3257ebe843a343f545c15939:partition",
    "workflow:verified-history:3257ebe843a343f545c15939:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "required_effects": [
    {"key": "factory-metadata-not-forward-references", "value": true, "evaluator": "evidence"},
    {"key": "type-bearing-expressions-analyzed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "genuine-forward-reference-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-call-traversal-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-adjacent-typing-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:3257ebe843a343f545c15939:inspect",
      "after": "workflow:verified-history:3257ebe843a343f545c15939:partition",
      "reason": "The partition requires current identification of recognized factories, annotation state, and type-bearing versus metadata components.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix"]
    },
    {
      "before": "workflow:verified-history:3257ebe843a343f545c15939:partition",
      "after": "workflow:verified-history:3257ebe843a343f545c15939:validate",
      "reason": "The modified traversal and regression assertions require fresh verification of both false-positive removal and genuine type-reference diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"]
    }
  ]
}
```

Current plans may omit the edit when public evidence shows that the required behavior is already satisfied. They must not drop validation of an edit that is actually performed. Port compatibility, current prerequisites, and current verification determine execution order.
