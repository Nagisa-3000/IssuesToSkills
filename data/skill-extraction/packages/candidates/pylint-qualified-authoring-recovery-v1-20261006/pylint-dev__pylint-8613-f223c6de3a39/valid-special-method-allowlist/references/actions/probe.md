# Probe the registry omission

Inspect current public owners and reproduce the warning without changing tracked source. Establish that registry membership, not signature or unrelated inference logic, causes rejection. Unknown diagnosis does not produce a confirmed port.

```arex-contract-v4
{
  "id": "workflow:verified-history:6811635fea96a3e3f778e2f1:probe",
  "intent": "Establish applicability of a narrow accepted-name repair.",
  "mechanism": "Trace a valid-method reproduction to an omitted entry in the consumed acceptance registry.",
  "semantic_role": "diagnose-registry-omission",
  "owner_role": "special-method-acceptance-registry",
  "operation": "Read diagnostic membership handling, locate current registry and fixture owners, establish public method validity, inspect no-warning conventions, and reproduce rejection without editing tracked source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "diagnosis", "semantic_role": "registry-omission-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "registry-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "method-validity-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "regression-harness-understood", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "invalid-name-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Record hashed current owner anchors, public validity evidence, enabled-diagnostic reproduction output, traced membership handling, and fixture assertion conventions. Confirm tracked source is unchanged. Emit confirmed diagnosis only if these checks establish the omission.",
      "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:fix", "pylint-dev/pylint:8613:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:special-method-acceptance-registry", "role:special-method-diagnostic-regression-suite"],
  "write_set": [],
  "exclusions": [
    {"key": "registry-omission-confirmed", "value": false, "evaluator": "evidence"}
  ],
  "source_ids": ["pylint-dev/pylint:8613:repair:f223c6de3a39"],
  "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:fix", "pylint-dev/pylint:8613:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:6811635fea96a3e3f778e2f1"
}
```

Empty commands require current public Oracle bindings. The read/probe operation has no tracked-source modifications; this is not a global unchanged-checkout invariant for the editing Workflow.
