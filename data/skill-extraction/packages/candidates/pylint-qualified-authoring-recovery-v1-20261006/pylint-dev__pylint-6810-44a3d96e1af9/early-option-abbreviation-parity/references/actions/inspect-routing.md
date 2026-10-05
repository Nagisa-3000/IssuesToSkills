# Inspect routing

Locate current owners; read early lookup, downstream policy, competing names, value consumption, and forwarding. Compare public full/abbreviated invocations in an isolated environment. Do not modify tracked source. Report UNKNOWN when policy or boundaries cannot be established.

```arex-contract-v4
{
  "id": "workflow:verified-history:1013e5aeb1e4479ac812713d:inspect-routing",
  "intent": "Determine whether downstream-supported abbreviations bypass an early callback.",
  "mechanism": "Compare early matching with parser acceptance and inspect competing option prefixes.",
  "semantic_role": "routing-policy-analysis",
  "owner_role": "early-option-router",
  "operation": "Read bound owners and run isolated public full-versus-abbreviated probes without changing tracked code; record current bindings and evidence.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "routing-analysis", "semantic_role": "routing-policy-analysis", "artifact_kind": "evidence-report", "language": "python", "scope": "current-cli-option-pipeline", "phase": "pre-edit", "state": "reviewed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "routing-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "canonical-option-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "neighbor-option-routing", "value": "preserved", "evaluator": "evidence"},
    {"key": "argument-consumption-and-forwarding", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-routing-gap",
      "instruction": "Bind current public probes; record full and abbreviated early effects, parser policy, competing names, value handling, and evidence that tracked source was unchanged.",
      "evidence_refs": ["pylint-dev/pylint:6810:body", "pylint-dev/pylint:6810:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6810:repair:44a3d96e1af9"],
  "evidence_refs": ["pylint-dev/pylint:6810:title", "pylint-dev/pylint:6810:body", "pylint-dev/pylint:6810:fix"],
  "resource": "references/actions/inspect-routing.md",
  "package_id": "workflow:verified-history:1013e5aeb1e4479ac812713d",
  "read_set": ["role:early-option-router", "role:main-option-parser", "role:early-option-regressions"],
  "write_set": [],
  "exclusions": [
    {"key": "downstream-abbreviation-policy", "value": "exact-only", "evaluator": "evidence"},
    {"key": "early-main-processing-split", "value": false, "evaluator": "evidence"}
  ]
}
```
