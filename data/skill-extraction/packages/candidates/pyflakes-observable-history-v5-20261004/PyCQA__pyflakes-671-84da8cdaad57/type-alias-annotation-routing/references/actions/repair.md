# Route the alias initializer and add regressions

After inspection establishes compatibility:

1. Preserve handling of the target and the declaration annotation.
2. Preserve the no-initializer branch.
3. Inside the present-initializer branch, use the existing typing-aware recognition mechanism to determine whether the annotation denotes `TypeAlias`.
4. For that case only, pass the initializer to the existing annotation-processing path.
5. Retain ordinary node/value handling otherwise.
6. Add public regressions for quoted and unquoted aliases at module and class scope, plus value-less aliases with and without an unrelated imported type.

Do not introduce a standalone string scanner or broaden every string assignment into annotation processing. Do not include the historical incidental type-comment correction unless independently warranted in the current checkout.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:repair",
  "intent": "Make explicit TypeAlias initializers participate in annotation name-use analysis.",
  "mechanism": "Select annotation processing for a present initializer only when the declaration annotation is recognized as the typing TypeAlias construct.",
  "semantic_role": "type-alias-routing-repair",
  "owner_role": "annotated-assignment-dispatch",
  "operation": "Edit initializer dispatch and add focused public annotation regressions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "routing-assessment",
      "semantic_role": "type-alias-routing-assessment",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate-change",
      "semantic_role": "type-alias-routing-candidate",
      "artifact_kind": "code-and-test-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:annotated-assignment-dispatch",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:typing-marker-recognition",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-processing",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:type-annotation-regressions",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "quoted-type-annotation-processing",
      "value": "supported",
      "evaluator": "evidence"
    },
    {
      "key": "type-alias-initializer-routing",
      "value": "incorrect-ordinary-processing",
      "evaluator": "evidence"
    },
    {
      "key": "typing-marker-recognition",
      "value": "scope-aware-and-compatible",
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "type-alias-initializer-routing",
      "value": "annotation-processing",
      "evaluator": "evidence"
    },
    {
      "key": "alias-import-usage-regressions",
      "value": "covered",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "ordinary-initializer-routing",
      "value": "ordinary-node-processing",
      "evaluator": "evidence"
    },
    {
      "key": "value-less-alias-import-usage",
      "value": "does-not-consume-unrelated-import",
      "evaluator": "evidence"
    },
    {
      "key": "existing-annotation-processing",
      "value": "retained",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-routing-change",
      "instruction": "Review the current diff for a TypeAlias-specific initializer branch, reuse of annotation processing, preserved ordinary and absent-value branches, and focused regression definitions. This review does not replace the validation Action.",
      "evidence_refs": [
        "PyCQA/pyflakes:671:fix",
        "PyCQA/pyflakes:671:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:671:repair:84da8cdaad57"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:671:fix",
    "PyCQA/pyflakes:671:regression"
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "read_set": [
    "role:annotated-assignment-dispatch",
    "role:typing-marker-recognition",
    "role:annotation-processing",
    "role:type-annotation-regressions"
  ],
  "write_set": [
    "role:annotated-assignment-dispatch",
    "role:type-annotation-regressions"
  ],
  "invalidates": [
    "current-routing-assessed",
    "public-validation",
    "alias-import-usage-observations"
  ],
  "exclusions": [
    {
      "key": "required-adapter",
      "value": true,
      "evaluator": "evidence",
      "description": "This workflow does not supply a bridge for an incompatible AST or annotation-processing interface."
    }
  ]
}
```

Effects describe intended post-edit state. They become observed facts only after current review and validation.
