# Locate the satisfaction transition

Inspect current public source without editing it. Bind the actual Python call-accounting owner and its regression harness, record hashed anchors, and run the public reproduction with current diagnostics. Confirm that positional-only metadata and a keyword collector coexist, and that same-name keyword processing incorrectly marks the positional parameter supplied.

A correct diagnostic makes repair inapplicable. Missing inference or branch evidence permits further probes only. Empty oracle command arrays require current public argv bindings before execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89:locate",
  "intent": "Confirm and bind the keyword-accounting defect.",
  "mechanism": "Inspect positional-only metadata, keyword collection, and the supplied-state transition; observe the public reproduction.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "call-argument-accounting",
  "operation": "Read current source and run a public probe without source edits; record current role bindings, anchors, and diagnostic observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "bound-accounting",
      "semantic_role": "call-accounting-repair-context",
      "artifact_kind": "code-and-test-bindings",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "accounting-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-test-harness-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-binding-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-current-mechanism",
      "instruction": "Inspect current signature metadata and supplied-state logic. Run the public required-positional-only plus **kwargs reproduction, record diagnostics and anchors, and verify that no source files changed.",
      "evidence_refs": ["pylint-dev/pylint:8559:body", "pylint-dev/pylint:8559:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:call-argument-accounting", "role:argument-regression-harness"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8559:repair:2db55f6a4896"],
  "evidence_refs": ["pylint-dev/pylint:8559:body", "pylint-dev/pylint:8559:fix"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:33b6359d2826e0cbb3dcbe89"
}
```

Output state `mechanism-confirmed` is conditional on actual supporting observations, not guaranteed by running the probe.
