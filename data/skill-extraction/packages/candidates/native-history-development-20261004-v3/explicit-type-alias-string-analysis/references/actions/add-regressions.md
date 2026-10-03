# Add regression assertions

Use the currently bound annotation test owner and public test conventions. Add or retain explicit assertions for:
1. module alias with unquoted imported type;
2. module alias with quoted imported type;
3. class alias with unquoted imported type;
4. class alias with quoted imported type;
5. marker annotation without a value;
6. no-value declaration plus an otherwise unused imported type.

The first five cases expect no diagnostics; the sixth expects the unrelated type's unused-import diagnostic. Historical assertions used `typing_extensions.TypeAlias` and `foo.Bar`. Adapt fixture names and version gating to current supported environments.

Preserve existing assertions. Presence of test code is not proof that tests ran. Retain [validation](validate-regressions.md).

```arex-contract-v4
{
  "id": "explicit-type-alias-string-analysis.tests",
  "intent": "Make the repaired alias behavior and no-value boundary observable.",
  "mechanism": "Add a quoted/unquoted module/class matrix and no-value diagnostic controls.",
  "semantic_role": "alias-regression-coverage",
  "owner_role": "annotation-regression-tests",
  "operation": "Add targeted assertions in the current public annotation regression suite.",
  "kind": "edit",
  "inputs": [
    {"name": "routed-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "value-routing-patched", "optional": false}
  ],
  "outputs": [
    {"name": "regression-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "regressions-present", "optional": false}
  ],
  "preconditions": [
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "value-routing-change-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "targeted-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-regression-assertions-retained", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-value-dispatch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-matrix",
      "instruction": "Inspect added or retained test assertions for all six cases and their expected diagnostic sets, confirm existing assertions remain, then execute the validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:671:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671"],
  "evidence_refs": ["PyCQA/pyflakes:671:regression"],
  "resource": "references/actions/add-regressions.md",
  "package_id": "explicit-type-alias-string-analysis",
  "read_set": ["role:annotation-regression-tests"],
  "write_set": ["role:annotation-regression-tests"],
  "invalidates": ["current-regression-results"]
}
```
