# Validate target and preserved behavior

Bind public commands to the current repository test runner. Execute the focused alias regression and the existing annotation suite. Review or probe nearest-binding shadowing, unsupported modules, absent bindings, direct-name helpers, and receiver-shape restrictions.

If the original `Literal` reproduction remains relevant, run it separately and record its actual outcome. The historical `overload` regression does not independently establish all `Literal` behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:validate",
  "intent": "Observe target correctness and adjacent behavior after the edit.",
  "mechanism": "Run public regression checks and inspect lexical-binding boundary cases.",
  "semantic_role": "receiver-recognition-validation",
  "owner_role": "annotation-regression-suite",
  "operation": "Execute bound current public tests and boundary probes; record results against the edited anchors without changing production code.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "typing-helper-repair-candidate",
      "artifact_kind": "checkout-patch",
      "language": "python",
      "scope": "typing-helper-recognition",
      "phase": "current",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "typing-helper-validation-results",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "typing-helper-recognition",
      "phase": "current",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "repair-candidate-available",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "current-public-oracles-bound",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence",
      "description": "Results are recorded, including any failures; recording alone does not establish repair success."
    }
  ],
  "preserves": [
    {
      "key": "adjacent-helper-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "aliased-overload-regression",
      "instruction": "Run the current counterpart of the supplied aliased typing-module overload regression and record whether unexpected diagnostics occur.",
      "evidence_refs": ["PyCQA/pyflakes:561:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-binding-behavior",
      "instruction": "Run the current annotation suite and public boundary probes for unaliased imports, direct-name helpers, nearer shadowing bindings, unsupported modules, unbound receivers, and non-simple-name receivers. Reject any violation of preserved behavior.",
      "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:2f5b3f202404ca13ec4e8055:repair"
  ],
  "read_set": [
    "role:typing-helper-detector",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:fix", "PyCQA/pyflakes:561:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

Empty historical command arrays are not execution authorization. Obtain current argv bindings first. FAIL rejects success; UNKNOWN is not a pass. Any further edit makes the validation observation stale and requires revalidation.
