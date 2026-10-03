# Inspect the binding insertion owner

Read the current scope insertion implementation and annotation tests without modifying the checkout. Trace the reported export-use loss to replacement of an existing binding. Locate and hash current code anchors, distinguish annotation-only bindings from valued assignments, and bind the test owner.

The output is a reviewed binding map, not a claim that historical paths still exist.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
  "intent": "Establish applicability and current semantic owners.",
  "mechanism": "Trace annotation-only insertion to loss of existing binding metadata.",
  "semantic_role": "binding-overwrite-inspection",
  "owner_role": "scope-binding-insertion-owner",
  "operation": "Read current insertion and annotation classification code, inspect export-use consumers and regression facilities, and record current anchors and semantic checks without editing files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "reviewed-bindings", "semantic_role": "annotation-binding-repair-context", "artifact_kind": "binding-map", "language": "Python", "scope": "current-checkout", "phase": "review", "state": "reviewed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "binding-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "inspect-overwrite",
      "instruction": "Record whether annotation-only insertion overwrites a pre-existing export/value binding, identify the current owners, and distinguish absent-name insertion and ordinary replacement. Inspection must not alter files.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
  "read_set": ["role:scope-binding-insertion-owner", "role:annotation-binding-classifier", "role:export-use-consumer", "role:annotation-regression-test-owner"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489"
}
```

If mechanism checks are UNKNOWN, collect more public observations. If they FAIL, do not pass the reviewed context to the repair.
