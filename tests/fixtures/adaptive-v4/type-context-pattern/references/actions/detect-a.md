# Identify current type-only context

```arex-contract-v4
{
  "mechanism": "Preserve runtime diagnostics while narrowing type-only context",
  "source_ids": [
    "source:a"
  ],
  "evidence_refs": [
    "evidence:a"
  ],
  "package_id": "pattern:type-context",
  "preserves": [
    {
      "key": "runtime_preserved",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "oracle": [
    {
      "id": "oracle:a",
      "instruction": "Run public type-only and runtime boundary cases.",
      "evidence_refs": [
        "evidence:a"
      ],
      "kind": "repository_test",
      "command": [
        "python",
        "checker.py"
      ]
    }
  ],
  "id": "detect:a",
  "intent": "Identify current type-only context",
  "semantic_role": "detect_context",
  "owner_role": "context_owner",
  "kind": "read",
  "operation": "Inspect the current context producer and distinguish static usage from runtime availability.",
  "inputs": [],
  "outputs": [
    {
      "name": "context",
      "semantic_role": "type_context",
      "artifact_kind": "ContextFacts",
      "language": "Python",
      "scope": "module",
      "phase": "static",
      "state": "resolved",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "context_known",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "read_set": [
    "context_owner"
  ],
  "resource": "references/actions/detect-a.md"
}
```
