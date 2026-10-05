# Inspect the tracking boundary

Locate current owners and inspect resource-call admission, target-field extraction, deferred tracking, and immediate diagnostic emission. Probe AST types and lint public snippets; do not execute subprocess calls themselves.

This probe does not edit tracked source or assertions. Put generated artifacts outside tracked source and record their locations. Role-based existence predicates require real current bindings and boolean values.

```arex-contract-v4
{
  "id": "workflow:verified-history:4b0b98b3c492f42522a4c12d:inspect",
  "intent": "Determine whether unsupported targets enter name-based deferred resource tracking.",
  "mechanism": "Compare target types with consumed fields and confirm a separate immediate diagnostic path.",
  "semantic_role": "tracking-boundary-inspection",
  "owner_role": "context-manager-assignment-tracker",
  "operation": "Read current owner bindings and run public AST and linter probes for names, attributes, list items, and dictionary items; record hashed anchors without source edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "assessment",
      "semantic_role": "assignment-tracking-assessment",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout-resource-checker",
      "phase": "pre-edit",
      "state": "assessed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-base-pinned", "value": true, "evaluator": "evidence"},
    {"key": "role:context-manager-assignment-tracker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "tracking-boundary-assessed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-target-tracking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "immediate-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-target-admission",
      "instruction": "Record actual target types, unsafe extraction, supported fields, and the separate immediate diagnostic path using current public probes. Compare tracked source hashes before and after inspection to confirm no edits.",
      "evidence_refs": ["pylint-dev/pylint:4732:body", "pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:context-manager-assignment-tracker", "role:immediate-resource-diagnostic", "role:resource-checker-functional-assertions"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4732:repair:a2c166cf5fc3"],
  "evidence_refs": ["pylint-dev/pylint:4732:body", "pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:4b0b98b3c492f42522a4c12d"
}
```

An assessment can report mismatch or UNKNOWN. Its existence does not authorize an edit until the modifying Action's semantic prerequisites are independently satisfied. Effects are intended properties, not execution claims.
