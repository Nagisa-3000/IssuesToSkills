# Validate both edits and adjacent behavior

After both edits, execute current public Oracle bindings. Run the focused reproduction and relevant annotation tests. Check existing-name annotation preservation, absent-name annotation insertion, ordinary replacement, annotation-with-value assignment semantics, and unchanged usage propagation.

The adjacent checks are current preservation probes derived from the implementation guard. They are not claims that the supplied historical regression added those tests.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
  "intent": "Observe repair behavior and detect damage to adjacent insertion semantics.",
  "mechanism": "Execute public reproduction and repository tests and review or probe preserved insertion cases.",
  "semantic_role": "annotation-binding-validation",
  "owner_role": "annotation-test-suite",
  "operation": "Execute bound current public checks and record outcomes for both edits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "guard-edit",
      "semantic_role": "annotation-insertion-repair",
      "artifact_kind": "source-edit",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "edited-unvalidated"
    },
    {
      "name": "regression-edit",
      "semantic_role": "export-annotation-regression-test",
      "artifact_kind": "test-edit",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "edited-unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "annotation-binding-check-results",
      "artifact_kind": "test-results",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "role:scope-binding-insertion", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-test-suite", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-public-validation-passes", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-bindings-still-replace", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotations-still-insert", "value": true, "evaluator": "evidence"},
    {"key": "existing-usage-propagation-retained", "value": true, "evaluator": "evidence"},
    {"key": "scope-selection-unchanged", "value": true, "evaluator": "evidence"},
    {"key": "existing-annotation-tests-retained", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "exported-import-mre",
      "instruction": "Run the assigned-__all__ plus alternative annotation-only public reproduction through the current analyzer. Record diagnostics and verify no unexpected diagnostic or unused-import report for z.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-suite",
      "instruction": "Run the focused regression and relevant current public annotation tests. Record commands and results. Review or publicly probe existing-name annotation preservation, absent-name annotation insertion, ordinary replacement, annotation-with-value assignment, scope selection, and usage propagation.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "validation_for": [
    "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
    "workflow:verified-history:eedcc58f60ba24cb02758489:regression"
  ],
  "read_set": ["role:scope-binding-insertion", "role:annotation-binding-classifier", "role:annotation-test-suite"],
  "write_set": []
}
```

No command in this card is currently bound. Record actual PASS/FAIL/UNKNOWN outcomes; the intended passing effect is not evidence of success. Refresh stale observations. This validation must remain in the verification closure for both edits.
