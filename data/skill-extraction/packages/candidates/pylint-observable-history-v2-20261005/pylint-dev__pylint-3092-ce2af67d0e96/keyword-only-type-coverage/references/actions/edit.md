# Extend coverage and encode the regression

At the current collector owner, preserve ordinary annotation processing. Traverse keyword-only parameters using their own corresponding annotations; add a name only when its annotation is present. Extend the same type-evidence set before the existing missing-type comparison.

At the current test owner, add or retain the focused regression: two ordinary annotated parameters and two annotated keyword-only parameters, all described in a Google-style `Args:` section without explicit types. Assert no checker messages.

Do not combine unrelated collections under a shared index, treat `*` as an argument, disable the diagnostic, or exempt unannotated keyword-only parameters. If the coverage and regression already exist, omit this modifying operation and validate current behavior.

Effects below are intended results requiring review and validation, not observed execution outcomes.

```arex-contract-v4
{
  "id": "workflow:verified-history:9458ec98dda8784befed789c:edit",
  "intent": "Repair the annotation-evidence omission and add a focused regression.",
  "mechanism": "Add only annotated keyword-only names to the existing type-evidence set.",
  "semantic_role": "coverage-repair",
  "owner_role": "parameter-type-evidence-collector",
  "operation": "Extend the separate keyword-only annotation traversal before comparison and add the no-message regression at the bound test owner.",
  "kind": "edit",
  "inputs": [
    {"name": "coverage-review", "semantic_role": "coverage-review", "artifact_kind": "review-record", "language": "Python", "scope": "parameter-documentation-checker", "phase": "diagnosis", "state": "recorded"}
  ],
  "outputs": [
    {"name": "repair-candidate", "semantic_role": "repair-candidate", "artifact_kind": "checkout-change", "language": "Python", "scope": "parameter-documentation-checker", "phase": "repair", "state": "unvalidated"}
  ],
  "preconditions": [
    {"key": "keyword-only-annotation-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "keyword-only-annotation-alignment-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "signature-annotation-credit-policy", "value": true, "evaluator": "evidence"},
    {"key": "role:parameter-type-evidence-collector", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:parameter-documentation-test-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "annotated-keyword-only-coverage", "value": true, "evaluator": "evidence"},
    {"key": "focused-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-annotation-credit-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-type-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-targeted-diff",
      "instruction": "Review the current diff for aligned separate keyword-only annotation traversal, addition only for present annotations, retained ordinary annotation credit and comparison, and the described four-parameter no-message regression.",
      "evidence_refs": ["pylint-dev/pylint:3092:fix", "pylint-dev/pylint:3092:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3092:repair:ce2af67d0e96"],
  "evidence_refs": ["pylint-dev/pylint:3092:fix", "pylint-dev/pylint:3092:regression"],
  "read_set": ["role:parameter-type-evidence-collector", "role:parameter-documentation-test-suite"],
  "write_set": ["role:parameter-type-evidence-collector", "role:parameter-documentation-test-suite"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:9458ec98dda8784befed789c"
}
```
