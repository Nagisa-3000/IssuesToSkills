# Partition call traversal by argument role

Modify the current Python typing-call visitor and annotation-state owner, not a hard-coded historical path.

The evidenced implementation uses explicit collections for omitted child fields, annotated nodes, and non-annotated traversal. Its distinctions are:

- `TypedDict`: for a literal dictionary second argument, dictionary values are types; its keys and other arguments are metadata/non-annotation traversal. Keyword values are treated as types.
- `NamedTuple`: recognize a list or tuple of two-element list/tuple pairs; each pair's second element is a type and first element is a label. Keyword values are treated as types.
- `TypeVar`: arguments after the first and the `bound` keyword value are type expressions; other keyword values retain non-annotation traversal.
- `cast`: the first argument enters annotation context whenever present, rather than only when it is a string.

The historical `cast` branch does not use the omission partition and still falls through to ordinary child handling. Do not claim the historical diff globally visits every node exactly once. For partitioned branches, omission must prevent accidental re-analysis of metadata as annotations and avoid duplicating selected type traversal.

Retain typing-aware resolution and ordinary fallback traversal. Do not blindly extend these historical keyword classifications to new current APIs whose keyword semantics differ; establish those semantics first or stop.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:partition",
  "intent": "Separate metadata traversal from annotation traversal in recognized typing calls.",
  "mechanism": "Select actual type nodes, omit their automatic child paths, traverse metadata with annotation state disabled, then traverse selected types in annotation context.",
  "semantic_role": "repair-traversal",
  "owner_role": "python-annotation-call-analysis",
  "operation": "Edit call dispatch and annotation-context traversal to implement the evidenced role partition.",
  "kind": "edit",
  "inputs": [
    {
      "name": "located-checkout",
      "semantic_role": "annotation-traversal-checkout",
      "artifact_kind": "source-checkout",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "repair",
      "state": "located-and-applicability-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "partitioned-checkout",
      "semantic_role": "annotation-traversal-checkout",
      "artifact_kind": "source-checkout",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "repair",
      "state": "partition-implemented-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "owner-exists", "value": true, "evaluator": "symbol_exists", "description": "role:python-annotation-call-analysis"},
    {"key": "argument-role-misclassification-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "typing-call-semantics-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "role-partition-implemented", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "typing-name-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-call-analysis-preserved", "value": true, "evaluator": "evidence"},
    {"key": "true-type-forward-references-checked", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-role-partition",
      "instruction": "Review current changed traversal against argument roles: factory names and labels are non-annotations; supported type positions remain annotations; ordinary dispatch remains intact. Execution validation is retained by the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:575:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:fix"],
  "resource": "references/actions/partition.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939",
  "read_set": ["role:python-typing-name-resolution", "role:python-annotation-call-analysis"],
  "write_set": ["role:python-annotation-call-analysis"],
  "invalidates": ["current-traversal-behavior", "current-diagnostic-results", "current-import-usage-results"]
}
```

`role:python-annotation-call-analysis` is the symbol owner to resolve in the current checkout. All preservation predicates require review or probes; they are not established by their names.
