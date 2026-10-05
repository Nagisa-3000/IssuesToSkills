# Validate the modified state

Render current public Oracle bindings before executing them. Inspect actual diagnostics and normalized names, not exit codes alone. Check ordinary fields, omitted variadics, escaped and unescaped starred fields, raw literal behavior, adjacent Google controls, and unrelated expectations.

This operation does not edit source files. Record failed or unavailable checks explicitly. Sphinx rendering is a separate observation and remains UNKNOWN unless executed.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2490b7f20db2a942170750b:validate",
  "intent": "Establish repair behavior and preserved adjacent behavior through public checks.",
  "mechanism": "Execute positive and negative Sphinx fixtures, literal probes, and adjacent documentation controls against the modified state.",
  "semantic_role": "sphinx-escape-validation",
  "owner_role": "sphinx-variadic-fixtures",
  "operation": "Run current bound public commands; compare actual diagnostics and names with assertions; record hashes, exit statuses, PASS/FAIL/UNKNOWN outcomes, and scope limitations without editing.",
  "kind": "validate",
  "inputs": [
    {
      "name": "modified-target",
      "semantic_role": "sphinx-repair-state",
      "artifact_kind": "code-and-public-regression-diff",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "modified-awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-results",
      "semantic_role": "sphinx-repair-validation",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "validation",
      "state": "observed-pass-fail-or-unknown",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:sphinx-variadic-fixtures", "value": true, "evaluator": "file_exists"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observation-current", "value": true, "evaluator": "evidence"},
    {"key": "required-public-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-parameter-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-google-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "sphinx-matrix",
      "instruction": "Execute current public tests for ordinary names, omitted variadics, raw escaped one/two-star fields, and unescaped starred fields. Require escaped fields to satisfy variadic documentation, unescaped starred and absent fields to produce the intended missing-documentation diagnostics, and unrelated expectations to remain unchanged. Inspect normalized names.",
      "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "literal-and-adjacent-controls",
      "instruction": "Run current public literal/checker probes for raw escaped examples and ordinary/Google-style controls. Require absence of the reported anomalous-backslash warning for raw examples and preservation of adjacent behavior. Record rendering separately as PASS/FAIL/UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:f2490b7f20db2a942170750b:repair"],
  "read_set": ["role:sphinx-parameter-parser", "role:sphinx-variadic-fixtures", "role:escaped-docstring-example"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5406:repair:608ed329aaee"],
  "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f2490b7f20db2a942170750b"
}
```

Effects are conditional on actual observations. A completed attempt may have FAIL or UNKNOWN outcomes; it does not then establish `required-public-checks-pass`.
