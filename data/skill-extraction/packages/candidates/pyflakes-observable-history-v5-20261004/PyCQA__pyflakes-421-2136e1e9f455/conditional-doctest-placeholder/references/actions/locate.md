# Locate owners and establish the collision

Inspect current public code and bind the doctest initializer, collision handler, and doctest test owner. Confirm that the module scope is the scope queried by the historical guard's semantic equivalent. Review the synthetic binding's missing source and the collision path's source assumption.

Adapt the reported reproduction to the current public environment. Record observations rather than assuming the old traceback still applies. If behavior is already repaired, record that fact instead of manufacturing a failure.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:locate",
  "intent": "Establish applicability and current owner bindings.",
  "mechanism": "Review scope setup and binding collision behavior and probe the public reproduction.",
  "semantic_role": "collision-applicability-probe",
  "owner_role": "doctest-initializer",
  "operation": "Locate semantic owners and observe the current synthetic-underscore collision mechanism.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "initializer", "semantic_role": "doctest-initializer-code", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "baseline-reviewed", "optional": false},
    {"name": "tests", "semantic_role": "doctest-regression-tests", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "baseline-reviewed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings", "value": "recorded", "evaluator": "evidence"},
    {"key": "collision-applicability", "value": "observed", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "current-checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "establish-collision",
      "instruction": "Inspect current public scope setup and binding replacement code; adapt the reported doctest reproduction and record whether the source-less underscore insertion encounters an existing module underscore. Record current owner anchors and any failure.",
      "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:doctest-initializer", "role:binding-collision-handler", "role:doctest-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:title", "PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:regression"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

Outputs are expected artifacts of the current probe, not supplied execution results. An empty command requires a current binding before execution.
