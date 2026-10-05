# Define unresolved-name regressions

Use the current diagnostic fixture conventions to add direct-name and subscript cases under `len()` conditions. Require undefined-variable diagnostics for the unresolved base names, no inference traceback, and no speculative length-condition recommendation. Preserve existing expectations; do not reuse historical line numbers as current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:4cd11cf9432439d81e30121e:regression",
  "intent": "Expose direct and nested unresolved length-argument inference in public tests.",
  "mechanism": "Add len(undefined_name) and len(undefined_name[0]) conditions with undefined-variable expectations.",
  "semantic_role": "unresolved-length-regression-definition",
  "owner_role": "length-condition-regression-suite",
  "operation": "Edit the bound public fixtures and diagnostic expectations to cover both unresolved-name shapes without changing unrelated expected behavior.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-fixture-owner-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "boundary-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:length-condition-regression-suite", "value": true, "evaluator": "file_exists", "description": "Current public diagnostic fixtures and their expectations are located and bound."}
  ],
  "effects": [
    {"key": "unresolved-length-regressions-defined", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "independent-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inferable-length-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-expectations",
      "instruction": "Inspect both unresolved-name fixture shapes and their expected undefined-variable diagnostics. Confirm no speculative len-as-condition message is expected and unrelated expectations remain unchanged. Retain public execution by the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:4215:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4215:repair:0f1245c2959f"],
  "evidence_refs": ["pylint-dev/pylint:4215:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:4cd11cf9432439d81e30121e",
  "read_set": ["role:length-condition-regression-suite"],
  "write_set": ["role:length-condition-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```
