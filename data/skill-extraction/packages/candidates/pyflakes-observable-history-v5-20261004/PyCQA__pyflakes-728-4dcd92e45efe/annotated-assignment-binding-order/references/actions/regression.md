# Add the undefined-self-reference regression

Add a public test in the located annotation regression owner using a fresh scope and `x: int = x`. Assert the analyzer's undefined-name diagnostic, not merely that checking finishes.

The historical assertion used `m.UndefinedName`. That symbol belongs to the historical implementation; bind the equivalent public diagnostic in the current test harness.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:regression",
  "intent": "Make suppression of the undefined annotated initializer name observable as a regression.",
  "mechanism": "Assert the undefined-name diagnostic for an unbound annotated self-reference.",
  "semantic_role": "lock-in-self-reference-diagnostic",
  "owner_role": "annotation-regression-suite",
  "operation": "Add a focused public regression assertion for x: int = x with no prior x binding.",
  "kind": "edit",
  "inputs": [
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
  "outputs": [
    {
      "name": "extended-regression-suite",
      "semantic_role": "annotation-regression-suite",
      "artifact_kind": "test-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "self-reference-assertion-added"
    }
  ],
  "preconditions": [
    {
      "key": "role:annotation-regression-suite",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "annotation-regression-owner-located",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "undefined-self-reference-regression-present",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "existing-annotation-assertions-retained",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "regression-assertion-review",
      "instruction": "Inspect that the new public test uses x: int = x in an isolated scope and asserts the undefined-name diagnostic through the current harness. Execute it in the linked validate Action.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:regression"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotation-regression-suite"
  ],
  "write_set": [
    "role:annotation-regression-suite"
  ],
  "invalidates": [
    "target-and-adjacent-checks-pass"
  ],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:body",
    "PyCQA/pyflakes:728:regression"
  ],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
