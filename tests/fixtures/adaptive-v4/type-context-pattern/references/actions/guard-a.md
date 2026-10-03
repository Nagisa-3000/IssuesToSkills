# Narrow the actual diagnostic guard

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
  "id": "guard:a",
  "intent": "Narrow the actual diagnostic guard",
  "semantic_role": "narrow_guard",
  "owner_role": "diagnostic_owner",
  "kind": "edit",
  "operation": "At the current diagnostic owner, exempt only type-only usage; preserve runtime checking.",
  "inputs": [
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
  "outputs": [],
  "preconditions": [
    {
      "key": "context_known",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "effects": [
    {
      "key": "diagnostic_fixed",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "write_set": [
    "diagnostic_owner"
  ],
  "resource": "references/actions/guard-a.md"
}
```
