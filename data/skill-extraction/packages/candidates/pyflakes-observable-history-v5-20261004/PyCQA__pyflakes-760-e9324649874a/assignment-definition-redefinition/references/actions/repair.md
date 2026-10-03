# Extend definition-side recognition and add a regression

Consume the reviewed context and re-check its code anchors. Edit the current semantic owner corresponding to the definition binding. Keep the inherited redefinition predicate as an alternative; add recognition of the prior assignment binding only when its name equals the new definition's name.

In the historical Python implementation, this was:

```python
super().redefines(other) or (
    isinstance(other, Assignment) and self.name == other.name
)
```

Adapt names only after confirming equivalent semantics. Do not move the check into a blanket class-body duplicate-name rule, broaden it to all binding types, reverse the direction, or discard the inherited predicate.

Add a regression under the current unused-redefinition test owner: `x = 1` followed by `def x(): pass` must expect the existing unused-redefinition message. Keep report formatting and unrelated diagnostic rules unchanged. A class-body reproduction can be checked during validation without claiming that it was a historical regression assertion.

```arex-contract-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf:repair",
  "intent": "Make a definition recognize a same-name assignment as a redefined binding.",
  "mechanism": "Disjoin the inherited predicate with a same-name assignment-type check and add the assignment-to-function regression assertion.",
  "semantic_role": "definition-assignment-recognition-repair",
  "owner_role": "python-definition-binding-predicate",
  "operation": "Edit the definition predicate and the unused-redefinition regression test.",
  "kind": "edit",
  "inputs": [
    {
      "name": "repair_context",
      "semantic_role": "assignment-definition-repair-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "assignment-definition-repair-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:python-definition-binding-predicate",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:python-assignment-binding-type",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:python-unused-redefinition-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "supported-directional-collision",
      "value": true,
      "evaluator": "evidence",
      "description": "Current review confirms an assignment hidden by a definition is unintentionally omitted from the existing diagnostic policy."
    },
    {
      "key": "reviewed-anchors-current",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "definition-recognizes-same-name-assignment",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "assignment-function-regression-asserted",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "inherited-redefinition-rule",
      "value": "preserved",
      "evaluator": "evidence"
    },
    {
      "key": "ordinary-assignment-rebinding-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    },
    {
      "key": "existing-unused-scope-policy",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-predicate-and-regression",
      "instruction": "Review the candidate diff for retained inherited behavior, a type-restricted same-name assignment branch, and an assertion expecting the existing unused-redefinition diagnostic for assignment followed by function definition. This review is not a substitute for the validate Action.",
      "evidence_refs": [
        "PyCQA/pyflakes:760:fix",
        "PyCQA/pyflakes:760:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:760:repair:e9324649874a"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:760:fix",
    "PyCQA/pyflakes:760:regression"
  ],
  "read_set": [
    "role:python-binding-redefinition-model",
    "role:python-unused-redefinition-tests"
  ],
  "write_set": [
    "role:python-definition-binding-predicate",
    "role:python-unused-redefinition-tests"
  ],
  "invalidates": [
    "pre-edit-diagnostic-observations",
    "pre-edit-test-results",
    "reviewed-code-anchor-hashes"
  ],
  "exclusions": [
    {
      "key": "blanket-class-duplicate-name-ban",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "incompatible-binding-model",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:ee79eebf2283561900232caf"
}
```

Effects describe the intended candidate. They become observed facts only through diff review and post-edit validation.
