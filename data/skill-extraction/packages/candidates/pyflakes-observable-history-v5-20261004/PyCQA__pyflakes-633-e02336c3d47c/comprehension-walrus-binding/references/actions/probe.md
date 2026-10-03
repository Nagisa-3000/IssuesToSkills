# Inspect assignment-expression scope ownership

Locate current semantic owners rather than searching only for historical class names. Trace a stored assignment-expression target through classification and insertion. Determine whether the current scope stack has consecutive comprehension scopes and identify the containing boundary.

Use the single-generator and nested-comprehension examples from the public regression evidence as probes. Record diagnostic results independently of code-review findings. An absent runtime assignment due to lazy evaluation is not this lexical-binding defect.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd9457af9cbbabf21f89fac4:probe",
  "intent": "Confirm applicability and bind current classification, insertion, scope-model, and test owners.",
  "mechanism": "Trace assignment-expression target classification and its insertion destination across comprehension scopes.",
  "semantic_role": "scope-routing-diagnosis",
  "owner_role": "binding-inserter",
  "operation": "Inspect current public AST handling and scope storage; run adapted public diagnostic probes.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosed-scope-model",
      "semantic_role": "assignment-expression-scope-repair-context",
      "artifact_kind": "code-and-observations",
      "language": "python",
      "scope": "current-analyzer-checkout",
      "phase": "diagnosis",
      "state": "owners-bound-and-defect-confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "scope-routing-applicability", "value": "determined", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-scope-routing",
      "instruction": "Record current owner anchors, trace the public generator and nested-comprehension targets, and determine whether their bindings incorrectly remain in comprehension scopes.",
      "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:binding-classifier", "role:binding-inserter", "role:comprehension-scope-model", "role:scope-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:633:repair:e02336c3d47c"],
  "evidence_refs": ["PyCQA/pyflakes:633:body", "PyCQA/pyflakes:633:fix", "PyCQA/pyflakes:633:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:fd9457af9cbbabf21f89fac4"
}
```

Emit the successful output state only when current observations support it. If the defect is absent or ownership is unknown, report that result rather than manufacturing a compatible PortValue.
