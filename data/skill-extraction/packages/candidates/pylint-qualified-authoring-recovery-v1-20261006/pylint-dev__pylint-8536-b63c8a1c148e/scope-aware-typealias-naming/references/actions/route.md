# Route explicit local aliases

Change the current function-local classification owner, not naming regexes or the alias recognizer. Retain surrounding eligibility guards. Inspect annotations only on annotated assignments; recognized explicit aliases use the existing alias naming category, and other assignments use ordinary-variable naming.

```arex-contract-v4
{
  "id": "workflow:verified-history:b980c9ec644c821d41e50e10:route",
  "intent": "Correct the naming category for explicit local aliases.",
  "mechanism": "Guard annotation recognition by annotated-assignment node kind and dispatch recognized aliases to existing alias naming.",
  "semantic_role": "repair-classification",
  "owner_role": "local-name-classifier",
  "operation": "Edit eligible function-local assignment dispatch to select alias naming for recognized explicit annotated aliases and retain the ordinary-variable fallback.",
  "kind": "edit",
  "inputs": [
    {
      "name": "classification-findings",
      "semantic_role": "local-alias-classification-findings",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "function-local-naming",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "local-classification-defect-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "compatible-alias-recognizer-located", "value": true, "evaluator": "evidence"},
    {"key": "role:local-name-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:typealias-recognizer", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "explicit-local-alias-routing", "value": "typealias", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-variable-routing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "scope-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-alias-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-category-dispatch",
      "instruction": "Inspect the diff for annotated-assignment guarding, existing recognizer reuse, alias-category dispatch, ordinary-variable fallback, and unchanged eligibility guards. This review does not replace final public diagnostic validation.",
      "evidence_refs": ["pylint-dev/pylint:8536:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8536:repair:b63c8a1c148e"],
  "evidence_refs": ["pylint-dev/pylint:8536:fix"],
  "read_set": ["role:local-name-classifier", "role:typealias-recognizer"],
  "write_set": ["role:local-name-classifier"],
  "resource": "references/actions/route.md",
  "package_id": "workflow:verified-history:b980c9ec644c821d41e50e10"
}
```

Expected effects require current observation. Retain the [validate Action](validate.md) after this edit.
