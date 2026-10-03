# Validate non-crashing analysis and preserved diagnostics

Bind commands to the current public test runner. Run the regression expecting an unused-import diagnostic, the original public reproduction or its faithful current adaptation, and the relevant doctest test file.

Check both branches of the guard. For the absent-module-binding branch, use current public tests or a public probe that requires the existing synthetic `_` semantics. Do not infer branch preservation solely from a passing collision regression.

The supplied historical regression is an assertion, not a recorded historical run. The later changed-test-only qualification does not authorize claiming whole-project success.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:validate",
  "intent": "Observe that the repair prevents the crash while preserving adjacent doctest behavior and diagnostics.",
  "mechanism": "Execute the targeted regression, public reproduction, and neighboring doctest checks with both guard branches covered.",
  "semantic_role": "repair-validation",
  "owner_role": "doctest-regression-tests",
  "operation": "Run bound public checks and record results without editing tracked source or tests; refresh validation observations after the repair.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "conditional-binding-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "conditional-binding-validation",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "public-checks-passed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "synthetic-insertion-guarded", "value": true, "evaluator": "evidence"},
    {"key": "module-underscore-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "role:doctest-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unused-module-import-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-module-underscore-placeholder-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-doctest-analysis-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "module-underscore-regression",
      "instruction": "Run the current regression with an unused module import aliased to underscore and a pass doctest. Require no traceback and the expected unused-import diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:421:regression", "PyCQA/pyflakes:421:body"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "doctest-adjacent-behavior",
      "instruction": "Run the relevant current doctest test file and inspect or publicly probe the no-module-underscore branch. Require retained synthetic underscore availability and unchanged adjacent diagnostics. This is a current preservation check, not a claim of historical execution.",
      "evidence_refs": ["PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:regression"],
  "validation_for": ["workflow:verified-history:c76d35c9a48e360887b3c443:repair"],
  "read_set": ["role:doctest-scope-initializer", "role:doctest-regression-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

Emit a passed validation output only after all bound checks pass. Missing commands, unavailable tests, or incomplete branch checks are UNKNOWN; failures reject completion.
