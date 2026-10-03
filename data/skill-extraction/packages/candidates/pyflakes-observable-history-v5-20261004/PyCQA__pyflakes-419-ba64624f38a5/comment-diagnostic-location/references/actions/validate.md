# Validate location and adjacent behavior

Bind and render current public test commands. Execute the line regression and relevant neighboring annotation tests. Repeat the public reported reproduction when available.

Review unchanged semantic association, parser arguments, diagnostic kind, and column propagation. The historical regression asserts a line only; do not claim historical column validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:validate",
  "intent": "Verify the repaired comment location and detect adjacent annotation regressions.",
  "mechanism": "Execute public position and neighboring annotation checks with preservation review.",
  "semantic_role": "diagnostic-position-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute bound public checks and record scoped outcomes.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation-results",
      "semantic_role": "type-comment-validation-results",
      "artifact_kind": "test-and-review-evidence",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "current",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-line-regression", "value": "added", "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-position-and-adjacent-results", "value": "recorded", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "implementation-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-comment-line",
      "instruction": "Execute the bound current public regression and verify that the invalid standalone type comment on line 2 produces the expected syntax-error diagnostic at line 2.",
      "evidence_refs": ["PyCQA/pyflakes:419:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-adjacent-annotations",
      "instruction": "Execute relevant neighboring public annotation tests and review preserved semantic association, parsing arguments, and diagnostic kind. Record actual coverage and outcomes without claiming whole-project success.",
      "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:a9e64c06fdea4cfd948ba20e:repair"],
  "read_set": ["role:type-comment-diagnostic-pipeline", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:fix", "PyCQA/pyflakes:419:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```

A failed assertion is FAIL, not permission to relax it. Unavailable execution is UNKNOWN. Refresh stale observations and keep this validation in the verification closure after repair.
