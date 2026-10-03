# Route recognized alias values through annotation analysis

Edit only the currently bound semantic owners.

Preserve target processing and processing of the declared annotation. If an annotated assignment has a value and its annotation is recognized as the typing `TypeAlias` marker, process that value with the existing annotation handler. Otherwise retain normal expression traversal. Keep the missing-value guard.

Add regression assertions for direct and string alias values in module and class scopes, plus valueless declarations with and without an unused imported name. Use the current repository's test harness. The supplied historical tests used `typing_extensions.TypeAlias`; do not claim broader marker-recognition coverage without current evidence.

The output is an edited candidate, not a verified repair. This Action invalidates validation freshness, not required behavior assurances.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:edit",
  "intent": "Correct explicit alias value classification and encode the evidenced regression boundaries.",
  "mechanism": "Conditionally dispatch a value to annotation analysis using the existing typing-marker recognizer.",
  "semantic_role": "alias-value-dispatch-repair",
  "owner_role": "annotated-assignment-analysis",
  "operation": "Modify the bound annotated-assignment visitor and annotation regression tests; preserve target and annotation handling, ordinary value traversal, and the no-value guard.",
  "kind": "edit",
  "inputs": [
    {
      "name": "checked-alias-dispatch",
      "semantic_role": "alias-dispatch-review",
      "artifact_kind": "code-and-probe-record",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "pre-edit",
      "state": "compatible-and-defect-observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "alias-dispatch-candidate",
      "semantic_role": "alias-dispatch-change",
      "artifact_kind": "implementation-and-regression-diff",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "compatible-alias-dispatch-owner-observed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:annotated-assignment-analysis",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-analysis",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:typing-marker-recognition",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-regression-tests",
      "value": true,
      "evaluator": "file_exists"
    }
  ],
  "effects": [
    {
      "key": "recognized-alias-value-annotation-dispatch",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "alias-regression-assertions-added",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-assignment-value-semantics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "valueless-assignment-use-accounting-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "existing-annotation-analysis-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-conditional-dispatch",
      "instruction": "Review the current diff for recognition-gated annotation dispatch, unchanged ordinary traversal, unchanged no-value behavior, and regression assertions matching module/class and direct/string cases. Test execution is required by the separate validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671:repair:84da8cdaad57"],
  "evidence_refs": ["PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "read_set": [
    "role:annotated-assignment-analysis",
    "role:annotation-analysis",
    "role:typing-marker-recognition",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:annotated-assignment-analysis",
    "role:annotation-regression-tests"
  ],
  "invalidates": ["public-validation-observed", "baseline-diagnostics-current"]
}
```
