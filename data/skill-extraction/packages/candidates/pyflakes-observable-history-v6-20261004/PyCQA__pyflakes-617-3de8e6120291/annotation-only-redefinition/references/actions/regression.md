# Add an import/annotation/use regression

Use the current public test harness to assert no diagnostics for:

```python
from a import b, c
b: c
print(b)
```

The annotation type `c` is also imported and used in the annotation. Preserve the harness's version support; historically this syntax was guarded for Python 3.6 or later.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:regression",
  "intent": "Protect the reported import/annotation/use sequence with a public assertion.",
  "mechanism": "Add a no-diagnostic annotation regression using an imported value and imported annotation type.",
  "semantic_role": "annotation-redefinition-regression",
  "owner_role": "annotation-test-owner",
  "operation": "Add or confirm an equivalent public regression in the current annotation test harness; respect the checkout's supported syntax versions and retain existing tests.",
  "kind": "edit",
  "inputs": [
    {"name": "implementation", "semantic_role": "annotation-only-redefinition-implementation", "artifact_kind": "source-code", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "candidate", "optional": false}
  ],
  "outputs": [
    {"name": "regression", "semantic_role": "import-annotation-use-regression", "artifact_kind": "test-code", "language": "python", "scope": "current-checkout", "phase": "verification", "state": "ready", "optional": false}
  ],
  "preconditions": [
    {"key": "role:annotation-test-owner", "value": true, "evaluator": "file_exists"},
    {"key": "public-annotation-harness-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "import-annotation-use-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-definition-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-regression",
      "instruction": "Inspect the added assertion for an import, a value-free annotation using an imported type, and subsequent use; ensure it expects no diagnostics and does not suppress the analyzer.",
      "evidence_refs": ["PyCQA/pyflakes:617:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:annotation-test-owner"],
  "write_set": ["role:annotation-test-owner"],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7"
}
```

Test presence is not execution success. Retain [validation](validate.md).
