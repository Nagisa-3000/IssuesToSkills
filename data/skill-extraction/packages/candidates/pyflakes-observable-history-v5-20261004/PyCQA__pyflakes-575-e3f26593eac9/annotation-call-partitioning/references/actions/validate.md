# Validate the final checkout

Bind current public test commands to the current checkout. No supplied evidence records a historical command or historical test execution; empty command arrays below require current binding, not execution as-is.

Run the focused regression suite and adjacent annotation tests. Review and probe ordinary call fallback and typing-name resolution. Broader public project tests are desirable when available, but are not claimed as historically qualified.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:validate",
  "intent": "Verify both modifying Actions without weakening adjacent analysis.",
  "mechanism": "Execute paired public examples and current regression tests, then record diagnostic and preservation results.",
  "semantic_role": "repair-validation",
  "owner_role": "python-annotation-regression-tests",
  "operation": "Run bound public checks against the final implementation and assertions.",
  "kind": "validate",
  "inputs": [
    {
      "name": "regression-ready-checkout",
      "semantic_role": "annotation-traversal-checkout",
      "artifact_kind": "source-checkout",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "repair",
      "state": "partition-and-regressions-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-observations",
      "semantic_role": "annotation-repair-validation",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "paired-regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-validation-results-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "metadata-and-type-distinction",
      "instruction": "Run the public nested factory examples, including the punctuation-label report. Verify no metadata-derived undefined names and retained diagnostics for genuine missing type names.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-regression-suite",
      "instruction": "Run current focused and adjacent annotation tests. Verify imported names used inside NamedTuple, TypeVar constraints/bounds, and cast type expressions are accounted for; retain applicable version guards. Record actual results and scope, including failures or unknowns.",
      "evidence_refs": ["PyCQA/pyflakes:575:regression", "PyCQA/pyflakes:575:fix"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "fallback-and-resolution",
      "instruction": "Review and publicly probe that ordinary non-typing calls retain ordinary traversal and factory recognition uses current typing-aware resolution rather than textual name matching.",
      "evidence_refs": ["PyCQA/pyflakes:575:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:3257ebe843a343f545c15939:partition",
    "workflow:verified-history:3257ebe843a343f545c15939:regressions"
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939",
  "read_set": ["role:python-annotation-call-analysis", "role:python-typing-name-resolution", "role:python-annotation-regression-tests"],
  "write_set": []
}
```

An observed output can contain failures; only passing current semantic checks establish required Workflow effects. Do not label validation successful merely because it ran.
