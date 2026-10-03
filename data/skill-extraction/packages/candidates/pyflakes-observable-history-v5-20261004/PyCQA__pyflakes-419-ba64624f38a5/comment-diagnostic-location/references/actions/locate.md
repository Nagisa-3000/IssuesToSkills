# Locate the diagnostic-position source

Bind the current type-comment diagnostic pipeline and annotation-test owner. Compare the actual comment location with the diagnostic location, then trace collection, deferred parsing, and message construction.

Record the public reproduction, current owner bindings, and hashed code anchors. A mismatch caused by another mechanism rejects the repair, rather than authorizing carrier substitution.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:locate",
  "intent": "Determine whether a statement's coordinates incorrectly position an invalid type-comment diagnostic.",
  "mechanism": "Compare source and reported positions and inspect the diagnostic carrier.",
  "semantic_role": "diagnostic-position-discovery",
  "owner_role": "type-comment-diagnostic-pipeline",
  "operation": "Read bound current owners and reproduce the public mismatch.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "located-context",
      "semantic_role": "type-comment-position-context",
      "artifact_kind": "code-and-probe-evidence",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "current",
      "state": "located",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "position-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-position-source",
      "instruction": "Use the current public reproduction and code review to determine whether the associated statement supplies the diagnostic position despite independently available comment coordinates. Record PASS, FAIL, or UNKNOWN with current anchors.",
      "evidence_refs": ["PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:type-comment-diagnostic-pipeline", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:title", "PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```

The output is a reviewed context, not assumed proof of applicability. UNKNOWN mechanism checks permit further probing only.
