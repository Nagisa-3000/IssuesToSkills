# Add lowercase recommendation assertions

Use the current public suite and registry. Preserve uppercase and invalid-ID controls. Historical symbolic names and output formatting are not automatically valid in another checkout.

```arex-contract-v4
{
  "id": "workflow:verified-history:3af38f4091bb3d8442540d61:regression",
  "intent": "Expose lowercase numeric-ID recommendation behavior in public regression assertions.",
  "mechanism": "Assert separate recommendations for two lowercase numeric IDs in one enable directive.",
  "semantic_role": "lowercase-recommendation-regression",
  "owner_role": "symbolic-recommendation-regression-suite",
  "operation": "Edit the bound Python public fixture and expected results to cover two lowercase numeric IDs, correct enable replacements, and original spelling. Retain existing uppercase recommendations and invalid-ID diagnostics. Adapt symbols and formatting using the current public registry and harness.",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:symbolic-recommendation-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "accepted-lowercase-numeric-ids", "value": true, "evaluator": "evidence"},
    {"key": "current-message-symbols-established", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "lowercase-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "uppercase-recommendations-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unknown-id-error-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-id-spelling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regressions",
      "instruction": "Inspect the fixture and expected results for two lowercase IDs, two registry-backed enable replacements, original spelling, and retained uppercase and invalid-ID controls. For causal diagnosis, execute the strengthened test against the unchanged resolver and distinguish missing recommendations from environment failures.",
      "evidence_refs": ["pylint-dev/pylint:5000:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5000:repair:bbaa7bc9200a"],
  "evidence_refs": ["pylint-dev/pylint:5000:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:3af38f4091bb3d8442540d61",
  "kind": "edit",
  "read_set": ["role:numeric-id-symbol-resolver", "role:symbolic-recommendation-regression-suite"],
  "write_set": ["role:symbolic-recommendation-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```
