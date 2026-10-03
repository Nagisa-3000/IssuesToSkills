# Add indirect-target regression coverage

Use the current public diagnostic harness. Add an unused import followed by tuple-target `__all__` assignment, asserting the unused-import diagnostic. The analyzer must not treat this target as a direct export declaration.

This tests static analysis, not runtime unpacking validity. Do not replace diagnostic assertions with exception tolerance.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
  "intent": "Protect ordinary unused-import behavior for indirect __all__ targets.",
  "mechanism": "Add an indirect-target diagnostic assertion using the public test harness.",
  "semantic_role": "indirect-target-regression",
  "owner_role": "export-binding-tests",
  "operation": "Add a public test equivalent to import bar followed by (__all__,) = (\"foo\",), asserting the unused-import diagnostic without accepting an analyzer exception.",
  "kind": "edit",
  "inputs": [
    {"name": "guarded-candidate", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "guarded"}
  ],
  "outputs": [
    {"name": "covered-candidate", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "covered"}
  ],
  "preconditions": [
    {"key": "special-export-dispatch-direct-parent-only", "value": true, "evaluator": "evidence"},
    {"key": "current-diagnostic-harness-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:export-binding-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "indirect-export-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-export-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-indirect-regression",
      "instruction": "Inspect the added test for the unused import, indirect tuple target and unused-import assertion. Confirm that exceptions and missing diagnostics are not accepted.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:regression"],
  "read_set": ["role:export-binding-tests"],
  "write_set": ["role:export-binding-tests"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d"
}
```
