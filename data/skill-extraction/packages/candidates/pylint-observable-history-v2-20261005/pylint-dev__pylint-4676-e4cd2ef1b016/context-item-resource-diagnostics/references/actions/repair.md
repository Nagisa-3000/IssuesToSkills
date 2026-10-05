# Repair recognition and regression assertions

Only proceed when the current probe confirms the supported mechanism and compatible AST semantics. Replace immediate-parent-only exclusion with the evidenced frame-bounded context-item membership check at the bound semantic owner.

The historical check walks toward the call's frame, then compares the call's line with the first-to-last item interval at the first `With` ancestor. Confirm that current spans distinguish the relevant header expressions from body calls. If they cannot, stop; this evidence does not authorize an invented bridge or a blanket ancestor exemption.

Add public assertions for ternary resource branches, direct single-line and multiline context items. Retain the independent body-call warning control. Keep the diagnostic enabled.

```arex-contract-v4
{
  "id": "workflow:verified-history:ec6290f765c15f3fdc7283d4:repair",
  "intent": "Correct context-item recognition and encode its diagnostic boundaries.",
  "mechanism": "Replace immediate-parent identity with frame-bounded ancestor traversal and context-item source-interval membership, accompanied by regression assertions.",
  "semantic_role": "context-membership-repair",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Edit the bound checker owner and public regression-test owner to recognize conditional context items while retaining unmanaged-body warning expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "owner-bindings",
      "semantic_role": "context-membership-owner-bindings",
      "artifact_kind": "binding-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "observed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate-checkout",
      "semantic_role": "context-membership-repair-candidate",
      "artifact_kind": "checkout",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "supported-immediate-parent-mechanism", "value": true, "evaluator": "evidence"},
    {"key": "role:resource-diagnostic-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:resource-diagnostic-test-owner", "value": true, "evaluator": "file_exists"},
    {"key": "frame-and-item-span-semantics-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "context-item-recognition-corrected", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-body-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-resource-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-membership-edit",
      "instruction": "Review the current public diff for bounded item membership rather than blanket With-descendant suppression. Confirm conditional, direct single-line, and multiline assertions and retention of the body-warning control. Behavioral acceptance requires the explicit validate Action.",
      "evidence_refs": ["pylint-dev/pylint:4676:fix", "pylint-dev/pylint:4676:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4676:repair:e4cd2ef1b016"],
  "evidence_refs": ["pylint-dev/pylint:4676:fix", "pylint-dev/pylint:4676:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:ec6290f765c15f3fdc7283d4",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "write_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "blanket-with-descendant-suppression", "value": true, "evaluator": "evidence"}
  ]
}
```

Effects describe required candidate behavior, not observed success. Editing makes prior validation observations stale; it does not remove the obligation to preserve adjacent behavior.
