# Register configured modules before applying options

Use existing current loader and normalization APIs. Preserve absent-plugin-option behavior and missing-file handling.

```arex-contract-v4
{
  "id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:register",
  "intent": "Register extension modules before applying extension-owned options.",
  "mechanism": "Insert guarded normalized registration between configuration reading and application.",
  "semantic_role": "configured-extension-registration",
  "owner_role": "functional-config-initializer",
  "operation": "After reading per-test configuration, check for its plugin-list option. If present, normalize its value using the existing helper and invoke the existing module loader. Apply configuration afterward and retain surrounding missing-file handling.",
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
    {"key": "role:functional-config-initializer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:extension-module-loader", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:config-list-normalizer", "value": true, "evaluator": "symbol_exists"},
    {"key": "registration-stage-omitted", "value": true, "evaluator": "evidence"},
    {"key": "current-loader-supports-pre-application-registration", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "configured-extensions-registered-before-options", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-functional-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-option-file-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-registration-order",
      "instruction": "Review the diff and public trace for read, guarded normalized registration, then option application. Verify the absent-option branch and retained missing-file handling.",
      "evidence_refs": ["pylint-dev/pylint:4291:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4291:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4291:fix"],
  "read_set": ["role:extension-module-loader", "role:config-list-normalizer"],
  "write_set": ["role:functional-config-initializer"],
  "resource": "references/actions/register.md",
  "package_id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c"
}
```

Effects remain expected until observed. Retain [validation](validate.md) after this edit even if adequate regression fixtures already exist. Do not change checker analysis to compensate for missing harness registration.
