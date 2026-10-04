# Inspect scope classification

Resolve the current scope registry and annotation-test owners. Compare ordinary and async name-collision probes and trace argument binding to scope classification. Record registry representation and capability policy.

Use bound public commands with probe source in memory or outside tracked files. Emit confirmed context only if omitted registration is causal; an exception-text match alone is insufficient.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-inspect",
  "intent": "Establish whether omitted asynchronous scope classification causes annotated argument-binding failure.",
  "mechanism": "Compare ordinary and asynchronous probes and inspect scope lookup and registration.",
  "semantic_role": "diagnose-classification-omission",
  "owner_role": "ast-scope-classification",
  "operation": "Locate current scope and test owners, inspect registry representation and runtime policy, and run bound public probes without modifying tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "scope-review", "semantic_role": "scope-omission-context", "artifact_kind": "code-and-probe-record", "language": "python", "scope": "current-scope-classification", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-inspection-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-semantics-appropriate", "value": true, "evaluator": "evidence"},
    {"key": "runtime-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "confirm-scope-omission",
      "instruction": "Record owner anchors, ordinary-function registry value representation, async membership, capability policy, scope lookup and binding path, actual ordinary/async probe outcomes, and before/after tracked-file status. Emit confirmed context only if current evidence connects omitted async classification to the failure; unknown or contrary results block editing.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:title", "PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"],
  "resource": "references/actions/scope-inspect.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
