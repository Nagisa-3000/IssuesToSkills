# Guard specialized metadata access

In the current name-based special-decorator recognizer, retain the name-exists check. Insert the appropriate import-binding type check before the import full-name comparison. Preserve short-circuit order so ordinary assignment bindings cannot reach specialized metadata access.

The historical realization checked `ImportationFrom` before comparing `fullName` to `typing.overload`. Reuse those names only if current inspection confirms the same owners. Do not replace all decorator recognition with a broad “has attribute” heuristic, and do not alter an adjacent attribute-based branch without evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:guard",
  "intent": "Prevent non-import bindings from reaching import-specific metadata in special-decorator detection.",
  "mechanism": "Insert a binding-type predicate into a short-circuit conjunction before the metadata comparison.",
  "semantic_role": "binding-type-guard-repair",
  "owner_role": "special-decorator-recognizer",
  "operation": "Edit only the confirmed name-resolution condition to require the appropriate import-binding type before its full-name metadata is read.",
  "kind": "edit",
  "inputs": [
    {"name": "located-repair-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "located", "optional": false}
  ],
  "outputs": [
    {"name": "guarded-repair-state", "semantic_role": "overload-detection-repair", "artifact_kind": "code_bundle", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "guarded", "optional": false}
  ],
  "preconditions": [
    {"key": "unsafe-binding-access-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "import-binding-type-owns-metadata", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "import-metadata-access-type-guarded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-import-overload-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-short-circuit-guard",
      "instruction": "Review the current diff: scope membership precedes the binding-type check, which precedes specialized metadata access; unrelated decorator branches remain unchanged.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:special-decorator-recognizer", "role:scope-binding-types"],
  "write_set": ["role:special-decorator-recognizer"],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```
