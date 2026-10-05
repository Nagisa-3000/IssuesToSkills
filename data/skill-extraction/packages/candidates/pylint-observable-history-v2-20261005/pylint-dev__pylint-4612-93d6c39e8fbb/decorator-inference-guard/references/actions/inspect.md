# Inspect the inference boundary

Locate the current decorator-name matcher and public analyzer-regression owner. Read the inference loop, invalid-result representation, sentinel semantics, both matching branches, and exception handling. Trace the public failure or bind a public reproduction.

Record owner bindings, pinned base, hashed anchors and observed facts without modifying tracked source. A fixture decorator alone does not establish applicability. If the mechanism remains UNKNOWN, retain observations but do not emit a confirmed-boundary PortValue.

```arex-contract-v4
{
  "id": "workflow:verified-history:7551c627c4b85df38e889528:inspect",
  "intent": "Establish applicability and current owner bindings.",
  "mechanism": "Inspect the inference-to-name boundary for invalid results reaching attribute access.",
  "semantic_role": "mechanism-probe",
  "owner_role": "decorator-name-matcher",
  "operation": "Read current owners and observe the public failure boundary without editing tracked source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "confirmed-boundary", "semantic_role": "decorator-inference-boundary", "artifact_kind": "evidence-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "inference-boundary-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "resolvable-decorator-matching-preserved", "value": true, "evaluator": "evidence"},
    {"key": "inference-error-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-boundary",
      "instruction": "Record current role bindings, pinned base, hashed anchors, invalid-result semantics and public evidence that unguarded decorator name access is the relevant boundary. Confirm tracked source is unchanged. Emit confirmed output only after establishing the mechanism.",
      "evidence_refs": ["pylint-dev/pylint:4612:body", "pylint-dev/pylint:4612:fix", "pylint-dev/pylint:4612:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4612:repair:93d6c39e8fbb"],
  "evidence_refs": ["pylint-dev/pylint:4612:body", "pylint-dev/pylint:4612:fix", "pylint-dev/pylint:4612:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:7551c627c4b85df38e889528",
  "read_set": ["role:decorator-name-matcher", "role:analyzer-regression-suite"],
  "write_set": []
}
```

The effects describe successful inspection, not observed execution. Bind the Oracle to current public instructions and argv commands before use.
