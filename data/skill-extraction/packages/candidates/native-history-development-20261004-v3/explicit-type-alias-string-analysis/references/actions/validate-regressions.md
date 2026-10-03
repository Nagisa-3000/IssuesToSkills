# Validate both modifications

Bind current public reproduction and repository-test commands and render their argv before execution. Empty arrays in this card mean no current command is supplied.

Run the public reproduction, the six-case matrix, and existing annotation tests. Inspect or publicly probe ordinary non-`TypeAlias` value processing. Record per-check PASS, FAIL, or UNKNOWN, diagnostics, command exit statuses, and tested scope.

A no-value case incorrectly counting an unrelated import indicates over-broad use marking. A non-marker value entering annotation processing indicates over-broad dispatch. Either failure prevents acceptance. Broader public regression checks are useful when available, but changed-test-only qualification does not imply whole-project safety.

```arex-contract-v4
{
  "id": "explicit-type-alias-string-analysis.validate",
  "intent": "Observe repair behavior and adjacent invariants after both modifications.",
  "mechanism": "Execute current public reproductions and annotation tests against the final checkout.",
  "semantic_role": "repair-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Bind and execute public oracles, refresh invalidated observations, and record scoped tri-state results.",
  "kind": "validate",
  "inputs": [
    {"name": "regression-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "regressions-present", "optional": false}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "alias-repair-validation", "artifact_kind": "report", "language": "python", "scope": "current-public-checkout", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"},
    {"key": "targeted-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-regressions-checked", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unchanged-during-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "quoted-alias-reproduction",
      "instruction": "Execute current public quoted PathLike alias and quoted function-annotation comparison; record diagnostic sets and require absence of false unused-import diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:671:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "alias-and-adjacent-regressions",
      "instruction": "Execute the current public annotation suite with all six alias cases; require no diagnostics for the four value cases and the isolated no-value case, and the expected unused import for the no-value control. Inspect or publicly probe ordinary-value dispatch and record exact validation scope.",
      "evidence_refs": ["PyCQA/pyflakes:671:regression", "PyCQA/pyflakes:671:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671"],
  "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"],
  "resource": "references/actions/validate-regressions.md",
  "package_id": "explicit-type-alias-string-analysis",
  "validation_for": ["explicit-type-alias-string-analysis.route", "explicit-type-alias-string-analysis.tests"],
  "read_set": ["role:annotated-assignment-handler", "role:annotation-regression-tests"],
  "write_set": []
}
```
