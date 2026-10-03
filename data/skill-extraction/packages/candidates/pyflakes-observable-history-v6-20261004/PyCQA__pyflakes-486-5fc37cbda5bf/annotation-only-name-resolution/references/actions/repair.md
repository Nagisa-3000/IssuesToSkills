# Repair annotation-only binding semantics

Adapt the mechanism to the located current Python analyzer; do not copy historical paths as bindings.

The historical edit:

- Added a Python-version-gated `AnnAssign` type tuple.
- Introduced `Annotation(Binding)` for a declaration without a value.
- Visited annotated-assignment targets even when no value existed.
- Classified no-value annotated assignments as `Annotation`, leaving other assignment classification branches in place.
- Skipped annotation-only bindings during lookup unless postponed annotation conditions applied.
- Replaced boolean annotation state with `NONE`, `STRING`, and `BARE`, restoring the previous state on context exit.
- Marked parsed string annotations and a string-handling call path with `STRING`.
- Defined postponed context as string annotation state or the future-annotations flag.

Add/adapt public regression assertions alongside the implementation. Do not introduce new unused-variable warnings for annotation-only locals as part of this repair: the supplied tests explicitly documented that limitation.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:repair",
  "intent": "Represent annotation-only names without treating them as ordinary value assignments.",
  "mechanism": "Use a distinct binding kind and a postponed-annotation lookup gate with restorable annotation context state.",
  "semantic_role": "annotation-resolution-repair",
  "owner_role": "annotation_binding_owner",
  "operation": "Modify current binding construction, annotated-assignment handling and annotation-context lookup together; add public tests for eager, quoted and future annotation behavior and unused-variable accounting.",
  "kind": "edit",
  "inputs": [
    {
      "name": "resolution_review",
      "semantic_role": "annotation-resolution-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "outputs": [
    {
      "name": "resolution_patch",
      "semantic_role": "annotation-resolution-change",
      "artifact_kind": "code-and-tests",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "binding-owner-exists", "value": true, "evaluator": "symbol_exists", "description": "role:annotation_binding_owner"},
    {"key": "regression-owner-exists", "value": true, "evaluator": "file_exists", "description": "role:annotation_regression_owner"},
    {"key": "resolution-owners-located", "value": true, "evaluator": "evidence"},
    {"key": "resolution-mechanism-compatible", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-only-resolution-corrected", "value": true, "evaluator": "evidence", "description": "Expected repair effect, requiring current public validation."}
  ],
  "preserves": [
    {"key": "ordinary-value-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unused-variable-accounting-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-binding-gate",
      "instruction": "Review the patch for a separate no-value binding, postponed-context lookup, context restoration, and unchanged value-bearing assignment handling. Acceptance additionally requires the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:annotation_binding_owner", "role:annotation_regression_owner"],
  "write_set": ["role:annotation_binding_owner", "role:annotation_regression_owner"],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```

For the owner-existence predicates, resolve the `role:` locator in the description to the current object before evaluation; do not test the historical path. Expected effects are not execution results.
