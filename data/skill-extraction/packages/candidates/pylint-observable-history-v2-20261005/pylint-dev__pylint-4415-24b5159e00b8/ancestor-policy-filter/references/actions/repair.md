# Filter the count and encode regression controls

Count an ancestor only when its resolved qualified name is absent from the authorized exemption set. Keep the existing transitive iterator and strict configured comparison.

Add a supported standard-library-derived negative diagnostic control and retain excessive user-defined positive controls. Change expected counts only when excluded ancestors justify the change.

```arex-contract-v4
{
  "id": "workflow:verified-history:58d864f47bb516a028d64059:repair",
  "intent": "Correct the ancestry metric and encode negative and positive diagnostic controls.",
  "mechanism": "Explicit qualified-name exemption membership filters the existing transitive ancestor stream before counting.",
  "semantic_role": "ancestry-policy-repair",
  "owner_role": "ancestor-counting-owner",
  "operation": "Edit the bound counting owner to count nonexempt ancestors and the bound regression owner to add a supported stdlib negative control while retaining excessive user-defined positive controls.",
  "kind": "edit",
  "inputs": [
    {
      "name": "policy-binding",
      "semantic_role": "ancestry-policy-binding",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "ancestry-policy-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:ancestor-counting-owner",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The role resolves to the actual current ancestor-counting symbol."
    },
    {
      "key": "role:ancestry-regression-owner",
      "value": true,
      "evaluator": "file_exists",
      "description": "The role resolves to current public ancestry regression resources."
    },
    {"key": "current-policy-binding-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-exemptions-authorized", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "supported-exempt-ancestors-not-counted", "value": true, "evaluator": "evidence"},
    {"key": "negative-and-positive-regression-controls-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "user-defined-ancestry-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "configured-threshold-comparison-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-design-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observation-fresh"],
  "exclusions": [
    {"key": "blanket-standard-library-exemption-required", "value": true, "evaluator": "evidence"},
    {"key": "direct-bases-only-metric-required", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-filter-and-controls",
      "instruction": "Review the current diff for resolved-qname filtering of the same transitive traversal, justified exemption entries, unchanged strict configured comparison, a supported stdlib negative control, and retained excessive user-defined positive controls. Check that expected-count changes correspond to excluded ancestors. Execution remains required by the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:4415:fix", "pylint-dev/pylint:4415:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ancestor-counting-owner", "role:ancestry-regression-owner"],
  "write_set": ["role:ancestor-counting-owner", "role:ancestry-regression-owner"],
  "source_ids": ["pylint-dev/pylint:4415:repair:24b5159e00b8"],
  "evidence_refs": ["pylint-dev/pylint:4415:fix", "pylint-dev/pylint:4415:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:58d864f47bb516a028d64059"
}
```

These effects are targets, not execution claims. Resolve current names rather than blindly copying historical entries. Do not delete legitimate expected diagnostics to make tests pass. The edit invalidates validation freshness, not preserved behavior assurances.
