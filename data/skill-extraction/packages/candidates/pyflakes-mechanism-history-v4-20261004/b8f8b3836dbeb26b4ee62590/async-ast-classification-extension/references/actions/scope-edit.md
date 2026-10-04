# Extend scope classification and cover the collision

Use the bound registry's existing ordinary-function representation and current capability gate. Cover a module-level class and identically named annotated async parameter with a `None` return annotation and no expected diagnostics.

Do not modify parent traversal or diagnostic expectations. Existing equivalent coverage may satisfy the test effect without another test edit; performed modifications still retain validation.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit",
  "intent": "Restore missing asynchronous scope classification and reproducing coverage.",
  "mechanism": "Register asynchronous nodes with existing ordinary-function scope semantics under runtime capability policy.",
  "semantic_role": "extend-classification-and-cover",
  "owner_role": "ast-scope-classification",
  "operation": "Edit the bound scope registry and missing annotation coverage while retaining registry shape, capability gating, parent traversal, and existing diagnostic assertions.",
  "kind": "edit",
  "inputs": [
    {"name": "scope-review", "semantic_role": "scope-omission-context", "artifact_kind": "code-and-probe-record", "language": "python", "scope": "current-scope-classification", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "scope-change", "semantic_role": "scope-validation-target", "artifact_kind": "code-and-test-change", "language": "python", "scope": "current-scope-classification", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-semantics-appropriate", "value": true, "evaluator": "evidence"},
    {"key": "runtime-policy-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:ast-scope-classification", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "async-classification-extended", "value": true, "evaluator": "evidence"},
    {"key": "async-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-compatibility-preserved", "value": true, "evaluator": "evidence"},
    {"key": "downstream-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-scope-change",
      "instruction": "Review the actual diff for registration using the ordinary-function value representation and current capability gate. Inspect new or equivalent no-diagnostic class/parameter collision coverage with None return annotation. Confirm parent traversal and existing expectations are unchanged. Record the patch as unvalidated and retain scope-validate.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/scope-edit.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
