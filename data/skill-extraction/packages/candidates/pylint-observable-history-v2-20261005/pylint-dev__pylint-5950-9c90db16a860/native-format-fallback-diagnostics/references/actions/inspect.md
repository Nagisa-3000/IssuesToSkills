# Inspect native and delegated ownership

Read current public source and tests without changing source. Trace the format argument through native dispatch, fallback, and diagnostic ownership. Record actual current anchors rather than assuming historical locations. Establish whether Graphviz preflight and permissive unknown-capability behavior are compatible with the current application.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb:inspect",
  "intent": "Establish current native versus delegated format ownership.",
  "mechanism": "Trace CLI help and selection through native serializers and Graphviz checks.",
  "semantic_role": "format-ownership-inspection",
  "owner_role": "output-format-routing",
  "operation": "Read current help, routing, native inventory, Graphviz checks, conversion dispatch and tests; run a safely bound public reproduction if needed. Make no source edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "ownership-map",
      "semantic_role": "format-ownership-map",
      "artifact_kind": "public-code-observations",
      "language": "python",
      "scope": "current-checkout-output-format-routing",
      "phase": "pre-edit",
      "state": "inspected",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-base-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "format-ownership-established", "value": true, "evaluator": "evidence"},
    {"key": "graphviz-fallback-semantics-compatible", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "native-output-independent-of-graphviz", "value": true, "evaluator": "evidence"},
    {"key": "supported-output-writing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inconclusive-capability-fallback-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-import-path-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-routing",
      "instruction": "Record current hashed anchors for native inventory, help, dispatch, Graphviz checks, conversion and tests. Identify the public diagnostic origin, verify native bypass, and review compatibility of capability discovery and warning-and-continue. Confirm inspection did not edit source; incompatible semantics must reject the realization.",
      "evidence_refs": ["pylint-dev/pylint:5950:body", "pylint-dev/pylint:5950:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:output-format-routing", "role:native-format-inventory", "role:graphviz-capability-check", "role:conversion-dispatch", "role:format-regression-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5950:repair:9c90db16a860"],
  "evidence_refs": ["pylint-dev/pylint:5950:body", "pylint-dev/pylint:5950:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:0b2bfb6f55fbde63a9be0bbb"
}
```

Effects and outputs are conditional requirements: inspection cannot establish compatibility merely by assigning matching predicate names. Populate the ownership map from public current observations. Do not invent a bridge for a different backend or language.
