# Guard specialized argument resolution

Apply the smallest local edit at the specialized call-value checker. Use the current callable's actual parameter name, not a mechanically copied historical name.

Resolve by the supported positional slot and keyword. Catch only the helper's missing-argument exception. In that branch, use the existing keyword-unpacking inference helper. If it yields no usable argument, return from the specialized check, leaving ordinary signature checking intact.

Initialize direct-resolution confidence using the current equivalent of `HIGH`; switch to the equivalent of `INFERENCE` for the fallback. Retain the existing inference-error handling, target-value comparison, and single-warning behavior. Pass the chosen confidence into the diagnostic.

```arex-contract-v4
{
  "id": "workflow:verified-history:d00504c6d18cf355ce8404aa:repair",
  "intent": "Eliminate the local missing-argument crash without hiding call-signature errors.",
  "mechanism": "Guard position-or-keyword extraction, infer an unpacked keyword on the missing-argument branch, and return when no target argument is available.",
  "semantic_role": "repair-argument-resolution",
  "owner_role": "call-value-checker",
  "operation": "Edit only the bound specialized checker to add the narrow guard, fallback and diagnostic confidence propagation.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"},
    {"key": "argument-resolution-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:call-value-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:argument-resolution-helpers", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "missing-argument-handled-locally", "value": true, "evaluator": "evidence"},
    {"key": "keyword-fallback-confidence-propagated", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-signature-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-copy-check-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exceptions-not-swallowed", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-local-guard",
      "instruction": "Inspect the final diff for position-or-keyword lookup, a catch restricted to the missing-argument exception, keyword-unpacking fallback, absence early return, preserved inference-error handling, and confidence propagation. Reject broad exception catches or changes to signature enforcement.",
      "evidence_refs": ["pylint-dev/pylint:8774:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8774:repair:92485a35e516"],
  "evidence_refs": ["pylint-dev/pylint:8774:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d00504c6d18cf355ce8404aa",
  "read_set": ["role:argument-resolution-helpers", "role:call-value-checker"],
  "write_set": ["role:call-value-checker"],
  "invalidates": ["public-validation-observed"]
}
```

The required public validation is [validate](validate.md). Diff review alone does not establish repair success.
