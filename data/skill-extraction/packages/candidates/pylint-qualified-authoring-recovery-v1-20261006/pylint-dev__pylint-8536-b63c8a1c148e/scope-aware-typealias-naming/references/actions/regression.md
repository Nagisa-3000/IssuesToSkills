# Add diagnostic and non-alias controls

Use the current public naming fixture and expectation format. Include bad and good explicit local aliases, a good union-valued explicit alias, and an ordinary union annotation followed by assignment. Preserve existing assertions.

```arex-contract-v4
{
  "id": "workflow:verified-history:b980c9ec644c821d41e50e10:regression",
  "intent": "Expose the local alias false negative and guard against annotation false positives.",
  "mechanism": "Extend public naming fixtures with explicit aliases and an ordinary annotated local control.",
  "semantic_role": "establish-regression-controls",
  "owner_role": "naming-regression-suite",
  "operation": "Add function-local alias controls and the bad alias diagnostic expectation, using current locations and message format while retaining previous expectations.",
  "kind": "edit",
  "inputs": [
    {
      "name": "classification-findings",
      "semantic_role": "local-alias-classification-findings",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "function-local-naming",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "local-classification-defect-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:naming-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "local-alias-controls-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-variable-routing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-alias-policy-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-regression-assertions-retained", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-fixture-controls",
      "instruction": "Inspect fixtures and expectations for one bad explicit local alias expecting type-alias invalid-name, good simple and union-valued aliases without new naming expectations, and an ordinary union annotation followed by assignment. Confirm prior assertions remain.",
      "evidence_refs": ["pylint-dev/pylint:8536:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8536:repair:b63c8a1c148e"],
  "evidence_refs": ["pylint-dev/pylint:8536:regression"],
  "read_set": ["role:naming-regression-suite"],
  "write_set": ["role:naming-regression-suite"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:b980c9ec644c821d41e50e10"
}
```

Historical deletion statements prevented unrelated local-use diagnostics. Adapt fixture hygiene only as needed within this edit; it is not a separate production cleanup. Retain [final validation](validate.md).
