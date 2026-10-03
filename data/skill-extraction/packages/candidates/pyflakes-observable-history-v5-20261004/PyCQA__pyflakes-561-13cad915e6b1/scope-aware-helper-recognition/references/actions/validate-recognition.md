# Validate recognition and preserved behavior

Bind and render public commands for the current checkout. Execute the added regression and relevant annotation suite. Record the pinned base, command argv, results, and tested scope.

Publicly probe or review canonical imports, aliases, nearest-binding shadowing, unrelated imports, absent bindings, direct-name handling, and helper-name filtering. These are preservation checks inferred from the implementation boundary, not invented historical assertions. A failing or unavailable required check prevents PASS.

When relevant, execute the reported Literal reproduction separately. Otherwise record it as not applicable; do not infer Literal coverage from overload coverage.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate",
  "intent": "Observe edited recognition and preservation boundaries using current public checks.",
  "mechanism": "Execute aliased overload and adjacent annotation tests and inspect or probe import-origin boundaries.",
  "semantic_role": "recognition-validation",
  "owner_role": "typing-annotation-regressions",
  "operation": "Run bound public checks and record actual tri-state outcomes with scope limits.",
  "kind": "validate",
  "inputs": [
    {"name": "test_ready_snapshot", "semantic_role": "recognition-repair-snapshot", "artifact_kind": "checkout", "language": "python", "scope": "helper-recognition-and-tests", "phase": "repair", "state": "regression-ready", "optional": false}
  ],
  "outputs": [
    {"name": "validation_record", "semantic_role": "recognition-validation-results", "artifact_kind": "check-report", "language": "agnostic", "scope": "helper-recognition-and-tests", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "alias-overload-regression", "value": "present", "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-alias-and-adjacent-tests",
      "instruction": "Execute the current public aliased-overload regression and relevant annotation suite. Record actual results and diagnostics; required failures or unavailable tests prevent validation PASS.",
      "evidence_refs": ["PyCQA/pyflakes:561:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-origin-boundaries",
      "instruction": "Use current public probes and diff review to verify canonical and aliased supported imports, nearest-binding shadowing, absent and unrelated imports, preserved direct-name handling, attribute-shape guard, and helper-name filtering. Record unobserved claims as UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix"],
      "kind": "public_probe",
      "command": []
    },
    {
      "id": "check-reported-literal-case",
      "instruction": "When relevant to the current public issue, adapt and execute the original Literal reproduction and record its separate result. Otherwise record it as not applicable without claiming Literal coverage from the overload test.",
      "evidence_refs": ["PyCQA/pyflakes:561:body"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:resolve",
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:regression"
  ],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression", "PyCQA/pyflakes:561:body"],
  "read_set": ["role:typing-helper-recognizer", "role:lexical-import-bindings", "role:typing-annotation-regressions"],
  "write_set": [],
  "resource": "references/actions/validate-recognition.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

The output records observations, including failures and unknowns. Only actual passing required observations establish `current-public-validation = pass`.
