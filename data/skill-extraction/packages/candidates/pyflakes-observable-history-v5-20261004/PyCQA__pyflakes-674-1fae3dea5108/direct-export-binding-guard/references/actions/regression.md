# Add the indirect-target regression

Add a public diagnostic test containing an unused import and a one-element tuple-unpacking assignment to the special export name. Expect the unused-import diagnostic, not a special export result or a new invalid-assignment warning.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
  "intent": "Make non-crashing ordinary treatment of unpacked export names observable.",
  "mechanism": "Assert the diagnostic for an unused import when the export name is only indirectly assigned.",
  "semantic_role": "unpacking-regression-authoring",
  "owner_role": "python-export-diagnostic-tests",
  "operation": "Add a regression equivalent to import bar followed by (__all__,) = ('foo',), expecting the unused-import diagnostic.",
  "kind": "edit",
  "inputs": [
    {"name": "boundary", "semantic_role": "export-binding-boundary", "artifact_kind": "review", "language": "python", "scope": "current-checkout", "phase": "inspection", "state": "established"}
  ],
  "outputs": [
    {"name": "regression-tests", "semantic_role": "export-diagnostic-regressions", "artifact_kind": "tests", "language": "python", "scope": "current-checkout", "phase": "candidate", "state": "modified"}
  ],
  "preconditions": [
    {"key": "role:python-export-diagnostic-tests", "value": true, "evaluator": "file_exists"},
    {"key": "unused-import-oracle-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "unpacking-regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-export-test-assertions", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "regression-assertion-review",
      "instruction": "Inspect the new public test for a tuple-unpacked export target and an explicit unused-import expectation; ensure the harness treats internal errors as failures.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "read_set": ["role:python-export-diagnostic-tests"],
  "write_set": ["role:python-export-diagnostic-tests"],
  "invalidates": ["export-diagnostic-suite-results"]
}
```

The historical assertion is authoritative; its presence does not imply it has run in the current checkout.
