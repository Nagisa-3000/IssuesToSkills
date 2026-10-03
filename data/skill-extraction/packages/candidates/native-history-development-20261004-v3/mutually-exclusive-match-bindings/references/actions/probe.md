# Locate and reproduce

Inspect the current redefinition logic and its shared alternative classifier.
Locate the public match regression suite separately. Run the reported
distinct-case reproduction and an equivalent `if`/`else` control using current
public bindings. Record diagnostics and hashed owner anchors.

Only emit confirmed context when inspection and reproduction agree that the
match omission explains the failure. Otherwise record UNKNOWN or FAIL and stop
editing under this workflow. Do not modify checkout source.

```arex-contract-v4
{
  "id": "mutually-exclusive-match-bindings:probe",
  "intent": "Establish current applicability of the historical mechanism.",
  "mechanism": "Compare public branch reproductions and inspect shared alternative classification.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "python-branch-alternative-classifier",
  "operation": "Locate implementation and test owners and confirm the match alternative omission.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "located-context", "semantic_role": "confirmed-match-alternative-omission", "artifact_kind": "binding-and-probe-record", "language": "python", "scope": "current-analyzer", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Run current public match and if/else reproductions; record exact diagnostics, locate owners, and inspect whether omission of separate match case bodies causes the reported redefinition.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:771"],
  "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
  "read_set": ["role:python-branch-alternative-classifier", "role:python-match-regression-suite"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "mutually-exclusive-match-bindings"
}
```

The confirmed output is conditional and expected, not an already observed fact.
