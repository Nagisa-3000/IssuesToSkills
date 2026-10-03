# Repair the carrier and add public regression coverage

When current evidence confirms this mechanism, pass a lightweight carrier exposing the actual comment's `lineno` and `col_offset` as the diagnostic node. Use an existing compatible carrier if available; otherwise introduce the minimal coordinate-only object.

Do not globally mutate AST positions or change annotation parsing to fix diagnostic placement. Preserve the semantic statement association, parsed text, explicit parser coordinates, and diagnostic kind.

Add a public two-line fixture: assignment first, invalid standalone type comment second. Expect the type-comment syntax-error diagnostic and explicitly assert line 2.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:repair",
  "intent": "Use actual comment coordinates for diagnostics without changing annotation semantics.",
  "mechanism": "Substitute a coordinate-only diagnostic carrier and add a line-number regression.",
  "semantic_role": "diagnostic-position-repair",
  "owner_role": "type-comment-diagnostic-pipeline",
  "operation": "Edit the bound diagnostic carrier and public annotation regression tests.",
  "kind": "edit",
  "inputs": [
    {
      "name": "located-context",
      "semantic_role": "type-comment-position-context",
      "artifact_kind": "code-and-probe-evidence",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "current",
      "state": "located",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "patched-context",
      "semantic_role": "type-comment-position-context",
      "artifact_kind": "code-and-probe-evidence",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "current",
      "state": "patched",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:type-comment-diagnostic-pipeline", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "statement-carrier-causes-comment-location-mismatch", "value": true, "evaluator": "evidence"},
    {"key": "actual-comment-coordinates-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "diagnostic-carrier", "value": "actual-comment-coordinates", "evaluator": "evidence"},
    {"key": "public-line-regression", "value": "added", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "comment-semantic-association", "value": "unchanged", "evaluator": "evidence"},
    {"key": "annotation-parsing-and-message-kind", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-carrier-change",
      "instruction": "Review the current diff to confirm that actual comment line and column supply the diagnostic carrier, semantic association and parsing arguments remain unchanged, and the public regression asserts the invalid comment's line 2.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:type-comment-diagnostic-pipeline", "role:annotation-regression-tests"],
  "write_set": ["role:type-comment-diagnostic-pipeline", "role:annotation-regression-tests"],
  "invalidates": ["current-diagnostic-position-results", "current-annotation-test-results"],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```

Declared effects are intended postconditions, not observed execution results. The modifying operation retains the explicit [validation Action](validate.md).
