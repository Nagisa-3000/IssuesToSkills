# Validate the guard and adjacent recognition

Run the adapted public regression through the current repository's test harness. Confirm completion without a metadata-access failure and exactly two unused-redefinition diagnostics.

Run available public checks for actual from-import overload decorators and the neighboring attribute-form overload branch. Review the patch to ensure the latter branch has not changed. Missing current checks leave the corresponding preservation claim UNKNOWN; they do not justify reporting success.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:validate",
  "intent": "Observe corrected ordinary-decorator handling and preserved overload recognition.",
  "mechanism": "Execute the focused regression and adjacent public tests, then review the branch boundary.",
  "semantic_role": "binding-type-guard-validation",
  "owner_role": "decorator-recognition-tests",
  "operation": "Run current public regression and preservation checks and record results.",
  "kind": "validate",
  "inputs": [
    {
      "name": "guarded-recognizer-change",
      "semantic_role": "guarded-recognizer-change",
      "artifact_kind": "patch",
      "language": "Python",
      "scope": "overload-decorator-recognizer-and-tests",
      "phase": "post-edit",
      "state": "guard-and-regression-added",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "binding-type-guard-validation-results",
      "artifact_kind": "test-and-review-record",
      "language": "Python",
      "scope": "overload-decorator-recognizer-and-tests",
      "phase": "post-validation",
      "state": "results-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "guard-and-regression", "value": "present", "evaluator": "evidence"},
    {"key": "role:decorator-recognition-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "decorator-test-results", "value": "observed", "evaluator": "evidence"},
    {"key": "overload-recognition-results", "value": "observed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "ordinary-decorator-regression",
      "instruction": "Execute the public regression with the locally assigned x and y decorators and three definitions of t. Require no metadata-access exception and exactly two unused-redefinition diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:422:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-overload-preservation",
      "instruction": "Run available current public tests for from-import and attribute-form overload recognition, and review that the attribute-form branch is unchanged. Record missing coverage as UNKNOWN; the historical diff alone is not a current execution result.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:314f3449f8ccd1beab92c625:repair"],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
  "read_set": ["role:overload-decorator-recognizer", "role:decorator-recognition-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```

Empty command arrays are unbound historical guidance, not executable commands. Bind and render current public argv commands before running validation.
