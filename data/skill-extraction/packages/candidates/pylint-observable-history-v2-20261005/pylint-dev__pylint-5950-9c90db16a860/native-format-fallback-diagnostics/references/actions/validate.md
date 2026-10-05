# Validate corrected routing and preservation

Bind current public test commands and observe diagnostics, exits, backend probes and writer calls. Execute the three historically asserted branches and additional current checks derived from implementation: native bypass, missing Graphviz, help, and exact-token rejection. These additional checks are not claimed as historical regression assertions.

Also run public adjacent import-path tests. Record actual results, not inferred success from a structurally valid plan. No source edits are made by this Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:validate",
  "intent": "Observe public repair behavior and adjacent preservation after edits.",
  "mechanism": "Controlled format-routing tests and adjacent import-path regressions.",
  "semantic_role": "format-repair-validation",
  "owner_role": "format-regression-tests",
  "operation": "Execute bound current public checks and record commands, diagnostics, exit codes, backend and writer calls, and tri-state oracle results; refresh validation observations without changing source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "format-repair",
      "semantic_role": "format-diagnostic-change",
      "artifact_kind": "code-and-test-diff",
      "language": "python",
      "scope": "current-checkout-output-format-routing",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "format-validation-observations",
      "artifact_kind": "public-test-results",
      "language": "python",
      "scope": "current-checkout-output-format-routing",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "native-and-backend-diagnostics-separated", "value": true, "evaluator": "evidence"},
    {"key": "role:format-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "native-output-independent-of-graphviz", "value": true, "evaluator": "evidence"},
    {"key": "supported-output-writing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inconclusive-capability-fallback-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-import-path-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "format-routing-matrix",
      "instruction": "Run bound public checks: native output without Graphviz and without capability probing; supported delegated output with fallback notice, one writer call and success; unparseable capabilities with warning, one writer call and success; known unsupported output with backend-specific list, failure and no writing; missing Graphviz with dependency-specific failure; exact-token membership; help listing current native formats and explaining delegation. Explicitly bind current exit expectations; historical values were 0 and 32.",
      "evidence_refs": ["pylint-dev/pylint:5950:fix", "pylint-dev/pylint:5950:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-import-path",
      "instruction": "Run bound public import-path regressions and observe unchanged expected sys.path behavior.",
      "evidence_refs": ["pylint-dev/pylint:5950:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:repair"],
  "read_set": ["role:format-regression-tests", "role:output-format-routing", "role:graphviz-capability-check", "role:adjacent-import-path-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5950:repair:9c90db16a860"],
  "evidence_refs": ["pylint-dev/pylint:5950:fix", "pylint-dev/pylint:5950:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb"
}
```

Empty argv arrays require explicit current binding before execution. A validation record may contain FAIL or UNKNOWN; merely recording observations is not a repair-success claim. Success requires passing bound checks and established preservation assurances.
