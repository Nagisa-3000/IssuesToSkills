# Normalize and type-guard recognition

In the bound classifier, return false for a parent other than annotated assignment. Read its annotation into a local variable. Unwrap one Subscript to its value. Compare `Name.name` or `Attribute.attrname` to `ClassVar` only under the matching node-type guard. Return false otherwise.

Add public equivalents of qualified unsubscripted and subscripted regression forms. Preserve existing direct forms and naming diagnostics. Update moved diagnostic locations without deleting messages. Do not substitute broad exception handling, add import-alias inference, or introduce qualifier identity requirements as part of this repair.

Effects below are candidate obligations until observed through validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:8196d401013577b7b429876a:repair",
  "intent": "Make ClassVar annotation recognition shape-safe and cover qualified naming behavior.",
  "mechanism": "Normalize one subscript layer and use node-specific identifier fields under explicit guards.",
  "semantic_role": "shape-safe-annotation-edit",
  "owner_role": "annotation-classifier",
  "operation": "Edit the bound classifier and public naming regression owners to implement guarded recognition and qualified-form assertions.",
  "kind": "edit",
  "inputs": [
    {"name": "inspection", "semantic_role": "annotation-repair-context", "artifact_kind": "review-record", "language": "python", "scope": "classvar-naming", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "patch", "semantic_role": "annotation-repair-candidate", "artifact_kind": "checkout-diff", "language": "python", "scope": "classvar-naming", "phase": "repair", "state": "unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "matching-shape-mechanism", "value": true, "evaluator": "evidence"},
    {"key": "role:annotation-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-naming-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "shape-safe-classvar-recognition", "value": true, "evaluator": "evidence"},
    {"key": "qualified-classvar-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-classvar-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-guarded-edit",
      "instruction": "Review the diff for the annotated-parent guard, single Subscript unwrap, guarded Name.name and Attribute.attrname comparisons, false fallback, qualified-form assertions and preservation of existing diagnostics. Record candidate effects without claiming execution success.",
      "evidence_refs": ["pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4264:repair:c1c41b849ce0"],
  "evidence_refs": ["pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"],
  "read_set": ["role:annotation-classifier", "role:class-constant-naming-consumer", "role:annotation-naming-regressions"],
  "write_set": ["role:annotation-classifier", "role:annotation-naming-regressions"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:8196d401013577b7b429876a"
}
```
