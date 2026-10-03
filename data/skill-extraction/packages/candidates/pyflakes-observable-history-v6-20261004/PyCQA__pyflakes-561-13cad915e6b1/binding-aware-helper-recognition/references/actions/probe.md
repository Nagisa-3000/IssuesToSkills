# Probe the receiver detector and lexical binding model

Locate the current helper-recognition owner, import-binding representation, scope lookup order, and annotation regression owner. Review the public reproduction and determine whether this mechanism applies. Read-only inspection does not modify the checkout.

Do not infer applicability from the word `Literal` alone. The supplied repair concerns a simple-name module receiver. Check whether the current direct-import helper branch already resolves aliases independently.

```arex-contract-v4
{
  "id": "workflow:verified-history:2f5b3f202404ca13ec4e8055:probe",
  "intent": "Establish current semantic bindings and applicability.",
  "mechanism": "Inspect helper dispatch and nearest-scope import provenance.",
  "semantic_role": "receiver-recognition-discovery",
  "owner_role": "typing-helper-detector",
  "operation": "Read current detector, import bindings, scope stack, and regression suite; record hashed owner anchors and whether module spelling causes the public alias failure. Do not edit files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-owners",
      "semantic_role": "typing-helper-repair-context",
      "artifact_kind": "owner-map",
      "language": "python",
      "scope": "typing-helper-recognition",
      "phase": "current",
      "state": "reviewed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "receiver-owner-review",
      "value": "recorded",
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "adjacent-helper-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-current-bindings",
      "instruction": "Record current owner anchors, nearest-scope lookup behavior, import provenance fields, and public evidence for or against the module-alias mechanism. Confirm inspection made no edits.",
      "evidence_refs": ["PyCQA/pyflakes:561:body", "PyCQA/pyflakes:561:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:typing-helper-detector",
    "role:lexical-import-binding-model",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs": ["PyCQA/pyflakes:561:body", "PyCQA/pyflakes:561:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:2f5b3f202404ca13ec4e8055"
}
```

An output is an expected review artifact, not an observed result. If bindings or semantics remain UNKNOWN, continue public inspection or stop; do not authorize the repair.
