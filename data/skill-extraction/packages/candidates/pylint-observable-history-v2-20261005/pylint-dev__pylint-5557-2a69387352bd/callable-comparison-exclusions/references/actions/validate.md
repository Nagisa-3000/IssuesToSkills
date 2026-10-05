# Execute public exclusion and preservation checks

Bind current public commands to the current checkout and test runner. Execute them after the modifying Action. Inspect diagnostic identities and locations rather than relying solely on process success; unrelated diagnostics can affect linter exit codes.

Check supported exclusions and ordinary comparison controls. Record actual results, failures, skips, and scope. Validation does not edit tracked source to conceal failures. Any subsequent modification makes its observation stale.

```arex-contract-v4
{
  "id": "workflow:verified-history:c24ac7f0cdc266e6796600de:validate",
  "intent": "Observe supported exclusions and preservation of adjacent public diagnostic behavior.",
  "mechanism": "Execute public reproductions and comparison regression tests with negative and positive controls.",
  "semantic_role": "validate-callable-classification",
  "owner_role": "comparison-regression-suite",
  "operation": "Run bound current public Oracles, inspect diagnostics and regression outcomes, record tri-state checks and scope, and refresh validation evidence without changing tracked source.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "callable-comparison-validation",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "supported-exclusions-implemented", "value": true, "evaluator": "evidence"},
    {"key": "supported-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence",
      "description": "A required successful effect, asserted only after actual public checks pass; failures or unknowns do not satisfy it."
    }
  ],
  "preserves": [
    {"key": "ordinary-callable-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "noncallable-and-unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-exclusions",
      "instruction": "Execute bound public reproductions. Verify absence of comparison-with-callable for Any, Optional, and a function with print() followed by a direct body Raise. Record unrelated diagnostics separately and check for inference crashes.",
      "evidence_refs": ["pylint-dev/pylint:5557:body", "pylint-dev/pylint:5557:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-comparison-controls",
      "instruction": "Execute bound current comparison regression tests and neighboring public controls. Verify that an ordinary nonraising bare function compared to a noncallable still warns, while two ordinary eligible callables and noncallable pairs retain baseline behavior. Check unrelated diagnostic expectations; record actual outcomes, skips, and scope.",
      "evidence_refs": ["pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:c24ac7f0cdc266e6796600de:repair"],
  "source_ids": ["pylint-dev/pylint:5557:repair:2a69387352bd"],
  "evidence_refs": ["pylint-dev/pylint:5557:body", "pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
  "read_set": ["role:callable-comparison-checker", "role:comparison-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:c24ac7f0cdc266e6796600de"
}
```
