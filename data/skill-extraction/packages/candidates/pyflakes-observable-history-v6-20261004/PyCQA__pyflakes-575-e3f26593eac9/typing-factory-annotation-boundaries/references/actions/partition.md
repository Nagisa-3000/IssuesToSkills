# Partition traversal and add public regression assertions

Apply this operation only after the current review establishes the supported mechanism.

Use the current traversal API to separate type-bearing nodes from ordinary components. Traverse the latter with annotation interpretation disabled; traverse the former with annotation handling enabled. Avoid accidental omission or duplicate diagnostics, and keep unsupported AST shapes on the appropriate ordinary fallback.

Supported historical distinctions:

- `TypedDict`: dictionary field values and functional keyword values are type-bearing; factory names and dictionary keys are metadata.
- `NamedTuple`: in a structurally valid tuple/list of two-element fields, the second element is type-bearing and the first is a label; functional keyword values are type-bearing.
- `TypeVar`: positional constraints after the name and the `bound` value are type-bearing; the name and other keyword expressions are not promoted to annotations.
- `cast`: its first argument is type-bearing even when it is not a bare string.

Add public regression assertions for false positives and genuine unresolved references. These are expected repair outcomes until validation observes them.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:partition",
  "intent": "Correct annotation-context boundaries for recognized typing-factory calls.",
  "mechanism": "Partition traversal into ordinary metadata and annotated type-bearing expressions, with guarded AST-shape handling and regression assertions.",
  "semantic_role": "boundary-repair",
  "owner_role": "typing-call-traversal-owner",
  "operation": "Modify the current typing call traversal and annotation regression suite to implement the evidenced partition without globally suppressing string analysis.",
  "kind": "edit",
  "inputs": [
    {
      "name": "boundary-review",
      "semantic_role": "typing-factory-boundary-review",
      "artifact_kind": "analysis-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "partitioned-checkout",
      "semantic_role": "typing-factory-boundary-implementation",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:typing-call-traversal-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-owner", "value": true, "evaluator": "file_exists"},
    {"key": "boundary-classification-observed", "value": true, "evaluator": "evidence"},
    {"key": "supported-boundary-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "factory-metadata-not-forward-references", "value": true, "evaluator": "evidence"},
    {"key": "type-bearing-expressions-analyzed", "value": true, "evaluator": "evidence"},
    {"key": "boundary-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-forward-reference-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-call-traversal-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-adjacent-typing-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-partition",
      "instruction": "Review the current public diff for explicit metadata/type separation, guarded NamedTuple sequence recognition, retained ordinary fallback, and regression assertions that still detect unresolved type names. Execution success must be established by the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"],
  "read_set": ["role:typing-call-traversal-owner", "role:annotation-regression-owner"],
  "write_set": ["role:typing-call-traversal-owner", "role:annotation-regression-owner"],
  "invalidates": ["public-validation-observed", "boundary-classification-observed"],
  "exclusions": [
    {"key": "supported-boundary-mechanism-confirmed", "value": false, "evaluator": "evidence"}
  ],
  "resource": "references/actions/partition.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939"
}
```

Invalidation means prior observations must be refreshed. It does not relax preserved behavior. Retain the [validate Action](validate.md) whenever this operation modifies state.
