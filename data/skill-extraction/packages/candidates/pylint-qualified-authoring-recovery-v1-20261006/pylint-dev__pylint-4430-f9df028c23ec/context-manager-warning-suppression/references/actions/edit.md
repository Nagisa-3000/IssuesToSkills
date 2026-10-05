# Add the immediate-frame exclusion and assertions

Require compatible current bindings and reproduced false positives. Use a shared predicate on the immediate frame. Reject unsupported frame types; recognize `__enter__` by frame name or the resolved `contextlib.contextmanager` decorator.

Guard both allocation-assignment and replaceable-call emission conditions while retaining safe inference and recognized-call filtering. Do not suppress whole classes or arbitrary descendant frames.

Add silent allocation and acquisition assertions for both supported forms. Retain ordinary positive cases and module-level allocation advice. Adjust expected output only for intended diagnostic changes and location shifts.

```arex-contract-v4
{
  "id": "workflow:verified-history:b74613551e6d8c24ed7692fa:edit",
  "intent": "Correct managed-frame false positives without weakening ordinary resource advice.",
  "mechanism": "Guard both warning paths with a shared immediate-frame predicate and encode public positive and negative assertions.",
  "semantic_role": "managed-frame-exclusion",
  "owner_role": "resource-advice-emitter",
  "operation": "Edit the bound Python checker and public regression suite to implement and assert the supported frame-local exclusion.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnostic-binding", "semantic_role": "diagnostic-binding", "artifact_kind": "owner-binding-report", "language": "Python", "scope": "resource-advice-checker", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "outputs": [
    {"name": "managed-frame-patch", "semantic_role": "managed-frame-patch", "artifact_kind": "code-and-test-diff", "language": "Python", "scope": "resource-advice-checker", "phase": "post-edit", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "emission-paths-and-frames-observed", "value": true, "evaluator": "evidence"},
    {"key": "managed-frame-false-positive-reproduced", "value": true, "evaluator": "evidence"},
    {"key": "resolved-decorator-identity-supported", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "managed-frame-advice-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-resource-advice-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-inference-filter-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-with-silence-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-exclusion-diff",
      "instruction": "Review the current diff for one immediate-frame predicate, guards on both emission paths, unchanged inference filters, and assertions for managed silence and ordinary advice. Diff review is not execution validation.",
      "evidence_refs": ["pylint-dev/pylint:4430:fix", "pylint-dev/pylint:4430:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4430:repair:f9df028c23ec"],
  "evidence_refs": ["pylint-dev/pylint:4430:fix", "pylint-dev/pylint:4430:regression"],
  "read_set": ["role:resource-advice-emitter", "role:ast-frame-classifier", "role:diagnostic-regression-suite"],
  "write_set": ["role:resource-advice-emitter", "role:diagnostic-regression-suite"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:b74613551e6d8c24ed7692fa"
}
```

Effects are intended postconditions. Mark the validation observation stale, not the behavioral assurances. Retain [validation](validate.md).
