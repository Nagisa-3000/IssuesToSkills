# Add the export/annotation regression assertion

Add the public reproduction to the current annotation test owner, asserting no diagnostics. Preserve its branch structure: one branch assigns exports and the other supplies only the annotation. Adapt syntax availability guards to the current supported Python versions; the historical test required Python 3.6 or newer.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:regression",
  "intent": "Capture the export-use regression in a public test.",
  "mechanism": "Assert that a conditional annotation-only declaration does not erase export usage.",
  "semantic_role": "export-annotation-regression",
  "owner_role": "annotation-regression-test-owner",
  "operation": "Add the reported conditional __all__ assignment and annotation-only declaration to the current public test suite, expecting no diagnostics.",
  "kind": "edit",
  "inputs": [
    {"name": "reviewed-bindings", "semantic_role": "annotation-binding-repair-context", "artifact_kind": "binding-map", "language": "Python", "scope": "current-checkout", "phase": "review", "state": "reviewed"}
  ],
  "outputs": [
    {"name": "regression-assertion", "semantic_role": "export-annotation-test", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "preconditions": [
    {"key": "test-owner-located", "value": true, "evaluator": "symbol_exists", "description": "role:annotation-regression-test-owner"},
    {"key": "annotation-overwrite-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "export-annotation-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-rebinding-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotation-insertion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-expression-use-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression",
      "instruction": "Inspect the added test for the exported import, TYPE_CHECKING conditional, valued __all__ branch, annotation-only branch, and no-diagnostics assertion. Ensure it is runnable on supported Python versions.",
      "evidence_refs": ["PyCQA/pyflakes:605:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"],
  "read_set": ["role:annotation-regression-test-owner"],
  "write_set": ["role:annotation-regression-test-owner"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489"
}
```

Do not infer test success from the presence of the assertion.
