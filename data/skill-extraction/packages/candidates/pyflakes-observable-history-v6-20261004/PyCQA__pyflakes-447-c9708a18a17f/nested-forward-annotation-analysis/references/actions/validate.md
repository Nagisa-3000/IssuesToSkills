# Validate nested annotations and adjacent behavior

Bind public commands to the current checkout's analyzer and test runner. No command was supplied as a historical execution record, so command arrays below remain empty until current binding.

Run the original reproduction, then regression tests covering:

- `Optional['Queue[str]']` in a return annotation and the reported parameter form.
- `"Optional['Queue[str]']"` to exercise nested strings during deferred processing.
- `from __future__ import annotations` with a partially quoted annotation on supported Python versions.
- `Literal['some string']` imported from each supported typing provider and `Literal['some string', 'foo bar']`.
- Qualified `typing_extensions.overload` alongside existing bare overload coverage.

Also run current public probes for ordinary runtime strings, nearest-scope binding recognition, context restoration, and supported string/non-string AST representations. Those are current validation obligations derived from implementation boundaries, not additional claimed historical regression assertions.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:validate",
  "intent": "Observe target repair behavior and preservation of adjacent analyzer behavior.",
  "mechanism": "Public reproduction plus annotation, Literal, overload, and deferred-analysis regression checks.",
  "semantic_role": "annotation-repair-validation",
  "owner_role": "python-annotation-regression-tests",
  "operation": "Execute current bound public probes and repository tests without source edits; record commands, diagnostics, results and scope limits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "nested-annotation-repair-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "nested-annotation-public-validation",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "results-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "regression-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "literal-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "existing-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "analysis-phase-integrity-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-reproduction",
      "instruction": "Run the current public original reproduction and confirm that Queue and Optional are recognized as used. Compare the fully quoted form and record actual analyzer output.",
      "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent-regressions",
      "instruction": "Run current public annotation regression tests and boundary probes for Literal strings, nested deferred strings, postponed annotations, overloads, runtime strings, binding recognition, and supported AST nodes. Record failures and unexecuted cases explicitly.",
      "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:b2b64a5ca411f99a2e3c45e0:edit"],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
  "read_set": ["role:python-static-analysis-annotation-traversal", "role:python-static-analysis-deferred-runner", "role:python-typing-binding-recognition", "role:python-annotation-regression-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0"
}
```

An observed result may be FAIL. `public-validation-observed` denotes fresh execution evidence, not passing acceptance. Declare repair success only when the target and preservation checks pass within the recorded scope.
