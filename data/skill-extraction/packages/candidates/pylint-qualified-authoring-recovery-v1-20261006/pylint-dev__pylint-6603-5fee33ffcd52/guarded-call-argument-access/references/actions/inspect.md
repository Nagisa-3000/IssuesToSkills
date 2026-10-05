# Inspect call eligibility

Locate the current checker and regression harness by semantic ownership. Read the public traceback, AST structure, and eligibility condition. Determine whether empty positional arguments can reach `args[0]` and whether returning early is appropriate for this specialized analysis. Record public anchors and owner bindings without editing files.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd4221a31ba02747212c0c88:inspect",
  "intent": "Establish the unsafe argument-access mechanism and current owner bindings.",
  "mechanism": "Review the empty-call reproduction and the ordered short-circuit eligibility tests.",
  "semantic_role": "diagnose-call-eligibility",
  "owner_role": "call-eligibility-checker",
  "operation": "Read public code and reproduction; record bindings and mechanism findings without modifying the checkout.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "eligibility-review", "semantic_role": "empty-call-owner-bindings", "artifact_kind": "review-record", "language": "python", "scope": "current-checker", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "empty-call-guard-applicable", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "valid-call-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-call-validity-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-unsafe-access",
      "instruction": "Review the current public AST checker and reproduction. Confirm an empty positional list can reach first-element access and that the specialized check should skip this shape. Record owner anchors; if uncertain, return UNKNOWN. Confirm the inspection made no file edits.",
      "evidence_refs": ["pylint-dev/pylint:6603:body", "pylint-dev/pylint:6603:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:call-eligibility-checker", "role:checker-regression-fixture"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6603:repair:5fee33ffcd52"],
  "evidence_refs": ["pylint-dev/pylint:6603:body", "pylint-dev/pylint:6603:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:fd4221a31ba02747212c0c88"
}
```

A confirmed output is expected only after the public review succeeds. An unresolved review is not a compatible input for an editing Action.
