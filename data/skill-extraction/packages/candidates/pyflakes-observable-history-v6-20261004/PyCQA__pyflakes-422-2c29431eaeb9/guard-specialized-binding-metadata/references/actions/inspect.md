# Inspect binding and recognizer semantics

Read the current recognizer, scope-binding classes, and relevant tests without modifying files. Establish whether an ordinary assignment binding can reach import-specific metadata access. Confirm the import-binding category actually owns the metadata and that conjunction evaluation will short-circuit before access.

A vague release-failure title or CI URL is insufficient by itself. Record current anchors and semantic checks; do not infer current paths from historical ones.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:inspect",
  "intent": "Determine whether the historical guard mechanism applies to the current recognizer.",
  "mechanism": "Read the name-resolution branch and binding hierarchy to identify unguarded specialized metadata access.",
  "semantic_role": "binding-access-diagnosis",
  "owner_role": "special-decorator-recognizer",
  "operation": "Read current public code and tests, locate semantic owners, and record the binding-type and short-circuit checks without changing checkout state.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "located-repair-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "located", "optional": false}
  ],
  "preconditions": [
    {"key": "recognizer-owner-exists", "value": true, "evaluator": "symbol_exists", "description": "role:special-decorator-recognizer"},
    {"key": "binding-owner-exists", "value": true, "evaluator": "symbol_exists", "description": "role:scope-binding-types"}
  ],
  "effects": [
    {"key": "unsafe-binding-access-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-owner-bindings-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-import-overload-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-binding-access",
      "instruction": "Review current public anchors to confirm that non-import bindings can reach specialized metadata access and that the proposed import-binding class owns that metadata. Verify this probe made no edits.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:special-decorator-recognizer", "role:scope-binding-types", "role:decorator-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```
