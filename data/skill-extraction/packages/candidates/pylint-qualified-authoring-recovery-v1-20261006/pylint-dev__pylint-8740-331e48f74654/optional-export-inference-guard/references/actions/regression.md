# Add the minimal regression

Use the bound public fixture convention. Add an explanatory module docstring and `__all__ += []` without a preceding definition. Assert the undefined-variable diagnostic; do not accept a fatal analyzer error or require a zero linter exit merely because no crash is expected.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:regression",
  "intent": "Make uninferable local exports a durable diagnostic regression.",
  "mechanism": "Minimal undefined augmented assignment paired with an explicit undefined-variable expectation.",
  "semantic_role": "uninferable-export-regression",
  "owner_role": "export-regression-suite",
  "operation": "Add or update a public fixture containing undefined __all__ augmented by an empty list and its diagnostic expectation. Follow current discovery conventions and exclude fatal analyzer errors from accepted output.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "matching-inference-failure-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:export-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "undefined-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "successful-export-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "fixture-review",
      "instruction": "Review the public fixture and diagnostic expectation. Confirm that __all__ is not previously initialized, the input contains __all__ += [], undefined-variable for __all__ is expected, and no fatal analyzer error is accepted.",
      "evidence_refs": ["pylint-dev/pylint:8740:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8740:repair:331e48f74654"],
  "evidence_refs": ["pylint-dev/pylint:8740:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8",
  "read_set": ["role:export-regression-suite"],
  "write_set": ["role:export-regression-suite"],
  "invalidates": ["public-validation-observed"]
}
```

Retain [Validate](validate.md) for this edit. The expected effect does not claim that the fixture has been created or executed.
