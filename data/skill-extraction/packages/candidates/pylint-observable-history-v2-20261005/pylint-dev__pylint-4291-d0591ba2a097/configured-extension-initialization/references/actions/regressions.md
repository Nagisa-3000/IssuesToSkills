# Add public extension regressions

Pair source, per-test configuration, and exact expected output. Exercise an extension-owned option and review adjacent extension-enabled fixtures.

```arex-contract-v4
{
  "id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:regressions",
  "intent": "Expose omitted extension registration through public functional assertions.",
  "mechanism": "Add configured-extension fixtures and diagnostically justified adjacent expectations.",
  "semantic_role": "extension-regression-coverage",
  "owner_role": "functional-extension-fixtures",
  "operation": "Create or adapt source/configuration/output fixtures requesting a real extension and setting its option. Assert exact diagnostic identities, counts, locations and messages. Review adjacent extension fixtures and add only justified expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "initialization-assessment",
      "semantic_role": "initialization-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-functional-harness",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:functional-extension-fixtures", "value": true, "evaluator": "file_exists"},
    {"key": "public-extension-diagnostic-identities-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "extension-regression-expectations-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-functional-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-option-file-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-public-expectations",
      "instruction": "Review source/configuration/output consistency against public diagnostic definitions. Verify counts, locations and messages, and justify adjacent changes rather than blindly accepting generated output.",
      "evidence_refs": ["pylint-dev/pylint:4291:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4291:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4291:body", "pylint-dev/pylint:4291:regression"],
  "read_set": ["role:public-functional-runner", "role:extension-module-loader"],
  "write_set": ["role:functional-extension-fixtures"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c"
}
```

Historically, the primary fixture asserts four singular `bad-builtin` diagnostics; the adjacent fixture asserts four return/yield documentation diagnostics. These are source-specific examples, not universal messages. Retain [validation](validate.md) after fixture edits.
