# Repair rendering and paired assertions

Use the current bound renderer and regression owners. Keep the existing one-positional-list-comprehension gate and body extraction. When keywords are present, parenthesize the extracted generator body and append every keyword's AST rendering in order, separated by comma-space.

Add a flagged list-comprehension call with `default=42`, the exact corrected expected suggestion, and its already-generator counterpart without a diagnostic expectation. Retain keyword-free fixtures. Do not suppress the warning or mechanically bless defective actual output.

```arex-contract-v4
{
  "id": "workflow:verified-history:4f600acd843f37945bbd0765:repair",
  "intent": "Preserve keyword arguments and valid call syntax in generator suggestions.",
  "mechanism": "Conditionally parenthesize the generator body, append ordered keyword AST renderings, and add paired regression assertions.",
  "semantic_role": "keyword-preserving-rendering-edit",
  "owner_role": "generator-suggestion-renderer",
  "operation": "Edit the bound suggestion renderer and corresponding public fixture and expected-output resources using the observed current AST interfaces.",
  "kind": "edit",
  "inputs": [
    {
      "name": "rendering-review",
      "semantic_role": "generator-rendering-applicability",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "outputs": [
    {
      "name": "rendering-change",
      "semantic_role": "keyword-preserving-generator-change",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "rendering-applicability-observed", "value": true, "evaluator": "evidence"},
    {"key": "role:generator-suggestion-renderer", "value": true, "evaluator": "symbol_exists", "description": "Locate the replacement-rendering owner in the current checkout."},
    {"key": "role:generator-suggestion-regressions", "value": true, "evaluator": "file_exists", "description": "Locate current public fixture and expected-output resources."}
  ],
  "effects": [
    {"key": "keyword-aware-suggestion-rendering", "value": true, "evaluator": "evidence"},
    {"key": "paired-keyword-regression-assertions", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "keyword-free-suggestion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-eligibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-rendering-diff",
      "instruction": "Review the diff for conditional generator parentheses and complete ordered keyword serialization. Confirm the positional gate and keyword-free branch are unchanged. Confirm paired fixture inputs and exact keyword-preserving expected output.",
      "evidence_refs": ["pylint-dev/pylint:8563:fix", "pylint-dev/pylint:8563:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8563:repair:4a485e28f0a5"],
  "evidence_refs": ["pylint-dev/pylint:8563:fix", "pylint-dev/pylint:8563:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:4f600acd843f37945bbd0765",
  "read_set": ["role:generator-suggestion-renderer", "role:generator-suggestion-regressions"],
  "write_set": ["role:generator-suggestion-renderer", "role:generator-suggestion-regressions"]
}
```

Declared effects are intended postconditions, not observed successes. Every composed plan retaining this modification must retain [validate](validate.md). The freshness fact invalidated here is distinct from preserved behavior assurances.
