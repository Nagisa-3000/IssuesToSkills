# Validate output, syntax, and adjacent behavior

Bind the current public test harness. Execute the relevant generator-suggestion fixtures and parse the actual suggested replacement as Python. Compare diagnostics with reviewed expectations, including keyword-free cases. Record failures rather than automatically updating expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:4f600acd843f37945bbd0765:validate",
  "intent": "Observe corrected suggestions and preserved diagnostic behavior.",
  "mechanism": "Exercise paired keyword cases and existing keyword-free fixtures through the public harness, then check suggested-call syntax.",
  "semantic_role": "post-edit-validation",
  "owner_role": "generator-suggestion-test-runner",
  "operation": "Execute current bound public regression and syntax checks, retain actual outputs and exit status, and refresh validation observations without editing expectations.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "generator-suggestion-validation",
      "artifact_kind": "test-result-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "keyword-aware-suggestion-rendering", "value": true, "evaluator": "evidence"},
    {"key": "paired-keyword-regression-assertions", "value": true, "evaluator": "evidence"},
    {"key": "role:generator-suggestion-test-runner", "value": true, "evaluator": "file_exists", "description": "Locate the current public harness and bind its command."}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "keyword-free-suggestion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-eligibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-generator-regressions",
      "instruction": "Run the bound public harness and retain actual output and exit status. Confirm the flagged list-comprehension case suggests exactly min((x * x for x in range(10)), default=42), or the reviewed current-format equivalent retaining the same AST. Parse the suggestion as Python. Confirm the already-generator counterpart emits no consider-using-generator diagnostic and keyword-free expectations are unchanged. Any mismatch or failed check blocks completion.",
      "evidence_refs": ["pylint-dev/pylint:8563:regression", "pylint-dev/pylint:8563:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:4f600acd843f37945bbd0765:repair"],
  "source_ids": ["pylint-dev/pylint:8563:repair:4a485e28f0a5"],
  "evidence_refs": ["pylint-dev/pylint:8563:regression", "pylint-dev/pylint:8563:fix"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4f600acd843f37945bbd0765",
  "read_set": ["role:generator-suggestion-renderer", "role:generator-suggestion-regressions", "role:generator-suggestion-test-runner"],
  "write_set": []
}
```

The empty command array is deliberately unbound. Historical commands do not authorize current execution. A validation record may contain failure; only passing current Oracles satisfy completion.
