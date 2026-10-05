# Probe the source-coordinate owner

Read the current emitter and public fixtures without modifying them. Compare token start coordinates, reported columns, and the desired anchor. The historical report's symptom is not sufficient by itself: explicitly establish that the current token starts at the hash and that the diagnostic accepts zero-based source columns.

If the current requirement is to locate TODO itself, reject this realization rather than changing the anchor.

```arex-contract-v4
{
  "id": "workflow:verified-history:e90ff4df6c32dee9a7842f73:probe",
  "intent": "Establish current applicability of the comment-token source-anchor repair.",
  "mechanism": "Compare token-relative note indexing with source token positions and the public diagnostic column contract.",
  "semantic_role": "coordinate-applicability-probe",
  "owner_role": "comment-note-emitter",
  "operation": "Read the current Python comment-note emitter and its public regression owner; bind their symbols and hashed anchors. Inspect or publicly reproduce comments at differing source positions. Record the token start, coordinate units, current expression, required anchor, and preservation baseline. Make no source or expectation edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "coordinate-review",
      "semantic_role": "comment-column-repair-context",
      "artifact_kind": "public-review-record",
      "language": "Python",
      "scope": "current-checkout-comment-note-diagnostics",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:comment-note-emitter", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:comment-note-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "source-anchor-applicability-established", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "note-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-content-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-coordinate-semantics",
      "instruction": "Review current bound owners and public reproduction. Establish that token start is the hash position, column units match the diagnostic API, the present error is token-relative indexing, and the required anchor is immediately after the hash. Record evidence and confirm the probe made no edits.",
      "evidence_refs": ["pylint-dev/pylint:4218:body", "pylint-dev/pylint:4218:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4218:repair:ea1fcd6a9440"],
  "evidence_refs": ["pylint-dev/pylint:4218:body", "pylint-dev/pylint:4218:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:e90ff4df6c32dee9a7842f73",
  "read_set": ["role:comment-note-emitter", "role:comment-note-regression-suite"],
  "write_set": [],
  "exclusions": [
    {"key": "required-anchor", "value": "matched-note-start", "evaluator": "evidence"},
    {"key": "column-units-compatible", "value": false, "evaluator": "evidence"}
  ]
}
```
