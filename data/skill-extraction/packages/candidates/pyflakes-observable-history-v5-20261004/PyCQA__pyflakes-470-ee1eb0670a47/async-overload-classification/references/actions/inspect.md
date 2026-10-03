# Inspect the diagnostic and classification boundary

Locate the current overload predicate, function-node compatibility owner, and public tests. Compare equivalent sync and async overload sequences. Review whether the async node fails the type guard before typing decorator inspection.

Record real bindings, code anchors, runtime policy, and public results. Reject this hypothesis if async nodes are already recognized or decorator resolution causes the failure. UNKNOWN findings permit further probing, not editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:inspect",
  "intent": "Determine whether a synchronous-only function-node guard causes async overload diagnostics.",
  "mechanism": "Compare sync and async overload diagnostics and inspect the AST classification boundary.",
  "semantic_role": "classification-diagnosis",
  "owner_role": "overload-classification",
  "operation": "Locate current owners and gather public mechanism evidence without editing.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "classification-findings",
      "semantic_role": "overload-classification-findings",
      "artifact_kind": "owner-map-and-probe-record",
      "language": "python",
      "scope": "current-checkout-overload-analysis",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "classification-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-node-boundary",
      "instruction": "Record current owner bindings and public sync/async diagnostics. Review whether the source guard excludes AsyncFunctionDef while retaining typing decorator recognition. Record contradictory or unknown findings explicitly.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c",
  "read_set": ["role:overload-classification", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "exclusions": [
    {"key": "async-node-already-recognized", "value": true, "evaluator": "evidence"},
    {"key": "failure-caused-by-decorator-resolution", "value": true, "evaluator": "evidence"}
  ]
}
```
