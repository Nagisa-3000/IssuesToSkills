# Inspect initialization

Read current public initialization and fixtures without modifying source or expectations. Distinguish omitted registration from unavailable imports, incorrect symbols, or checker-analysis defects.

```arex-contract-v4
{
  "id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c:inspect",
  "intent": "Determine whether configured extension registration is omitted before option application.",
  "mechanism": "Trace the current configuration initialization path against the public reproduction.",
  "semantic_role": "initialization-diagnosis",
  "owner_role": "functional-config-initializer",
  "operation": "Locate initializer, loader, list helper and fixture owners; record anchored read/register/apply ordering and unresolved facts without changing source or fixtures.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "initialization-assessment-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-functional-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-option-file-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-initialization",
      "instruction": "Record current anchors for configuration reading, list parsing, loader invocation or absence, and option application. Record import availability separately. Confirm source and fixture hashes are unchanged by probing.",
      "evidence_refs": ["pylint-dev/pylint:4291:body", "pylint-dev/pylint:4291:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4291:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4291:body", "pylint-dev/pylint:4291:fix"],
  "read_set": ["role:functional-config-initializer", "role:extension-module-loader", "role:config-list-normalizer", "role:functional-extension-fixtures"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:8cca50f66c7ae1d6c7d7631c"
}
```

Unknown bindings authorize further public probes, not presumed historical bindings or edits.
