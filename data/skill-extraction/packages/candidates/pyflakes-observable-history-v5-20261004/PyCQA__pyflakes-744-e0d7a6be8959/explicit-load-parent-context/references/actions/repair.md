# Pass known context explicitly and add a regression

Change the load-analysis interface to accept parent context. Update every current caller:

- Ordinary name-load dispatch supplies its established parent-context lookup.
- Early augmented-assignment load handling supplies the owning statement directly, without requiring target metadata.
- Keep the builtin-print diagnostic condition dependent on the supplied parent, rather than deleting that diagnostic.
- Preserve load-target, value-visit, target-visit order.
- Add a no-crash analyzer regression for `print += 1`, adapted to the current public test harness.

The historical repair did not solve this by changing traversal order, suppressing `AttributeError`, or removing incompatible-print detection.

```arex-contract-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa:repair",
  "intent": "Remove the early load handler's dependence on uninitialized target parent metadata.",
  "mechanism": "Make context an explicit argument and supply it from callers with known context.",
  "semantic_role": "explicit-load-context-repair",
  "owner_role": "ast-load-analysis",
  "operation": "Edit load dispatch, augmented-assignment dispatch, and the no-crash regression.",
  "kind": "edit",
  "inputs": [
    {
      "name": "context-diagnosis",
      "semantic_role": "load-context-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "explicit-load-context-repair",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "early-load-reads-uninitialized-context", "value": true, "evaluator": "evidence"},
    {"key": "explicit-owner-context-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:ast-load-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:augmented-assignment-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:diagnostic-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "explicit-load-parent-context", "value": true, "evaluator": "evidence"},
    {"key": "augmented-assignment-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "load-value-store-analysis-order", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-load-and-print-diagnostics", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-explicit-context-edit",
      "instruction": "Review the diff: every load-handler call supplies appropriate context, the early target path avoids target metadata lookup, analysis order is unchanged, and the no-crash regression is present.",
      "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
  "read_set": ["role:parent-context-provider", "role:ast-load-analysis", "role:augmented-assignment-analysis", "role:diagnostic-regression-tests"],
  "write_set": ["role:ast-load-analysis", "role:augmented-assignment-analysis", "role:diagnostic-regression-tests"],
  "invalidates": ["load-handler-call-compatibility", "augmented-assignment-analysis-no-crash", "ordinary-load-and-print-diagnostics"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:73c1883f7ed05d43025127fa"
}
```

Effects are proposed edit outcomes. They require current review and the linked validation Action; they are not claims that a current patch has passed.
