# Inspect the current diagnostic mechanism

Read current public code without modifying it. Locate the resource-warning gate, AST parent semantics, safe-inference utility, and diagnostic-test owner. Observe the public reproduction and inspect the inferred identity of the immediate parent callable.

A method spelling or lexical `ExitStack` nesting is insufficient. Record UNKNOWN if identity cannot be inferred or observed. Expected effects below require actual evidence; the contract itself is not an execution record.

```arex-contract-v4
{
  "id": "workflow:verified-history:556cefd05a1df4981665346d:inspect",
  "intent": "Determine whether the current false positive matches direct inferred cleanup registration.",
  "mechanism": "Inspect the diagnostic gate and immediate parent-call inference without changing source.",
  "semantic_role": "bind-cleanup-diagnostic",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Locate current Python diagnostic, AST, inference, and public test owners; record hashed anchors, observed warning, parent-call identity, and adjacent controls without editing files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "binding",
      "semantic_role": "cleanup-diagnostic-binding",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "direct-registration-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:resource-diagnostic-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:resource-diagnostic-test-owner", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-current-mechanism",
      "instruction": "Record public current anchors and inference observations. Confirm the warning originates at the resource call, the immediate parent is the recognized registration call, its inferred identity is supported, and the exemption is missing. Locate adjacent controls and verify inspection changes no tracked source or test files.",
      "evidence_refs": ["pylint-dev/pylint:4654:body", "pylint-dev/pylint:4654:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4654:repair:c2d03c6b3881"],
  "evidence_refs": ["pylint-dev/pylint:4654:body", "pylint-dev/pylint:4654:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:556cefd05a1df4981665346d",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"]
}
```
