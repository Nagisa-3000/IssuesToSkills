# Probe the source/filter boundary

Locate current owners and trace an isolated public fixture. Compare valid original source with actual secondary-parser input. Establish preprocessing order, structural exclusion options, callback diagnostic identity and coordinates, callback-free callers, and public test ownership.

Do not edit tracked code or tests. If applicability is absent or unknown, record that outcome rather than emitting a confirmed output port.

```arex-contract-v4
{
  "id": "workflow:verified-history:da14748ad2e8a043ad8319eb:probe",
  "intent": "Establish current applicability and semantic bindings.",
  "mechanism": "Trace complete source, diagnostic filtering, and secondary AST-dependent analysis.",
  "semantic_role": "applicability-probe",
  "owner_role": "duplicate-preprocessing",
  "operation": "Read current implementation and observe an isolated public reproduction without changing tracked files; record source loss, callback semantics, standalone callers, and test ownership.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "confirmed-boundary", "semantic_role": "preprocessing-binding", "artifact_kind": "code-review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "role:duplicate-preprocessing", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:duplicate-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "pre-parse-suppression-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "callback-coordinate-contract-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "suppression-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-coordinate-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enabled-comparison-and-exclusion-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "callback-free-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-boundary",
      "instruction": "Record valid original source, secondary-parser input, filtering order, callback diagnostic identity and original one-based coordinate semantics, callback-free callers, and public test binding. Confirm no tracked file changes. Emit confirmed applicability only when prerequisites are observed.",
      "evidence_refs": ["pylint-dev/pylint:6301:body", "pylint-dev/pylint:6301:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:duplicate-preprocessing", "role:duplicate-regression-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6301:repair:1664202ba5de"],
  "evidence_refs": ["pylint-dev/pylint:6301:body", "pylint-dev/pylint:6301:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:da14748ad2e8a043ad8319eb"
}
```

Effects describe the successful applicable branch, not guaranteed observations. Semantic claims require public evidence, not merely matching predicate names.
