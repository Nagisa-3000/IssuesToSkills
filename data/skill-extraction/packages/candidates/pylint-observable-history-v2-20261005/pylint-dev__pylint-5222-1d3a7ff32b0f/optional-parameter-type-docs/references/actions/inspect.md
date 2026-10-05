# Inspect recognition and collection

Read current owners and run a public reproduction without modifying tracked production or test files. Record observations separately.

```arex-contract-v4
{
  "id": "workflow:verified-history:00bdb5de0892c0cbbab00de9:inspect",
  "package_id": "workflow:verified-history:00bdb5de0892c0cbbab00de9",
  "resource": "references/actions/inspect.md",
  "kind": "probe",
  "intent": "Determine whether omitted inline types cause rejection of described NumPy parameter entries.",
  "mechanism": "Trace entry matching and independent documentation/type membership using a mixed public reproduction.",
  "semantic_role": "diagnose-optional-inline-types",
  "owner_role": "numpy-parameter-parser",
  "operation": "Locate the current NumPy parser, section splitter, checker consumer and tests. Record pinned revision and anchor hashes. Observe diagnostics for annotated and unannotated name-only headers with descriptions, compared with an explicitly typed entry. Confirm style selection and trace the rejection. Do not edit tracked files.",
  "inputs": [],
  "outputs": [
    {"name": "diagnosis", "semantic_role": "optional-type-diagnosis", "artifact_kind": "inspection-report", "language": "python", "scope": "parameter-documentation-checker", "phase": "diagnosis", "state": "bound-and-observed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "entry-rejection-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-type-diagnostics", "value": "preserved", "evaluator": "evidence"},
    {"key": "adjacent-docstring-behavior", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnose-entry-rejection",
      "instruction": "Record actual diagnostics, current owner symbols, hashes and NumPy style selection. Establish whether description-only entries are rejected despite their descriptions. Distinguish the unannotated argument's legitimate missing-type diagnostic. Verify inspection leaves tracked files unchanged.",
      "evidence_refs": ["pylint-dev/pylint:5222:body", "pylint-dev/pylint:5222:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:numpy-parameter-parser", "role:parameter-documentation-checker", "role:documentation-checker-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5222:repair:1d3a7ff32b0f"],
  "evidence_refs": ["pylint-dev/pylint:5222:body", "pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"]
}
```

Effects are intended observations, not predeclared successful findings. If the mechanism is absent, record it as unsupported or already corrected; do not force a patch. Unknown ownership permits further probes only.
