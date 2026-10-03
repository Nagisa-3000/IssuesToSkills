# Historical realization

```arex-workflow-v4
{
  "id": "workflow:a",
  "goal": "Repair type-only diagnostic while preserving runtime behavior",
  "mechanism": "Preserve runtime diagnostics while narrowing type-only context",
  "action_ids": [
    "detect:a",
    "guard:a",
    "validate:a"
  ],
  "source_ids": [
    "source:a"
  ],
  "required_effects": [
    {
      "key": "diagnostic_fixed",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    },
    {
      "key": "validated",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "invariants": [
    {
      "key": "runtime_preserved",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "dependencies": []
}
```
