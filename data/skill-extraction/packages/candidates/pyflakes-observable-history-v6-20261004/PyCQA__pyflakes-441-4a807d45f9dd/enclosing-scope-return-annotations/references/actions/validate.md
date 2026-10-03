# Validate the scope boundary and adjacent behavior

Run current public commands bound to the regression owner and reproduction. Record actual results. The historical test assertions guide expected behavior but are not a historical execution log.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:validate",
  "intent": "Establish that the repair removes the false positive while retaining real undefined-name diagnostics.",
  "mechanism": "Check paired positive and negative scope regressions and adjacent annotation behavior after the modification.",
  "semantic_role": "annotation-scope-validation",
  "owner_role": "python-annotation-regression-tests",
  "operation": "Execute bound current public reproductions and regression tests; review retained body and decorator traversal; record pass, fail, or unknown without changing source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "annotation-traversal-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "annotation-scope-validation-result",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "public-checks-passed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "paired-regressions-present",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:python-annotation-regression-tests",
      "value": true,
      "evaluator": "file_exists"
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
      "key": "function-body-only-annotation-name-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "ordinary-function-body-checking-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "decorator-handling-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "paired-scope-regressions",
      "instruction": "Run the bound current public paired regressions: class-level TypeVar in parameter and return annotations must produce no undefined-name diagnostic, while a return annotation whose name is assigned only inside the function body must report an undefined name.",
      "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-traversal-checks",
      "instruction": "Run available adjacent public annotation and function-checking tests and review the traversal diff to confirm ordinary body checking and existing decorator handling remain intact. Record coverage limits; missing checks remain unknown.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:46d18832864f51ea6f6d3968:repair"],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
  "read_set": ["role:python-function-traversal", "role:python-annotation-regression-tests"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

The success-state output is conditional on passing observations. Failed or unavailable checks must be reported as FAIL or UNKNOWN, not coerced into success. Whole-project and cross-project assurances require additional current evidence.
