# Correct traversal and add paired regressions

Apply the smallest equivalent omission at the current function-traversal owner. Keep existing decorator exclusion and earlier annotation handling intact. Add public regressions for both sides of the scope boundary at the current annotation-test owner.

The historical implementation and test paths are documented in [the episode](../episode.md), not assumed as current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:repair",
  "intent": "Prevent return annotations from being checked again under function-body scope.",
  "mechanism": "Exclude the return-annotation child from function-scope traversal while retaining the established annotation-processing path.",
  "semantic_role": "annotation-traversal-repair",
  "owner_role": "python-function-traversal",
  "operation": "Modify the later function-scope traversal to omit return annotations as well as decorators, and add paired enclosing-class and body-only-name regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "applicability",
      "semantic_role": "annotation-traversal-applicability",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {
      "key": "role:python-function-traversal",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:python-annotation-regression-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "existing-enclosing-scope-annotation-handling-confirmed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "later-function-scope-return-retraversal-confirmed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "return-annotation-traversal-corrected",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "paired-regressions-present",
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
  "invalidates": ["public-validation-observed", "pre-edit-traversal-observation-current"],
  "oracle": [
    {
      "id": "review-minimal-scope-edit",
      "instruction": "Review the current diff for a targeted return-child omission, retained decorator handling and earlier annotation processing, and both regression assertions. This review is not a substitute for the explicit validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
  "read_set": ["role:python-function-traversal", "role:python-annotation-regression-tests"],
  "write_set": ["role:python-function-traversal", "role:python-annotation-regression-tests"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

Effects are expected obligations until reviewed and tested, not observations of execution. Never replace this targeted omission with global undefined-name suppression.
