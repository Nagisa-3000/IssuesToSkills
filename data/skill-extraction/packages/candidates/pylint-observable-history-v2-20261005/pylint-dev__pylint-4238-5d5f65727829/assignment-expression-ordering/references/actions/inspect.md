# Inspect expression ordering

Locate the current checker, runtime policy, and public fixtures. Inspect statement ancestry, frame relation, AST line/column information, and actual diagnostics. Compare the single-line and multiline reproduction. This operation reads code and runs non-mutating probes; it does not edit tracked files.

```arex-contract-v4
{
  "id": "workflow:verified-history:611e9bc5eaac38ef599b59a7:inspect",
  "intent": "Determine whether the current false diagnostic matches the sourced ordering mechanism.",
  "mechanism": "Compare Python evaluation order with statement-kind and source-coordinate eligibility predicates.",
  "semantic_role": "ordering-diagnosis",
  "owner_role": "assignment-use-checker",
  "operation": "Read the bound checker, runtime policy, and fixtures. Probe earlier-binding and genuine earlier-read examples without modifying tracked files. Record owner anchors, statement kinds, frame relation, runtime version, AST coordinates, and actual diagnostics. Produce mechanism-confirmed analysis only when public evidence supports it.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "ordering-analysis",
      "semantic_role": "assignment-expression-ordering-analysis",
      "artifact_kind": "evidence-record",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:assignment-use-checker",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "Locate the diagnostic decision owner in the current checkout; existence does not prove mechanism applicability."
    }
  ],
  "effects": [
    {"key": "ordering-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-earlier-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-ordering",
      "instruction": "Record current owner bindings, hashed anchors, interpreter/AST version, statement kinds, frame relation, coordinates, and actual single-line/multiline diagnostics. Confirm assignment-before-read evaluation order and inspect genuine earlier-read controls. Verify tracked files are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:4238:body", "pylint-dev/pylint:4238:fix", "pylint-dev/pylint:4238:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4238:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:4238:body", "pylint-dev/pylint:4238:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:611e9bc5eaac38ef599b59a7",
  "read_set": ["role:assignment-use-checker", "role:runtime-version-policy", "role:assignment-expression-regressions"],
  "write_set": [],
  "exclusions": [
    {"key": "read-actually-precedes-binding", "value": true, "evaluator": "evidence"}
  ]
}
```

If evidence is insufficient, retain UNKNOWN rather than producing a confirmed output. If the read actually precedes the binding, reject applicability.
