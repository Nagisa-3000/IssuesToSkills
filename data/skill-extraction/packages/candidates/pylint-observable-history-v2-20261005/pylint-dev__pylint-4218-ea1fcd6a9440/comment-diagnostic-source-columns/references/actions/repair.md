# Repair the emission column and public expectations

Use current owner bindings, not historical file paths. Replace the column calculation only when the probe establishes the same semantic defect.

The supported rule is token start column plus one. It intentionally does not search for the first non-whitespace character after the hash. Remove an extracted match value only if it becomes unused. Preserve matching, line selection, message text, and configuration handling.

Update public regression expectations by deriving coordinates from source positions, not by accepting whatever the edited program emits. Inspect changed expectations and leave unrelated output fields untouched.

```arex-contract-v4
{
  "id": "workflow:verified-history:e90ff4df6c32dee9a7842f73:repair",
  "intent": "Correct comment-note source columns and encode the anchor in public regression expectations.",
  "mechanism": "Use comment token source start plus one instead of a matched-note index within the token.",
  "semantic_role": "source-column-repair",
  "owner_role": "comment-note-emitter",
  "operation": "Edit the bound Python emitter's column argument to use the comment token's source-start column plus one. Remove only the now-unused note extraction if applicable. Edit the bound public regression expectations to assert independently derived source columns for affected comments while retaining warning labels, lines, counts, and message strings.",
  "kind": "edit",
  "inputs": [
    {
      "name": "coordinate-review",
      "semantic_role": "comment-column-repair-context",
      "artifact_kind": "public-review-record",
      "language": "Python",
      "scope": "current-checkout-comment-note-diagnostics",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "comment-column-candidate",
      "artifact_kind": "checkout-change-record",
      "language": "Python",
      "scope": "current-checkout-comment-note-diagnostics",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "source-anchor-applicability-established", "value": true, "evaluator": "evidence"},
    {"key": "role:comment-note-emitter", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comment-note-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "comment-column-rule", "value": "token-source-start-plus-one", "evaluator": "evidence"},
    {"key": "public-column-expectations", "value": "source-anchored", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "note-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-content-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-coordinate-diff",
      "instruction": "Review the public diff against the current coordinate review. Confirm only the column derivation, unused extraction, and affected coordinate expectations change; verify the rule anchors immediately after the hash and the recognition, line, and text logic are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4218:repair:ea1fcd6a9440"],
  "evidence_refs": ["pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:e90ff4df6c32dee9a7842f73",
  "read_set": ["role:comment-note-emitter", "role:comment-note-regression-suite"],
  "write_set": ["role:comment-note-emitter", "role:comment-note-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```
