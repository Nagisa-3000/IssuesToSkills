# Validate diagnostics and adjacent annotation behavior

Bind public commands to the current checkout, then execute the added regression and affected annotation suite. Review retained annotation/initializer dispatch and run adjacent public checks.

The additional adjacent probes are current validation requirements, not claims that those exact probes were historically executed. Broader testing may increase confidence but is not historically attested here. Do not mark success for unexecuted commands, unknown required checks, or failing adjacent behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:validate",
  "intent": "Observe the repaired diagnostic and preserved adjacent behavior.",
  "mechanism": "Execute the public self-initializer regression and affected annotation tests, supplemented by public diagnostic probes.",
  "semantic_role": "repair-validation",
  "owner_role": "annotation-regression-suite",
  "operation": "Run current bound public checks without editing source or tests; record commands, outputs, statuses, and coverage limits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patch",
      "semantic_role": "binding-order-repair",
      "artifact_kind": "source-and-test-patch",
      "language": "python",
      "scope": "annotated-assignment",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "binding-order-validation",
      "artifact_kind": "test-result-record",
      "language": "python",
      "scope": "annotated-assignment",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "target-analysis-after-initializer",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "self-initializer-regression-added",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:annotation-regression-suite",
      "value": true,
      "evaluator": "file_exists",
      "description": "The current public regression suite is located and bound."
    }
  ],
  "effects": [
    {
      "key": "annotated-self-initializer-diagnostic",
      "value": "undefined-name",
      "evaluator": "evidence"
    },
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence",
      "description": "Established only after required public checks complete successfully."
    }
  ],
  "preserves": [
    {
      "key": "ordinary-assignment-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-and-initializer-dispatch-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "run-self-initializer-regression",
      "instruction": "Execute the current public regression and require an undefined-name diagnostic for the unbound initializer x in x: int = x.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:regression",
        "PyCQA/pyflakes:728:body"
      ],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-adjacent-behavior",
      "instruction": "Execute the affected annotation suite and public checks for ordinary x = x, a previously bound x used as an initializer, annotation-only declarations, and existing special initializer/TypeAlias handling where present. Review dispatch preservation. Record coverage gaps and reject success on failures or unknown required checks.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:fix",
        "PyCQA/pyflakes:728:regression",
        "PyCQA/pyflakes:728:body"
      ],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:88cc33218756cccdf2ac071b:reorder"
  ],
  "read_set": [
    "role:annotated-assignment-analyzer",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:regression",
    "PyCQA/pyflakes:728:fix",
    "PyCQA/pyflakes:728:body"
  ],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
