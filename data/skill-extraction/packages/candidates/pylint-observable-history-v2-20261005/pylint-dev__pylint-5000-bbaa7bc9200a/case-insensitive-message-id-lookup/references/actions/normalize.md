# Normalize only the numeric lookup key

Apply the registry's established uppercase convention at its symbol lookup boundary. Do not uppercase symbolic names, entire directives, or the input retained for diagnostic messages.

```arex-contract-v4
{
  "id": "workflow:verified-history:3af38f4091bb3d8442540d61:normalize",
  "intent": "Resolve accepted lowercase numeric IDs to the same symbols as uppercase IDs.",
  "mechanism": "Uppercase the numeric mapping lookup key without replacing the original argument.",
  "semantic_role": "lookup-key-normalization",
  "owner_role": "numeric-id-symbol-resolver",
  "operation": "Edit the bound Python symbol resolver to access its numeric-ID mapping with an uppercase key. Retain the original argument and existing unknown-ID exception path.",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:numeric-id-symbol-resolver", "value": true, "evaluator": "symbol_exists"},
    {"key": "accepted-lowercase-numeric-ids", "value": true, "evaluator": "evidence"},
    {"key": "uppercase-keys-raw-lookup", "value": true, "evaluator": "evidence"},
    {"key": "recommendation-uses-resolver", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "numeric-symbol-lookup-case-insensitive", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "uppercase-recommendations-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unknown-id-error-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-id-spelling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-normalization",
      "instruction": "Review the current diff for lookup-key-only normalization and unchanged original-input storage and exception handling. Require the explicit validate Action for behavioral confirmation.",
      "evidence_refs": ["pylint-dev/pylint:5000:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5000:repair:bbaa7bc9200a"],
  "evidence_refs": ["pylint-dev/pylint:5000:fix"],
  "resource": "references/actions/normalize.md",
  "package_id": "workflow:verified-history:3af38f4091bb3d8442540d61",
  "kind": "edit",
  "read_set": ["role:numeric-id-symbol-resolver"],
  "write_set": ["role:numeric-id-symbol-resolver"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "lowercase-ids-intentionally-invalid", "value": true, "evaluator": "evidence"},
    {"key": "case-distinct-message-identities", "value": true, "evaluator": "evidence"}
  ]
}
```
