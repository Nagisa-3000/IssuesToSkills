# Validate alias routing and adjacent behavior

Bind public current oracles and execute them after the repair. Refresh the routing review against the changed code.

The positive matrix is quoted/unquoted initializer × module/class scope. Value-less declarations form a negative control: the marker itself is used, but an unrelated imported type remains unused.

Also check the original quoted-function-annotation contrast and review or probe ordinary annotated string values. The ordinary-value preservation requirement comes from the retained implementation branch; it is not an extra historical regression claimed by this package.

Record commands, results, diagnostics, and coverage limits. A focused suite pass is not a whole-project or cross-project guarantee.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:validate",
  "intent": "Establish that the repaired alias routing fixes name-use diagnostics without changing adjacent behavior.",
  "mechanism": "Execute public alias regression cases and compare preserved ordinary-value, absent-value, and existing annotation behavior.",
  "semantic_role": "type-alias-routing-validation",
  "owner_role": "type-annotation-regressions",
  "operation": "Run bound current public tests and reproductions, inspect changed routing, and record observed results.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-change",
      "semantic_role": "type-alias-routing-candidate",
      "artifact_kind": "code-and-test-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "type-alias-routing-validation-result",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "results-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "candidate-change-present",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-oracles-bound",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "validation-results-recorded",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-content",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "alias-regression-matrix",
      "instruction": "Run the current public annotation suite containing quoted and unquoted TypeAlias initializers at module and class scope; verify value-less declarations and the expected unused import for an unrelated type with no initializer.",
      "evidence_refs": [
        "PyCQA/pyflakes:671:regression"
      ],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "reproduction-and-preservation",
      "instruction": "Run the adapted original quoted-alias reproduction and quoted-function-annotation contrast. Review or publicly probe non-TypeAlias annotated string values to establish that ordinary value handling is unchanged; inspect target and declaration annotation handling and the absent-value guard.",
      "evidence_refs": [
        "PyCQA/pyflakes:671:body",
        "PyCQA/pyflakes:671:fix"
      ],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:671:repair:84da8cdaad57"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:671:body",
    "PyCQA/pyflakes:671:fix",
    "PyCQA/pyflakes:671:regression"
  ],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "validation_for": [
    "workflow:verified-history:d3771ee821e88935b9bcf1ce:repair"
  ],
  "read_set": [
    "role:annotated-assignment-dispatch",
    "role:typing-marker-recognition",
    "role:annotation-processing",
    "role:type-annotation-regressions"
  ],
  "write_set": []
}
```

The validation report may contain FAIL or UNKNOWN. Record `public-validation = passed` only when all required public checks actually pass.
