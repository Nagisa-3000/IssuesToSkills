# Inspect the inference boundary

Read current code and use a public reproduction to distinguish discovery in module locals from successful inference. Locate both semantic owners and record hashed anchors. Do not modify tracked checkout files. A contradicted boundary rejects this mechanism; missing observations permit further probes only.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:inspect",
  "intent": "Establish applicability and bind the current semantic owners.",
  "mechanism": "Inspect the optional module-export consumer and reproduce undefined augmented export inference.",
  "semantic_role": "inference-boundary-discovery",
  "owner_role": "module-export-checker",
  "operation": "Read current code and run a public minimal reproduction without modifying tracked files. Identify the failing inference-consumption expression, documented exception type, successful path, independent diagnostics, and regression-suite owner.",
  "kind": "probe",
  "inputs": [],
  "outputs": [],
  "preconditions": [],
  "effects": [
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "matching-inference-failure-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "undefined-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "successful-export-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "boundary-confirmed",
      "instruction": "Inspect current code anchors and public probe output. Confirm that consuming the inferred __all__ raises the documented inference-failure exception on an undefined augmented assignment, that the check is optional, and that tracked files did not change.",
      "evidence_refs": ["pylint-dev/pylint:8740:body", "pylint-dev/pylint:8740:fix", "pylint-dev/pylint:8740:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8740:repair:331e48f74654"],
  "evidence_refs": ["pylint-dev/pylint:8740:body", "pylint-dev/pylint:8740:fix", "pylint-dev/pylint:8740:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8",
  "read_set": ["role:module-export-checker", "role:export-regression-suite"],
  "write_set": []
}
```

The effects are observations to establish in the current checkout, not claims that this authored Action has run. Bind the Oracle to a current public command before execution.
