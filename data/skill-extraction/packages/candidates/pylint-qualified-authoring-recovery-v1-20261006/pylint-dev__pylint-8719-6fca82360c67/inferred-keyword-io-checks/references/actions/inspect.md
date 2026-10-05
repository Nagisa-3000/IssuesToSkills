# Inspect argument discovery

Read current semantic owners and run a bound public reproduction without modifying implementation or assertion files. Record current anchors, signatures, inference shapes, diagnostics, and Oracle bindings. Distinguish a missing kwargs lookup from unrelated inference or signature errors.

```arex-contract-v4
{
  "id": "workflow:verified-history:0a9b8ce52750bdf712058d20:inspect",
  "package_id": "workflow:verified-history:0a9b8ce52750bdf712058d20",
  "resource": "references/actions/inspect.md",
  "kind": "probe",
  "intent": "Establish applicability of dictionary-backed keyword fallback.",
  "mechanism": "Compare direct lookup with safely inferred unpacked dictionary arguments.",
  "semantic_role": "argument-discovery-review",
  "owner_role": "python-call-analysis",
  "operation": "Locate current owners, read argument discovery and IO checks, and record a public reproduction without editing source or assertions.",
  "inputs": [],
  "outputs": [
    {"name": "review", "semantic_role": "io-keyword-repair-context", "artifact_kind": "review-record", "language": "python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "reviewed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "io-keyword-owners-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "fallback-applicability-established", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "read_set": ["role:python-call-analysis", "role:io-diagnostic-checker", "role:io-functional-tests"],
  "write_set": [],
  "oracle": [
    {
      "id": "public-reproduction",
      "instruction": "Bind and run a current public lint invocation for a dictionary-supplied encoding example. Record diagnostics, inspect direct lookup and dictionary inference, and confirm implementation and assertion hashes remain unchanged. Record UNKNOWN rather than asserting applicability if inference is unresolved.",
      "kind": "public_mre",
      "command": [],
      "evidence_refs": ["pylint-dev/pylint:8719:body", "pylint-dev/pylint:8719:fix"]
    }
  ],
  "source_ids": ["pylint-dev/pylint:8719:repair:6fca82360c67"],
  "evidence_refs": ["pylint-dev/pylint:8719:body", "pylint-dev/pylint:8719:fix"]
}
```
