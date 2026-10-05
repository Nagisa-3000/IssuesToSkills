# Repair exception aggregation and assertions

Modify the bound current analyzer only after confirming the matching defect and compatible child semantics.

The historical rule used `all` over `TryExcept.get_children()` and removed handler exclusion from generic recursion. Apply the corresponding semantic correction, not a blind universal all-children algorithm.

Preserve nested-function exclusion and raise handling. The historical conditional helper required a later direct sibling return for an `if` without `else`; adopt this only when current evidence establishes compatibility and need.

Add two positive cases and both explicit-`None` negatives. Retain earlier expectations rather than accepting missing diagnostics. If stricter self-lint exposes internal implicit-`None` paths, make them explicit only after confirming their runtime result already is `None`; exclude unrelated rewrites.

```arex-contract-v4
{
  "id": "workflow:verified-history:3d852bae39e6f31c4d255bd3:repair",
  "intent": "Account for exception-handler fallthrough in return completeness.",
  "mechanism": "Use exception-inclusive completeness aggregation and encode positive and explicit-None regressions.",
  "semantic_role": "exception-return-completeness-repair",
  "owner_role": "return-completeness-analyzer",
  "operation": "Edit the bound analyzer and regression suite; make only evidenced behavior-neutral internal explicit-None adjustments where needed.",
  "kind": "edit",
  "inputs": [
    {"name": "probed-analysis", "semantic_role": "return-analysis-checkout", "artifact_kind": "checkout-binding", "language": "python", "scope": "return-consistency", "phase": "repair", "state": "probed", "optional": false}
  ],
  "outputs": [
    {"name": "edited-analysis", "semantic_role": "return-analysis-checkout", "artifact_kind": "checkout-binding", "language": "python", "scope": "return-consistency", "phase": "validation", "state": "edited", "optional": false}
  ],
  "preconditions": [
    {"key": "applicability-observed", "value": true, "evaluator": "evidence"},
    {"key": "matching-handler-fallthrough-defect", "value": true, "evaluator": "evidence"},
    {"key": "compatible-exception-child-semantics", "value": true, "evaluator": "evidence"},
    {"key": "role:return-completeness-analyzer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:return-consistency-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "exception-aggregation-repaired", "value": true, "evaluator": "evidence"},
    {"key": "regression-matrix-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "explicit-none-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-repair-diff",
      "instruction": "Review handler inclusion and completeness aggregation, retained conditional/nested-function/raise semantics, all four regression cases, and retained earlier diagnostics. Confirm any internal return None only makes an existing implicit None result explicit.",
      "evidence_refs": ["pylint-dev/pylint:3468:fix", "pylint-dev/pylint:3468:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3468:repair:fb332490c2e5"],
  "evidence_refs": ["pylint-dev/pylint:3468:fix", "pylint-dev/pylint:3468:regression"],
  "read_set": ["role:return-completeness-analyzer", "role:return-consistency-regression-suite", "role:checker-internal-fallthrough-callers"],
  "write_set": ["role:return-completeness-analyzer", "role:return-consistency-regression-suite", "role:checker-internal-fallthrough-callers"],
  "invalidates": ["public-validation-observed", "diagnostic-observations-fresh"],
  "exclusions": [
    {"key": "runtime-policy-change-requested", "value": true, "evaluator": "evidence"},
    {"key": "incompatible-ast-representation", "value": true, "evaluator": "evidence"}
  ],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:3d852bae39e6f31c4d255bd3"
}
```

Retain [validation](validate.md). Diff review is not test execution. Intended repair effects require fresh public confirmation.
