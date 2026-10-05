# Guard the comparison and add coverage

Apply only with current PASS evidence for the supported mechanism. Add the positional-variadic exception in the default-count branch, not a global signature suppression. Retain existing warning controls. Any source or test modification requires [validation](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:65539eb7c9013462474b0b56:repair",
  "intent": "Correct the collecting-override false positive using a narrow guard and regression assertion.",
  "mechanism": "Require absence of positional variadics before fewer declared defaults trigger signature-differs.",
  "semantic_role": "repair-default-count-compatibility",
  "owner_role": "override-signature-checker",
  "operation": "Retain the bound defaults comparison and conjoin absence of a positional variadic parameter on the override. Add a public regression with a defaulted base parameter and a forwarding *args, **kwargs override without a signature-differs expectation. Preserve nonvariadic warning expectations and preceding argument-mismatch logic.",
  "kind": "edit",
  "inputs": [
    {
      "name": "assessment",
      "semantic_role": "default-count-compatibility-assessment",
      "artifact_kind": "public-code-and-probe-record",
      "language": "python",
      "scope": "override-signature-checking",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "guarded-default-count-candidate",
      "artifact_kind": "source-and-regression-change",
      "language": "python",
      "scope": "override-signature-checking",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "supported-default-count-mechanism-observed", "value": true, "evaluator": "evidence"},
    {"key": "positional-variadic-binding-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:override-signature-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:override-signature-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "default-count-guard-added", "value": true, "evaluator": "evidence"},
    {"key": "collecting-override-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonvariadic-default-loss-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "preceding-argument-mismatch-branch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "kwargs-only-exception-requested", "value": true, "evaluator": "evidence"},
    {"key": "different-diagnostic-branch-causal", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-narrow-edit",
      "instruction": "Review the diff: the defaults comparison remains and requires absence of positional variadics; preceding argument-mismatch logic is unchanged; the collecting regression has no signature-differs expectation; existing nonvariadic warning assertions remain.",
      "evidence_refs": ["pylint-dev/pylint:3737:fix", "pylint-dev/pylint:3737:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:override-signature-checker", "role:override-signature-regression-suite"],
  "write_set": ["role:override-signature-checker", "role:override-signature-regression-suite"],
  "source_ids": ["pylint-dev/pylint:3737:repair:3ed4b9c0cc18"],
  "evidence_refs": ["pylint-dev/pylint:3737:fix", "pylint-dev/pylint:3737:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:65539eb7c9013462474b0b56"
}
```

Effects specify the intended edit, not observed repair success. Validation freshness becomes stale; behavioral preservation remains required.
