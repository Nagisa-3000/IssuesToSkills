# Probe the current inference boundary

Read current code and public diagnostics without editing tracked resources. Bind semantic owners rather than assuming the [historical paths](../episode.md) still apply. Record the exception hierarchy, callback anchors, and fixture conventions in TaskContext.

```arex-contract-v4
{
  "id": "workflow:verified-history:4cd11cf9432439d81e30121e:probe",
  "intent": "Determine whether the current crash matches the supported inference boundary.",
  "mechanism": "Trace unresolved length-argument inference and inspect the exception family and diagnostic fixture owner.",
  "semantic_role": "inference-boundary-binding",
  "owner_role": "length-condition-checker",
  "operation": "Read current public code, run the bound public reproduction, and record checker and fixture bindings plus compatible, incompatible, or unknown findings. Do not edit tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [],
  "preconditions": [],
  "effects": [
    {"key": "current-boundary-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "current-fixture-owner-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "independent-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inferable-length-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-boundary",
      "instruction": "Inspect current inference consumption and exception hierarchy; run the bound unresolved-name reproduction. Record compatibility and real role bindings, diagnostics, and traceback presence. Check that tracked source and fixtures were not modified.",
      "evidence_refs": ["pylint-dev/pylint:4215:body", "pylint-dev/pylint:4215:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4215:repair:0f1245c2959f"],
  "evidence_refs": ["pylint-dev/pylint:4215:body", "pylint-dev/pylint:4215:fix", "pylint-dev/pylint:4215:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:4cd11cf9432439d81e30121e",
  "read_set": ["role:length-condition-checker", "role:length-condition-regression-suite"],
  "write_set": []
}
```

Review completion is not proof of compatibility. Subsequent edits require affirmative evidence that the local boundary and exception semantics match.
