# Enrich the diagnostic and align assertions

At the existing invalid-value emission boundary, add a message interpolation slot and supply the inferred AST object's class name. Historically this was `args=inferred.__class__.__name__` with a `%s` template.

Do not substitute the user's runtime type, alter acceptance predicates, change inference traversal, or remove exemption branches. Keep diagnostic symbol, source spans, object labels, and confidence. Update only the corresponding expected message texts and review them individually.

Effects below describe intended postconditions, not execution results. The separate validation Action must observe correctness.

```arex-contract-v4
{
  "id": "workflow:verified-history:124787fcb0844f5e9acb613d:edit",
  "intent": "Include the inferred AST node kind in invalid assignment diagnostics.",
  "mechanism": "Pair an interpolation slot with the inferred object's class-name argument and align expected output.",
  "semantic_role": "typed-diagnostic-update",
  "owner_role": "special-class-assignment-diagnostic",
  "operation": "Edit the bound diagnostic definition and rejection emission, then update matching regression message expectations without changing classification, inference traversal, metadata, or unrelated assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "bound-diagnostic-context",
      "semantic_role": "inferred-kind-diagnostic-context",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "special-class-assignment",
      "phase": "pre-edit",
      "state": "bound-and-reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "diagnostic-change",
      "semantic_role": "inferred-kind-diagnostic-change",
      "artifact_kind": "checkout-diff",
      "language": "Python",
      "scope": "special-class-assignment",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "diagnostic-context-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "supported-diagnostic-mechanism", "value": true, "evaluator": "evidence"},
    {"key": "role:special-class-assignment-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:special-class-assignment-diagnostic", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:special-class-assignment-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "diagnostic-kind-included", "value": true, "evaluator": "evidence"},
    {"key": "assertions-match-diagnostic", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "acceptance-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-metadata-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "inference-traversal-change-required", "value": true, "evaluator": "evidence"},
    {"key": "acceptance-rule-change-required", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-diagnostic-diff",
      "instruction": "Review matched template arity and the inferred AST class-name argument. Confirm unchanged acceptance predicates, traversal, symbol, source spans, object labels, confidence, and unrelated expectations. Retain the explicit validate Action; diff review alone is not execution evidence.",
      "evidence_refs": ["pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:special-class-assignment-checker",
    "role:special-class-assignment-diagnostic",
    "role:special-class-assignment-regression-suite"
  ],
  "write_set": [
    "role:special-class-assignment-checker",
    "role:special-class-assignment-diagnostic",
    "role:special-class-assignment-regression-suite"
  ],
  "source_ids": ["pylint-dev/pylint:7467:repair:b47aa3076ee0"],
  "evidence_refs": ["pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:124787fcb0844f5e9acb613d"
}
```
