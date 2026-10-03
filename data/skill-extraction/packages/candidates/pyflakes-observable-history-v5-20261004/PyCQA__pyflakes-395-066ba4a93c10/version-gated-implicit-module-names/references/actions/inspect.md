# Inspect the current owners

Locate the implicit module-name model, interpreter-version policy, scope lookup, and undefined-name regression harness. Read their actual semantics, bind hashed anchors, and reproduce the public issue. A configured target version that differs from runtime policy is a compatibility question, not permission to copy the historical gate.

This probe produces a confirmed context only when current evidence supports it. Otherwise record UNKNOWN or FAIL and do not authorize editing. It must not change checkout content.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:inspect",
  "intent": "Determine whether the evidenced registry-and-runtime-version repair applies.",
  "mechanism": "Inspect semantic owners and probe the public module-level reproduction.",
  "semantic_role": "applicability-inspection",
  "owner_role": "implicit-module-name-model",
  "operation": "inspect-current-owners",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "owner-context",
      "semantic_role": "implicit-name-repair-context",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "module-name-checking",
      "phase": "pre-edit",
      "state": "owners-and-semantics-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "repair-owners", "value": "located", "evaluator": "evidence"},
    {"key": "registry-version-semantics", "value": "confirmed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-owner-and-reproduction",
      "instruction": "Bind current owners and public argv commands, inspect registry and scope behavior, and record the public reproduction outcome and interpreter version. Confirm runtime-version compatibility or report FAIL/UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:title", "PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8",
  "read_set": ["role:implicit-module-name-model", "role:interpreter-version-policy", "role:scope-name-lookup", "role:undefined-name-regressions"],
  "write_set": []
}
```
