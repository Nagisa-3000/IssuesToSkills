# Inspect signature opacity

Locate current diagnostic and regression owners. Reproduce the public constructor warning, inspect the inferred inherited argument list, and record override argument names. Distinguish unavailable metadata from a known empty list.

This read/probe operation does not modify tracked source. Temporary probes belong outside tracked code. Record current bindings and hashed anchors, rather than treating historical paths as current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:79391484ce4048a1c8e1217a:inspect",
  "intent": "Determine whether the current false positive matches the supported opaque-signature mechanism.",
  "mechanism": "Observe the public diagnostic and compare inherited argument availability with override argument names.",
  "semantic_role": "signature-opacity-inspection",
  "owner_role": "delegation-diagnostic-owner",
  "operation": "Locate current owners, inspect argument representations, and run a bound public reproduction without tracked edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "signature-analysis",
      "semantic_role": "opaque-parent-delegation-analysis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "delegation-diagnostic",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-issue-and-pinned-base-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "opaque-parent-nonself-override-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "target-false-positive-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inspectable-signature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "self-only-guard-boundary-preserved", "value": true, "evaluator": "evidence"},
    {"key": "fixture-interface-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-opacity",
      "instruction": "Observe the public default-message constructor warning, unavailable inherited arguments, and override argument names different from self alone. Record located owners and hashed anchors; confirm no tracked edits.",
      "evidence_refs": ["pylint-dev/pylint:7319:body", "pylint-dev/pylint:7319:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:7319:repair:7fdf8d9ee090"],
  "evidence_refs": ["pylint-dev/pylint:7319:body", "pylint-dev/pylint:7319:fix"],
  "read_set": ["role:delegation-diagnostic-owner", "role:delegation-regression-owner"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:79391484ce4048a1c8e1217a"
}
```

Emit an applicability-established output only after confirming the mechanism. Inspectable signatures, self-only arguments, or unresolved metadata semantics do not authorize the repair.
