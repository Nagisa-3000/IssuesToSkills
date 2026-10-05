# Validate behavior and preservation

Bind current public commands. Run the primary regression, reviewed adjacent extension fixtures, and ordinary neighboring tests without rewriting source or expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:validate",
  "intent": "Observe configured-extension behavior and preserved adjacent behavior after edits.",
  "mechanism": "Execute public assertions and review registration order and preserved initialization branches.",
  "semantic_role": "public-repair-validation",
  "owner_role": "public-functional-runner",
  "operation": "Render and execute current bound public checks; record collection, comparisons, skips, failures, ordering evidence and preservation results without changing source or expected output.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:public-functional-runner", "value": true, "evaluator": "file_exists"},
    {"key": "configured-extensions-registered-before-options", "value": true, "evaluator": "evidence"},
    {"key": "extension-regression-expectations-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-functional-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-option-file-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-configured-extension-regressions",
      "instruction": "Execute current primary and reviewed adjacent extension fixtures. Compare exact symbols, multiplicity, locations, messages and option-dependent behavior; record actual results and skips.",
      "evidence_refs": ["pylint-dev/pylint:4291:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-adjacent-initialization",
      "instruction": "Run ordinary neighboring public tests and public checks for absent plugin options and missing option files. Review registration order and record preservation evidence and untested branches.",
      "evidence_refs": ["pylint-dev/pylint:4291:fix", "pylint-dev/pylint:4291:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:register",
    "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:regressions"
  ],
  "source_ids": ["pylint-dev/pylint:4291:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4291:fix", "pylint-dev/pylint:4291:regression"],
  "read_set": ["role:functional-config-initializer", "role:functional-extension-fixtures", "role:public-functional-runner"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c"
}
```

Empty command arrays require current Oracle bindings. Recording execution does not imply semantic PASS. Failed or skipped required targets prevent a repair-success claim; unobserved preservation remains UNKNOWN.
