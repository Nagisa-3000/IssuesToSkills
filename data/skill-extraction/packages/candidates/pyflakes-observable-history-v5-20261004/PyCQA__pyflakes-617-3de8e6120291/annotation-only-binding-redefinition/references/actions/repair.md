# Repair the annotation-only decision and add regression coverage

Only proceed when current inspection establishes a distinct annotation-only binding abstraction and the reported failure mechanism.

Make that abstraction explicitly decline to redefine another binding. In the historical realization, this was an override returning `False`. Keep the change confined to annotation-only semantics; do not disable redefinition warnings globally or change ordinary value assignments.

Add a no-diagnostics regression equivalent to importing both a value and its annotation name, annotating the value without assignment, and then using the value. Retain syntax-version guards if the current supported interpreter range requires them.

The patch and test are expected effects, not proof of repair. Validation is mandatory.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:repair",
  "intent": "Exclude annotation-only bindings from redefining prior names.",
  "mechanism": "Override the annotation-only redefinition predicate to return false and add an imported-name annotation regression.",
  "semantic_role": "annotation-only-semantics-repair",
  "owner_role": "annotation-binding-analysis",
  "operation": "Modify the annotation-only decision and its regression test.",
  "kind": "edit",
  "inputs": [
    {
      "name": "inspected-checkout",
      "semantic_role": "annotation-redefinition-checkout",
      "artifact_kind": "checkout-snapshot",
      "language": "python",
      "scope": "annotation-binding-and-regression",
      "phase": "pre-repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "patched-checkout",
      "semantic_role": "annotation-redefinition-checkout",
      "artifact_kind": "checkout-snapshot",
      "language": "python",
      "scope": "annotation-binding-and-regression",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:annotation-binding-analysis",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "role:annotation-regression-tests",
      "value": true,
      "evaluator": "file_exists"
    },
    {
      "key": "annotation-only-redefinition-mechanism-confirmed",
      "value": true,
      "evaluator": "evidence",
      "description": "Current review and public probes establish a distinct annotation-only abstraction responsible for the false diagnostic."
    }
  ],
  "effects": [
    {
      "key": "annotation-only-non-redefining",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-import-regression-added",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "value-defining-redefinition-analysis",
      "value": "preserved",
      "evaluator": "evidence"
    },
    {
      "key": "annotation-expression-analysis",
      "value": "preserved",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "review-scoped-repair",
      "instruction": "Review the diff to confirm only annotation-only redefinition semantics are changed and that the regression imports an annotation name, annotates without assignment, and later uses the imported value.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7",
  "read_set": ["role:annotation-binding-analysis", "role:redefinition-analysis", "role:annotation-regression-tests"],
  "write_set": ["role:annotation-binding-analysis", "role:annotation-regression-tests"],
  "invalidates": ["annotation-diagnostic-observations", "annotation-test-results", "checkout-code-anchors"],
  "exclusions": [
    {
      "key": "target-is-value-defining-assignment",
      "value": true,
      "evaluator": "evidence"
    }
  ]
}
```
