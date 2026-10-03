# Repair the usage metadata and regression assertion

At the confirmed annotation-only, non-postponed load branch, replace the boolean used marker with the representation already consumed by downstream scope-sensitive stores: current scope plus load node. Preserve the branch guard and subsequent control flow.

Add or retain a regression assertion with an annotation-only outer name, an attribute load of that name, and a same-name nested local assignment. Assert undefined-name and unused-local diagnostics, not silence.

This is one modifying Action covering both the implementation and its regression assertion. Its explicit validation Action is mandatory after modification.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
  "intent": "Restore the structured usage-state contract and protect the triggering scope interaction.",
  "mechanism": "Replace a truthy sentinel with current-scope/load-node metadata in the affected annotation load branch.",
  "semantic_role": "annotation-usage-metadata-repair",
  "owner_role": "annotation-usage-tracking",
  "operation": "Edit the confirmed usage producer to record the current scope and load node using the existing structured contract; add the focused undefined-name plus unused-local regression assertion in the bound test owner.",
  "kind": "edit",
  "inputs": [
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
  "outputs": [
    {
      "name": "candidate-usage-repair",
      "semantic_role": "annotation-usage-repair-candidate",
      "artifact_kind": "source-and-regression-change",
      "language": "python",
      "scope": "annotation-load-and-nested-store",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "usage-state-mismatch-confirmed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:annotation-usage-tracking",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-regression-tests",
      "value": true,
      "evaluator": "symbol_exists"
    }
  ],
  "effects": [
    {
      "key": "annotation-usage-metadata",
      "value": "scope-and-load-node",
      "evaluator": "evidence"
    },
    {
      "key": "target-regression-assertion-present",
      "value": true,
      "evaluator": "evidence"
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
  "invalidates": [
    "pre-edit-public-check-results-current"
  ],
  "oracle": [
    {
      "id": "review-repair-shape",
      "instruction": "Review the public candidate diff: the affected producer records current scope and load node, the annotation/postponement guard and continuation remain unchanged, and the regression expects undefined-name and unused-local diagnostics. This review does not replace execution by the validate Action.",
      "evidence_refs": [
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
    "PyCQA/pyflakes:764:fix",
    "PyCQA/pyflakes:764:regression"
  ],
  "read_set": [
    "role:annotation-usage-tracking",
    "role:scope-sensitive-binding-store",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:annotation-usage-tracking",
    "role:annotation-regression-tests"
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

Effects describe the intended candidate change, not observed test success. Reject the edit if current metadata has incompatible structure or the branch is materially different.
