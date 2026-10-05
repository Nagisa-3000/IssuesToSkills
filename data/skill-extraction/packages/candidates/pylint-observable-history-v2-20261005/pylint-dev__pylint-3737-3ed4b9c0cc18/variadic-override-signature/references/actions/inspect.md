# Inspect and reproduce

Bind current owners and public probes. Inspect without modifying tracked source. Record tri-state findings; a reviewed assessment does not itself establish applicability.

```arex-contract-v4
{
  "id": "workflow:verified-history:65539eb7c9013462474b0b56:inspect",
  "intent": "Determine whether current code exhibits the supported default-count false-positive mechanism.",
  "mechanism": "Observe override defaults, reference defaults, and positional variadic metadata at the diagnostic decision.",
  "semantic_role": "diagnose-default-count-compatibility",
  "owner_role": "override-signature-checker",
  "operation": "Read current checker and public tests. Run a bound public reproduction with a defaulted base parameter and collecting override. Record hashed anchors, causal branch, positional variadic representation, nonvariadic controls, and PASS/FAIL/UNKNOWN applicability findings. Do not edit tracked source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "assessment",
      "semantic_role": "default-count-compatibility-assessment",
      "artifact_kind": "public-code-and-probe-record",
      "language": "python",
      "scope": "override-signature-checking",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:override-signature-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "mechanism-assessment-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonvariadic-default-loss-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "preceding-argument-mismatch-branch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-causal-branch",
      "instruction": "Capture the diagnostic and trace whether fewer declared defaults trigger signature-differs despite positional variadic presence. Record evidence-backed tri-state checks for supported-default-count-mechanism-observed and positional-variadic-binding-confirmed. Compare tracked-source diffs before and after inspection to confirm no source edit.",
      "evidence_refs": ["pylint-dev/pylint:3737:body", "pylint-dev/pylint:3737:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:override-signature-checker", "role:override-signature-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3737:repair:3ed4b9c0cc18"],
  "evidence_refs": ["pylint-dev/pylint:3737:body", "pylint-dev/pylint:3737:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:65539eb7c9013462474b0b56"
}
```

UNKNOWN permits more probes only. A different causal mechanism rejects the repair branch; do not invent an adapter.
