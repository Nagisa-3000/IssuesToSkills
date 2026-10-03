# Inspect the use-metadata contract

Locate the annotation-read producer, downstream scope-sensitive consumer, and public diagnostic test harness. Review all current assignments and reads relevant to the use-state representation. Reproduce through the public checker interface when available.

Require evidence that the current mismatch is the same one described by the source. A boolean-indexing symptom alone is insufficient.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
  "intent": "Establish current applicability and owner bindings.",
  "mechanism": "Trace annotation-only read metadata to its scope-sensitive assignment consumer and inspect the public regression harness.",
  "semantic_role": "contract-inspection",
  "owner_role": "binding-use-analysis",
  "operation": "Inspect producers, consumers, annotation-mode guards, and diagnostic tests.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "inspected-contract", "semantic_role": "binding-use-contract", "artifact_kind": "analysis-record", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "inspected", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-contract-review", "value": "recorded", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-mismatch",
      "instruction": "Record current producer and consumer anchors, annotation-mode guard, test owner, and public reproduction result; establish whether a truthy boolean reaches an indexed metadata consumer.",
      "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:764:repair:e19886e58363"],
  "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:fix", "PyCQA/pyflakes:764:regression"],
  "read_set": ["role:binding-use-producer", "role:binding-use-consumer", "role:annotation-regression-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

An inspection record can conclude not applicable. The downstream edit prerequisites require positive current evidence, not merely the existence of this record.
