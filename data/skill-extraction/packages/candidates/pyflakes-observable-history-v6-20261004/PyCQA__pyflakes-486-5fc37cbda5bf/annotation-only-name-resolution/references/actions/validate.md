# Validate repaired resolution and adjacent behavior

Bind the Oracle to current public commands and execute them after the patch. Include the current repository's surrounding annotation and undefined-name tests where available.

Required public cases:

1. `T: object; def f(t: T): ...` reports undefined `T` without future annotations.
2. `T: object; def g(t: 'T'): ...` does not report undefined `T`.
3. With future annotations, both annotation forms avoid the undefined-name report.
4. Without future annotations, ordinary loads are not silenced by an annotation-only declaration.
5. Value-bearing assignments still establish ordinary bindings.
6. Unused module and class annotation-only declarations do not produce unused-variable messages.
7. The historically documented annotation-only local produces no unused-variable message; a subsequent unused `x = 3` produces one, not two.
8. Existing malformed forward-annotation and adjacent name-resolution checks remain intact.

Items 4, 5 and 8 are current preservation probes derived from the implementation boundaries and surrounding supplied assertions, not claimed additional historical test executions.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:validate",
  "intent": "Observe the repaired distinction and preserved neighboring diagnostics.",
  "mechanism": "Run public regression assertions across eager, quoted and future contexts and adjacent binding behavior.",
  "semantic_role": "annotation-resolution-validation",
  "owner_role": "annotation_regression_owner",
  "operation": "Execute current bound public tests and minimal reproductions, record diagnostics and exit results, and refresh validation freshness only when all required checks pass.",
  "kind": "validate",
  "inputs": [
    {
      "name": "resolution_patch",
      "semantic_role": "annotation-resolution-change",
      "artifact_kind": "code-and-tests",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "validation_record",
      "semantic_role": "annotation-resolution-validation",
      "artifact_kind": "test-results",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "regression-owner-exists", "value": true, "evaluator": "file_exists", "description": "role:annotation_regression_owner"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Set only after current required public checks pass."}
  ],
  "preserves": [
    {"key": "ordinary-value-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unused-variable-accounting-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotation-regression-matrix",
      "instruction": "Execute the public annotation matrix and adjacent binding/unused-variable tests described in this card. Record actual outcomes; fail if eager names are incorrectly accepted or quoted/future annotation-only names are incorrectly rejected.",
      "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:be71c3f9e9544046d28904cd:repair"],
  "read_set": ["role:annotation_binding_owner", "role:annotation_regression_owner"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```

This operation does not edit code. Failed or unavailable checks leave validation FAIL or UNKNOWN, respectively; neither establishes the expected effect.
