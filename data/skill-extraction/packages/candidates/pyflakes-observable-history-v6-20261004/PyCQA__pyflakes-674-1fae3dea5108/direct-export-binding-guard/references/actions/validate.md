# Validate the final candidate

Bind commands to the current public checkout and environment. Run the original analyzer reproduction, the new unused-import regression, and relevant existing export/import tests. Review coverage of supported direct assignment forms.

This Action does not edit source or tests. Record the exact candidate and results; subsequent edits make the validation observation stale. Coverage gaps remain UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
  "intent": "Observe crash avoidance and preservation of adjacent export/import behavior.",
  "mechanism": "Execute current public reproductions and relevant repository tests on the final candidate.",
  "semantic_role": "export-boundary-validation",
  "owner_role": "export-binding-tests",
  "operation": "Run bound public commands without editing source or tests; record candidate identity, diagnostics, results and coverage gaps.",
  "kind": "validate",
  "inputs": [
    {"name": "covered-candidate", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "covered"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "export-boundary-validation-results", "artifact_kind": "public-check-results", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "observed"}
  ],
  "preconditions": [
    {"key": "special-export-dispatch-direct-parent-only", "value": true, "evaluator": "evidence"},
    {"key": "indirect-export-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Satisfied only after current checks execute successfully and support the required behavior assurances."}
  ],
  "preserves": [
    {"key": "direct-export-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "original-crash-reproduction",
      "instruction": "Run the current analyzer on __all__, = (\"fizz\", \"buzz\"). Require no internal exception; do not infer runtime validity or require an unsupported new diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:674:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "indirect-target-unused-import",
      "instruction": "Run the public regression for import bar followed by (__all__,) = (\"foo\",). Require the unused-import diagnostic and no internal exception.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-export-import-behavior",
      "instruction": "Run relevant public export/import tests and review coverage of supported direct Assign, AugAssign and AnnAssign paths. Require preserved direct-export and ordinary unused-import behavior; mark coverage gaps UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression"
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "read_set": ["role:export-binding-dispatch", "role:export-binding-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d"
}
```
