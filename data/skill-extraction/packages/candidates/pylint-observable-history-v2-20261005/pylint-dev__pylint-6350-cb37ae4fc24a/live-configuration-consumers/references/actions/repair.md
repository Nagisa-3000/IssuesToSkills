# Repair live ownership and add regression

After current compatibility checks pass, bind integrated consumers to the authoritative namespace object rather than another copy. Keep private namespace storage for standalone construction. Migrate every affected runtime read and remove redundant synchronization only after confirming that it has no remaining responsibility.

The historical migrated settings were minimum similarity lines, ignore comments, ignore docstrings, ignore imports, and ignore signatures. Preserve their current meanings. Inspect initialization order before assigning defaults: do not overwrite values already parsed in the current lifecycle.

Add a public regression using two import-only files exceeding the effective duplicate threshold. Enable the target duplicate diagnostic and ignore-import option while isolating unrelated unused-import output. Adding this assertion is not executing it.

```arex-contract-v4
{
  "id": "workflow:verified-history:44cf4d12e6c9f03961fb6377:repair",
  "intent": "Remove stale option copies while preserving standalone construction and public option semantics.",
  "mechanism": "Share live host configuration in integrated mode, retain private standalone storage, migrate runtime reads, remove redundant synchronization, and add an import-only regression.",
  "semantic_role": "live-configuration-repair",
  "owner_role": "configuration-consumer",
  "operation": "Edit the bound Python consumer and public regression suite to implement confirmed compatible namespace ownership and public option coverage.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosed-consumer",
      "semantic_role": "configuration-consumer",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "configuration-and-similarity",
      "phase": "repair",
      "state": "diagnosed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "edited-consumer",
      "semantic_role": "configuration-consumer",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "configuration-and-similarity",
      "phase": "validation",
      "state": "edited-with-regression",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "ownership-diagnosis-recorded", "value": true, "evaluator": "evidence"},
    {"key": "stale-option-copies-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "live-namespace-compatible", "value": true, "evaluator": "evidence"},
    {"key": "initialization-order-safe", "value": true, "evaluator": "evidence"},
    {"key": "role:configuration-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "runtime-options-live", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "standalone-option-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "similarity-algorithm-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-live-ownership",
      "instruction": "Review the edited diff for exact host namespace sharing, separate standalone storage, consistent affected option reads, safe initialization, removal only of redundant synchronization, and a public two-file import-only regression. Reject diagnostic disabling or threshold workarounds. Diff review alone does not establish runtime success.",
      "evidence_refs": ["pylint-dev/pylint:6350:fix", "pylint-dev/pylint:6350:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:configuration-consumer", "role:configuration-regression-suite"],
  "write_set": ["role:configuration-consumer", "role:configuration-regression-suite"],
  "source_ids": ["pylint-dev/pylint:6350:repair:cb37ae4fc24a"],
  "evidence_refs": ["pylint-dev/pylint:6350:fix", "pylint-dev/pylint:6350:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:44cf4d12e6c9f03961fb6377"
}
```
