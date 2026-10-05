# Correct lifecycle classification and deferred reporting

Apply only the portions established by inspection. Keep changes local to diagnostic policy, visitor state, and public regression coverage.

For executor classification, remove the two inferred executor constructor identities from the set that requires context use. Do not remove `multiprocessing.Pool` or unrelated resource constructors.

For delayed use, record recognized assigned constructor calls, suppress their immediate duplicate emission, remove a pending name when a later matching `with` consumes it, and report remaining calls at appropriate scope completion. Report an overwritten pending allocation before replacement. Pair inferable unpacked assignments conservatively; skip deductions that cannot be established. Maintain existing context-manager-owned and automatic-release exclusions. Initialize and clear state at the appropriate checker lifecycle boundaries.

The historical implementation searched name expressions, not arbitrary attribute or alias dataflow. Do not claim those extensions are established. Ensure visitor message guards permit the necessary state updates when the target message alone is enabled.

```arex-contract-v4
{
  "id": "workflow:verified-history:d5bff35cdcd2562bddc778f8:repair",
  "intent": "Correct over-eager resource-context diagnostics while retaining positive warnings.",
  "mechanism": "Narrow mandatory-context classification and defer reporting for assigned recognized calls until matching context use, overwrite, or scope exit.",
  "semantic_role": "diagnostic-lifecycle-correction",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Edit currently bound Python diagnostic owners and public regression fixtures according to the observed lifecycle review. Add persistent executor and delayed-with negative assertions, mixed-use positive assertions, and verify state reset boundaries by review. Do not broadly disable the diagnostic.",
  "kind": "edit",
  "inputs": [
    {
      "name": "lifecycle-review",
      "semantic_role": "resource-diagnostic-lifecycle-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "outputs": [
    {
      "name": "lifecycle-patch",
      "semantic_role": "resource-diagnostic-lifecycle-change",
      "artifact_kind": "patch",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "preconditions": [
    {"key": "current-lifecycle-review-recorded", "value": true, "evaluator": "evidence"},
    {"key": "current-owner-bound", "value": true, "evaluator": "symbol_exists", "description": "role:resource-diagnostic-owner"},
    {"key": "public-regression-owner-bound", "value": true, "evaluator": "file_exists", "description": "role:resource-regression-owner"},
    {"key": "historical-mechanism-applicable", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "lifecycle-diagnostic-policy-corrected", "value": true, "evaluator": "evidence"},
    {"key": "public-lifecycle-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-resource-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-context-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-lifecycle-diff",
      "instruction": "Review the current diff for exact inferred executor exclusions, conservative pending-call tracking, duplicate prevention, scope completion and reset, overwrite handling, public fixture additions, and absence of broad diagnostic suppression. These are expected changes, not observed success until reviewed.",
      "evidence_refs": ["pylint-dev/pylint:4689:fix", "pylint-dev/pylint:4689:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:resource-diagnostic-owner", "role:resource-regression-owner"],
  "write_set": ["role:resource-diagnostic-owner", "role:resource-regression-owner"],
  "source_ids": ["pylint-dev/pylint:4689:repair:dd54e55265c5"],
  "evidence_refs": ["pylint-dev/pylint:4689:fix", "pylint-dev/pylint:4689:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:d5bff35cdcd2562bddc778f8"
}
```

Here `symbol_exists` and `file_exists` must resolve the explicit `role:` bindings stated in the predicate descriptions in the current checkout. They do not establish the semantic applicability predicate, which requires separate evidence-backed review.
