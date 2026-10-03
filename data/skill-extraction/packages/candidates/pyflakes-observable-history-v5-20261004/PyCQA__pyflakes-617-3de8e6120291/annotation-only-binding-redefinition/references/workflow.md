# Canonical historical workflow

The repair separates annotation-only metadata from value-defining bindings in the redefinition decision, and protects that distinction with a no-diagnostics regression.

Inspection is a prerequisite reconstructed from the public report and implementation, not a claim that an historical inspection command was recorded. Validation describes the historical regression assertion; current execution must supply fresh results.

```arex-workflow-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7",
  "goal": "Prevent annotation-only declarations from falsely redefining imported names while retaining normal annotation and value-binding analysis.",
  "mechanism": "Make the annotation-only binding abstraction explicitly non-redefining and add a regression using an imported value and imported annotation name.",
  "action_ids": [
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:inspect",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:repair",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "required_effects": [
    {
      "key": "annotation-only-non-redefining",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-import-regression-validated",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
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
  "dependencies": [
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:inspect",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:repair",
      "reason": "Confirm that the false diagnostic is owned by an annotation-only redefinition path before changing that path.",
      "evidence_refs": ["PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"]
    },
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:repair",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate",
      "reason": "The new annotation-import regression and adjacent checks must evaluate the modified semantics.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"]
    }
  ]
}
```
