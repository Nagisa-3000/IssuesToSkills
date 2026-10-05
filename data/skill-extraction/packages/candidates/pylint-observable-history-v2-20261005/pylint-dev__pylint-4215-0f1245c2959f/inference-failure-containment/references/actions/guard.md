# Guard inference-result consumption

At the bound checker, protect only the acquisition of the inferred argument instance. Catch the confirmed `InferenceError` family and return locally on failure. Retain existing generator/comprehension handling and the successful inference path.

Historical implementation:

```python
try:
    instance = next(len_arg.infer())
except astroid.InferenceError:
    return
```

Adapt identifiers only after current semantic review. Do not wrap the entire callback or use a broad exception catch.

```arex-contract-v4
{
  "id": "workflow:verified-history:4cd11cf9432439d81e30121e:guard",
  "intent": "Prevent failed argument inference from aborting analysis.",
  "mechanism": "Catch the inference exception family at result consumption and abandon only the current diagnostic check.",
  "semantic_role": "local-inference-failure-containment",
  "owner_role": "length-condition-checker",
  "operation": "Edit the bound Python callback to catch InferenceError around length-argument inference-result acquisition and return locally before type-dependent checks on failure.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-boundary-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "boundary-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:length-condition-checker", "value": true, "evaluator": "symbol_exists", "description": "The current length-condition callback is located and bound."},
    {"key": "inference-exception-family-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "inference-failure-contained", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "independent-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inferable-length-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-local-catch",
      "instruction": "Review the current diff for a catch limited to inference-result consumption, the confirmed InferenceError family, and local return on failure. Confirm unchanged successful-inference and earlier fast paths. Retain runtime validation after this edit.",
      "evidence_refs": ["pylint-dev/pylint:4215:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4215:repair:0f1245c2959f"],
  "evidence_refs": ["pylint-dev/pylint:4215:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:4cd11cf9432439d81e30121e",
  "read_set": ["role:length-condition-checker"],
  "write_set": ["role:length-condition-checker"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "requires-broad-exception-suppression", "value": true, "evaluator": "evidence"}
  ]
}
```

Effects are obligations, not execution claims. Retain the [validate Action](validate.md) after modification.
