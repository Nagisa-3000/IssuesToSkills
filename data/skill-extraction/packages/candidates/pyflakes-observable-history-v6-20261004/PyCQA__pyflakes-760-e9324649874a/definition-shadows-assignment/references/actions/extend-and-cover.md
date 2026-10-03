# Extend definition redefinition and add coverage

Modify the definition-binding predicate to accept a prior assignment only when its name matches, in addition to every case already accepted by the superclass predicate. Add a public regression asserting the existing unused-redefinition diagnostic for an assignment followed by a same-name function.

Keep unused-status decisions and diagnostic emission in their existing policy owners. Do not implement a blanket class-body reassignment ban or change the assignment-side predicate to flag ordinary rebinding.

```arex-contract-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf:extend-and-cover",
  "intent": "Correct definition-over-assignment classification and lock the target behavior into public regression coverage.",
  "mechanism": "Logical OR of existing superclass behavior with a same-name assignment-binding check.",
  "semantic_role": "definition-assignment-redefinition-repair",
  "owner_role": "binding-redefinition-owner",
  "operation": "Edit the current definition-binding predicate and its public unused-redefinition tests; preserve existing classification and diagnostic policy.",
  "kind": "edit",
  "inputs": [
    {
      "name": "located-context",
      "semantic_role": "compatible-binding-redefinition-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "definition-assignment-redefinition-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "binding-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Resolve role:binding-redefinition-owner."},
    {"key": "assignment-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Resolve role:assignment-binding-owner."},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "Resolve role:unused-redefinition-tests-owner."},
    {"key": "compatible-definition-assignment-policy", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "definition-assignment-rule-present", "value": true, "evaluator": "evidence"},
    {"key": "target-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "superclass-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-rebinding-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-rule-and-regression",
      "instruction": "Review the current diff for retained superclass classification, assignment type and name equality checks, and a public assignment-to-function regression expecting the existing unused-redefinition diagnostic. This review does not replace post-edit execution.",
      "evidence_refs": ["PyCQA/pyflakes:760:fix", "PyCQA/pyflakes:760:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:760:repair:e9324649874a"],
  "evidence_refs": ["PyCQA/pyflakes:760:fix", "PyCQA/pyflakes:760:regression", "PyCQA/pyflakes:760:body"],
  "read_set": ["role:binding-redefinition-owner", "role:assignment-binding-owner", "role:unused-redefinition-tests-owner"],
  "write_set": ["role:binding-redefinition-owner", "role:unused-redefinition-tests-owner"],
  "resource": "references/actions/extend-and-cover.md",
  "package_id": "workflow:verified-history:ee79eebf2283561900232caf"
}
```

The effects and output state are expected results of applying the Action, not pre-recorded execution observations. Retain the [validate Action](validate.md) whenever this Action is included.
