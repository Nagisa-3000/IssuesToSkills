# Inspect the inferred slot-name consumer

Locate the current semantic owners rather than assuming historical paths. Read the inferred branch and the public regression harness without modifying the checkout. Confirm that a node such as the inferred builtin `str` reaches an unguarded `.value` access. Identify existing direct-string, inferred-string, duplicate, and nonduplicate slot cases.

Unknown facts require additional public inspection. A different failure mechanism stops this workflow.

```arex-contract-v4
{
  "id": "workflow:verified-history:d6e93404a2d76602b0907d8c:inspect",
  "intent": "Establish that the current failure matches unsafe inferred slot-name extraction.",
  "mechanism": "Trace the public reproduction into the inferred-name consumer and inspect adjacent comparison tests.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "slot-name-collector",
  "operation": "Read current code and public tests; record owner bindings and the unsafe inferred-value assumption without changing files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspected-slot-repair-scope",
      "semantic_role": "slot-repair-scope",
      "artifact_kind": "checkout-and-observations",
      "language": "python",
      "scope": "slot-name-collector-and-regression-suite",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "slot-collector-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "regression-owner-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "valid-inherited-slot-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-slot-validation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-inferred-value-assumption",
      "instruction": "Inspect the bound collector and public traceback. Confirm inference can return a node without a string value and that the failing consumer assumes otherwise. Verify the inspection changed no source or test files.",
      "evidence_refs": ["pylint-dev/pylint:6100:body", "pylint-dev/pylint:6100:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:slot-name-collector", "role:slot-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6100:repair:ca3bc0e3fadb"],
  "evidence_refs": ["pylint-dev/pylint:6100:body", "pylint-dev/pylint:6100:fix", "pylint-dev/pylint:6100:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:d6e93404a2d76602b0907d8c"
}
```
