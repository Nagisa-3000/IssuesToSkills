# Probe and bind the scope mechanism

Compare a generator decorator on functions with matching and nonmatching parameter names. Trace the bound generator variable through consumed-name lookup and scope classification. Read and run public probes without editing tracked source or fixtures.

Proceed only if the current consumed-name guard and decorator classifier explain the observed collision. A historical path or symbol spelling is not a current semantic binding.

```arex-contract-v4
{
  "id": "workflow:verified-history:2d9cfc7283460de886b0b9d6:probe",
  "intent": "Establish the current decorator-local binding collision and bind its semantic owners.",
  "mechanism": "Compare parameter-name controls and inspect consumed-name, comprehension and decorator-context classification.",
  "semantic_role": "scope-mechanism-probe",
  "owner_role": "name-resolution-checker",
  "operation": "Read current owners and run public collision controls without changing tracked files; record pinned anchors, observed diagnostics and current scope semantics.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "scope-binding", "semantic_role": "decorator-scope-binding", "artifact_kind": "binding-record", "language": "python", "scope": "current-checkout", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-reproduction-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "scope-mechanism-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-undefined-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nondecorator-homonym-protection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-check-path-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "scope-collision-controls",
      "instruction": "Run current public matching/nonmatching parameter controls. Observe whether only the matching case incorrectly reports the generator-bound x. Inspect the consumed binding and verify decorator classification of the actual consumer node. Record hashed current anchors and verify no tracked files changed. If the mechanism is different or unknown, do not authorize repair.",
      "evidence_refs": ["pylint-dev/pylint:3791:body", "pylint-dev/pylint:3791:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3791:repair:a054796d7008"],
  "evidence_refs": ["pylint-dev/pylint:3791:title", "pylint-dev/pylint:3791:body", "pylint-dev/pylint:3791:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:2d9cfc7283460de886b0b9d6",
  "read_set": ["role:name-resolution-checker", "role:decorator-context-classifier", "role:scope-regression-suite"],
  "write_set": []
}
```
