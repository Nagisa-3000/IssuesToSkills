# Inspect signature collection

Locate the current function-signature collector and annotation tests. Inspect whether its AST argument enumeration includes positional-only arguments. Reproduce the reported diagnostic using a public analyzer command bound to the current checkout.

The supplied report establishes the historical symptom; the patch establishes the omitted AST category. Neither establishes the state of a new checkout. Produce a hashed, evidence-backed assessment with concrete owner bindings. Reject this mechanism when positional-only annotations already enter the annotation pipeline.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:inspect",
  "intent": "Establish whether the current unused-import false positive is caused by omitted positional-only annotation collection.",
  "mechanism": "Compare positional-only AST fields with the categories enumerated by the current signature collector and observe the public reproduction.",
  "semantic_role": "diagnose-positional-only-omission",
  "owner_role": "function-signature-collector",
  "operation": "Inspect current collector, runtime gate, tests, and public diagnostic; record concrete bindings and applicability.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "assessment",
      "semantic_role": "positional-only-omission-assessment",
      "artifact_kind": "inspection-record",
      "language": "Python",
      "scope": "current-checkout-function-signature-analysis",
      "phase": "diagnosis",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "applicability-assessed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-unmodified",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Inspect the bound signature collector and run the public mixed-parameter reproduction on a compatible runtime. Record whether the positional-only annotation is omitted and whether its import receives an unused-import diagnostic. Treat a different mechanism as inapplicable.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:body",
        "PyCQA/pyflakes:507:fix"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:507:repair:be8803601900"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:507:title",
    "PyCQA/pyflakes:507:body",
    "PyCQA/pyflakes:507:fix"
  ],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": [
    "role:function-signature-collector",
    "role:python-runtime-compatibility-gate",
    "role:annotation-regression-tests",
    "role:public-analyzer-entry-point"
  ],
  "write_set": []
}
```
