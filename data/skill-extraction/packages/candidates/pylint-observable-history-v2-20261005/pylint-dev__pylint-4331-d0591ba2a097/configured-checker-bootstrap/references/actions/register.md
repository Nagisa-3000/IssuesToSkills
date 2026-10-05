# Register requested modules before applying options

Use established current APIs to obtain and normalize the explicitly configured
plugin list. Guard an absent entry. Register those modules after parsing and
before applying configuration. Preserve ordinary initialization, reporter setup,
suppression settings, and missing-file handling. Require final validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:register",
  "intent": "Honor per-fixture optional checker configuration.",
  "mechanism": "Insert guarded explicit module registration between parsing and option application.",
  "semantic_role": "bootstrap-repair",
  "owner_role": "functional-harness-bootstrap",
  "operation": "Edit the bound Python bootstrap to obtain and normalize requested plugin modules and register them before applying options, using compatible current APIs and retaining existing error handling.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "bootstrap-diagnosis", "artifact_kind": "evidence-record", "language": "Python", "scope": "functional-harness", "phase": "diagnosis", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "bootstrap", "semantic_role": "bootstrap-repair", "artifact_kind": "source-code", "language": "Python", "scope": "functional-harness", "phase": "repair", "state": "edited"}
  ],
  "preconditions": [
    {"key": "bootstrap-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-parser-loader-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:functional-harness-bootstrap", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "configured-registration-before-application", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-harness-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-config-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "public-checks-passed"],
  "oracle": [
    {
      "id": "review-order",
      "instruction": "Review the diff and current call sequence for parse, guarded requested-module registration, then option application. Confirm ordinary initialization and missing-file handling remain intact; require final public validation.",
      "evidence_refs": ["pylint-dev/pylint:4331:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4331:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4331:fix"],
  "read_set": ["role:functional-harness-bootstrap"],
  "write_set": ["role:functional-harness-bootstrap"],
  "resource": "references/actions/register.md",
  "package_id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833"
}
```

Effects are intended results until currently observed. Invalidated validation
facts are distinct from required preserved behaviors.
