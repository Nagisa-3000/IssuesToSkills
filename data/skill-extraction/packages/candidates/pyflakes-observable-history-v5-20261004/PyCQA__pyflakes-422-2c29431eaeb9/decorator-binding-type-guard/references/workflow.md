# Historical Workflow: guard overload recognition by binding class

The source repair and regression support the edit and its target behavior. Inspection and current validation below are reusable operational requirements, not claims of additional recorded historical execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:314f3449f8ccd1beab92c625",
  "goal": "Recognize from-import overload decorators without treating ordinary decorator bindings as import bindings.",
  "mechanism": "Check the resolved binding class after scope membership and before import-specific qualified-name access; assert ordinary-decorator redefinition diagnostics.",
  "action_ids": [
    "workflow:verified-history:314f3449f8ccd1beab92c625:inspect",
    "workflow:verified-history:314f3449f8ccd1beab92c625:repair",
    "workflow:verified-history:314f3449f8ccd1beab92c625:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:422:repair:2c29431eaeb9"],
  "required_effects": [
    {"key": "non-import-binding-metadata-access", "value": "prevented", "evaluator": "evidence"},
    {"key": "ordinary-decorator-redefinition-diagnostics", "value": "two", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "from-import-overload-recognition", "value": "preserved", "evaluator": "evidence"},
    {"key": "attribute-decorator-branch", "value": "unchanged", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:314f3449f8ccd1beab92c625:inspect",
      "after": "workflow:verified-history:314f3449f8ccd1beab92c625:repair",
      "reason": "Bind the current recognizer and establish the metadata ownership and unsafe access before selecting the evidenced guard.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix"]
    },
    {
      "before": "workflow:verified-history:314f3449f8ccd1beab92c625:repair",
      "after": "workflow:verified-history:314f3449f8ccd1beab92c625:validate",
      "reason": "The guard and regression assertion must exist before checking corrected behavior and preserved neighboring recognition.",
      "evidence_refs": ["PyCQA/pyflakes:422:fix", "PyCQA/pyflakes:422:regression"]
    }
  ]
}
```
