# Add paired regression assertions

Use the current public test harness. Add tests for harmless metadata and genuine unresolved types, rather than merely checking disappearance of one diagnostic.

The historical assertions include:

- Clean `List[TypedDict("x", {})]`, keyword-field `TypedDict`, and both pair-list and keyword `NamedTuple` forms.
- Seven `UndefinedName` diagnostics across seven expressions with actual unresolved type names, including nested `List["a"]` and `TypeVar` constraints/bounds.
- Clean imported-name usage within `NamedTuple`, `TypeVar`, and `cast` type expressions.
- Clean class annotations containing nested `TypedDict` and `NamedTuple`, with a Python-version guard.

Also preserve the reported punctuation-label reproduction as a public check. This is an adaptation of the report, not an additional historical regression assertion.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:regressions",
  "intent": "Encode both metadata suppression and retained type-name checking.",
  "mechanism": "Add paired positive and negative public assertions using the current annotation-analysis harness.",
  "semantic_role": "repair-regression-coverage",
  "owner_role": "python-annotation-regression-tests",
  "operation": "Edit regression tests for nested factory calls and adjacent typing behavior.",
  "kind": "edit",
  "inputs": [
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
  "outputs": [
    {
      "name": "regression-ready-checkout",
      "semantic_role": "annotation-traversal-checkout",
      "artifact_kind": "source-checkout",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "repair",
      "state": "partition-and-regressions-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "test-owner-exists", "value": true, "evaluator": "file_exists", "description": "role:python-annotation-regression-tests"},
    {"key": "role-partition-implemented", "value": true, "evaluator": "evidence"},
    {"key": "current-public-test-harness-understood", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "paired-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-annotation-assertions-retained", "value": true, "evaluator": "evidence"},
    {"key": "version-appropriate-test-coverage", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-coverage",
      "instruction": "Inspect the current tests for separate assertions about harmless metadata, unresolved true types, imported names, and class nesting; ensure expected diagnostics are not reduced to a blanket suppression.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:regression", "PyCQA/pyflakes:575:body"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939",
  "read_set": ["role:python-annotation-call-analysis", "role:python-annotation-regression-tests"],
  "write_set": ["role:python-annotation-regression-tests"],
  "invalidates": ["current-test-results"]
}
```
