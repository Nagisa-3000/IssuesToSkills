# Validate corrected and preserved diagnostics

Execute current-bound public checks. Compare diagnostic presence and absence; a zero exit alone may be insufficient for fixtures intentionally emitting messages.

Exercise required interpreter branches where available. A modern-runtime pass does not establish pre-3.9 fallback coverage.

```arex-contract-v4
{
  "id": "workflow:verified-history:611e9bc5eaac38ef599b59a7:validate",
  "intent": "Observe corrected behavior and preserved adjacent diagnostics after editing.",
  "mechanism": "Run positive and negative public diagnostic checks with explicit runtime-branch coverage.",
  "semantic_role": "ordering-validation",
  "owner_role": "assignment-expression-regressions",
  "operation": "Execute current-bound public regression commands and report-derived examples. Compare actual diagnostics with expected messages for f-string and conditional-expression variants, genuine earlier reads, and unrelated controls. Record versions, branches exercised, failures, skips, and untested branches. Do not edit tracked resources.",
  "kind": "validate",
  "inputs": [
    {
      "name": "ordering-candidate",
      "semantic_role": "assignment-expression-ordering-candidate",
      "artifact_kind": "checkout-change",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "ordering-validation",
      "semantic_role": "assignment-expression-ordering-validation",
      "artifact_kind": "test-observation",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "checks-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "ordering-repair-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-controls-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-earlier-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-ordering-regressions",
      "instruction": "Execute the current public assignment-expression diagnostic suite. Require no false used-before-assignment for supported earlier-binding cases, retained messages for genuine earlier reads, and retained unrelated expected diagnostics. Record exit status and exact message comparisons.",
      "evidence_refs": ["pylint-dev/pylint:4238:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "run-multiline-reproduction",
      "instruction": "Execute single-line and multiline report-derived examples with the current analyzer. Inspect runtime and AST branch coverage. Confirm no false used-before-assignment in applicable ordinary, annotated, and augmented assignments. Mark unavailable required branches UNKNOWN, not passed.",
      "evidence_refs": ["pylint-dev/pylint:4238:body", "pylint-dev/pylint:4238:fix", "pylint-dev/pylint:4238:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4238:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:4238:body", "pylint-dev/pylint:4238:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:611e9bc5eaac38ef599b59a7",
  "validation_for": ["workflow:verified-history:611e9bc5eaac38ef599b59a7:repair"],
  "read_set": ["role:assignment-use-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "write_set": []
}
```

Recorded observations may include FAIL or UNKNOWN. The freshness effect is not itself a passing assurance; all required behavioral and oracle checks must independently pass before claiming public repair success.
