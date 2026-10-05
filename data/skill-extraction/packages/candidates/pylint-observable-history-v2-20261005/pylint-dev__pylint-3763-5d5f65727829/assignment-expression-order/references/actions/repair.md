# Repair recognition and distinguishing fixtures

Consume the confirmed inspection report. Broaden the conditional-expression statement gate to the evidenced ordinary assignment, annotated assignment, augmented assignment, and expression statement types in the current Python AST interface. Retain the `IfExp` requirement, same-frame check, and ancestor condition. Do not blanket-exempt walrus uses.

If current observations justify a legacy joined-string workaround, retain all historical restrictions:

- Runtime earlier than Python 3.9.
- Equal definition/read line numbers.
- Assignment, annotated assignment, or augmented assignment owner.
- Joined-string value.

Preserve normal column and earlier-line checks. Do not infer a need for this branch solely from runtime version.

Add public positive fixtures for applicable owners, initializing augmented-assignment targets:

```python
x = b if (b := True) else False
x2: bool = b2 if (b2 := True) else False
x3 = 0
x3 += b3 if (b3 := 4) else 6
foo if (foo := 3 - 2) > 0 else 0
```

Keep `pointless-statement` for the standalone expression and E0601 for genuine early reads. For an applicable legacy branch, add multiline f-string fixtures assigning in an earlier interpolation and reading in a later interpolation under the three supported assignment owners. Update expected locations only to reflect fixture insertions, not to conceal unexpected diagnostics.

```arex-contract-v4
{
  "id": "workflow:verified-history:0d5d796f6706ce7801b87899:repair",
  "intent": "Correct supported statement-owner recognition and add distinguishing public regression assertions.",
  "mechanism": "Broaden the conditional-expression owner gate without weakening scope constraints; narrowly guard any evidenced legacy joined-string ordering fallback.",
  "semantic_role": "ordering-repair",
  "owner_role": "variable-order-checker",
  "operation": "Edit bound checker ownership recognition, necessary runtime predicates, and public fixtures with diagnostic expectations. Preserve frame/ancestry and ordinary ordering checks.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspection",
      "semantic_role": "assignment-order-binding-report",
      "artifact_kind": "public-evidence-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "patch",
      "semantic_role": "assignment-order-repair",
      "artifact_kind": "checkout-patch",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-before-read-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-frame-and-ancestry-match", "value": true, "evaluator": "evidence"},
    {"key": "role:variable-order-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:assignment-expression-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "conditional-assignment-order-recognized", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-coverage-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-early-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "independent-expression-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "frame-and-ancestry-constraints-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "read-actually-precedes-assignment", "value": true, "evaluator": "evidence"},
    {"key": "incompatible-ast-semantics", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-repair",
      "instruction": "Review the bound current diff for evidenced owner recognition, retained IfExp/frame/ancestor conditions, and distinguishing positive and negative fixtures. For a changed joined-string branch, verify every version, location, statement-type, and value-type guard, plus ordinary ordering checks. This review does not replace post-edit execution.",
      "evidence_refs": ["pylint-dev/pylint:3763:fix", "pylint-dev/pylint:3763:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:variable-order-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "write_set": ["role:variable-order-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "source_ids": ["pylint-dev/pylint:3763:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:3763:fix", "pylint-dev/pylint:3763:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:0d5d796f6706ce7801b87899"
}
```
