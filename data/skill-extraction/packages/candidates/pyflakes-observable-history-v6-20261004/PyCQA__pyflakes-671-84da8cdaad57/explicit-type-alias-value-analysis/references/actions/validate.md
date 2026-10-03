# Validate alias uses and adjacent behavior

Bind public commands to the current checkout and supported Python environment. Run the original alias-string reproduction and function-annotation control, then the regression suite covering the changed owner.

Required alias assertions:

- Direct and string values both recognize the imported type.
- Module and class scope variants both work.
- A valueless `TypeAlias` declaration is accepted.
- An unrelated import remains unused when the declaration has no value.

Also check the preserved ordinary-expression branch and adjacent annotation diagnostics. The ordinary-string negative control is a current preservation probe derived from the retained normal-expression branch; it is not represented as an added historical regression test.

Only emit the validated output after all bound required checks pass. Report partial execution and unsupported environments explicitly. The historical assertion set is not a substitute for execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:validate",
  "intent": "Observe the repaired alias behavior and the preserved assignment/annotation boundaries.",
  "mechanism": "Execute public reproductions and repository regression checks against the edited candidate.",
  "semantic_role": "alias-dispatch-public-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Run bound public analysis and test commands, record diagnostics and test results, and review the preservation boundary; do not modify implementation or tests.",
  "kind": "validate",
  "inputs": [
    {
      "name": "alias-dispatch-candidate",
      "semantic_role": "alias-dispatch-change",
      "artifact_kind": "implementation-and-regression-diff",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "alias-dispatch-validation",
      "semantic_role": "alias-dispatch-verification",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "post-validation",
      "state": "required-public-checks-passed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "recognized-alias-value-annotation-dispatch",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "alias-regression-assertions-added",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-assignment-value-semantics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "valueless-assignment-use-accounting-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "existing-annotation-analysis-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "public-alias-reproduction",
      "instruction": "Run the current public alias-string reproduction and function-annotation control. Confirm the referenced imported type is not reported unused; run an ordinary-string negative control to ensure strings are not globally treated as annotations.",
      "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "alias-and-adjacent-regressions",
      "instruction": "Run the current annotation regression suite with module/class direct/string aliases, valueless declarations, and the truly unused-import case. Inspect adjacent annotation failures and record the scope actually executed.",
      "evidence_refs": ["PyCQA/pyflakes:671:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671:repair:84da8cdaad57"],
  "evidence_refs": ["PyCQA/pyflakes:671:body", "PyCQA/pyflakes:671:fix", "PyCQA/pyflakes:671:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "read_set": [
    "role:annotated-assignment-analysis",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:d3771ee821e88935b9bcf1ce:edit"
  ]
}
```
