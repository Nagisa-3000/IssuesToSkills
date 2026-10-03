# Repair assignment-expression classification and routing

Apply only after current evidence confirms the mismatch.

Distinguish walrus-target bindings from ordinary assignments in the current classifier. For that binding category only, select the first non-comprehension scope by walking outward across contiguous comprehension scopes at insertion. Do not skip actual function scopes.

Retain unrelated annotation guards, duplicate-binding handling, and use-tracking bookkeeping. Add public single-generator and nested-comprehension assertions equivalent to the historical tests. Gate syntax-dependent assertions for unsupported Python versions where appropriate, but require a supported runtime for validation.

The effects below are expected repair obligations, not already observed results. Keep the explicit validate Action in the plan.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:repair",
  "intent": "Bind assignment-expression targets in their enclosing non-comprehension scope without rerouting ordinary bindings.",
  "mechanism": "Introduce or use a distinct assignment-expression binding category and skip contiguous comprehension scopes only for that category.",
  "semantic_role": "scope-routing-repair",
  "owner_role": "assignment-binding-router",
  "operation": "Edit the current binding classification and insertion owners to implement the evidenced routing distinction; add single-generator and nested-comprehension public assertions in the current regression-test owner.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-routing",
      "semantic_role": "assignment-expression-routing-state",
      "artifact_kind": "source-and-probe-record",
      "language": "python",
      "scope": "analyzer-binding-and-regressions",
      "phase": "pre-repair",
      "state": "reviewed"
    }
  ],
  "outputs": [
    {
      "name": "patched-routing",
      "semantic_role": "assignment-expression-routing-state",
      "artifact_kind": "source-and-probe-record",
      "language": "python",
      "scope": "analyzer-binding-and-regressions",
      "phase": "post-repair",
      "state": "awaiting-validation"
    }
  ],
  "preconditions": [
    {"key": "routing-review-recorded", "value": true, "evaluator": "evidence"},
    {"key": "walrus-routing-mismatch-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-expression-syntax-supported", "value": true, "evaluator": "evidence"},
    {"key": "contiguous-comprehension-routing-applicable", "value": true, "evaluator": "evidence", "description": "Current review confirms the binding should skip only the comprehension-scope chain, not a real function boundary."},
    {"key": "role:assignment-binding-router", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comprehension-scope-model", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:scope-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "walrus-target-enclosing-scope-visible", "value": true, "evaluator": "evidence"},
    {"key": "single-and-nested-regressions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-assignment-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "iteration-variable-isolation-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-binding-bookkeeping-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-routing-diff",
      "instruction": "Review the current diff: only assignment-expression bindings skip contiguous comprehension scopes; ordinary assignments and iteration targets retain their owners; unrelated binding bookkeeping remains intact; and both public regression assertions are present.",
      "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4",
  "read_set": [
    "role:assignment-binding-router",
    "role:comprehension-scope-model",
    "role:scope-regression-tests"
  ],
  "write_set": [
    "role:assignment-binding-router",
    "role:scope-regression-tests"
  ],
  "invalidates": ["public-validation-observed"]
}
```
