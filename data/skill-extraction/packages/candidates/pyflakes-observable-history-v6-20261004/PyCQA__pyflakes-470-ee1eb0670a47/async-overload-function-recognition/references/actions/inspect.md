# Inspect recognition and compatibility

Compare public sync and async overload sequences. Read the recognition gate, decorator resolution, supported AST types, runtime guards, and existing public coverage. Record actual owner bindings and hashed anchors.

This probe makes no checkout edits. Emit a confirmed review only when current evidence establishes the omission. Missing information remains UNKNOWN; a different root cause rejects the modifying workflow.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:inspect",
  "intent": "Determine whether an omitted async function AST node causes the overload false positive.",
  "mechanism": "Compare public sync/async behavior and inspect the recognition gate and runtime support.",
  "semantic_role": "diagnose-function-node-omission",
  "owner_role": "overload-recognition",
  "operation": "Read current owners and run a bound public reproduction without editing checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "recognition-review",
      "semantic_role": "overload-node-omission-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout-overload-recognition",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "recognition-owners-located", "value": true, "evaluator": "evidence"},
    {"key": "async-function-node-omission-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Bind and run a current public sync/async typing overload reproduction. Confirm correct decorator resolution, sync acceptance, async failure, and a synchronous-only source-node gate. Record owner anchors, supported AST classes, runtime policy, and coverage. Confirm that the probe made no checkout edits. Emit a confirmed review only if the omission is established.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c"
}
```
