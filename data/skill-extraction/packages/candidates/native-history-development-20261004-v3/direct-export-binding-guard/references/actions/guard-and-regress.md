# Guard dispatch and add a regression

Edit only after fresh current inspection establishes the mismatch and fallback.

Restrict special export binding to compatible immediate assignment parents. The historical set was `ast.Assign`, `ast.AugAssign`, and `ast.AnnAssign`; confirm those current representations. Retain the name check, module-scope check, earlier branches, and ordinary fallback.

Add a public regression analyzing:

```python
import bar
(__all__,) = ("foo",)
```

Require an unused-import diagnostic. Do not execute the snippet as a program or invent an invalid-assignment diagnostic. Mark the resulting change unvalidated and stale preservation observations for rechecking.

```arex-contract-v4
{
  "id": "direct-export-binding-guard.guard-and-regress",
  "intent": "Constrain assignment-only export dispatch and define an indirect-target regression.",
  "mechanism": "Add an immediate-parent type guard to existing special dispatch and add an unused-import assertion for tuple-target __all__.",
  "semantic_role": "repair-export-dispatch-boundary",
  "owner_role": "name-store-binding-dispatcher",
  "operation": "guard-special-dispatch-and-add-regression",
  "kind": "edit",
  "inputs": [
    {
      "name": "binding-boundary",
      "semantic_role": "verified-export-dispatch-context",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "mechanism-and-owners-observed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "role:name-store-binding-dispatcher", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:export-binding-regression-tests", "value": true, "evaluator": "file_exists"},
    {
      "key": "historical-parent-mismatch-present",
      "value": true,
      "evaluator": "evidence",
      "description": "Fresh current evidence shows indirect parents can enter assignment-only export handling."
    },
    {"key": "ordinary-binding-fallback-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "export-dispatch-parent-compatible", "value": true, "evaluator": "evidence"},
    {"key": "indirect-export-regression-defined", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-module-export-handling", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-unused-import-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "module-scope-restriction", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-earlier-binding-branches", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-guard-and-regression",
      "instruction": "Review the current source/test diff for a compatible immediate-parent guard, retained name and module checks, unchanged earlier branches and fallback, and a tuple-target regression expecting the unused-import diagnostic. Record review evidence; execution validation remains mandatory.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674"],
  "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "resource": "references/actions/guard-and-regress.md",
  "package_id": "direct-export-binding-guard",
  "read_set": [
    "role:name-store-binding-dispatcher",
    "role:export-binding-handler",
    "role:export-binding-regression-tests"
  ],
  "write_set": [
    "role:name-store-binding-dispatcher",
    "role:export-binding-regression-tests"
  ],
  "invalidates": [
    "current-public-validation",
    "direct-module-export-handling",
    "ordinary-unused-import-analysis",
    "module-scope-restriction",
    "existing-earlier-binding-branches"
  ]
}
```

Effects and preservation predicates are expected requirements, not observed execution results.
