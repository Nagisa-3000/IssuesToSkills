# Inspect usage-state compatibility

Locate the current annotation load handler, usage-state consumer, and annotation regression-test owner. Read only; this operation must not change tracked files. Treat the historical traceback as a locator hint, not a binding to a current path.

Confirm that the annotation-only load records `True`, that a downstream store can subscript a truthy usage value, and that normal structured usage values carry scope and node. Review the postponed-annotation guard. If current code already records structured metadata, or uses a different contract, do not authorize the historical edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
  "intent": "Determine whether the current analyzer has the evidenced producer-consumer mismatch.",
  "mechanism": "Read the annotation usage producer, scope-sensitive store consumer, and local test conventions.",
  "semantic_role": "usage-state-contract-inspection",
  "owner_role": "annotation-usage-tracking",
  "operation": "Locate current semantic owners and review their code without editing; record code anchors, branch guards, representation expectations, and applicable public tests.",
  "kind": "read",
  "inputs": [],
  "outputs": [
    {
      "name": "inspected-usage-context",
      "semantic_role": "annotation-usage-repair-context",
      "artifact_kind": "code-review-record",
      "language": "python",
      "scope": "annotation-load-and-nested-store",
      "phase": "pre-edit",
      "state": "mismatch-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "usage-state-mismatch-confirmed",
      "value": true,
      "evaluator": "evidence",
      "description": "Emit the confirmed output only if current evidence shows a boolean producer and a scope/node consumer."
    },
    {
      "key": "annotation-regression-owner-located",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "Resolve the current role:annotation-regression-tests binding."
    }
  ],
  "preserves": [
    {
      "key": "annotation-only-load-undefined-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "nested-unused-local-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "adjacent-annotation-branch-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "confirm-current-contract",
      "instruction": "Review current public code anchors to confirm the boolean assignment, the structured consumer contract, and the relevant annotation test owner. Verify the inspection made no file changes. Record UNKNOWN or FAIL instead of confirming a mismatch without evidence.",
      "evidence_refs": [
        "PyCQA/pyflakes:764:body",
        "PyCQA/pyflakes:764:fix",
        "PyCQA/pyflakes:764:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:764:repair:e19886e58363"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:764:body",
    "PyCQA/pyflakes:764:fix",
    "PyCQA/pyflakes:764:regression"
  ],
  "read_set": [
    "role:annotation-usage-tracking",
    "role:scope-sensitive-binding-store",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

The output is expected only on a confirmed match; it is not an assertion that inspection has already occurred. Bind the owner-existence check to the real current symbol, not the historical test class name.
