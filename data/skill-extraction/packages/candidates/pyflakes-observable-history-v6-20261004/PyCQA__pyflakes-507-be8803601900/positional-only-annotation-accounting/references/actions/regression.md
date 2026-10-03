# Add a focused public assertion

Use the bound annotation harness to assert no diagnostic for an import referenced only by a positional-only parameter annotation. Preserve neighboring assertions. Gate syntax-bearing source appropriately if supported runtimes lack this syntax.

If an equivalent assertion already exists, a current plan may treat this operation as satisfied after inspection. Any collector edit still requires validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:regression",
  "intent": "Protect positional-only annotation reference accounting against regression.",
  "mechanism": "Add a no-diagnostic assertion for an imported name used only in a positional-only parameter annotation.",
  "semantic_role": "focused-regression",
  "owner_role": "annotation-test-suite",
  "operation": "Edit the bound public annotation suite with the focused assertion and any runtime gate required by current support policy.",
  "kind": "edit",
  "inputs": [
    {
      "name": "implementation-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "implementation",
      "state": "collector-edited-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "test-ready-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "regression",
      "state": "assertion-present-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:annotation-test-suite", "value": true, "evaluator": "file_exists"},
    {"key": "current-runtime-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "focused-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "parameter-binding-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-focused-assertion",
      "instruction": "Confirm that the public test uses the imported name only in a positional-only annotation, asserts no diagnostic, preserves neighboring assertions, and handles unsupported runtimes according to current policy.",
      "evidence_refs": ["PyCQA/pyflakes:507:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:507:repair:be8803601900"],
  "evidence_refs": ["PyCQA/pyflakes:507:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": ["role:annotation-test-suite"],
  "write_set": ["role:annotation-test-suite"],
  "invalidates": ["public-validation-fresh"]
}
```
