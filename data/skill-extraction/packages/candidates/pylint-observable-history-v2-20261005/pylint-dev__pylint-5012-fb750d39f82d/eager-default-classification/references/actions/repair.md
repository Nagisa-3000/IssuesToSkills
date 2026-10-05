# Complete classification and add focused assertions

Use current semantic bindings from the confirmed diagnosis. Combine positional defaults with keyword-only defaults, filtering absent keyword-only entries before traversing descendants. Keep exact object identity comparison, FunctionDef/Lambda handling, and the false fallback for unsupported scopes.

Add an escaping-function regression with both `def func(*, _i=i)` and `def func2(_i=i)`. Their bodies use `_i`; append both functions to a list returned after the loop. Retain genuine closure warnings and adjust only expected locations displaced by inserted lines.

The historical implementation used `itertools.chain` and `any`. Equivalent current code requires semantic review and validation; the historic syntax does not authorize incompatible adaptations.

```arex-contract-v4
{
  "id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32:repair",
  "intent": "Complete eager-default classification and add focused regression assertions.",
  "mechanism": "Search both default collections, exclude absent keyword-only defaults, and preserve identity matching.",
  "semantic_role": "complete-default-classification",
  "owner_role": "default-expression-classifier",
  "operation": "Edit the bound classifier and public regression owners without removing genuine diagnostic expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "default-binding-diagnosis",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "default-classification-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:default-expression-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:loop-closure-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "compatible-omission-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "default-collections-complete", "value": true, "evaluator": "evidence"},
    {"key": "focused-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "positional-default-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-closure-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "exact-node-matching-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-candidate",
      "instruction": "Review the public diff for both default collections, absent-entry filtering, exact-node identity, retained scope handling, escaping eager-capture assertions, and unchanged genuine warning expectations apart from necessary location shifts. Keep the explicit validate Action.",
      "evidence_refs": ["pylint-dev/pylint:5012:fix", "pylint-dev/pylint:5012:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:default-expression-classifier", "role:loop-closure-regression-suite"],
  "write_set": ["role:default-expression-classifier", "role:loop-closure-regression-suite"],
  "source_ids": ["pylint-dev/pylint:5012:repair:fb750d39f82d"],
  "evidence_refs": ["pylint-dev/pylint:5012:fix", "pylint-dev/pylint:5012:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32"
}
```
