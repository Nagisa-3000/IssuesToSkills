# Repair constructor-local matching

For each private assignment, retain `self` as an acceptable assignment receiver. Only when its scope is a function named `__new__`, extend acceptable names using simple-name return values. Guard return node kinds before accessing `.name`.

For same-name private attribute reads through `self`, admit assignments on these acceptable receivers. Retain pre-existing matching branches. Do not extend this exception to all class assignments or implement blanket suppression.

The historical realization used `scope.nodes_of_class(astroid.Return)` with an `astroid.Name` guard. It does not establish nested-scope soundness or general alias inference. If current scope traversal differs materially, stop automatic transfer.

```arex-contract-v4
{
  "id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:repair",
  "intent": "Recognize consumption through self of private assignments on named __new__ return objects.",
  "mechanism": "Extend acceptable assignment receiver names from guarded simple-name returns within __new__.",
  "semantic_role": "repair-returned-instance-matching",
  "owner_role": "private-member-checker",
  "operation": "Edit the bound matcher to collect Name-valued returns for assignments scoped to __new__ and accept corresponding same-attribute reads through self, retaining existing rules.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "returned-instance-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "checker-edit", "semantic_role": "returned-instance-checker-edit", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "preconditions": [
    {"key": "returned-instance-mismatch-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:private-member-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "returned-local-consumption-recognized", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "non-name-return-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-matching-change",
      "instruction": "Review scope gating, return node-kind guards, same attribute-name matching, self consumer restriction, and retention of preceding matching branches. Runtime validation remains mandatory.",
      "evidence_refs": ["pylint-dev/pylint:4668:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4668:repair:f6c813824183"],
  "evidence_refs": ["pylint-dev/pylint:4668:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2",
  "read_set": ["role:private-member-checker"],
  "write_set": ["role:private-member-checker"],
  "invalidates": ["public-validation-observed"]
}
```

Effects are intended postconditions, not execution results. Retain [validation](validate.md).
