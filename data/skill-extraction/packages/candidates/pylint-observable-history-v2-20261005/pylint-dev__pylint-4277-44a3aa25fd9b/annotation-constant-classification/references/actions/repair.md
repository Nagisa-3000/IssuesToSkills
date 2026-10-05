# Repair annotation policy and assertions

Use `Final`, not `ClassVar`, in the bound annotation-based constant branch. If needed, parameterize the existing helper: require an annotated assignment, unwrap the outer subscript, and compare the name or attribute suffix with the requested typing name.

Review callers before replacing a helper; preserve legitimate class-variable queries. Do not claim suffix matching establishes import origin.

Update differential public assertions in the same edit closure. Preserve Enum handling and configuration lookup. Add Final default/snake_case cases and remove only ClassVar-induced constant expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0:repair",
  "intent": "Separate class storage from annotation-declared constants.",
  "mechanism": "Parameterize outer-annotation recognition and select Final rather than ClassVar for constant naming, with differential assertions.",
  "semantic_role": "constant-annotation-policy-repair",
  "owner_role": "class-attribute-naming-classifier",
  "operation": "Edit bound classifier, recognizer, and public naming assertions without changing Enum classification or configured naming policy.",
  "kind": "edit",
  "inputs": [
    {"name": "reviewed-classification-bindings", "semantic_role": "classification-repair-context", "artifact_kind": "binding-record", "language": "Python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "reviewed"}
  ],
  "outputs": [
    {"name": "candidate-naming-repair", "semantic_role": "annotation-naming-candidate", "artifact_kind": "checkout-revision", "language": "Python", "scope": "current-public-checkout", "phase": "post-edit", "state": "unvalidated"}
  ],
  "preconditions": [
    {"key": "classification-bindings-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "classvar-causes-constant-classification", "value": true, "evaluator": "evidence"},
    {"key": "role:class-attribute-naming-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotated-assignment-recognizer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:naming-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "annotation-constant-policy", "value": "Final-not-ClassVar", "evaluator": "evidence"},
    {"key": "differential-naming-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "enum-naming-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-constant-style-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "public-naming-checks-passed"],
  "oracle": [
    {
      "id": "review-policy-diff",
      "instruction": "Review the public diff for Final-not-ClassVar constant classification, supported AST forms, preserved Enum and configuration branches, and unaffected helper callers. Review differential public assertions before executing them.",
      "evidence_refs": ["pylint-dev/pylint:4277:fix", "pylint-dev/pylint:4277:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:class-attribute-naming-classifier", "role:annotated-assignment-recognizer", "role:naming-regression-suite"],
  "write_set": ["role:class-attribute-naming-classifier", "role:annotated-assignment-recognizer", "role:naming-regression-suite"],
  "source_ids": ["pylint-dev/pylint:4277:repair:44a3aa25fd9b"],
  "evidence_refs": ["pylint-dev/pylint:4277:fix", "pylint-dev/pylint:4277:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:ed1fdb4232b2b4ee5e41a4a0"
}
```

Resolve role existence predicates to current concrete resources; their values are booleans, not resource locators. Effects are intended postconditions, not observed execution. [Validate](validate.md) remains mandatory. Invalidated observation keys are distinct from preserved behavior assurances.
