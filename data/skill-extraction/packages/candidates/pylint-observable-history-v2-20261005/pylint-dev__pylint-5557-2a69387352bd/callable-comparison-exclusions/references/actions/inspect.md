# Inspect current inference and diagnostic ownership

Locate the current callable-comparison diagnostic owner and public comparison regression owner. Record hashed code anchors and actual output from the public reproduction. Inspect inferred node types, qualified decorator names, immediate body elements, and the emission condition.

Do not invoke the compared function. This read/probe operation must not edit tracked source. Disposable probe artifacts are distinct from source changes. A reviewed diagnosis can report incompatibility or uncertainty; it does not imply permission to repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:c24ac7f0cdc266e6796600de:inspect",
  "intent": "Determine whether a current false positive has the source-supported callable classification mechanism.",
  "mechanism": "Inspect public output and safely inferred function-like operands for immediate Raise nodes and qualified special-form decoration.",
  "semantic_role": "classify-current-mechanism",
  "owner_role": "callable-comparison-checker",
  "operation": "Locate current owners, reproduce the warning with a bound public probe, inspect the warning gate and inferred representation, and record an applicability decision without modifying tracked source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "callable-comparison-diagnosis",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "mechanism-applicability-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-callable-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "noncallable-and-unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-inference",
      "instruction": "Bind a current public reproduction and inference probe. Record warning identity/location, inferred node category, immediate Raise presence, decorator names, exactly-one gate, and current owner hashes. Verify tracked source is unchanged and the compared callable was not invoked. Report unsupported facts as UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:5557:body", "pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5557:repair:2a69387352bd"],
  "evidence_refs": ["pylint-dev/pylint:5557:body", "pylint-dev/pylint:5557:fix", "pylint-dev/pylint:5557:regression"],
  "read_set": ["role:callable-comparison-checker", "role:comparison-regression-suite"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:c24ac7f0cdc266e6796600de"
}
```
