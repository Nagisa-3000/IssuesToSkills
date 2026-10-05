# Guard extraction by supported AST kind

At the bound extraction point, preserve the name branch, make constant access conditional on the constant node type, and locally return for all other node kinds. Preserve the assignment-value comparison and surrounding eligibility checks. A local return suppresses only this suggestion analysis; it must not terminate the entire AST walk.

```arex-contract-v4
{
  "id": "workflow:verified-history:ba0f15907d742a3c30dae2cf:guard",
  "intent": "Remove unsafe constant-style access for unsupported comparison operands.",
  "mechanism": "Explicit Name and Const branches followed by an early return for unsupported kinds.",
  "semantic_role": "operand-kind-guard",
  "owner_role": "comparison-operand-extractor",
  "operation": "Edit only the bound operand extraction branch: retain name extraction, gate value extraction on the constant type, and return from the local check otherwise.",
  "kind": "edit",
  "inputs": [
    {"name": "reviewed-owner", "semantic_role": "operand-owner-review", "artifact_kind": "review-record", "language": "python", "scope": "comparison-operand-extractor", "phase": "diagnosis", "state": "reviewed"}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "operand-owner-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "unsupported-operand-fallback-safe", "value": true, "evaluator": "evidence", "description": "Current review establishes that unsupported shapes may be skipped by this suggestion check."},
    {"key": "role:comparison-operand-extractor", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "operand-kind-guard-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-constant-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "neighboring-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-kind-guard",
      "instruction": "Review the diff: only Name reads name, only Const reads value, other kinds return locally, and subsequent operand/body comparison and surrounding checks remain intact. Retain the validate Action for runtime confirmation.",
      "evidence_refs": ["pylint-dev/pylint:4379:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4379:repair:95c05e024cf4"],
  "evidence_refs": ["pylint-dev/pylint:4379:fix"],
  "read_set": ["role:comparison-operand-extractor"],
  "write_set": ["role:comparison-operand-extractor"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:ba0f15907d742a3c30dae2cf"
}
```
