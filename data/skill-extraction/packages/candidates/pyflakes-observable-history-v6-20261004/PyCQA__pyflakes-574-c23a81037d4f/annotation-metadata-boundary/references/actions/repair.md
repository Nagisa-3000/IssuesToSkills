# Repair the traversal boundary

Apply only with current evidence of the defect and resolved owners. Adapt to current code; do not silently reuse historical paths.

The historical branch:
1. Recognized a bare name or attribute named `Annotated`.
2. Visited `node.value`.
3. Selected an `ast.Tuple` slice, or a tuple inside `ast.Index`.
4. Used normal slice traversal for non-tuples or fewer than two elements.
5. Visited the first element in the inherited context.
6. Visited remaining elements inside `with self._enter_annotation(AnnotationState.NONE):`.
7. Visited `node.ctx`.

Retain existing `Literal` and generic typing behavior. Use scoped restoration rather than a persistent annotation-state reset. Metadata expressions must still be visited; suppressing all diagnostics or skipping metadata is not equivalent.

Add/adapt public regression assertions for the four historical cases. Ordinary metadata-expression checking, exceptional context restoration, and supported AST-layout review are current validation obligations motivated by the implementation, not additional historical test claims.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
  "intent": "Separate Annotated type and metadata checking contexts.",
  "mechanism": "Partition multi-argument slices and scope metadata traversal to non-annotation state.",
  "semantic_role": "boundary-repair",
  "owner_role": "annotation-subscript-visitor",
  "operation": "Edit the current visitor and public regression tests to retain inherited type checking for the first argument and ordinary expression checking for metadata, preserving fallback traversal and scoped restoration.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspection",
      "semantic_role": "annotation-boundary-inspection",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "annotation-boundary-candidate",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:annotation-subscript-visitor", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-state-manager", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "metadata-forward-parsing-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "metadata-traversal-context", "value": "non-annotation", "evaluator": "evidence"},
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "type-reference-checking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enclosing-annotation-state-preserved", "value": true, "evaluator": "evidence"},
    {"key": "literal-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-expression-checking-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-partition",
      "instruction": "Review the current public diff for inherited first-argument context, scoped NONE metadata context, restoration, fallback traversal, value/context visits, retained Literal behavior and the four historical regression assertions. Execution is required in the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotation-subscript-visitor",
    "role:annotation-state-manager",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:annotation-subscript-visitor",
    "role:annotation-regression-tests"
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6"
}
```

Effects describe intended candidate properties, not observed successful execution. Every plan retaining this edit must retain its public validate Action. Stale observation freshness is distinct from the behavior assurances that must survive the edit.
