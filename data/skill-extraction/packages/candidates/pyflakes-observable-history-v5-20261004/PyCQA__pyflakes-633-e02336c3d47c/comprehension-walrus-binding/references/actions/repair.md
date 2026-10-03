# Distinguish and route assignment-expression bindings

Implement the supported mechanism in the currently bound Python analyzer:

1. Distinguish names stored by assignment expressions from ordinary assignment bindings.
2. Preserve existing syntax-version guards.
3. For only the distinguished binding type, choose the insertion destination by skipping consecutive comprehension/generator scopes.
4. Stop at the nearest non-comprehension scope. Do not walk through a function or other non-comprehension boundary.
5. Preserve ordinary assignment insertion and existing annotation treatment.
6. Add public regression assertions for a single generator target and targets in nested comprehensions.

Historical implementation used a dedicated binding subclass; an equivalent current representation is acceptable only after evidence-backed semantic review. Do not redirect all stored names or comprehension iteration variables.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
  "intent": "Correct containing-scope insertion for assignment-expression targets.",
  "mechanism": "Use a distinct assignment-expression binding classification to conditionally bypass consecutive comprehension scopes.",
  "semantic_role": "scope-routing-repair",
  "owner_role": "binding-inserter",
  "operation": "Edit bound classification and insertion owners and add public scope regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosed-scope-model",
      "semantic_role": "assignment-expression-scope-repair-context",
      "artifact_kind": "code-and-observations",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "diagnosis",
      "state": "owners-bound-and-defect-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "scope-routing-patch",
      "semantic_role": "assignment-expression-scope-patch",
      "artifact_kind": "code-and-tests",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "repair",
      "state": "modified-unvalidated"
    }
  ],
  "preconditions": [
    {"key": "role:binding-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:binding-inserter", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comprehension-scope-model", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:scope-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-scope-routing-defect", "value": true, "evaluator": "evidence"},
    {"key": "containing-scope-boundary-understood", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "assignment-expression-target-scope", "value": "nearest-containing-non-comprehension-scope", "evaluator": "evidence"},
    {"key": "single-and-nested-regression-assertions", "value": "present", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-binding-scope-selection", "value": "unchanged", "evaluator": "evidence"},
    {"key": "annotation-binding-treatment", "value": "unchanged", "evaluator": "evidence"},
    {"key": "iteration-variable-locality", "value": "preserved", "evaluator": "evidence"},
    {"key": "syntax-version-guards", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-routing-diff",
      "instruction": "Review the current diff to verify that only assignment-expression bindings bypass consecutive comprehension scopes, that the first non-comprehension scope is the destination, and that ordinary and annotation branches remain unchanged.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:binding-classifier", "role:binding-inserter", "role:comprehension-scope-model", "role:scope-regression-tests"],
  "write_set": ["role:binding-classifier", "role:binding-inserter", "role:scope-regression-tests"],
  "invalidates": ["current-diagnostic-results", "public-scope-regressions", "adjacent-binding-results"],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4"
}
```

Effects describe intended changes, not observed success. Retain the explicit validation Action after this edit.
