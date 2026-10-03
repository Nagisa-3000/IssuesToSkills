# Resolve the nearest import origin

Replace only the spelling-based module classification for an attribute whose receiver is a name:

1. Search scopes from innermost to outermost.
2. Stop at the first binding for that name.
3. Accept only an import whose full module identity belongs to the existing supported typing-module set.
4. Return false for absent, non-import, or unrelated-import bindings.
5. Retain the attribute-shape guard, helper-name predicate, and direct-name branch.

Never search past a shadowing binding. Assignment aliases and chained attributes are outside this edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
  "intent": "Recognize module-qualified helpers independently of local import spelling.",
  "mechanism": "Classify the imported origin of the nearest lexical receiver binding.",
  "semantic_role": "binding-origin-repair",
  "owner_role": "typing-helper-recognizer",
  "operation": "Replace receiver spelling classification with nearest-scope supported-import recognition.",
  "kind": "edit",
  "inputs": [
    {"name": "located_snapshot", "semantic_role": "recognition-repair-snapshot", "artifact_kind": "checkout", "language": "python", "scope": "helper-recognition-and-tests", "phase": "repair", "state": "located", "optional": false}
  ],
  "outputs": [
    {"name": "corrected_snapshot", "semantic_role": "recognition-repair-snapshot", "artifact_kind": "checkout", "language": "python", "scope": "helper-recognition-and-tests", "phase": "repair", "state": "origin-resolution-edited", "optional": false}
  ],
  "preconditions": [
    {"key": "role:typing-helper-recognizer", "value": true, "evaluator": "symbol_exists"},
    {"key": "compatible-scope-import-metadata", "value": true, "evaluator": "evidence"},
    {"key": "spelling-based-recognition-gap", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "module-helper-origin-resolution", "value": "nearest-supported-import", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-name-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "helper-name-predicate-preserved", "value": true, "evaluator": "evidence"},
    {"key": "attribute-shape-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nearest-binding-controls-recognition", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-bindings-not-typing", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-origin-resolution",
      "instruction": "Review the bound current diff for inner-to-outer lookup, first-binding termination, supported import-origin membership, and preserved recognition branches. Confirm behavior with the explicit validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:fix"],
  "read_set": ["role:typing-helper-recognizer", "role:lexical-import-bindings"],
  "write_set": ["role:typing-helper-recognizer"],
  "invalidates": ["current-helper-diagnostics", "current-public-validation"],
  "resource": "references/actions/resolve-import-origin.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

Effects are expected postconditions until observed. [Validation](validate-recognition.md) is mandatory after this modification.
