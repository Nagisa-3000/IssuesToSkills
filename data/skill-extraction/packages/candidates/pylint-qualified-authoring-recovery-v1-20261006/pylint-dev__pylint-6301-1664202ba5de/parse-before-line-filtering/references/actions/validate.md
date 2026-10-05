# Validate corrected and adjacent behavior

Run current-bound public tests with parser-error diagnostics visible. Exercise import/signature exclusion individually where supported and together as in the historical helper.

Cover suppressed bodies, per-line disables, another enabled function, enabled duplicate regions, raw-string/docstring handling, original coordinates, and callback-free operation.

Expected output and absence of fatal output are independent checks. Use each fixture's diagnostic exit expectations; duplicate-code reports may intentionally make a linter invocation nonzero.

```arex-contract-v4
{
  "id": "workflow:verified-history:da14748ad2e8a043ad8319eb:validate",
  "intent": "Observe corrected behavior and preserved adjacent behavior.",
  "mechanism": "Exercise secondary parsing under suppression while independently checking expected diagnostics and absence of fatal errors.",
  "semantic_role": "repair-validation",
  "owner_role": "duplicate-regression-tests",
  "operation": "Execute bound public regression commands and callback/coordinate probes; record statuses and outputs without changing tracked code or tests.",
  "kind": "validate",
  "inputs": [
    {"name": "repaired-preprocessing", "semantic_role": "preprocessing-change", "artifact_kind": "patch", "language": "Python", "scope": "current-checkout", "phase": "repair", "state": "edited"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "public-validation", "artifact_kind": "test-observation", "language": "Python", "scope": "current-checkout", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "role:duplicate-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "complete-source-parsed-before-suppression", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-expose-fatal-output", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "True only after every required bound public check passes."}
  ],
  "preserves": [
    {"key": "suppression-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-coordinate-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enabled-comparison-and-exclusion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "callback-free-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-public-regressions",
      "instruction": "Run current-bound public duplicate-code tests with secondary parsing and parser-error visibility. Record fixture-specific statuses, expected reports, no fatal output, suppression semantics, original coordinates, structural exclusions, raw-string/docstring handling, and callback-free behavior.",
      "evidence_refs": ["pylint-dev/pylint:6301:body", "pylint-dev/pylint:6301:fix", "pylint-dev/pylint:6301:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:da14748ad2e8a043ad8319eb:edit"],
  "read_set": ["role:duplicate-preprocessing", "role:duplicate-regression-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6301:repair:1664202ba5de"],
  "evidence_refs": ["pylint-dev/pylint:6301:body", "pylint-dev/pylint:6301:fix", "pylint-dev/pylint:6301:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:da14748ad2e8a043ad8319eb"
}
```

Record failures as well as successes. Only passing observations establish the required effect. Historical assertions and later source qualification do not execute this Action.
