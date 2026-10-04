# Inspect overload classification

Resolve overload recognition, function-node-family policy, and public test owners. Compare synchronous and asynchronous overload sequences. Verify decorator identity before attributing warnings to a missing node class.

Run bound public probes without checkout edits. Unknown or contradictory results do not produce confirmed context.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-inspect",
  "intent": "Establish whether omitted asynchronous source-node classification causes overload false positives.",
  "mechanism": "Compare sync/async overload behavior and inspect the recognition node gate.",
  "semantic_role": "diagnose-classification-omission",
  "owner_role": "overload-recognition",
  "operation": "Locate current recognition, node-family, runtime-policy and test owners; read decorator resolution and run bound public probes without modifying checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "overload-review", "semantic_role": "overload-omission-context", "artifact_kind": "code-and-probe-record", "language": "python", "scope": "current-overload-classification", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-inspection-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-semantics-appropriate", "value": true, "evaluator": "evidence"},
    {"key": "runtime-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "confirm-overload-omission",
      "instruction": "Record current owner anchors, correct typing decorator resolution, sync acceptance, async failure, synchronous-only source-node gate, runtime-supported AST policy, existing coverage and unchanged checkout status. Emit confirmed context only if the node omission explains the contrast. An already async-aware gate or faulty decorator resolution blocks this repair.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:title", "PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/overload-inspect.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
