# Repair recursive classification and diagnostic integration

Modify only after inspection confirms the gap and compatible current policy.

The historical implementation distinguishes singleton recognition from constant recognition:

- Python 3.8+: singleton nodes are `ast.Constant` with values that are instances of `bool`, `type(Ellipsis)`, or `type(None)`.
- Earlier Python 3: singleton nodes are `ast.NameConstant` or `ast.Ellipsis`.
- Historical Python 2: singleton nodes are `ast.Name` with IDs in `{'True', 'False', 'Ellipsis', 'None'}`.
- A constant tuple is `ast.Tuple` with `all(_is_constant(elt) for elt in node.elts)`. The empty tuple qualifies.
- Python 3.8+ constants are `ast.Constant` or constant tuples. Earlier branches accept supported scalar AST classes, singleton nodes, or constant tuples.
- A reportable operand is constant and not singleton.

Adapt only the AST branches required by the current supported runtime matrix. In comparison traversal, inspect either operand for `ast.Is` or `ast.IsNot`, then advance `left = right`. Preserve ordinary child traversal. Do not infer arbitrary expression folding.

The historical message becomes `use ==/!= to compare constant literals (str, bytes, int, float, tuple)`. Update the current message consistently with the broadened rule. Add public assertions for empty tuples, nested all-constant tuples, and variable-containing tuples.

All declared behavioral effects below are targets requiring validation, not observed execution results.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
  "intent": "Close the constant-tuple diagnostic gap without flagging singleton identity or nonconstant tuples.",
  "mechanism": "Recursive all-elements tuple classification, explicit singleton exclusion, and pairwise comparison integration.",
  "semantic_role": "constant-identity-repair",
  "owner_role": "identity_comparison_checker",
  "operation": "Edit bound classification, comparison checking, diagnostic text, and public regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "classification_review",
      "semantic_role": "identity-classification-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "identity-literal-diagnostic",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "diagnostic_patch",
      "semantic_role": "identity-diagnostic-change",
      "artifact_kind": "checkout-diff",
      "language": "Python",
      "scope": "identity-literal-diagnostic",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "classification-gap-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-policy-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:constant_classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:identity_comparison_checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:identity_diagnostic", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:identity_regression_tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "constant-tuple-identity-diagnostic", "value": true, "evaluator": "evidence", "description": "Expected target behavior; execution must establish it."},
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-identity-exemption", "value": true, "evaluator": "evidence"},
    {"key": "variable-tuple-not-constant", "value": true, "evaluator": "evidence"},
    {"key": "scalar-literal-diagnostics", "value": true, "evaluator": "evidence"},
    {"key": "pairwise-chain-traversal", "value": true, "evaluator": "evidence"},
    {"key": "normal-child-traversal", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-classifier-patch",
      "instruction": "Review the diff for recursive tuple classification, singleton exclusion, supported AST branches, both operands and identity operators, chain advancement, preserved child traversal, consistent message text, and public regression assertions. Review is not execution success.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:constant_classifier", "role:identity_comparison_checker", "role:identity_diagnostic", "role:identity_regression_tests"],
  "write_set": ["role:constant_classifier", "role:identity_comparison_checker", "role:identity_diagnostic", "role:identity_regression_tests"],
  "invalidates": ["classification-gap-assessed", "public-validation-observed", "pre-edit-diagnostic-observations"],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f"
}
```
