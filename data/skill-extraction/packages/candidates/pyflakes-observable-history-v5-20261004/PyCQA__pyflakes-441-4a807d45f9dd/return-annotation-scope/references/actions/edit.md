# Exclude return annotations from inner traversal

At the bound function-definition traversal owner, exclude the return-annotation child from traversal after function scope entry. Retain the existing decorator exclusion and the correct annotation-processing pass.

The historical implementation changed a scalar omission to a list containing both `decorator_list` and `returns`. Use that exact form only if the current traversal API supports it; otherwise stop rather than invent an unsupported adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:edit",
  "intent": "Prevent return annotations from being revisited in the function-body scope.",
  "mechanism": "Add the return-annotation child to the inner traversal's omission set without removing its existing decorator omission.",
  "semantic_role": "repair-annotation-scope-boundary",
  "owner_role": "function-definition-traversal",
  "operation": "Modify the bound function-child traversal omission set after function scope entry.",
  "kind": "edit",
  "inputs": [
    {
      "name": "scope-review",
      "semantic_role": "annotation-scope-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "function-definition-traversal",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "traversal-patch",
      "semantic_role": "annotation-traversal-change",
      "artifact_kind": "source-change",
      "language": "python",
      "scope": "function-definition-traversal",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:function-definition-traversal", "value": true, "evaluator": "symbol_exists"},
    {"key": "wrong-scope-return-visit-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "correct-annotation-pass-retained", "value": true, "evaluator": "evidence"},
    {"key": "omission-api-supports-multiple-children", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "return-child-excluded-from-inner-traversal", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "decorator-inner-traversal-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "return-annotations-still-analyzed", "value": true, "evaluator": "evidence"},
    {"key": "body-only-return-name-rejected", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-diff",
      "instruction": "Inspect the current diff to confirm that only the inner traversal omission changes, the decorator exclusion remains, and the correct annotation pass is not removed.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:function-definition-traversal"],
  "write_set": ["role:function-definition-traversal"],
  "invalidates": ["annotation-diagnostics", "annotation-regression-results"],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

Effects and preservation requirements are expected obligations until current inspection and validation provide observations. This Action alone does not establish repair success.
