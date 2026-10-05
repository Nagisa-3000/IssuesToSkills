# Validate target and adjacent behavior

Bind and render current public Oracle commands before execution. Historical commands require adaptation and are not current authority.

Test bare names in supported current styles, supported escaped names, and existing supported starred spellings. Include genuine omissions, unrelated extra names, ordinary parameters, and exemptions. Inspect diagnostics rather than exit status alone.

The historical assertions cover bare kwargs in Google and NumPy, bare args/kwargs in Sphinx, and escaped args in Google. Broader current assurance requires broader current public checks, not extrapolation from qualification.

```arex-contract-v4
{
  "id": "workflow:verified-history:8f01015f3fde403e97d30645:validate",
  "intent": "Observe repaired behavior and preserved adjacent diagnostics.",
  "mechanism": "Execute public style-specific reproductions and repository regression controls.",
  "semantic_role": "post-edit-public-validation",
  "owner_role": "documentation-checker-tests",
  "operation": "Run bound public oracles, retain outputs, refresh stale parsed-name observations, and reject failed target cases or negative controls.",
  "kind": "validate",
  "inputs": [
    {"name": "repair-candidate", "semantic_role": "variadic-documentation-repair-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "documentation-parameter-checker", "phase": "post-edit", "state": "awaiting-public-validation"}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "variadic-documentation-validation", "artifact_kind": "public-test-report", "language": "python", "scope": "documentation-parameter-checker", "phase": "post-validation", "state": "observed-with-scope"}
  ],
  "preconditions": [
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-parsed-name-observation", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-parameters-and-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "string-literal-warning-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-supported-variadic-spellings",
      "instruction": "Execute current public cases for supported bare args/kwargs and escaped names. Inspect extracted names and assert absence of false missing/differing diagnostics; keep literal warnings distinct.",
      "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent-documentation-diagnostics",
      "instruction": "Execute current public regression tests and controls: genuine omissions still warn, unrelated names still differ, and ordinary parameters, exemptions, and existing supported spellings remain correct. Confirm string-literal warning behavior was not suppressed. Record exact scope.",
      "evidence_refs": ["pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:8f01015f3fde403e97d30645:repair"],
  "read_set": ["role:documentation-name-parser", "role:documentation-parameter-comparator", "role:documentation-checker-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5406:repair:3b744d180e5e"],
  "evidence_refs": ["pylint-dev/pylint:5406:body", "pylint-dev/pylint:5406:fix", "pylint-dev/pylint:5406:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:8f01015f3fde403e97d30645"
}
```
