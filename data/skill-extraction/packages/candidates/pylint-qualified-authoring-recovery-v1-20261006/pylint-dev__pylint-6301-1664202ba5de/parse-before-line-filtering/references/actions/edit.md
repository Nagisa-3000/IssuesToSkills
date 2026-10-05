# Retain source and defer suppression

Keep complete decoded source through structural parsing and source storage. Propagate an optional line-enablement callback through current ingestion, container, and normalization owners. Apply suppression after AST-dependent preparation, before stripping comparison candidates, with original one-based physical line numbers.

The historical diagnostic identity was `"R0801"`; establish the current public equivalent before editing. Retain callback-free operation.

Strengthen public assertions to exercise secondary parsing and expose parser errors. Keep expected-output checks and independently reject fatal output. Do not alter unrelated decode policy based solely on the historical fallback.

```arex-contract-v4
{
  "id": "workflow:verified-history:da14748ad2e8a043ad8319eb:edit",
  "intent": "Repair parse/filter ordering and expose the regression publicly.",
  "mechanism": "Transport intact source separately from an optional diagnostic-enable callback, then suppress only comparison candidates after structural parsing.",
  "semantic_role": "preprocessing-repair",
  "owner_role": "duplicate-preprocessing",
  "operation": "Edit bound source transport and normalized-line construction; strengthen bound public regression assertions for secondary parsing and fatal-output visibility.",
  "kind": "edit",
  "inputs": [
    {"name": "confirmed-boundary", "semantic_role": "preprocessing-binding", "artifact_kind": "code-review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "repaired-preprocessing", "semantic_role": "preprocessing-change", "artifact_kind": "patch", "language": "Python", "scope": "current-checkout", "phase": "repair", "state": "edited"}
  ],
  "preconditions": [
    {"key": "role:duplicate-preprocessing", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:duplicate-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "pre-parse-suppression-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "callback-coordinate-contract-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "complete-source-parsed-before-suppression", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-expose-fatal-output", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "suppression-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-coordinate-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enabled-comparison-and-exclusion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "callback-free-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-ordering-change",
      "instruction": "Review the current patch and public parser-input probe. Confirm intact source reaches structural parsing, subsequent suppression uses original coordinates, the callback remains optional, and expected-output and no-fatal assertions are separate.",
      "evidence_refs": ["pylint-dev/pylint:6301:fix", "pylint-dev/pylint:6301:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:duplicate-preprocessing", "role:duplicate-regression-tests"],
  "write_set": ["role:duplicate-preprocessing", "role:duplicate-regression-tests"],
  "source_ids": ["pylint-dev/pylint:6301:repair:1664202ba5de"],
  "evidence_refs": ["pylint-dev/pylint:6301:fix", "pylint-dev/pylint:6301:regression"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:da14748ad2e8a043ad8319eb"
}
```

Effects are expected until observed. Diff review alone does not prove runtime correctness. Retain the [validate Action](validate.md) after this modification.
