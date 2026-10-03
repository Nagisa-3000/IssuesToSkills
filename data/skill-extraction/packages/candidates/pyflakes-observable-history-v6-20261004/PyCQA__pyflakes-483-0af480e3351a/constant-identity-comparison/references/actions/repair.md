# Repair constant classification and regression coverage

Apply the mechanism only to compatible, reviewed current owners.

Define singleton recognition using the current supported AST representation. In the historical Python 3.8+ branch, this meant an `ast.Constant` whose value was a boolean, Ellipsis, or `None`. Older branches used `ast.NameConstant`/`ast.Ellipsis`, or Python 2 names. Do not add obsolete compatibility branches unless the current project supports them.

Define tuple constancy recursively: an `ast.Tuple` is constant when every element is constant. Define non-singleton constants as constant nodes that are not singleton nodes. Use this predicate on either operand for `ast.Is` and `ast.IsNot`, advancing the left operand through chained comparisons.

Align the diagnostic wording with the actual supported scope. Add or retain public regression coverage for empty tuples, nested constant tuples, and tuples containing variables. Preserve existing coverage and diagnostic location conventions.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair",
  "intent": "Extend identity-comparison diagnostics to recursively constant tuples while retaining singleton exemptions.",
  "mechanism": "Introduce or adapt singleton, recursive constant, and non-singleton constant predicates; integrate them into adjacent-pair identity checks and public regression coverage.",
  "semantic_role": "constant-classification-repair",
  "owner_role": "comparison-classifier",
  "operation": "Edit the bound comparison classifier and literal diagnostic as necessary, and add public tests at the bound comparison-regressions owner for empty and nested constant tuples and variable-containing tuples.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-target",
      "semantic_role": "identity-diagnostic-target",
      "artifact_kind": "binding-and-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "patched-target",
      "semantic_role": "identity-diagnostic-target",
      "artifact_kind": "source-and-regression-suite",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "validation",
      "state": "patched",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "repair-applicability-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "compatible-ast-semantics-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:comparison-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:literal-diagnostic", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comparison-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "constant-tuple-identity-diagnosed", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-boundaries-added", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-scope-wording-aligned", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonconstant-tuple-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-literal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nonidentity-comparison-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-classification-diff",
      "instruction": "Review the current diff for recursive tuple classification, explicit singleton exclusion, identity-only checks on both operands, chained-comparison traversal, aligned diagnostic wording, and the three supplied regression boundaries. Execution is delegated to the retained validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f",
  "read_set": ["role:comparison-classifier", "role:literal-diagnostic", "role:comparison-regressions"],
  "write_set": ["role:comparison-classifier", "role:literal-diagnostic", "role:comparison-regressions"],
  "invalidates": ["public-validation-observed"]
}
```

Effects are intended outcomes until independently observed in current validation. This card does not authorize rewriting user comparisons or changing runtime identity semantics.
