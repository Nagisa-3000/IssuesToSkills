# Separate coordinates from association

After a PASS probe, introduce or reuse a lightweight object carrying the comment's `lineno` and `col_offset`. Use it only at the diagnostic-position argument of the deferred annotation handler.

Preserve the parsed text, explicit coordinate arguments, diagnostic class, and semantic comment association. In the current annotation test owner, add an assignment on line 1 followed by a malformed type comment on line 2. Assert the intended syntax diagnostic and its line.

These are conditional current operations supported by the historical diff. Their effects require subsequent observation; they are not already verified. This Action always retains the [validation Action](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:edit",
  "intent": "Correct malformed type-comment diagnostic locations.",
  "mechanism": "Replace only the diagnostic-position argument with a comment-coordinate carrier and add a focused regression.",
  "semantic_role": "diagnostic-position-repair",
  "owner_role": "type-comment-processing-owner",
  "operation": "Add or reuse a carrier exposing lineno and col_offset, pass the comment coordinates through it to the deferred annotation diagnostic handler, and add a line-2 malformed-comment regression in the bound annotation test owner.",
  "kind": "edit",
  "inputs": [
    {
      "name": "confirmed-path",
      "semantic_role": "diagnostic-location-path",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "pre-edit",
      "state": "compatible-mismatch-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "modified-owners",
      "semantic_role": "diagnostic-location-repair",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "post-edit",
      "state": "pending-validation"
    }
  ],
  "preconditions": [
    {"key": "position-carrier-compatibility-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:type-comment-processing-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-diagnostic-consumer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:type-annotation-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "comment-location-reporting", "value": "corrected", "evaluator": "evidence"},
    {"key": "line-two-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "semantic-comment-association-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-position-only-change",
      "instruction": "Review the current diff for comment-coordinate assignment, replacement of only the diagnostic-position argument, unchanged parsing inputs and diagnostic class, unchanged semantic association, and a regression asserting the intended syntax diagnostic at line 2.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
  "read_set": [
    "role:type-comment-processing-owner",
    "role:annotation-diagnostic-consumer",
    "role:type-annotation-regression-tests"
  ],
  "write_set": [
    "role:type-comment-processing-owner",
    "role:type-annotation-regression-tests"
  ],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```
