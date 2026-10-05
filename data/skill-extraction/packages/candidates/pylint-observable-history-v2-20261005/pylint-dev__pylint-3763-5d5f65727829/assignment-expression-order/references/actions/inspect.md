# Inspect evaluation order and bind owners

Read current code and public fixtures without changing tracked files. Record the actual diagnostic, statement/value types, assignment/read locations, execution order, same-frame relationship, ancestry, runtime predicates, and test entry points. Hash code anchors and resolve semantic owners in the current checkout.

For multiline strings, directly inspect parser locations; a pre-3.9 version number alone is insufficient. Do not emit a confirmed report when order or scope facts are unknown or contradict the premise.

```arex-contract-v4
{
  "id": "workflow:verified-history:0d5d796f6706ce7801b87899:inspect",
  "intent": "Determine whether the current false diagnostic matches the supported assignment-before-read mechanism.",
  "mechanism": "Compare Python evaluation order with containing-statement recognition and definition/read location logic.",
  "semantic_role": "mechanism-inspection",
  "owner_role": "variable-order-checker",
  "operation": "Read bound checker, runtime policy, and public fixtures; run bound public diagnostic and AST probes; emit an evidence-backed owner and mechanism report without modifying tracked code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspection",
      "semantic_role": "assignment-order-binding-report",
      "artifact_kind": "public-evidence-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-reproduction-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-before-read-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-frame-and-ancestry-match", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-early-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "independent-expression-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "frame-and-ancestry-constraints-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-current-mechanism",
      "instruction": "Bind public AST and diagnostic probes to current code. Record diagnostic output, owner types, execution order, frame identity, ancestry, locations, and anchor hashes. Require observed assignment-before-read and matching scope facts before emitting a mechanism-confirmed report. Verify tracked files remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:3763:body", "pylint-dev/pylint:3763:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:variable-order-checker", "role:runtime-version-policy", "role:assignment-expression-regressions", "role:public-test-runner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3763:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:3763:body", "pylint-dev/pylint:3763:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:0d5d796f6706ce7801b87899"
}
```
