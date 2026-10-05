# Locate and confirm

Trace the outer dictionary lookup, inner subscript, and inner base separately. Read the current public traceback and checker branch; verify that an Attribute base reaches a Name-only access. Bind the current checker and diagnostic fixture owners, and record existing supported and negative expectations.

This probe does not edit repair targets. Test artifacts from a public probe do not authorize source modifications.

```arex-contract-v4
{
  "id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0:locate",
  "intent": "Establish applicability and current semantic owner bindings.",
  "mechanism": "Trace the public attribute-subscript shape to the unchecked inner-base name access.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "lookup-checker",
  "operation": "Inspect public current code, traceback, AST shape, and diagnostic fixtures without editing repair targets; record pinned anchors, owner bindings, and evidence for the specific short-circuit guard opportunity.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "confirmed-bindings",
      "semantic_role": "lookup-repair-bindings",
      "artifact_kind": "binding-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed"
    }
  ],
  "preconditions": [
    {"key": "public-input-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:lookup-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:lookup-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "supported-name-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-negative-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-unsafe-access",
      "instruction": "Use bound current public anchors and an AST/reproduction probe to confirm an Attribute inner base reaches the unchecked name read. Record the supported Name path and existing negative expectations. Confirm the checker and fixture targets were not edited.",
      "evidence_refs": ["pylint-dev/pylint:6557:body", "pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6557:repair:5fcccc13f1f7"],
  "evidence_refs": ["pylint-dev/pylint:6557:body", "pylint-dev/pylint:6557:fix", "pylint-dev/pylint:6557:regression"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:7c6d31165b0fa4f2628a0ec0",
  "read_set": ["role:lookup-checker", "role:lookup-regression-suite"],
  "write_set": []
}
```

The output is expected rather than already observed. Empty command arrays require current public Oracle bindings. An unconfirmed mechanism permits further probes only.
