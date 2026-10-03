# Probe the omission

Read current code and run a bound public reproduction without changing tracked files. Locate both owners and record hashed anchors, runtime support, and diagnostic output. An already-correct positional-only traversal or another causal mechanism rejects the repair. Outputs below are conditional expectations, not supplied observations.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:probe",
  "intent": "Determine whether omitted positional-only argument collection causes the false diagnostic.",
  "mechanism": "Compare a public positional-only annotation reproduction with the current function-argument collector.",
  "semantic_role": "omission-diagnosis",
  "owner_role": "function-argument-collector",
  "operation": "Inspect current collector and test owners, establish AST support, and execute a bound public reproduction without editing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosed-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "diagnosis",
      "state": "omission-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "collector-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "positional-only-ast-support-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:function-argument-collector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-test-suite", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "confirm-current-omission",
      "instruction": "Record public diagnostic output, current collector anchors, both owner bindings, and AST support evidence. Establish that the positional-only annotation is omitted rather than mishandled by another mechanism. Verify tracked files were not changed.",
      "evidence_refs": ["PyCQA/pyflakes:507:body", "PyCQA/pyflakes:507:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:507:repair:be8803601900"],
  "evidence_refs": ["PyCQA/pyflakes:507:title", "PyCQA/pyflakes:507:body", "PyCQA/pyflakes:507:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": ["role:function-argument-collector", "role:annotation-test-suite"],
  "write_set": [],
  "exclusions": [
    {"key": "positional-only-accounting-already-correct", "value": true, "evaluator": "evidence"},
    {"key": "different-cause-confirmed", "value": true, "evaluator": "evidence"}
  ]
}
```
