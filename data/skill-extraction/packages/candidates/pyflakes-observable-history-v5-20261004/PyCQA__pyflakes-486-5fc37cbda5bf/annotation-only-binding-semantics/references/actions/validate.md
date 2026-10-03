# Validate references and adjacent diagnostics

Bind current public commands, execute them, and preserve their actual outputs.

| Declaration/use | Historical assertion |
|---|---|
| `T: object`; bare parameter annotation `T`, no future import | `UndefinedName` |
| `T: object`; quoted parameter annotation `'T'`, no future import | No diagnostic |
| Future annotations import; declaration; both forms | No diagnostic |
| Unused module/class annotation-only declarations | No diagnostic |
| Unused function-local annotation only | No diagnostic; historical TODO |
| Local annotation followed by unused `x = 3` | One `UnusedVariable` |

Check malformed forward-annotation syntax, ordinary assignments, ordinary value reads, lookup continuation, and context restoration using current public tests or probes. These adjacent checks are motivated by the implementation and surrounding assertions; historical execution is not claimed.

Refresh invalidated binding/context observations. Missing required checks leave validation UNKNOWN; failing preservation checks prevent success. Contract effects are conditional targets, not supplied execution results.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:validate",
  "intent": "Verify corrected references and retained adjacent diagnostic behavior.",
  "mechanism": "Execute public context probes and relevant current repository regressions after the edit.",
  "semantic_role": "annotation-binding-validation",
  "owner_role": "python-analyzer-public-regression-suite",
  "operation": "Run bound public checks and report actual outcomes and coverage gaps.",
  "kind": "validate",
  "inputs": [
    {
      "name": "annotation-binding-patch",
      "semantic_role": "annotation-binding-patch",
      "artifact_kind": "source-change",
      "language": "Python",
      "scope": "current-analyzer",
      "phase": "repair",
      "state": "modified-awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "annotation-validation-report",
      "semantic_role": "annotation-validation-report",
      "artifact_kind": "test-report",
      "language": "Python",
      "scope": "current-analyzer",
      "phase": "validation",
      "state": "public-results-observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:python-analyzer-public-regression-suite",
      "value": true,
      "evaluator": "file_exists",
      "description": "The current role resolves to existing public regression resources."
    },
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "postponed-reference-matrix-validated", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-diagnostics-validated", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "bare-reference-without-postponement-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "annotation-only-is-not-runtime-value-assignment", "value": true, "evaluator": "evidence"},
    {"key": "later-unused-value-assignment-reported-once", "value": true, "evaluator": "evidence"},
    {"key": "annotation-context-restored-after-traversal", "value": true, "evaluator": "evidence"},
    {"key": "malformed-forward-annotation-diagnostics-retained", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-annotation-matrix",
      "instruction": "Execute public reproductions for bare, quoted, and future-postponed annotation-only names. Compare actual diagnostics with the historical assertion matrix and separately review ordinary value-read semantics.",
      "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-regression-suite",
      "instruction": "Execute current public tests for annotation scopes, unused declarations and assignments, malformed forward annotations, real assignments, lookup continuation, and context restoration. Record commands, exit statuses, diagnostics, and coverage gaps.",
      "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:be71c3f9e9544046d28904cd:repair"],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "read_set": ["role:python-analyzer-binding-and-annotation-owners", "role:python-analyzer-public-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```
