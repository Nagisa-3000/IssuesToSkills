# Modify alias-value routing

After current applicability is established, preserve target and marker-annotation processing. For a present value, use the existing scope-aware typing resolver to recognize `TypeAlias`; route only recognized alias values through the annotation handler. Retain ordinary expression processing otherwise and retain the no-value branch.

Do not evaluate quoted strings at runtime or substitute a spelling-only match. The declared effects are intended postconditions, not observed repair results. Review the diff and retain [validation](validate-regressions.md).

```arex-contract-v4
{
  "id": "explicit-type-alias-string-analysis.route",
  "intent": "Resolve references in explicit-alias values using existing annotation semantics.",
  "mechanism": "Conditionally dispatch recognized TypeAlias values through the annotation handler.",
  "semantic_role": "alias-value-routing",
  "owner_role": "annotated-assignment-handler",
  "operation": "Modify the present-value branch for scope-resolved TypeAlias annotated assignments.",
  "kind": "edit",
  "inputs": [
    {"name": "inspected-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "inspected", "optional": false}
  ],
  "outputs": [
    {"name": "routed-checkout", "semantic_role": "alias-analysis-checkout", "artifact_kind": "checkout", "language": "python", "scope": "current-public-checkout", "phase": "repair", "state": "value-routing-patched", "optional": false}
  ],
  "preconditions": [
    {"key": "alias-dispatch-applicable", "value": true, "evaluator": "evidence"},
    {"key": "role:annotated-assignment-handler", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:typing-marker-resolver", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-value-handler", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "quoted-alias-import-counted", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-value-dispatch-preserved", "value": true, "evaluator": "evidence"},
    {"key": "target-and-marker-analysis-preserved", "value": true, "evaluator": "evidence"},
    {"key": "no-value-does-not-use-unrelated-import", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-dispatch-boundary",
      "instruction": "Inspect the current diff for scope-resolved marker-only routing, retained target and marker processing, and retained ordinary-value and no-value branches; record review evidence and execute the linked validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:671:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:671"],
  "evidence_refs": ["PyCQA/pyflakes:671:fix"],
  "resource": "references/actions/route-alias-value.md",
  "package_id": "explicit-type-alias-string-analysis",
  "read_set": ["role:annotated-assignment-handler", "role:typing-marker-resolver", "role:annotation-value-handler"],
  "write_set": ["role:annotated-assignment-handler"],
  "invalidates": ["current-alias-diagnostics", "current-adjacent-diagnostics", "current-regression-results"]
}
```
