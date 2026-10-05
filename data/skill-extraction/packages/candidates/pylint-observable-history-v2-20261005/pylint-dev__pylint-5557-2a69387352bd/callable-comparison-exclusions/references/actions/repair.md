# Refine eligible callable counting and add regressions

Apply only after current evidence establishes compatible safe inference and function body/decorator APIs.

Retain the existing bare-callable category. Short-circuit its type check before accessing function-specific attributes. Count only nodes without `typing._SpecialForm` decoration and without an immediate `Raise` in their body. Keep the final eligible-count-equals-one warning rule.

Add public comparisons to `Any`, `Optional`, and a function containing `print()` followed by `raise Exception`. Retain existing ordinary-callable and noncallable controls and their expectations. The shallow scan is not control-flow analysis or proof that execution always raises.

Both checker and regression modifications remain in the validation closure. A reviewed diff is not executed validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:c24ac7f0cdc266e6796600de:repair",
  "intent": "Implement the supported callable exclusions and public regression assertions.",
  "mechanism": "Filter safely inferred bare-callable nodes by qualified special-form decoration and immediate body Raise before applying the exactly-one diagnostic gate.",
  "semantic_role": "refine-callable-classification",
  "owner_role": "callable-comparison-checker",
  "operation": "Edit the bound current diagnostic owner and comparison regression resources, preserving safe inference and ordinary diagnostic behavior.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "callable-comparison-diagnosis",
      "artifact_kind": "evidence-record",
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
      "semantic_role": "callable-comparison-repair",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:callable-comparison-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comparison-regression-suite", "value": true, "evaluator": "file_exists"},
    {
      "key": "supported-mechanism-compatible",
      "value": true,
      "evaluator": "evidence",
      "description": "Current probes establish the false-positive mechanism and compatible safe inference, body, and qualified decorator APIs."
    },
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "supported-exclusions-implemented", "value": true, "evaluator": "evidence"},
    {"key": "supported-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-callable-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "noncallable-and-unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "requires-transitive-or-nested-raise-analysis", "value": true, "evaluator": "evidence"},
    {"key": "requires-arbitrary-decorator-exclusion", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-classification-diff",
      "instruction": "Review the current diff for safe inference, guarded function-specific attributes, only immediate body Raise detection, qualified typing._SpecialForm exclusion, exactly-one eligible callable emission, and public regression assertions. Verify existing positive expectations are retained. Require the separate validate Action after edits.",
      "evidence_refs": ["pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5557:repair:2a69387352bd"],
  "evidence_refs": ["pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
  "read_set": ["role:callable-comparison-checker", "role:comparison-regression-suite"],
  "write_set": ["role:callable-comparison-checker", "role:comparison-regression-suite"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:c24ac7f0cdc266e6796600de"
}
```
