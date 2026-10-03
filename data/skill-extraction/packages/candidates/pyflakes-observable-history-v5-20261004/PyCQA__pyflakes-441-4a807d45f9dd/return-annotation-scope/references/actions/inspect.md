# Inspect annotation traversal and scope

Locate the current function-definition traversal owner, inspect scope entry and annotation handling, and reproduce the public symptom. Record concrete bindings and fresh observations. Do not infer a compatible scope model solely from a similar diagnostic.

The output is a current review artifact, not a historical execution result.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
  "intent": "Determine whether the reported return-annotation diagnostic comes from an inappropriate function-scope traversal.",
  "mechanism": "Inspect annotation-processing phases and compare the two public scope-boundary scenarios.",
  "semantic_role": "establish-annotation-traversal-applicability",
  "owner_role": "function-definition-traversal",
  "operation": "Locate and review the traversal owner, scope entry, retained annotation pass, and public regression bindings.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "traversal-applicability-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-scope-boundary",
      "instruction": "Record current code anchors showing scope entry, the inner return-annotation visit, and a retained enclosing-context annotation pass; record public reproductions and regression-runner bindings.",
      "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:function-definition-traversal", "role:annotation-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

If the correct earlier annotation pass cannot be established, mark applicability UNKNOWN or FAIL and do not edit. Empty command arrays require current public bindings; they are not executable test commands.
