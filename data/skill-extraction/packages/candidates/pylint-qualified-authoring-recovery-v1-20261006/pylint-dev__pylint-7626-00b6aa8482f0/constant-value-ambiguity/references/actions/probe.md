# Probe the inference-to-diagnostic boundary

Locate owners by semantic responsibility rather than historical paths. Read source and run public reproductions without modifying repository files. Observe inferred alternatives and emitted messages; matching owner names alone does not establish the mechanism.

```arex-contract-v4
{
  "id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:probe",
  "intent": "Determine whether value ambiguity is being lost before Boolean rewrite emission.",
  "mechanism": "Compare the operand's inference alternatives with safe-inference selection and consumer uncertainty handling.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "python-boolean-rewrite-boundary",
  "operation": "Read current helper, consumer, and harness contracts; execute a public loop-reassignment reproduction and definite/unknown controls. Do not edit repository files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "confirmed-boundary",
      "semantic_role": "constant-ambiguity-repair-context",
      "artifact_kind": "public-observation-record",
      "language": "python",
      "scope": "safe-inference-and-boolean-rewrite",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "mechanism-observed", "value": true, "evaluator": "evidence"},
    {"key": "owners-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "default-inference-contract-preserved", "value": true, "evaluator": "evidence"},
    {"key": "definite-value-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-ambiguity",
      "instruction": "Record current code anchors and public outputs showing unequal same-type constants, helper ambiguity handling, and the consumer's resulting unsafe suggestion. Also record definite-value and unknown-operand controls. If this mechanism is absent, do not produce a mechanism-confirmed output.",
      "evidence_refs": ["pylint-dev/pylint:7626:body", "pylint-dev/pylint:7626:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7626:repair:00b6aa8482f0"],
  "evidence_refs": ["pylint-dev/pylint:7626:body", "pylint-dev/pylint:7626:fix"],
  "read_set": ["role:python-safe-inference-helper", "role:python-boolean-rewrite-consumer", "role:python-public-regression-harness"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3"
}
```

An empty command is intentionally unbound. Populate a current public Oracle binding before execution. If observations are unknown, retain UNKNOWN rather than asserting the output state.
