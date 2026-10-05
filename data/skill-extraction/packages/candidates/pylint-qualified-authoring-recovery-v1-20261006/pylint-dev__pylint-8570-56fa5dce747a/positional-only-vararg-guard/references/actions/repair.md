# Add the narrow guard and assertions

Inside the existing vararg/default gate, return without the target diagnostic only when positional-only parameters exist and positional-or-keyword parameters do not. Do not remove warnings from mixed signatures.

Add all eight supported boundary assertions using the current public test harness. Preserve existing ordinary diagnostic assertions and any shared async visitor association. The diff review is not test execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b7e98c0346a9448ab645489:repair",
  "intent": "Correct the false positive and encode the supported boundary.",
  "mechanism": "Add a positional-only-present and positional-or-keyword-absent guard within the existing vararg/default gate.",
  "semantic_role": "narrow-diagnostic-repair",
  "owner_role": "signature-diagnostic-owner",
  "operation": "Modify the bound diagnostic visitor and regression owner to add the narrow guard and supported positive/negative signature matrix.",
  "kind": "edit",
  "inputs": [
    {"name": "boundary-analysis", "semantic_role": "signature-boundary-analysis", "artifact_kind": "review-record", "language": "python", "scope": "signature-diagnostic", "phase": "pre-edit", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "candidate-repair", "semantic_role": "signature-diagnostic-candidate", "artifact_kind": "checkout-change", "language": "python", "scope": "signature-diagnostic", "phase": "post-edit", "state": "unvalidated"}
  ],
  "preconditions": [
    {"key": "partition-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:signature-diagnostic-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:signature-regression-owner", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "narrow-guard-and-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "mixed-signature-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-diff",
      "instruction": "Review the exact partition guard, unchanged surrounding emission gate, preserved shared visitor association, and all eight public regression assertions. Record this as diff review, not test success.",
      "evidence_refs": ["pylint-dev/pylint:8570:fix", "pylint-dev/pylint:8570:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:signature-diagnostic-owner", "role:signature-regression-owner"],
  "write_set": ["role:signature-diagnostic-owner", "role:signature-regression-owner"],
  "source_ids": ["pylint-dev/pylint:8570:repair:56fa5dce747a"],
  "evidence_refs": ["pylint-dev/pylint:8570:fix", "pylint-dev/pylint:8570:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:0b7e98c0346a9448ab645489"
}
```
