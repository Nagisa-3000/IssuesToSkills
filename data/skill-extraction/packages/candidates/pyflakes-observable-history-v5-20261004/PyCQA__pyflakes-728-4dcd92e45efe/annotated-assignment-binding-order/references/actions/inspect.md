# Inspect the diagnostic asymmetry and owners

Locate the current annotated-assignment handler and type-annotation regression suite. In a fresh scope, compare ordinary and annotated self-reference diagnostics. Inspect whether target handling introduces the binding before initializer handling.

This is a probe, not permission to edit when the causal relationship remains unknown. The historical report used shell here-strings; bind an equivalent public reproduction for the current environment rather than assuming that shell syntax or executable is available.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:inspect",
  "intent": "Establish current applicability and locate the implementation and regression owners.",
  "mechanism": "Compare ordinary and annotated self-reference diagnostics and inspect target-binding order.",
  "semantic_role": "diagnose-premature-binding",
  "owner_role": "annotated-assignment-handler",
  "operation": "Read the handler and regression suite, reproduce the public asymmetry, and record whether target visitation installs a binding before initializer analysis.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-handler",
      "semantic_role": "annotated-assignment-handler",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "reviewed-premature-binding"
    },
    {
      "name": "reviewed-regression-suite",
      "semantic_role": "annotation-regression-suite",
      "artifact_kind": "test-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "reviewed"
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "premature-target-binding-confirmed",
      "value": true,
      "evaluator": "evidence",
      "description": "Expected successful probe result; absent confirmation means the repair is not authorized."
    },
    {
      "key": "annotation-regression-owner-located",
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
      "id": "diagnostic-asymmetry",
      "instruction": "In a fresh scope compare x = x with x: int = x, then inspect whether target handling introduces the new binding before initializer analysis. Record actual diagnostics and owner bindings.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:body",
        "PyCQA/pyflakes:728:fix"
      ],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": [
    "role:annotated-assignment-handler",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:body",
    "PyCQA/pyflakes:728:fix",
    "PyCQA/pyflakes:728:regression"
  ],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
