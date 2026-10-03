# Inspect the binding boundary

Locate the current overload-decorator recognizer, scope-binding classes, and public decorator tests. Inspect whether a scope member can be a local assignment and whether `.fullName` or equivalent metadata is import-specific.

Produce a current review with pinned anchors and real owner bindings. Do not infer applicability from the historical issue title. If the branch already checks binding class, the repair is not applicable.

```arex-contract-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625:inspect",
  "intent": "Establish whether the evidenced binding-type failure exists in the current recognizer.",
  "mechanism": "Review scope membership, binding-class ownership, and short-circuit ordering.",
  "semantic_role": "recognition-boundary-inspection",
  "owner_role": "overload-decorator-recognizer",
  "operation": "Locate current owners and inspect bare-name decorator resolution.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "binding-boundary-review",
      "semantic_role": "recognition-boundary-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "overload-decorator-recognizer",
      "phase": "pre-edit",
      "state": "unsafe-import-metadata-access-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-recognition-boundary", "value": "reviewed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-binding-boundary",
      "instruction": "Review current public anchors and binding classes. Confirm that bare decorator names may resolve to non-import bindings and that metadata is accessed without the corresponding type guard. If not confirmed, record UNKNOWN or not applicable rather than producing a confirmed output.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"],
  "read_set": ["role:overload-decorator-recognizer", "role:scope-binding-model", "role:decorator-recognition-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:314f3449f8ccd1beab92c625"
}
```

The output is conditional on confirming the defect; it is not an observation that this package has already made about a current checkout.
