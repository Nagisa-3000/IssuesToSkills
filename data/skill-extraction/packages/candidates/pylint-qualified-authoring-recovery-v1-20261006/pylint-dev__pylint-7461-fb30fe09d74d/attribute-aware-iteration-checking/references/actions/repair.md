# Repair identifier extraction and add the regression

Apply only after PASS evidence establishes the compatible iterator domain and guarded target receiver.

Preserve early returns and inference comparison. In the dictionary condition, extract `attrname` for the attribute iterator form and `name` for the simple-name form. Retain the comparison against the guarded target receiver's `name`. Align the related list, dictionary, and set helper annotations with `Name | Attribute` where current APIs support that domain.

Add or retain a functional case that initializes an instance dictionary, loops over its attribute, copies it into a local name, and assigns `None` into that local copy. It must expect neither a crash nor a dictionary-mutation diagnostic. Retain adjacent diagnostic expectations.

Do not broaden inference, alias analysis, or receiver semantics to make this repair fit. The edit makes prior validation observations stale; the linked validation Action remains mandatory.

```arex-contract-v4
{
  "id": "workflow:verified-history:d4547bc8e3248f1130d70f73:repair",
  "intent": "Correct the attribute iterator field mismatch and encode the copy regression.",
  "mechanism": "Choose the iterator identifier by node kind while retaining existing guards and receiver comparison.",
  "semantic_role": "targeted-repair",
  "owner_role": "iteration-checker",
  "operation": "Edit the bound checker and functional tests with Name/Attribute identifier extraction, consistent iterator annotations, and the instance-attribute copy-loop regression.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspection",
      "semantic_role": "iterator-field-inspection",
      "artifact_kind": "source-review",
      "language": "python",
      "scope": "iteration-checker-and-tests",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair",
      "semantic_role": "iterator-field-repair",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "iteration-checker-and-tests",
      "phase": "post-repair",
      "state": "edited",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:iteration-checker", "value": true, "evaluator": "symbol_exists", "description": "Resolve the current checker owner before evaluating existence."},
    {"key": "role:iteration-functional-tests", "value": true, "evaluator": "file_exists", "description": "Resolve the current public functional-test owner."},
    {"key": "supported-name-attribute-domain", "value": true, "evaluator": "evidence"},
    {"key": "guarded-target-receiver-has-name", "value": true, "evaluator": "evidence"},
    {"key": "unsupported-iterator-name-access", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "attribute-access-repaired", "value": true, "evaluator": "evidence"},
    {"key": "copy-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "simple-name-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-mutation-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-diff",
      "instruction": "Review the current diff for Attribute.attrname versus Name.name selection, retained early guards and inference comparison, unchanged guarded receiver comparison, consistent helper annotations, and a copy-loop fixture without a mutation expectation. Retain and execute the validate Action before accepting behavioral success.",
      "evidence_refs": ["pylint-dev/pylint:7461:fix", "pylint-dev/pylint:7461:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7461:repair:fb30fe09d74d"],
  "evidence_refs": ["pylint-dev/pylint:7461:fix", "pylint-dev/pylint:7461:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d4547bc8e3248f1130d70f73",
  "read_set": ["role:iteration-checker", "role:iteration-functional-tests"],
  "write_set": ["role:iteration-checker", "role:iteration-functional-tests"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "broader-alias-repair-required", "value": true, "evaluator": "evidence"},
    {"key": "incompatible-ast-interface", "value": true, "evaluator": "evidence"}
  ]
}
```
