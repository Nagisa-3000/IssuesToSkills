# Validate target and preserved behavior

Bind current public harness commands, render them, execute them, and record diagnostics and exit status. No historical executable command or current execution result is supplied.

Validate:
- the reported expression `Annotated[int, '>1']` has no metadata forward-syntax error;
- `Annotated['integer']` and `Annotated['integer', 1]` retain missing forward-type diagnostics;
- `Annotated[int, '> 0']` has no diagnostic;
- `Union[Annotated['int', '>0'], 'integer']` retains the outer missing-type diagnostic without a metadata syntax error;
- existing `Literal`, fallback and generic typing behavior survives;
- ordinary metadata expressions remain checked;
- enclosing annotation state is restored, including relevant exceptional traversal paths;
- all supported AST slice layouts are covered by execution or explicit review, with untested configurations disclosed.

The final three obligations extend current validation beyond the four supplied historical assertions; they are not claims of historical execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate",
  "intent": "Observe target correctness and preserved neighboring behavior.",
  "mechanism": "Run public reproductions and current annotation regression coverage, supplemented by state and AST-layout review.",
  "semantic_role": "repair-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute bound public checks and review coverage; record actual outcomes, failures and untested configurations without source edits. Establish the success effect only when target and preservation checks pass.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "annotation-boundary-candidate",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "annotation-boundary-validation",
      "artifact_kind": "test-results",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "public-oracle-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "target-and-preservation-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "type-reference-checking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enclosing-annotation-state-preserved", "value": true, "evaluator": "evidence"},
    {"key": "literal-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-expression-checking-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotation-regressions",
      "instruction": "Execute bound public reproductions and repository annotation checks. Verify metadata syntax-error suppression, retained missing-type diagnostics, Literal and fallback behavior, ordinary metadata expression checking and scoped restoration. Record commands, exit statuses, failures and AST/interpreter coverage limits.",
      "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair"],
  "read_set": [
    "role:annotation-subscript-visitor",
    "role:annotation-state-manager",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6"
}
```

A fresh observed result may be FAIL. Freshness alone cannot establish the success effect or any preservation assurance. Stop and report failures rather than marking intended effects as achieved.
