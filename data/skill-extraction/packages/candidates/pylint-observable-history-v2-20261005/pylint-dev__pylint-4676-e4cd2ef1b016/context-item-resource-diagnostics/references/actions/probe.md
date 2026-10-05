# Probe semantic ownership and boundaries

Locate the current resource diagnostic and public test owners. Read the diagnostic exclusion and inspect the flagged call's AST ancestry, frame, and source spans. Contrast the conditional context-item reproduction with a separate body resource call. Do not change tracked files.

Record real bindings and applicability evidence. Names resembling historical symbols do not prove compatible semantics.

```arex-contract-v4
{
  "id": "workflow:verified-history:ec6290f765c15f3fdc7283d4:probe",
  "intent": "Determine whether immediate-parent-only recognition causes a context-item false positive.",
  "mechanism": "Inspect the diagnostic condition and AST ancestry, frame boundaries, and item source spans for the reproduction and body control.",
  "semantic_role": "context-membership-diagnosis",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Locate current semantic owners and run a bound read-only public diagnostic probe; record code anchors, bindings, and applicability evidence without editing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "applicability-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-body-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-resource-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "probe-membership",
      "instruction": "Record public diagnostic output for a conditional context item and a separate body call, locate current checker and test owners, and inspect AST frame and item-span semantics. Explain whether immediate-parent-only exclusion causes the warning. Verify no tracked-file changes.",
      "evidence_refs": ["pylint-dev/pylint:4676:body", "pylint-dev/pylint:4676:fix", "pylint-dev/pylint:4676:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4676:repair:e4cd2ef1b016"],
  "evidence_refs": ["pylint-dev/pylint:4676:title", "pylint-dev/pylint:4676:body", "pylint-dev/pylint:4676:fix", "pylint-dev/pylint:4676:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:ec6290f765c15f3fdc7283d4",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "write_set": []
}
```

An applicability review can conclude insufficient or not applicable. The output is an observed binding record, not permission to repair unless the repair prerequisites pass.
