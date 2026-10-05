# Repair opt-in ambiguity handling and its consumer

The semantic owners are the Python safe-inference helper, its Boolean rewrite consumer, and their public regression harness.

1. Add a keyword-only, default-disabled option for comparing inferred constants.
2. Retain existing type ambiguity checks. When comparison is enabled and both the selected and subsequent inferred nodes are constants, reject unequal `.value` values as ambiguous.
3. Make the Boolean rewrite consumer enable that option.
4. Return without emitting either rewrite diagnostic on absent or uninferable results; do not substitute truthiness for uncertainty.
5. Preserve definite falsy simplification and definite truthy ternary suggestions. Mark these emissions with the current equivalent of inference confidence.
6. Add regressions for loop reassignment and unknown operands, retain definite-value controls, and update expected diagnostic confidence where appropriate.

Do not change unrelated callers to opt in automatically. This evidence supports equality comparison between constant values, not arbitrary node equivalence or a new control-flow solver.

```arex-contract-v4
{
  "id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:repair",
  "intent": "Prevent uncertain inferred values from authorizing Boolean rewrite diagnostics.",
  "mechanism": "Use opt-in constant-value comparison and conservative consumer handling of uncertain inference.",
  "semantic_role": "ambiguity-preserving-repair",
  "owner_role": "python-inference-rewrite-and-regression-owners",
  "operation": "Modify the bound safe-inference helper, Boolean rewrite consumer, and public regression fixtures according to the six steps in this Action.",
  "kind": "edit",
  "inputs": [
    {
      "name": "confirmed-boundary",
      "semantic_role": "constant-ambiguity-repair-context",
      "artifact_kind": "public-observation-record",
      "language": "python",
      "scope": "safe-inference-and-boolean-rewrite",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "patched-boundary",
      "semantic_role": "constant-ambiguity-repair-artifact",
      "artifact_kind": "checkout-diff",
      "language": "python",
      "scope": "safe-inference-and-boolean-rewrite",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "mechanism-observed", "value": true, "evaluator": "evidence"},
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:python-safe-inference-helper", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-boolean-rewrite-consumer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-public-regression-harness", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "opt-in-constant-ambiguity", "value": true, "evaluator": "evidence"},
    {"key": "uncertain-rewrite-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "inference-confidence-declared", "value": true, "evaluator": "evidence"},
    {"key": "public-regressions-defined", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "default-inference-contract-preserved", "value": true, "evaluator": "evidence"},
    {"key": "definite-value-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "pre-edit-diagnostic-observations-current"],
  "oracle": [
    {
      "id": "inspect-repair",
      "instruction": "Review the diff for default-disabled keyword-only comparison, unequal-constant rejection, conservative handling of None and Uninferable, inference-confidence emission, and explicit public regression controls. Effects are proposed until validation observes them.",
      "evidence_refs": ["pylint-dev/pylint:7626:fix", "pylint-dev/pylint:7626:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7626:repair:00b6aa8482f0"],
  "evidence_refs": ["pylint-dev/pylint:7626:fix", "pylint-dev/pylint:7626:regression"],
  "read_set": ["role:python-safe-inference-helper", "role:python-boolean-rewrite-consumer", "role:python-public-regression-harness"],
  "write_set": ["role:python-safe-inference-helper", "role:python-boolean-rewrite-consumer", "role:python-public-regression-harness"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3"
}
```
