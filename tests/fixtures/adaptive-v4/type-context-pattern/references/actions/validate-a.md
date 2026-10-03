# Check repaired and neighboring behavior

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
  "id": "validate:a",
  "intent": "Check repaired and neighboring behavior",
  "semantic_role": "verify_behavior",
  "owner_role": "diagnostic_owner",
  "kind": "validate",
  "operation": "Run the public MRE and a runtime diagnostic that must remain active.",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {
      "key": "diagnostic_fixed",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "effects": [
    {
      "key": "validated",
      "value": true,
      "evaluator": "evidence",
      "description": ""
    }
  ],
  "validation_for": [
    "guard:a"
  ],
  "read_set": [
    "diagnostic_owner"
  ],
  "resource": "references/actions/validate-a.md"
}
```
