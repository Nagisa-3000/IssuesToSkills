# Analyze initializer before binding target

Apply only to the confirmed Python visitor mechanism. Move existing target handling after annotation and optional initializer handling. Preserve the annotation call and all existing initializer-dispatch branches.

Add a public regression requiring an undefined-name diagnostic for unbound `x` in `x: int = x`. This modifying Action covers source and its regression. Its effects remain expected until checked; the linked [validation Action](validate.md) is mandatory.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
  "intent": "Prevent an annotated assignment from defining its target before checking its initializer.",
  "mechanism": "Relocate target handling after the existing annotation and optional initializer processing.",
  "semantic_role": "binding-order-repair",
  "owner_role": "annotated-assignment-analyzer",
  "operation": "Edit the bound visitor to defer target handling; add the self-initializer undefined-name assertion in the bound public annotation regression suite.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspection",
      "semantic_role": "binding-order-inspection",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "annotated-assignment",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {
      "key": "early-target-binding-confirmed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "role:annotated-assignment-analyzer",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The current visitor is located and bound."
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
      "key": "target-analysis-after-initializer",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "self-initializer-regression-added",
      "value": true,
      "evaluator": "evidence"
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
  "invalidates": [
    "public-validation-observed"
  ],
  "oracle": [
    {
      "id": "review-ordering-patch",
      "instruction": "Review the current diff: target handling follows existing annotation and optional initializer processing, all initializer-dispatch branches remain intact, and the public regression asserts undefined-name for x: int = x. This review does not replace execution of the validate Action.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:fix",
        "PyCQA/pyflakes:728:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotated-assignment-analyzer",
    "role:annotation-regression-suite"
  ],
  "write_set": [
    "role:annotated-assignment-analyzer",
    "role:annotation-regression-suite"
  ],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:fix",
    "PyCQA/pyflakes:728:regression"
  ],
  "resource": "references/actions/reorder.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
