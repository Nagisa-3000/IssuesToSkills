# Validate the guarded boundary

Discover the current public analyzer entry point and test runner, then bind and render actual argv commands. Analyze the reported source without executing it as a Python program. An analyzer's ordinary diagnostic exit code is not an internal crash; inspect diagnostic output and exception status.

Execute the tuple-target regression. Run adjacent public export tests, and review or probe supported direct assignment forms and module-scope gating. Record commands, exit status, diagnostics, test counts, current anchors, tri-state results, and coverage limits.

A required FAIL or UNKNOWN blocks a success claim. If broader tests are unavailable, retain that limit explicitly. Validation must not modify tracked source/test content.

```arex-contract-v4
{
  "id": "direct-export-binding-guard.validate",
  "intent": "Validate crash avoidance and preserved direct-export and ordinary-binding behavior.",
  "mechanism": "Execute current public reproductions and regression tests and review or probe the direct-assignment and scope boundary.",
  "semantic_role": "validate-export-dispatch-repair",
  "owner_role": "export-binding-regression-tests",
  "operation": "execute-public-checks-and-review-boundary",
  "kind": "validate",
  "inputs": [
    {
      "name": "guarded-change",
      "semantic_role": "export-dispatch-repair",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "export-dispatch-validation-evidence",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-validation",
      "state": "outcomes-and-limits-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "export-dispatch-parent-compatible", "value": true, "evaluator": "evidence"},
    {"key": "indirect-export-regression-defined", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {
      "key": "current-public-validation",
      "value": "passed",
      "evaluator": "evidence",
      "description": "Expected success effect; record failed or unknown instead if any required check fails or remains unresolved."
    }
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"},
    {"key": "direct-module-export-handling", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-unused-import-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "module-scope-restriction", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-earlier-binding-branches", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "analyze-indirect-target",
      "instruction": "Statically analyze __all__, = ('fizz', 'buzz') using a bound current public analyzer command. Require completion without an internal exception, including the historical Tuple.value failure. Record normal diagnostics separately; no new invalid-assignment warning is required.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "run-export-regressions",
      "instruction": "Execute the current tuple-target regression and require the unused-import diagnostic for bar. Run adjacent public export tests and review or probe supported Assign, AugAssign, AnnAssign handling, module-scope gating, earlier branches and fallback. Record exact commands, results and coverage limits.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "direct-export-binding-guard",
  "validation_for": ["direct-export-binding-guard.guard-and-regress"],
  "read_set": [
    "role:name-store-binding-dispatcher",
    "role:export-binding-handler",
    "role:export-binding-regression-tests"
  ],
  "write_set": []
}
```
