# Inspect the inferred-value diagnostic boundary

Read current owners, inference/rejection branches, exemptions, diagnostic definition, and regression harness. Hash relevant anchors and record real bindings. This probe makes no edits.

Produce a PASS applicability finding only when current evidence establishes the narrow diagnostic-enrichment mechanism. An unresolved crash or unavailable inferred value is not authorization to change traversal.

```arex-contract-v4
{
  "id": "workflow:verified-history:124787fcb0844f5e9acb613d:inspect",
  "intent": "Establish current applicability and bindings.",
  "mechanism": "Review the existing inference-to-diagnostic boundary and corresponding assertions.",
  "semantic_role": "diagnostic-boundary-inspection",
  "owner_role": "special-class-assignment-checker",
  "operation": "Read current public anchors, locate semantic owners, inspect rejection and exemption branches, and record tri-state applicability without modifying files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "bound-diagnostic-context",
      "semantic_role": "inferred-kind-diagnostic-context",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "special-class-assignment",
      "phase": "pre-edit",
      "state": "bound-and-reviewed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "diagnostic-context-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "acceptance-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-metadata-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-boundary",
      "instruction": "Verify current owner bindings and hashed anchors. Record PASS, FAIL, or UNKNOWN for an existing inferred-value rejection boundary, valid-class and uninferable exemptions, and a public regression harness. Confirm that inspection made no edits; do not claim unsupported applicability.",
      "evidence_refs": ["pylint-dev/pylint:7467:body", "pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:special-class-assignment-checker",
    "role:special-class-assignment-diagnostic",
    "role:special-class-assignment-regression-suite"
  ],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7467:repair:b47aa3076ee0"],
  "evidence_refs": ["pylint-dev/pylint:7467:body", "pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:124787fcb0844f5e9acb613d"
}
```
